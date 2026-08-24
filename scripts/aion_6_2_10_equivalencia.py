#!/usr/bin/env python3
"""
AION Passo 6.2.10 — Auditoria de equivalência interversional

Compara ocorrências da fórmula C = I × S × H^β em:
- CORPUS-002 (Paper A v6.2 FINAL — CURRENT)
- CORPUS-006 (Paper A v6.1 oficial — HISTORICAL)
- CORPUS-007 (Paper A v6.1 revisão — HISTORICAL/SCIENTIFIC_REVISION)

Para cada ocorrência, avalia:
1. Definição — é definição primária ou citação?
2. Contexto — em qual seção? qual função textual?
3. Equação — é a mesma equação ou variação?
4. Função epistemológica — introduz, define, cita, discute?

Classificação:
- EQUIVALENT — mesma função epistemológica, mesma equação, contexto equivalente
- RELATED — equação presente mas função epistemológica diferente
- NON-EQUIVALENT — equação diferente ou ausente

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

from aion_rag_proxy import parse_extracted_markdown
from aion_6_1_f_rebenchmark_lcr import CORPUS_V13_FILES

OUTPUT_DIR = Path('/home/z/my-project/download/rag')

# Documentos a comparar (genealogia do Paper A)
PAPER_A_DOCUMENTS = {
    'CORPUS-002': {
        'version': 'v6.2 FINAL',
        'state': 'CURRENT',
        'date': '2026-08-12',
        'path': CORPUS_V13_FILES['CORPUS-002_extracted.md']['path'],
    },
    'CORPUS-006': {
        'version': 'v6.1 oficial',
        'state': 'HISTORICAL',
        'date': '2026-08-10',
        'path': CORPUS_V13_FILES['CORPUS-006_extracted.md']['path'],
    },
    'CORPUS-007': {
        'version': 'v6.1 revisão',
        'state': 'HISTORICAL / SCIENTIFIC_REVISION',
        'date': '2026-08-12',
        'path': CORPUS_V13_FILES['CORPUS-007_extracted.md']['path'],
    },
}

# Oracle v2 (frozen) — 5 chunks PRIMARY em CORPUS-002
B1_ORACLE_V2_CHUNKS = [
    'CORPUS-002#p1_01',
    'CORPUS-002#p1_02',
    'CORPUS-002#p2_01',
    'CORPUS-002#p5_01',
    'CORPUS-002#p5_02',
]


# === Padrões de fórmula ===

FORMULA_PATTERNS = [
    r'C\s*=\s*I\s*[×x]\s*S\s*[×x]\s*H\s*β',
    r'C\s*=\s*I\s*[×x]\s*S\s*[×x]\s*H\^?\s*β',
    r'\\mathcal\{C\}\s*=\s*I\s*\\times\s*S\s*\\times\s*H',
]

# Indicadores de função epistemológica
EPISTEMIC_INDICATORS = {
    'PRIMARY_INTRODUCTION': [
        'we introduce', 'we present', 'we propose',
        'introduzimos', 'apresentamos', 'propomos',
    ],
    'PRIMARY_DEFINITION': [
        'we define', 'the metric is', 'is defined as', 'we adopt',
        'definimos', 'a métrica é', 'é definida como',
    ],
    'DERIVED_CALIBRATION': [
        'β = 0.5', 'calibrated via', 'LOOCV',
        'calibrado', 'canônico', 'canonical',
    ],
    'CONTEXTUAL_DISCUSSION': [
        'the composite c', 'does not outperform', 'structural signature',
        'interpretive', 'ablation',
    ],
    'CONTEXTUAL_LIMITATION': [
        'limitation', 'inconsistency', 'preliminary',
        'limitação', 'inconsistência', 'preliminar',
    ],
}


def find_formula_occurrences_in_document(doc_id: str, chunks: list) -> list:
    """Encontra todas as ocorrências da fórmula em um documento."""
    occurrences = []
    
    for chunk in chunks:
        if chunk.corpus_id != doc_id:
            continue
        
        text = chunk.text
        
        for pattern_idx, pattern in enumerate(FORMULA_PATTERNS):
            matches = list(re.finditer(pattern, text, re.IGNORECASE | re.DOTALL))
            for match in matches:
                # Extrai contexto: 300 chars antes e depois
                start = max(0, match.start() - 300)
                end = min(len(text), match.end() + 300)
                context = text[start:end]
                
                # Detecta função epistemológica
                epistemic_function = detect_epistemic_function(context)
                
                # Extrai a equação exata
                equation_text = match.group(0)
                
                occurrences.append({
                    'chunk_id': chunk.chunk_id,
                    'corpus_id': chunk.corpus_id,
                    'page': chunk.page,
                    'section': chunk.section,
                    'pattern_idx': pattern_idx,
                    'equation_text': equation_text,
                    'match_start': match.start(),
                    'context': context,
                    'context_excerpt': context[:400],
                    'epistemic_function': epistemic_function,
                    'in_oracle_v2': chunk.chunk_id in B1_ORACLE_V2_CHUNKS,
                })
    
    return occurrences


def detect_epistemic_function(context: str) -> dict:
    """Detecta a função epistemológica da ocorrência."""
    context_lower = context.lower()
    
    detected = {
        'PRIMARY_INTRODUCTION': [],
        'PRIMARY_DEFINITION': [],
        'DERIVED_CALIBRATION': [],
        'CONTEXTUAL_DISCUSSION': [],
        'CONTEXTUAL_LIMITATION': [],
    }
    
    for function, indicators in EPISTEMIC_INDICATORS.items():
        for indicator in indicators:
            if indicator in context_lower:
                detected[function].append(indicator)
    
    # Classifica função principal
    if detected['PRIMARY_INTRODUCTION']:
        primary_function = 'PRIMARY_INTRODUCTION'
        function_description = 'Introduz a fórmula/métrica pela primeira vez'
    elif detected['PRIMARY_DEFINITION']:
        primary_function = 'PRIMARY_DEFINITION'
        function_description = 'Define a fórmula operacionalmente'
    elif detected['DERIVED_CALIBRATION']:
        primary_function = 'DERIVED_CALIBRATION'
        function_description = 'Cita parâmetros calibrados (β=0.5, LOOCV)'
    elif detected['CONTEXTUAL_DISCUSSION']:
        primary_function = 'CONTEXTUAL_DISCUSSION'
        function_description = 'Discute a fórmula em contexto analítico'
    elif detected['CONTEXTUAL_LIMITATION']:
        primary_function = 'CONTEXTUAL_LIMITATION'
        function_description = 'Menciona limitações relacionadas à fórmula'
    else:
        primary_function = 'MENTION'
        function_description = 'Menção sem contexto definicional claro'
    
    return {
        'primary_function': primary_function,
        'function_description': function_description,
        'all_indicators': detected,
    }


def compare_semantically(occurrences_by_doc: dict) -> dict:
    """Compara semanticamente as ocorrências entre documentos."""
    comparison = {}
    
    # Para cada documento, identificar a ocorrência "canônica" (PRIMARY_INTRODUCTION ou PRIMARY_DEFINITION)
    for doc_id, occurrences in occurrences_by_doc.items():
        if not occurrences:
            comparison[doc_id] = {
                'total_occurrences': 0,
                'canonical_occurrence': None,
                'all_occurrences_summary': [],
            }
            continue
        
        # Encontra a ocorrência canônica (PRIMARY_INTRODUCTION ou PRIMARY_DEFINITION)
        canonical = None
        for occ in occurrences:
            if occ['epistemic_function']['primary_function'] in ('PRIMARY_INTRODUCTION', 'PRIMARY_DEFINITION'):
                canonical = occ
                break
        
        # Se não há canônica, usa a primeira
        if not canonical:
            canonical = occurrences[0]
        
        # Resumo de todas as ocorrências
        all_summary = []
        for occ in occurrences:
            all_summary.append({
                'chunk_id': occ['chunk_id'],
                'page': occ['page'],
                'equation_text': occ['equation_text'],
                'epistemic_function': occ['epistemic_function']['primary_function'],
                'in_oracle_v2': occ['in_oracle_v2'],
            })
        
        comparison[doc_id] = {
            'total_occurrences': len(occurrences),
            'canonical_occurrence': {
                'chunk_id': canonical['chunk_id'],
                'page': canonical['page'],
                'equation_text': canonical['equation_text'],
                'epistemic_function': canonical['epistemic_function']['primary_function'],
                'function_description': canonical['epistemic_function']['function_description'],
                'context_excerpt': canonical['context_excerpt'][:300],
                'in_oracle_v2': canonical['in_oracle_v2'],
            },
            'all_occurrences_summary': all_summary,
        }
    
    return comparison


def determine_equivalence(comparison: dict) -> dict:
    """Determina equivalência entre documentos."""
    print(f"\n{'=' * 80}")
    print("[ETAPA 4] DETERMINAÇÃO DE EQUIVALÊNCIA")
    print(f"{'=' * 80}")
    
    # Documento de referência: CORPUS-002 (versão FINAL/CURRENT)
    ref_doc = 'CORPUS-002'
    ref_canonical = comparison[ref_doc]['canonical_occurrence']
    
    print(f"\nDocumento de referência: {ref_doc} ({PAPER_A_DOCUMENTS[ref_doc]['version']})")
    print(f"  Chunk canônico: {ref_canonical['chunk_id']}")
    print(f"  Equação: {ref_canonical['equation_text']}")
    print(f"  Função: {ref_canonical['epistemic_function']} — {ref_canonical['function_description']}")
    
    equivalences = {}
    
    for doc_id in ['CORPUS-006', 'CORPUS-007']:
        doc_info = PAPER_A_DOCUMENTS[doc_id]
        doc_comparison = comparison[doc_id]
        
        print(f"\n--- {doc_id} ({doc_info['version']}, {doc_info['state']}) ---")
        print(f"  Total ocorrências: {doc_comparison['total_occurrences']}")
        
        if doc_comparison['total_occurrences'] == 0:
            print(f"  >>> Nenhuma ocorrência encontrada")
            equivalences[doc_id] = {
                'classification': 'NON-EQUIVALENT',
                'reason': 'Fórmula não encontrada neste documento',
                'canonical_occurrence': None,
            }
            continue
        
        canonical = doc_comparison['canonical_occurrence']
        print(f"  Chunk canônico: {canonical['chunk_id']}")
        print(f"  Equação: {canonical['equation_text']}")
        print(f"  Função: {canonical['epistemic_function']} — {canonical['function_description']}")
        
        # Comparar com referência
        ref_eq = ref_canonical['equation_text'] == canonical['equation_text']
        ref_function = ref_canonical['epistemic_function']
        doc_function = canonical['epistemic_function']
        same_function = ref_function == doc_function
        
        # Critérios de equivalência
        if ref_eq and same_function:
            classification = 'EQUIVALENT'
            reason = 'Mesma equação e mesma função epistemológica'
        elif ref_eq and not same_function:
            classification = 'RELATED'
            reason = f'Mesma equação mas função diferente ({doc_function} vs {ref_function})'
        elif not ref_eq:
            classification = 'RELATED'
            reason = f'Equação similar mas não idêntica: {canonical["equation_text"]}'
        else:
            classification = 'NON-EQUIVALENT'
            reason = 'Diferença significativa'
        
        # Verificar todas as ocorrências (não apenas canônica)
        all_occ = doc_comparison['all_occurrences_summary']
        primary_count = sum(1 for o in all_occ if o['epistemic_function'] in ('PRIMARY_INTRODUCTION', 'PRIMARY_DEFINITION'))
        derived_count = sum(1 for o in all_occ if o['epistemic_function'] == 'DERIVED_CALIBRATION')
        contextual_count = sum(1 for o in all_occ if 'CONTEXTUAL' in o['epistemic_function'])
        
        print(f"  >>> Classificação: {classification}")
        print(f"  >>> Razão: {reason}")
        print(f"  >>> Ocorrências: PRIMARY={primary_count}, DERIVED={derived_count}, CONTEXTUAL={contextual_count}")
        
        equivalences[doc_id] = {
            'classification': classification,
            'reason': reason,
            'canonical_occurrence': canonical,
            'all_occurrences_summary': all_occ,
            'occurrence_counts': {
                'PRIMARY': primary_count,
                'DERIVED': derived_count,
                'CONTEXTUAL': contextual_count,
            },
            'same_equation_as_reference': ref_eq,
            'same_function_as_reference': same_function,
        }
    
    return equivalences


def evaluate_oracle_extension(equivalences: dict) -> dict:
    """Etapa 5: Avaliar se o oracle deve ser estendido."""
    print(f"\n{'=' * 80}")
    print("[ETAPA 5] AVALIAÇÃO DE EXTENSÃO DO ORACLE")
    print(f"{'=' * 80}")
    
    # Oracle v2 atual: 5 chunks em CORPUS-002
    oracle_v2 = B1_ORACLE_V2_CHUNKS.copy()
    
    # Verificar quais chunks de CORPUS-006/007 são EQUIVALENT
    extension_candidates = []
    
    for doc_id, equiv in equivalences.items():
        if equiv['classification'] == 'EQUIVALENT':
            canonical = equiv['canonical_occurrence']
            extension_candidates.append({
                'chunk_id': canonical['chunk_id'],
                'corpus_id': doc_id,
                'version': PAPER_A_DOCUMENTS[doc_id]['version'],
                'state': PAPER_A_DOCUMENTS[doc_id]['state'],
                'reason': f'EQUIVALENT — {equiv["reason"]}',
            })
    
    print(f"\nOracle v2 atual: {len(oracle_v2)} chunks em CORPUS-002")
    print(f"Candidatos a extensão (EQUIVALENT): {len(extension_candidates)}")
    
    for candidate in extension_candidates:
        print(f"  • {candidate['chunk_id']} ({candidate['version']}, {candidate['state']})")
        print(f"    Razão: {candidate['reason']}")
    
    # Verificar RELATED também
    related_chunks = []
    for doc_id, equiv in equivalences.items():
        if equiv['classification'] == 'RELATED':
            canonical = equiv['canonical_occurrence']
            related_chunks.append({
                'chunk_id': canonical['chunk_id'],
                'corpus_id': doc_id,
                'version': PAPER_A_DOCUMENTS[doc_id]['version'],
                'state': PAPER_A_DOCUMENTS[doc_id]['state'],
                'reason': f'RELATED — {equiv["reason"]}',
            })
    
    print(f"\nCandidatos RELATED (não EQUIVALENT): {len(related_chunks)}")
    for related in related_chunks:
        print(f"  • {related['chunk_id']} ({related['version']}, {related['state']})")
        print(f"    Razão: {related['reason']}")
    
    # Recomendação
    if extension_candidates:
        recommendation = 'EXTENDER oracle para incluir chunks EQUIVALENT'
        proposed_oracle_v3 = oracle_v2 + [c['chunk_id'] for c in extension_candidates]
    elif related_chunks:
        recommendation = 'NÃO estender — chunks são RELATED mas não EQUIVALENT'
        proposed_oracle_v3 = oracle_v2  # mantém v2
    else:
        recommendation = 'NÃO estender — nenhuma equivalência encontrada'
        proposed_oracle_v3 = oracle_v2
    
    print(f"\nRecomendação: {recommendation}")
    print(f"Oracle v2 (atual): {oracle_v2}")
    print(f"Oracle v3 (proposto): {proposed_oracle_v3}")
    
    return {
        'oracle_v2_current': oracle_v2,
        'extension_candidates_equivalent': extension_candidates,
        'related_chunks': related_chunks,
        'recommendation': recommendation,
        'proposed_oracle_v3': proposed_oracle_v3,
    }


def main():
    print("=" * 80)
    print("AION Passo 6.2.10 — Auditoria de equivalência interversional")
    print("=" * 80)
    
    # ETAPA 1: Congelar Oracle v2
    print(f"\n[ETAPA 1] Oracle v2 CONGELADO (5 chunks PRIMARY em CORPUS-002)")
    print(f"  Chunks: {B1_ORACLE_V2_CHUNKS}")
    
    # Constrói chunks
    print(f"\n[SETUP] Construindo chunks do corpus v1.3.0...")
    all_chunks = []
    for filename, meta in CORPUS_V13_FILES.items():
        path = meta['path']
        if not path.exists():
            continue
        md_text = path.read_text(encoding='utf-8')
        chunks = parse_extracted_markdown(md_text, meta['id'])
        all_chunks.extend(chunks)
    print(f"  Total chunks: {len(all_chunks)}")
    
    # ETAPA 2: Mapear ocorrências da fórmula em cada documento
    print(f"\n{'=' * 80}")
    print("[ETAPA 2] MAPEAR OCORRÊNCIAS DA FÓRMULA")
    print(f"{'=' * 80}")
    
    occurrences_by_doc = {}
    for doc_id in ['CORPUS-002', 'CORPUS-006', 'CORPUS-007']:
        occurrences = find_formula_occurrences_in_document(doc_id, all_chunks)
        occurrences_by_doc[doc_id] = occurrences
        print(f"\n  {doc_id} ({PAPER_A_DOCUMENTS[doc_id]['version']}): {len(occurrences)} ocorrências")
        
        # Mostrar ocorrências por função epistemológica
        functions = defaultdict(int)
        for occ in occurrences:
            functions[occ['epistemic_function']['primary_function']] += 1
        for func, count in functions.items():
            print(f"    {func}: {count}")
    
    # ETAPA 3: Comparar semanticamente
    print(f"\n{'=' * 80}")
    print("[ETAPA 3] COMPARAÇÃO SEMÂNTICA")
    print(f"{'=' * 80}")
    
    comparison = compare_semantically(occurrences_by_doc)
    
    for doc_id, comp in comparison.items():
        print(f"\n  {doc_id} ({PAPER_A_DOCUMENTS[doc_id]['version']}):")
        print(f"    Total ocorrências: {comp['total_occurrences']}")
        if comp['canonical_occurrence']:
            canonical = comp['canonical_occurrence']
            print(f"    Canônica: {canonical['chunk_id']} ({canonical['page']})")
            print(f"    Equação: {canonical['equation_text']}")
            print(f"    Função: {canonical['epistemic_function']} — {canonical['function_description']}")
            print(f"    In oracle v2: {canonical['in_oracle_v2']}")
    
    # ETAPA 4: Determinar equivalência
    equivalences = determine_equivalence(comparison)
    
    # ETAPA 5: Avaliar extensão do oracle
    oracle_evaluation = evaluate_oracle_extension(equivalences)
    
    # Salvar relatório
    report = {
        'metadata': {
            'experiment': 'AION-6.2.10 — Auditoria de equivalência interversional',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'etapa_1_oracle_v2_frozen': B1_ORACLE_V2_CHUNKS,
        'etapa_2_occurrences_by_doc': {
            doc_id: [
                {
                    'chunk_id': o['chunk_id'],
                    'page': o['page'],
                    'equation_text': o['equation_text'],
                    'epistemic_function': o['epistemic_function']['primary_function'],
                    'in_oracle_v2': o['in_oracle_v2'],
                } for o in occs
            ] for doc_id, occs in occurrences_by_doc.items()
        },
        'etapa_3_semantic_comparison': {
            doc_id: {
                'total_occurrences': comp['total_occurrences'],
                'canonical_occurrence': comp['canonical_occurrence'],
                'all_occurrences_summary': comp['all_occurrences_summary'],
            } for doc_id, comp in comparison.items()
        },
        'etapa_4_equivalences': equivalences,
        'etapa_5_oracle_extension': oracle_evaluation,
        'next_steps': [
            'Aguardar determinação do Projetista Master sobre:',
            '1. Aceitar extensão do oracle para v3 (se EQUIVALENT encontrado)?',
            '2. Rebenchmark J com oracle v3?',
            '3. Investivar combinação J+E?',
        ],
    }
    
    json_path = OUTPUT_DIR / 'aion_6_2_10_equivalencia_interversional.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
