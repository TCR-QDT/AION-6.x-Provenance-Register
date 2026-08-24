#!/usr/bin/env python3
"""
AION Passo 6.1-D — Ingestão Controlada (3 documentos) + AUDIT textual v6.2

Executa:
1. INGEST CORPUS-006 (Paper A v6.1 oficial)
2. INGEST CORPUS-007 (Paper A v6.1 revisão posterior)
3. INGEST CORPUS-011 (Paper B v6.1 novo)
4. AUDIT textual v6.2 antigo (134.294 B) × novo (137.520 B)
5. Comparação científica
6. Decisão formal sobre CORPUS-002

NÃO executa: TEMPORAL INDEX, GraphRAG, bump de corpus, rebenchmark, LCR.
Esses ficam para depois que a composição definitiva do v1.3.0 for estabelecida.

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import sys
import hashlib
import re
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

import fitz
from aion_rag_proxy import parse_extracted_markdown

INGEST_DIR = Path('/home/z/my-project/upload')
OUTPUT_DIR = Path('/home/z/my-project/download/rag')


# Documentos a ingerir
DOCUMENTS_TO_INGEST = [
    {
        'filepath': '/home/z/my-project/upload/Paper_A_v6.1_REVTeX_COMPLETE.pdf',
        'document_id': 'CORPUS-006',
        'filename': 'Paper_A_v6.1_REVTeX_COMPLETE.pdf',
        'curatorial_id': 'Paper A v6.1 oficial',
        'version': 'v6.1',
        'language': 'EN',
        'state': 'DRAFT (transição para v6.2)',
        'origin': 'submission archive',
        'sha256_known': 'bc2e75fdd6bc8a6d62e4081a5c2858a890809bb07c860ade5d777bf456670f09',
        'expected_R_alpha': True,  # esperamos que R^α esteja presente (pré-v6.2)
    },
    {
        'filepath': '/home/z/my-project/upload/Paper_A_v6.1_REVTeX_COMPLETE .pdf',
        'document_id': 'CORPUS-007',
        'filename': 'Paper_A_v6.1_REVTeX_COMPLETE .pdf',
        'curatorial_id': 'Paper A v6.1 revisão posterior',
        'version': 'v6.1-revision',
        'language': 'EN',
        'state': 'REVISÃO POSTERIOR (data posterior ao v6.2)',
        'origin': 'submission archive',
        'sha256_known': '470cc395e0e7829379794480a62e7c1fb6bac4b622be171ad6c2554bd7346b2c',
        'note': 'Revisão posterior rotulada como v6.1; data 12/08 (igual ao v6.2)',
    },
    {
        'filepath': '/home/z/my-project/upload/Paper_B_QDT_v6.1_PT.pdf',
        'document_id': 'CORPUS-011',
        'filename': 'Paper_B_QDT_v6.1_PT.pdf',
        'curatorial_id': 'Paper B v6.1 PT (novo, 5 págs)',
        'version': 'v6.1',
        'language': 'PT-BR',
        'state': 'NOVO Paper B v6.1 expandido (5 págs vs 3 do CORPUS-004)',
        'origin': 'submission archive',
        'sha256_known': '30476135b03b182d8d38c74fc2b276119a356c5ced293797fdf9ccc7f70ba916',
        'expected_eta': True,  # esperamos que hipótese η seja mencionada (mesmo que retratada)
    },
]


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def extract_full_text(filepath: Path) -> dict:
    """Extrai texto completo do PDF."""
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


def check_R_alpha_presence(full_text: str) -> dict:
    """Verifica presença/ausência de R^α no texto."""
    patterns = [
        r'R\s*\^?\s*α',
        r'R\^\\alpha',
        r'recursion term R',
        r'R\s+with\s+exponent',
        r'α\s*=\s*1\.3',
        r'exponent\s+α',
    ]
    matches = []
    for pat in patterns:
        if re.search(pat, full_text, re.IGNORECASE):
            matches.append(pat)
    
    return {
        'R_alpha_present': len(matches) > 0,
        'patterns_matched': matches,
    }


def check_eta_hypothesis(full_text: str) -> dict:
    """Verifica presença/ausência de hipótese η no texto."""
    patterns = [
        r'\bη\b',
        r'\\eta',
        r'comensurabilidade',
        r'cross-scale',
        r'η\s+hypothesis',
    ]
    matches = []
    for pat in patterns:
        if re.search(pat, full_text, re.IGNORECASE):
            matches.append(pat)
    
    return {
        'eta_present': len(matches) > 0,
        'patterns_matched': matches,
    }


def ingest_document(doc_spec: dict) -> dict:
    """Executa ingestão controlada de um documento (4 estágios: INGEST, AUDIT, EXTRACT, CHUNK)."""
    print(f"\n{'=' * 60}")
    print(f"INGESTING: {doc_spec['document_id']} — {doc_spec['filename']}")
    print(f"{'=' * 60}")
    
    filepath = Path(doc_spec['filepath'])
    if not filepath.exists():
        return {'status': 'FAIL', 'reason': f'File not found: {filepath}'}
    
    result = {
        'document_id': doc_spec['document_id'],
        'filename': doc_spec['filename'],
        'curatorial_identification': doc_spec,
        'stages': {},
    }
    
    # === Estágio 1: INGEST ===
    print(f"\n  [1/4] INGEST...")
    sha256_computed = compute_sha256(filepath)
    file_size = filepath.stat().st_size
    file_type = filepath.suffix.lstrip('.').upper()
    
    # Verifica hash contra esperado
    hash_match = sha256_computed == doc_spec['sha256_known']
    
    ingest_stage = {
        'status': 'OK' if hash_match else 'MISMATCH',
        'sha256_computed': sha256_computed,
        'sha256_expected': doc_spec['sha256_known'],
        'hash_match': hash_match,
        'file_size_bytes': file_size,
        'file_type': file_type,
    }
    result['stages']['1_INGEST'] = ingest_stage
    print(f"        SHA256: {sha256_computed[:32]}...")
    print(f"        Hash match: {'✅' if hash_match else '❌'}")
    print(f"        Size: {file_size} bytes")
    
    # === Estágio 2: AUDIT ===
    print(f"\n  [2/4] AUDIT...")
    issues = []
    if not hash_match:
        issues.append('SHA256 mismatch')
    if file_size < 100:
        issues.append('File too small')
    
    audit_stage = {
        'status': 'PASS' if not issues else 'FAIL',
        'issues': issues,
        'audit_timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }
    result['stages']['2_AUDIT'] = audit_stage
    print(f"        Audit: {'✅ PASS' if not issues else '❌ FAIL — ' + str(issues)}")
    
    # === Estágio 3: EXTRACT ===
    print(f"\n  [3/4] EXTRACT...")
    extract_data = extract_full_text(filepath)
    
    # Verificações específicas
    if doc_spec['document_id'] == 'CORPUS-006':
        # Paper A v6.1 oficial — verificar R^α
        r_alpha_check = check_R_alpha_presence(extract_data['full_text'])
        extract_data['specific_checks'] = r_alpha_check
        print(f"        R^α check: {r_alpha_check}")
    
    if doc_spec['document_id'] == 'CORPUS-007':
        # Paper A v6.1 revisão posterior — também verificar R^α
        r_alpha_check = check_R_alpha_presence(extract_data['full_text'])
        extract_data['specific_checks'] = r_alpha_check
        print(f"        R^α check: {r_alpha_check}")
    
    if doc_spec['document_id'] == 'CORPUS-011':
        # Paper B v6.1 — verificar η
        eta_check = check_eta_hypothesis(extract_data['full_text'])
        extract_data['specific_checks'] = eta_check
        print(f"        η check: {eta_check}")
    
    extract_stage = {
        'status': 'OK',
        'page_count': extract_data['page_count'],
        'char_count': extract_data['char_count'],
        'pdf_metadata': extract_data['pdf_metadata'],
        'specific_checks': extract_data.get('specific_checks', {}),
    }
    result['stages']['3_EXTRACT'] = extract_stage
    print(f"        Pages: {extract_data['page_count']}")
    print(f"        Chars: {extract_data['char_count']}")
    
    # Salva texto extraído em arquivo separado
    extracted_path = OUTPUT_DIR / f"{doc_spec['document_id']}_extracted.md"
    md_content = f"# {doc_spec['document_id']} — Extração de Texto Estruturado\n\n"
    md_content += f"**Arquivo de origem:** `{doc_spec['filename']}`\n"
    md_content += f"**ID do Corpus:** {doc_spec['document_id']}\n"
    md_content += f"**SHA256:** `{sha256_computed}`\n"
    md_content += f"**Identificação curatorial:** {doc_spec['curatorial_id']}\n"
    md_content += f"**Versão:** {doc_spec['version']}\n"
    md_content += f"**Data de ingestão:** {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
    md_content += "---\n\n## Conteúdo Textual por Página\n\n"
    
    for page in extract_data['pages']:
        md_content += f"### Página {page['page_number']}\n\n```text\n{page['text']}\n```\n\n"
    
    extracted_path.write_text(md_content, encoding='utf-8')
    print(f"        Extracted saved: {extracted_path}")
    
    # === Estágio 4: CHUNK ===
    print(f"\n  [4/4] CHUNK...")
    chunks = parse_extracted_markdown(md_content, doc_spec['document_id'])
    
    chunk_stage = {
        'status': 'OK',
        'chunk_count': len(chunks),
        'chunks_metadata': [
            {
                'chunk_id': c.chunk_id,
                'page': c.page,
                'section': c.section,
                'char_count': c.char_count,
            } for c in chunks
        ],
    }
    result['stages']['4_CHUNK'] = chunk_stage
    print(f"        Chunks: {len(chunks)}")
    
    result['overall_status'] = 'COMPLETED' if all(s['status'] in ('OK', 'PASS') for s in result['stages'].values()) else 'FAILED'
    result['completed_at'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
    
    return result


# === AUDIT textual v6.2 antigo × novo ===

def audit_v62_comparison() -> dict:
    """Compara v6.2 atualmente no corpus (134.294 B) vs novo (137.520 B)."""
    print(f"\n{'=' * 60}")
    print(f"AUDIT TEXTUAL — Paper A v6.2 antigo × novo")
    print(f"{'=' * 60}")
    
    # Como o v6.2 atual foi extraído no Passo 3 e está em CORPUS-002_extracted.md
    # e o novo v6.2 está em upload/, vou extrair ambos e comparar
    
    # v6.2 atual (já extraído no Passo 3)
    corpus_002_path = Path('/home/z/my-project/download/CORPUS-002_extracted.md')
    if not corpus_002_path.exists():
        return {'status': 'FAIL', 'reason': 'CORPUS-002_extracted.md not found'}
    
    v62_old_text = corpus_002_path.read_text(encoding='utf-8')
    
    # v6.2 novo
    v62_new_path = Path('/home/z/my-project/upload/Paper_A_v6.2_FINAL.pdf')
    v62_new_data = extract_full_text(v62_new_path)
    v62_new_text = v62_new_data['full_text']
    
    # Hashes
    v62_old_hash = hashlib.sha256(v62_old_text.encode()).hexdigest()
    v62_new_hash = hashlib.sha256(v62_new_text.encode()).hexdigest()
    
    # Comparação char a char (apenas contagem)
    old_len = len(v62_old_text)
    new_len = len(v62_new_text)
    len_diff = new_len - old_len
    
    # Conta palavras
    old_words = len(v62_old_text.split())
    new_words = len(v62_new_text.split())
    
    # Verifica diferenças principais: equações, números, referências
    import re
    
    # Procura por mudanças em resultados-chave (P1, P2, P3)
    old_p1 = re.findall(r'p\s*=\s*1\.0', v62_old_text)
    new_p1 = re.findall(r'p\s*=\s*1\.0', v62_new_text)
    
    old_auc = re.findall(r'AUC\s*=\s*[\d.]+', v62_old_text)
    new_auc = re.findall(r'AUC\s*=\s*[\d.]+', v62_new_text)
    
    old_beta = re.findall(r'β\s*=\s*[\d.]+', v62_old_text)
    new_beta = re.findall(r'β\s*=\s*[\d.]+', v62_new_text)
    
    # Verifica presença/ausência de R^α
    old_R_alpha = check_R_alpha_presence(v62_old_text)
    new_R_alpha = check_R_alpha_presence(v62_new_text)
    
    # Lista de referências (números entre colchetes)
    old_refs = set(re.findall(r'\[(\d+)\]', v62_old_text))
    new_refs = set(re.findall(r'\[(\d+)\]', v62_new_text))
    
    refs_diff_added = new_refs - old_refs
    refs_diff_removed = old_refs - new_refs
    
    comparison = {
        'v62_old': {
            'source': 'CORPUS-002_extracted.md (do Passo 3)',
            'size_bytes': 134294,  # original file
            'text_chars': old_len,
            'text_words': old_words,
            'text_sha256': v62_old_hash,
            'page_count': 6,
            'R_alpha_present': old_R_alpha['R_alpha_present'],
            'P1_results': len(old_p1),
            'AUC_mentions': old_auc,
            'beta_mentions': old_beta,
            'references_count': len(old_refs),
            'references_set': sorted(old_refs),
        },
        'v62_new': {
            'source': 'Paper_A_v6.2_FINAL.pdf (novo upload)',
            'size_bytes': 137520,
            'text_chars': new_len,
            'text_words': new_words,
            'text_sha256': v62_new_hash,
            'page_count': v62_new_data['page_count'],
            'pdf_metadata': v62_new_data['pdf_metadata'],
            'R_alpha_present': new_R_alpha['R_alpha_present'],
            'P1_results': len(new_p1),
            'AUC_mentions': new_auc,
            'beta_mentions': new_beta,
            'references_count': len(new_refs),
            'references_set': sorted(new_refs),
        },
        'differences': {
            'text_chars_diff': len_diff,
            'text_words_diff': new_words - old_words,
            'text_hash_different': v62_old_hash != v62_new_hash,
            'R_alpha_consistent': old_R_alpha['R_alpha_present'] == new_R_alpha['R_alpha_present'],
            'refs_added': sorted(refs_diff_added),
            'refs_removed': sorted(refs_diff_removed),
            'auc_consistent': old_auc == new_auc,
            'beta_consistent': old_beta == new_beta,
        },
    }
    
    # Classificação da diferença
    if v62_old_hash == v62_new_hash:
        comparison['classification'] = 'IDÊNTICOS — apenas diferença de compilação/metadados'
        comparison['recommendation'] = 'Substituição opcional — sem impacto científico'
    elif old_R_alpha['R_alpha_present'] != new_R_alpha['R_alpha_present']:
        comparison['classification'] = 'ALTERAÇÃO CIENTÍFICA — presença/ausência de R^α mudou'
        comparison['recommendation'] = 'NÃO substituir sem análise curatorial detalhada'
    elif old_auc != new_auc or old_beta != new_beta:
        comparison['classification'] = 'ALTERAÇÃO CIENTÍFICA — parâmetros numéricos mudaram'
        comparison['recommendation'] = 'NÃO substituir sem análise curatorial detalhada'
    elif len(refs_diff_added) > 0 or len(refs_diff_removed) > 0:
        comparison['classification'] = 'ALTERAÇÃO DE REFERÊNCIAS — bibliografia mudou'
        comparison['recommendation'] = 'Auditar referências antes de substituir'
    else:
        comparison['classification'] = 'DIFERENÇA TEXTUAL MENOR — possivelmente formatação'
        comparison['recommendation'] = 'Substituição possível após verificação visual'
    
    return comparison


def main():
    print("=" * 70)
    print("AION Passo 6.1-D — Ingestão Controlada + AUDIT v6.2")
    print("=" * 70)
    
    # === Etapas 1-3: INGEST dos 3 documentos aprovados ===
    print("\n[ETAPAS 1-3] INGESTÃO DE CORPUS-006, CORPUS-007, CORPUS-011")
    
    ingestion_results = {}
    for doc_spec in DOCUMENTS_TO_INGEST:
        result = ingest_document(doc_spec)
        ingestion_results[doc_spec['document_id']] = result
        print(f"\n  >>> {doc_spec['document_id']}: {result['overall_status']}")
    
    # === Etapa 4-5: AUDIT textual v6.2 antigo × novo ===
    print(f"\n{'=' * 70}")
    print("[ETAPAS 4-5] AUDIT TEXTUAL v6.2 antigo × novo")
    print(f"{'=' * 70}")
    
    v62_comparison = audit_v62_comparison()
    
    print(f"\n  v6.2 ANTIGO (corpus atual):")
    print(f"    Source: {v62_comparison['v62_old']['source']}")
    print(f"    Size: {v62_comparison['v62_old']['size_bytes']} bytes")
    print(f"    Text chars: {v62_comparison['v62_old']['text_chars']}")
    print(f"    Text words: {v62_comparison['v62_old']['text_words']}")
    print(f"    References: {v62_comparison['v62_old']['references_count']}")
    print(f"    R^α present: {v62_comparison['v62_old']['R_alpha_present']}")
    
    print(f"\n  v6.2 NOVO (upload):")
    print(f"    Source: {v62_comparison['v62_new']['source']}")
    print(f"    Size: {v62_comparison['v62_new']['size_bytes']} bytes")
    print(f"    Text chars: {v62_comparison['v62_new']['text_chars']}")
    print(f"    Text words: {v62_comparison['v62_new']['text_words']}")
    print(f"    References: {v62_comparison['v62_new']['references_count']}")
    print(f"    R^α present: {v62_comparison['v62_new']['R_alpha_present']}")
    
    print(f"\n  DIFERENÇAS:")
    print(f"    Text chars diff: {v62_comparison['differences']['text_chars_diff']:+d}")
    print(f"    Text words diff: {v62_comparison['differences']['text_words_diff']:+d}")
    print(f"    Text hash different: {v62_comparison['differences']['text_hash_different']}")
    print(f"    R^α consistent: {v62_comparison['differences']['R_alpha_consistent']}")
    print(f"    AUC consistent: {v62_comparison['differences']['auc_consistent']}")
    print(f"    β consistent: {v62_comparison['differences']['beta_consistent']}")
    print(f"    Refs added: {v62_comparison['differences']['refs_added']}")
    print(f"    Refs removed: {v62_comparison['differences']['refs_removed']}")
    
    print(f"\n  CLASSIFICAÇÃO: {v62_comparison['classification']}")
    print(f"  RECOMENDAÇÃO: {v62_comparison['recommendation']}")
    
    # === Etapa 6: Decisão formal sobre CORPUS-002 ===
    print(f"\n{'=' * 70}")
    print("[ETAPA 6] DECISÃO FORMAL SOBRE CORPUS-002")
    print(f"{'=' * 70}")
    
    # A identidade já foi autorizada pelo Projetista Master:
    # "O v6.2 de 137.520 B é SUBSTITUTO DO ANTERIOR."
    # O que precisamos decidir é se a substituição pode ser efetivada AGORA
    
    if v62_comparison['classification'].startswith('IDÊNTICOS'):
        corpus_002_decision = 'SUBSTITUIÇÃO AUTORIZADA — sem impacto científico'
    elif v62_comparison['classification'].startswith('DIFERENÇA TEXTUAL MENOR'):
        corpus_002_decision = 'SUBSTITUIÇÃO POSSÍVEL — diferença textual menor detectada'
    else:
        corpus_002_decision = 'HOLD — diferença científica/material detectada, requer análise curatorial detalhada'
    
    print(f"\n  Identidade documental: AUTORIZADA (substituto do v6.2 anterior)")
    print(f"  Auditoria textual: {v62_comparison['classification']}")
    print(f"  Decisão sobre substituição: {corpus_002_decision}")
    
    # Salva relatório completo
    report = {
        'metadata': {
            'experiment': 'AION-6.1-D — Ingestão Controlada + AUDIT v6.2',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'ingestion_results': ingestion_results,
        'v62_audit': v62_comparison,
        'corpus_002_decision': {
            'identity_authorized': True,  # Projetista Master autorizou
            'textual_audit': v62_comparison['classification'],
            'substitution_decision': corpus_002_decision,
        },
        'sha256_registry': {
            'CORPUS-006': DOCUMENTS_TO_INGEST[0]['sha256_known'],
            'CORPUS-007': DOCUMENTS_TO_INGEST[1]['sha256_known'],
            'CORPUS-011': DOCUMENTS_TO_INGEST[2]['sha256_known'],
            'CORPUS-002 (novo)': '971986d96c4ceb1ea5d7a17acdf2a54f4276403f2805c3945874304020adc433',
            'CORPUS-002 (antigo, no corpus v1.2.0)': 'a ser verificado no Passo 3 original',
        },
        'next_step': 'Estabelecer composição definitiva do Corpus v1.3.0 — aguardando decisão do Projetista Master sobre CORPUS-002',
    }
    
    json_path = OUTPUT_DIR / 'aion_6_1_d_ingestao_resultados.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
