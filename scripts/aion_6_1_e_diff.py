#!/usr/bin/env python3
"""
AION Passo 6.1-E — Diff textual integral CORPUS-006 × CORPUS-007

Compara os dois PDFs nominalmente v6.1 (138KB vs 326KB) para determinar:
1. TEXTUAL_IDENTICAL — conteúdo idêntico
2. TEXTUAL_EQUIVALENT — diferenças de formatação sem alteração semântica
3. CONTENT_REVISION — alteração efetiva de conteúdo
4. SCIENTIFIC_REVISION — alteração de equações, parâmetros, resultados, hipóteses, conclusões

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import re
import hashlib
import difflib
from pathlib import Path
from datetime import datetime, timezone
import sys

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

import fitz

INGEST_DIR = Path('/home/z/my-project/upload')
OUTPUT_DIR = Path('/home/z/my-project/download/rag')


def extract_full_text(filepath: Path) -> dict:
    """Extrai texto completo do PDF, página por página."""
    doc = fitz.open(filepath)
    page_count = len(doc)
    pages = []
    full_text = ''
    
    for i, page in enumerate(doc):
        text = page.get_text('text')
        pages.append({'page_number': i + 1, 'text': text})
        full_text += text + '\n'
    
    metadata = dict(doc.metadata)
    doc.close()
    
    return {
        'pdf_metadata': metadata,
        'page_count': page_count,
        'full_text': full_text,
        'pages': pages,
        'char_count': len(full_text),
    }


def normalize_text(text: str) -> str:
    """Normaliza texto para comparação: remove espaços extras e quebras de linha múltiplas."""
    # Normaliza quebras de linha
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\r', '\n', text)
    # Remove espaços extras
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove linhas vazias consecutivas
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Strip
    text = text.strip()
    return text


def compute_text_hash(text: str) -> str:
    """Hash do texto para comparação rápida."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def diff_line_by_line(text_a: str, text_b: str) -> dict:
    """Diff linha a linha usando difflib."""
    lines_a = text_a.split('\n')
    lines_b = text_b.split('\n')
    
    # Gera diff unificado
    diff = list(difflib.unified_diff(
        lines_a, lines_b,
        fromfile='CORPUS-006',
        tofile='CORPUS-007',
        lineterm=''
    ))
    
    # Conta adições e remoções
    additions = sum(1 for line in diff if line.startswith('+') and not line.startswith('+++'))
    removals = sum(1 for line in diff if line.startswith('-') and not line.startswith('---'))
    
    return {
        'diff_lines': diff,
        'additions': additions,
        'removals': removals,
        'diff_size': len(diff),
    }


def find_scientific_differences(text_a: str, text_b: str) -> dict:
    """Procura diferenças em elementos científicos: equações, números, parâmetros."""
    
    # Procura por números e equações em ambos
    numbers_a = re.findall(r'-?\d+\.?\d*', text_a)
    numbers_b = re.findall(r'-?\d+\.?\d*', text_b)
    
    numbers_set_a = set(numbers_a)
    numbers_set_b = set(numbers_b)
    
    numbers_added = numbers_set_b - numbers_set_a
    numbers_removed = numbers_set_a - numbers_set_b
    
    # Procura por equações (padrões com = e símbolos matemáticos)
    eq_pattern = r'[A-Za-zα-ωΑ-Ω]\s*=\s*[^=\n]{1,80}'
    equations_a = set(re.findall(eq_pattern, text_a))
    equations_b = set(re.findall(eq_pattern, text_b))
    
    eq_added = equations_b - equations_a
    eq_removed = equations_a - equations_b
    
    # Procura por símbolos matemáticos
    math_symbols_pattern = r'[∂∇∫∑∏√∞±≤≥≠∈∉∪∩⊂⊃∀∃¬≡≅≈∝]'
    math_a = set(re.findall(math_symbols_pattern, text_a))
    math_b = set(re.findall(math_symbols_pattern, text_b))
    
    # Procura por referências [N]
    refs_a = set(re.findall(r'\[(\d+)\]', text_a))
    refs_b = set(re.findall(r'\[(\d+)\]', text_b))
    
    return {
        'numbers': {
            'total_a': len(numbers_a),
            'total_b': len(numbers_b),
            'unique_a': len(numbers_set_a),
            'unique_b': len(numbers_set_b),
            'added': sorted(numbers_added)[:20],  # amostra
            'removed': sorted(numbers_removed)[:20],
            'added_count': len(numbers_added),
            'removed_count': len(numbers_removed),
        },
        'equations': {
            'total_a': len(equations_a),
            'total_b': len(equations_b),
            'added': sorted(eq_added)[:10],
            'removed': sorted(eq_removed)[:10],
            'added_count': len(eq_added),
            'removed_count': len(eq_removed),
        },
        'math_symbols': {
            'a': sorted(math_a),
            'b': sorted(math_b),
            'identical': math_a == math_b,
        },
        'references': {
            'a': sorted(refs_a),
            'b': sorted(refs_b),
            'added': sorted(refs_b - refs_a),
            'removed': sorted(refs_a - refs_b),
        },
    }


def classify_difference(raw_diff: dict, scientific_diff: dict, normalized_hash_match: bool) -> dict:
    """Classifica a diferença em uma das 4 categorias."""
    
    if normalized_hash_match:
        return {
            'category': 'TEXTUAL_IDENTICAL',
            'description': 'Conteúdo textual idêntico após normalização',
            'implication': 'Diferença entre PDFs é puramente de compilação/metadados',
        }
    
    # Verifica se há diferenças científicas
    sci = scientific_diff
    has_scientific_diff = (
        sci['equations']['added_count'] > 0 or
        sci['equations']['removed_count'] > 0 or
        sci['numbers']['added_count'] > 0 or
        sci['numbers']['removed_count'] > 0 or
        not sci['math_symbols']['identical'] or
        sci['references']['added'] or
        sci['references']['removed']
    )
    
    if has_scientific_diff:
        # Verifica especificamente equações e números (critérios científicos)
        has_eq_changes = (
            sci['equations']['added_count'] > 0 or
            sci['equations']['removed_count'] > 0
        )
        has_number_changes = (
            sci['numbers']['added_count'] > 0 or
            sci['numbers']['removed_count'] > 0
        )
        has_ref_changes = (
            bool(sci['references']['added']) or
            bool(sci['references']['removed'])
        )
        
        if has_eq_changes or has_number_changes:
            return {
                'category': 'SCIENTIFIC_REVISION',
                'description': 'Alteração de equações, parâmetros ou resultados numéricos',
                'implication': 'CORPUS-007 é revisão científica efetiva — ambos devem ser preservados como documentos independentes',
                'details': {
                    'equations_added': sci['equations']['added_count'],
                    'equations_removed': sci['equations']['removed_count'],
                    'numbers_added': sci['numbers']['added_count'],
                    'numbers_removed': sci['numbers']['removed_count'],
                    'references_added': sci['references']['added'],
                    'references_removed': sci['references']['removed'],
                },
            }
        elif has_ref_changes:
            return {
                'category': 'CONTENT_REVISION',
                'description': 'Alteração de referências bibliográficas',
                'implication': 'CORPUS-007 é revisão de conteúdo — ambos devem ser preservados',
                'details': {
                    'references_added': sci['references']['added'],
                    'references_removed': sci['references']['removed'],
                },
            }
    
    # Há diff mas apenas formatação
    additions = raw_diff['additions']
    removals = raw_diff['removals']
    
    # Se as adições e remoções são simétricas (texto reorganizado), é EQUIVALENT
    if additions > 0 and removals > 0:
        return {
            'category': 'TEXTUAL_EQUIVALENT',
            'description': 'Diferenças de formatação/estrutura sem alteração semântica',
            'implication': 'CORPUS-007 é revisão de formatação — CORPUS-006 permanece como oficial; CORPUS-007 como artefato de proveniência',
            'details': {
                'line_additions': additions,
                'line_removals': removals,
            },
        }
    
    return {
        'category': 'TEXTUAL_EQUIVALENT',
        'description': 'Diferenças menores detectadas',
        'implication': 'CORPUS-007 tratado como revisão de proveniência',
        'details': {
            'line_additions': additions,
            'line_removals': removals,
        },
    }


def main():
    print("=" * 70)
    print("AION Passo 6.1-E — Diff textual CORPUS-006 × CORPUS-007")
    print("=" * 70)
    
    # Extrai texto de ambos os PDFs
    print("\n[EXTRACT] CORPUS-006 (Paper A v6.1 oficial, 138KB)...")
    corpus_006_path = INGEST_DIR / 'Paper_A_v6.1_REVTeX_COMPLETE.pdf'
    c006_data = extract_full_text(corpus_006_path)
    print(f"  Pages: {c006_data['page_count']}, Chars: {c006_data['char_count']}")
    
    print("\n[EXTRACT] CORPUS-007 (Paper A v6.1 revisão posterior, 326KB)...")
    corpus_007_path = INGEST_DIR / 'Paper_A_v6.1_REVTeX_COMPLETE .pdf'  # com espaço
    c007_data = extract_full_text(corpus_007_path)
    print(f"  Pages: {c007_data['page_count']}, Chars: {c007_data['char_count']}")
    
    # 1. Comparação bruta de hashes
    print("\n[1] COMPARAÇÃO DE HASHES (texto bruto)")
    hash_006_raw = compute_text_hash(c006_data['full_text'])
    hash_007_raw = compute_text_hash(c007_data['full_text'])
    hash_raw_match = hash_006_raw == hash_007_raw
    print(f"  CORPUS-006 (raw): {hash_006_raw[:32]}...")
    print(f"  CORPUS-007 (raw): {hash_007_raw[:32]}...")
    print(f"  Match: {'✅' if hash_raw_match else '❌'}")
    
    # 2. Comparação após normalização
    print("\n[2] COMPARAÇÃO APÓS NORMALIZAÇÃO")
    c006_normalized = normalize_text(c006_data['full_text'])
    c007_normalized = normalize_text(c007_data['full_text'])
    hash_006_norm = compute_text_hash(c006_normalized)
    hash_007_norm = compute_text_hash(c007_normalized)
    hash_norm_match = hash_006_norm == hash_007_norm
    print(f"  CORPUS-006 (normalized): {hash_006_norm[:32]}...")
    print(f"  CORPUS-007 (normalized): {hash_007_norm[:32]}...")
    print(f"  Match: {'✅' if hash_norm_match else '❌'}")
    print(f"  Normalized chars: CORPUS-006={len(c006_normalized)}, CORPUS-007={len(c007_normalized)}")
    
    # 3. Diff linha a linha
    print("\n[3] DIFF LINHA A LINHA")
    raw_diff = diff_line_by_line(c006_data['full_text'], c007_data['full_text'])
    print(f"  Diff size (lines): {raw_diff['diff_size']}")
    print(f"  Additions: +{raw_diff['additions']}")
    print(f"  Removals: -{raw_diff['removals']}")
    
    # Salva diff completo em arquivo
    diff_path = OUTPUT_DIR / 'diff_corpus_006_vs_007.txt'
    with open(diff_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(raw_diff['diff_lines']))
    print(f"  Diff saved: {diff_path}")
    
    # 4. Diferenças científicas
    print("\n[4] DIFERENÇAS CIENTÍFICAS")
    scientific_diff = find_scientific_differences(c006_data['full_text'], c007_data['full_text'])
    
    print(f"  Numbers:")
    print(f"    Total A: {scientific_diff['numbers']['total_a']}, Total B: {scientific_diff['numbers']['total_b']}")
    print(f"    Unique A: {scientific_diff['numbers']['unique_a']}, Unique B: {scientific_diff['numbers']['unique_b']}")
    print(f"    Added: {scientific_diff['numbers']['added_count']}")
    print(f"    Removed: {scientific_diff['numbers']['removed_count']}")
    if scientific_diff['numbers']['added']:
        print(f"    Sample added: {scientific_diff['numbers']['added'][:5]}")
    if scientific_diff['numbers']['removed']:
        print(f"    Sample removed: {scientific_diff['numbers']['removed'][:5]}")
    
    print(f"  Equations:")
    print(f"    Total A: {scientific_diff['equations']['total_a']}, Total B: {scientific_diff['equations']['total_b']}")
    print(f"    Added: {scientific_diff['equations']['added_count']}")
    print(f"    Removed: {scientific_diff['equations']['removed_count']}")
    if scientific_diff['equations']['added']:
        print(f"    Sample added: {scientific_diff['equations']['added'][:3]}")
    if scientific_diff['equations']['removed']:
        print(f"    Sample removed: {scientific_diff['equations']['removed'][:3]}")
    
    print(f"  Math symbols:")
    print(f"    A: {scientific_diff['math_symbols']['a']}")
    print(f"    B: {scientific_diff['math_symbols']['b']}")
    print(f"    Identical: {scientific_diff['math_symbols']['identical']}")
    
    print(f"  References:")
    print(f"    A: {scientific_diff['references']['a']}")
    print(f"    B: {scientific_diff['references']['b']}")
    print(f"    Added: {scientific_diff['references']['added']}")
    print(f"    Removed: {scientific_diff['references']['removed']}")
    
    # 5. Classificação
    print("\n[5] CLASSIFICAÇÃO DA DIFERENÇA")
    classification = classify_difference(raw_diff, scientific_diff, hash_norm_match)
    print(f"  Category: {classification['category']}")
    print(f"  Description: {classification['description']}")
    print(f"  Implication: {classification['implication']}")
    if 'details' in classification:
        print(f"  Details: {classification['details']}")
    
    # 6. Decisão curatorial
    print("\n[6] DECISÃO CURATORIAL")
    if classification['category'] == 'TEXTUAL_IDENTICAL':
        decision = (
            'CORPUS-006 permanece como documento oficial v6.1.\n'
            'CORPUS-007 fica registrado como revisão posterior/artefato de proveniência,\n'
            'mas NÃO como segundo documento epistemicamente independente.\n'
            'Ambos os hashes são preservados para auditoria.'
        )
        corpus_007_role = 'ARTEFATO_DE_PROVENIENCIA'
    elif classification['category'] == 'TEXTUAL_EQUIVALENT':
        decision = (
            'CORPUS-006 permanece como documento oficial v6.1.\n'
            'CORPUS-007 fica registrado como revisão de formatação,\n'
            'NÃO como documento epistemicamente independente.\n'
            'Ambos os hashes são preservados.'
        )
        corpus_007_role = 'ARTEFATO_DE_PROVENIENCIA'
    else:  # CONTENT_REVISION ou SCIENTIFIC_REVISION
        decision = (
            'CORPUS-006 e CORPUS-007 permanecem ambos no histórico documental.\n'
            'Suas relações temporais serão explicitamente registradas.\n'
            'Nenhum será descartado.'
        )
        corpus_007_role = 'DOCUMENTO_EPISTEMICAMENTE_INDEPENDENTE'
    
    print(f"  {decision}")
    print(f"  CORPUS-007 role: {corpus_007_role}")
    
    # Salva relatório completo
    report = {
        'metadata': {
            'experiment': 'AION-6.1-E — Diff CORPUS-006 × CORPUS-007',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'corpus_006': {
            'filepath': str(corpus_006_path),
            'sha256_pdf': 'bc2e75fdd6bc8a6d62e4081a5c2858a890809bb07c860ade5d777bf456670f09',
            'page_count': c006_data['page_count'],
            'char_count': c006_data['char_count'],
            'text_sha256_raw': hash_006_raw,
            'text_sha256_normalized': hash_006_norm,
        },
        'corpus_007': {
            'filepath': str(corpus_007_path),
            'sha256_pdf': '470cc395e0e7829379794480a62e7c1fb6bac4b622be171ad6c2554bd7346b2c',
            'page_count': c007_data['page_count'],
            'char_count': c007_data['char_count'],
            'text_sha256_raw': hash_007_raw,
            'text_sha256_normalized': hash_007_norm,
        },
        'comparison': {
            'raw_hash_match': hash_raw_match,
            'normalized_hash_match': hash_norm_match,
            'char_count_diff': c007_data['char_count'] - c006_data['char_count'],
        },
        'diff': {
            'diff_size_lines': raw_diff['diff_size'],
            'additions': raw_diff['additions'],
            'removals': raw_diff['removals'],
            'diff_file': str(diff_path),
        },
        'scientific_differences': scientific_diff,
        'classification': classification,
        'curatorial_decision': {
            'decision_text': decision,
            'corpus_007_role': corpus_007_role,
        },
    }
    
    json_path = OUTPUT_DIR / 'aion_6_1_e_diff_resultados.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    print(f"  Diff file: {diff_path}")
    print(f"  Diff size: {diff_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
