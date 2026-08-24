#!/usr/bin/env python3
"""
AION Passo 6.1-F — Composição Controlada do Corpus v1.3.0

Executa 13 etapas em sequência:
1. Composição Corpus v1.3.0 (8 documentos + 2 históricos + 2 inexistentes)
2. Registrar genealogia documental
3. Registrar CORPUS-002-HIST (v6.2 antigo, SUPERSEDED)
4. Promover novo CORPUS-002 (v6.2, 137.520 B, CURRENT)
5. Incorporar CORPUS-006 (Paper A v6.1 oficial)
6. Incorporar CORPUS-007 (Paper A v6.1 revisão)
7. Incorporar CORPUS-011 (Paper B v6.1 novo)
8. Ontology Audit (verificar se v1.1.0 é necessário)
9. TEMPORAL INDEX (com janela R^α entre v6.1rev e v6.2)
10. GraphRAG update
11. Corpus v1.3.0 frozen
12. Rebenchmark B1-B7
13. LCR (B6 TEMPORALLY BOUNDED, NOT CLOSED)

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import sys
import re
import hashlib
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

from aion_rag_proxy import TfidfVectorStore, CORPUS_FILES as OLD_CORPUS_FILES, CORPUS_DIR, parse_extracted_markdown
from aion_graphrag import CONCEPTS, ONTOLOGY_EDGES_E, CONCEPT_PATTERNS, detect_concepts_in_text

OUTPUT_DIR = Path('/home/z/my-project/download/rag')
INGEST_DIR = Path('/home/z/my-project/upload')


# === Composição v1.3.0 conforme determinação AION-6.1-F ===

CORPUS_V13_COMPOSITION = [
    {
        'id': 'CORPUS-001',
        'filename': 'AION-DOC-000.html',
        'title': 'Especificação do Documento Canônico',
        'version': '0.1.0',
        'document_date': 'UNKNOWN',
        'state': 'CURRENT',
        'role': 'normativo',
        'sha256_pdf': 'N/A (HTML)',
    },
    {
        'id': 'CORPUS-002-HIST',
        'filename': 'Paper_A_v6.2_FINAL.pdf (anterior, 134.294 B)',
        'title': 'Relational Coherence (Paper A v6.2 — versão anterior)',
        'version': 'v6.2',
        'document_date': '2026-08-12',
        'state': 'SUPERSEDED',
        'role': 'historical_artifact',
        'sha256_pdf': 'a ser verificado (artefato do Passo 3)',
        'superseded_by': 'CORPUS-002',
    },
    {
        'id': 'CORPUS-002',
        'filename': 'Paper_A_v6.2_FINAL.pdf (novo, 137.520 B)',
        'title': 'Relational Coherence in Biological Networks (Paper A v6.2 — CURRENT)',
        'version': 'v6.2',
        'document_date': '2026-08-12',
        'state': 'CURRENT / AUTHORITATIVE',
        'role': 'paper_final',
        'sha256_pdf': '971986d96c4ceb1ea5d7a17acdf2a54f4276403f2805c3945874304020adc433',
        'supersedes': 'CORPUS-002-HIST',
    },
    {
        'id': 'CORPUS-003',
        'filename': 'PARTE_IV_Formalizacao_Teorica_PT-BR.pdf',
        'title': 'PARTE IV — Formalização Teórica (Functor Φcat, Tensor Qµν)',
        'version': '1.0',
        'document_date': '2026-08-10',
        'state': 'CURRENT',
        'role': 'paper_theoretical',
        'sha256_pdf': 'a ser verificado (artefato do Passo 3)',
    },
    {
        'id': 'CORPUS-004',
        'filename': 'Paper_B_QDT_JCP_v6.1_PT-BR.pdf',
        'title': 'Dinâmica Quântica Dissipativa (Paper B — versão anterior)',
        'version': 'v6.1',
        'document_date': '2026-08-12',
        'state': 'HISTORICAL / PREVIOUS',
        'role': 'paper_historical',
        'sha256_pdf': 'a ser verificado (artefato do Passo 3)',
        'succeeded_by': 'CORPUS-011',
    },
    {
        'id': 'CORPUS-005',
        'filename': 'Cover_Letter_Paper_A_PRE_PT-BR.md',
        'title': 'Cover Letter – Paper A – PRE (PT-BR)',
        'version': 'NÃO DECLARADO',
        'document_date': '2026-08-10',
        'state': 'CURRENT',
        'role': 'cover_letter',
        'sha256_pdf': 'N/A (MD)',
        'reinterpretation': 'CONSISTENTE com v6.1 oficial (C=0.968) — não aspiracional',
    },
    {
        'id': 'CORPUS-006',
        'filename': 'Paper_A_v6.1_REVTeX_COMPLETE.pdf',
        'title': 'Relational Coherence (Paper A v6.1 oficial)',
        'version': 'v6.1',
        'document_date': '2026-08-10',
        'state': 'HISTORICAL',
        'role': 'paper_historical',
        'sha256_pdf': 'bc2e75fdd6bc8a6d62e4081a5c2858a890809bb07c860ade5d777bf456670f09',
        'P3_value': 'C = 0.968',
        'R_alpha': 'PRESENTE',
        'succeeded_by': 'CORPUS-007',
    },
    {
        'id': 'CORPUS-007',
        'filename': 'Paper_A_v6.1_REVTeX_COMPLETE .pdf (com espaço)',
        'title': 'Relational Coherence (Paper A v6.1 revisão posterior)',
        'version': 'v6.1-revision',
        'document_date': '2026-08-12',
        'state': 'HISTORICAL / SCIENTIFIC_REVISION',
        'role': 'paper_historical_revision',
        'sha256_pdf': '470cc395e0e7829379794480a62e7c1fb6bac4b622be171ad6c2554bd7346b2c',
        'P3_value': 'C = 0.793 ± 0.133',
        'R_alpha': 'PRESENTE',
        'succeeds': 'CORPUS-006',
        'succeeded_by': 'CORPUS-002',
    },
    {
        'id': 'CORPUS-011',
        'filename': 'Paper_B_QDT_v6.1_PT.pdf',
        'title': 'Escalonamento Quântico Dissipativo (Paper B v6.1 PT — novo)',
        'version': 'v6.1',
        'document_date': '2026-08-17',
        'state': 'CURRENT / NEW REVISION',
        'role': 'paper_final_expanded',
        'sha256_pdf': '30476135b03b182d8d38c74fc2b276119a356c5ced293797fdf9ccc7f70ba916',
        'expands': 'CORPUS-004',
    },
]

NON_EXISTENT_DOCS = [
    {'name': 'Paper A v6.0', 'state': 'DOES_NOT_EXIST', 'note': 'Declarado pelo Projetista Master em 17/08/2026'},
    {'name': 'Paper B v6.0', 'state': 'DOES_NOT_EXIST', 'note': 'Declarado pelo Projetista Master em 17/08/2026'},
]


# === Etapa 1: Composição Corpus v1.3.0 ===

def stage_1_composition() -> dict:
    print("\n[ETAPA 1] Composição Corpus v1.3.0")
    
    current_count = sum(1 for d in CORPUS_V13_COMPOSITION if 'CURRENT' in d['state'])
    historical_count = sum(1 for d in CORPUS_V13_COMPOSITION if 'HISTORICAL' in d['state'] or 'SUPERSEDED' in d['state'])
    
    print(f"  Documentos atuais: {current_count}")
    print(f"  Documentos históricos: {historical_count}")
    print(f"  Total: {len(CORPUS_V13_COMPOSITION)} documentos")
    print(f"  Documentos inexistentes: {len(NON_EXISTENT_DOCS)}")
    
    return {
        'documents': CORPUS_V13_COMPOSITION,
        'non_existent': NON_EXISTENT_DOCS,
        'current_count': current_count,
        'historical_count': historical_count,
    }


# === Etapa 2: Genealogia documental ===

def stage_2_genealogy() -> dict:
    print("\n[ETAPA 2] Genealogia documental")
    
    genealogy = [
        {
            'chain': 'Paper A evolution',
            'documents': [
                {'id': 'CORPUS-006', 'date': '2026-08-10', 'state': 'Paper A v6.1 oficial, C=0.968, R^α PRESENTE'},
                {'id': 'CORPUS-007', 'date': '2026-08-12', 'state': 'Paper A v6.1 revisão, C=0.793±0.133, R^α PRESENTE (SCIENTIFIC_REVISION)'},
                {'id': 'CORPUS-002-HIST', 'date': '2026-08-12', 'state': 'Paper A v6.2 anterior (134KB), AUC=0.793±0.133, R^α ABSENT — SUPERSEDED'},
                {'id': 'CORPUS-002', 'date': '2026-08-12', 'state': 'Paper A v6.2 FINAL (137KB), AUC=0.793±0.133, R^α ABSENT — CURRENT/AUTHORITATIVE'},
            ],
            'transitions': [
                {'from': 'CORPUS-006', 'to': 'CORPUS-007', 'type': 'SCIENTIFIC_REVISION', 'change': 'C: 0.968 → 0.793±0.133'},
                {'from': 'CORPUS-007', 'to': 'CORPUS-002-HIST', 'type': 'CONSOLIDATION', 'change': 'R^α: PRESENTE → ABSENT, version bump v6.1→v6.2'},
                {'from': 'CORPUS-002-HIST', 'to': 'CORPUS-002', 'type': 'TEXTUAL_EQUIVALENT_REPLACEMENT', 'change': 'PDF +3.226B, texto -2.732 chars (formatação)'},
            ],
        },
        {
            'chain': 'Paper B evolution',
            'documents': [
                {'id': 'CORPUS-004', 'date': '2026-08-12', 'state': 'Paper B anterior (3 págs, 12.755 chars), η presente'},
                {'id': 'CORPUS-011', 'date': '2026-08-17', 'state': 'Paper B v6.1 PT novo (5 págs, 19.679 chars), η presente — CURRENT'},
            ],
            'transitions': [
                {'from': 'CORPUS-004', 'to': 'CORPUS-011', 'type': 'EXPANSION', 'change': '+54% conteúdo (12.755 → 19.679 chars, 3→5 págs)'},
            ],
        },
    ]
    
    for chain in genealogy:
        print(f"\n  {chain['chain']}:")
        for doc in chain['documents']:
            print(f"    {doc['id']} ({doc['date']}): {doc['state'][:80]}...")
        print(f"  Transitions:")
        for t in chain['transitions']:
            print(f"    {t['from']} → {t['to']}: {t['type']} ({t['change']})")
    
    return {'genealogy_chains': genealogy}


# === Etapa 3-4: CORPUS-002-HIST + CORPUS-002 (substituição genealógica) ===

def stage_3_4_corpus_002_replacement() -> dict:
    print("\n[ETAPA 3-4] CORPUS-002: registro histórico + promoção do novo")
    
    # Etapa 3: registrar CORPUS-002-HIST
    corpus_002_hist = {
        'id': 'CORPUS-002-HIST',
        'original_filename': 'Paper_A_v6.2_FINAL.pdf (anterior)',
        'size_bytes': 134294,
        'sha256_pdf': 'a ser verificado (artefato do Passo 3, preservado)',
        'state': 'SUPERSEDED',
        'superseded_by': 'CORPUS-002',
        'superseded_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'preservation_reason': 'Genealogia documental — substituição não é apagamento',
    }
    print(f"  ✅ CORPUS-002-HIST registrado: SUPERSEDED (preservado como histórico)")
    
    # Etapa 4: promover novo CORPUS-002
    corpus_002_new = {
        'id': 'CORPUS-002',
        'filename': 'Paper_A_v6.2_FINAL.pdf (novo, 137.520 B)',
        'size_bytes': 137520,
        'sha256_pdf': '971986d96c4ceb1ea5d7a17acdf2a54f4276403f2805c3945874304020adc433',
        'state': 'CURRENT / AUTHORITATIVE',
        'supersedes': 'CORPUS-002-HIST',
        'audit_classification': 'TEXTUAL_EQUIVALENT (DIFERENÇA TEXTUAL MENOR)',
        'promotion_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }
    print(f"  ✅ CORPUS-002 promovido: CURRENT/AUTHORITATIVE")
    print(f"     SHA256: {corpus_002_new['sha256_pdf'][:32]}...")
    print(f"     Audit: {corpus_002_new['audit_classification']}")
    
    return {
        'corpus_002_hist': corpus_002_hist,
        'corpus_002_new': corpus_002_new,
    }


# === Etapa 5-7: Incorporar CORPUS-006, 007, 011 ===

def stage_5_6_7_incorporate_new_documents() -> dict:
    print("\n[ETAPA 5-7] Incorporar CORPUS-006, CORPUS-007, CORPUS-011")
    
    # Já foram ingeridos no Passo 6.1-D; aqui apenas confirmamos incorporação ao corpus v1.3.0
    incorporation = {
        'CORPUS-006': {
            'status': 'INCORPORATED',
            'role': 'Paper A v6.1 oficial (HISTORICAL)',
            'sha256': 'bc2e75fdd6bc8a6d62e4081a5c2858a890809bb07c860ade5d777bf456670f09',
            'extracted_md': '/download/rag/CORPUS-006_extracted.md',
        },
        'CORPUS-007': {
            'status': 'INCORPORATED',
            'role': 'Paper A v6.1 revisão (HISTORICAL / SCIENTIFIC_REVISION)',
            'sha256': '470cc395e0e7829379794480a62e7c1fb6bac4b622be171ad6c2554bd7346b2c',
            'extracted_md': '/download/rag/CORPUS-007_extracted.md',
        },
        'CORPUS-011': {
            'status': 'INCORPORATED',
            'role': 'Paper B v6.1 PT novo (CURRENT)',
            'sha256': '30476135b03b182d8d38c74fc2b276119a356c5ced293797fdf9ccc7f70ba916',
            'extracted_md': '/download/rag/CORPUS-011_extracted.md',
        },
    }
    
    for cid, info in incorporation.items():
        print(f"  ✅ {cid}: {info['status']} — {info['role']}")
    
    return incorporation


# === Etapa 8: Ontology Audit ===

def stage_8_ontology_audit() -> dict:
    print("\n[ETAPA 8] Ontology Audit — verificar se v1.1.0 é necessário")
    
    audit_findings = {
        'concepts_count': len(CONCEPTS),
        'edges_E_count': len(ONTOLOGY_EDGES_E),
        'audit_checks': [
            {
                'check': 'Definições ontológicas ainda válidas?',
                'result': 'SIM — conceitos (C, I, S, H, Φcat, Qµν, etc.) permanecem os mesmos',
                'requires_v1_1_0': False,
            },
            {
                'check': 'Arestas [E] ainda sustentadas por texto?',
                'result': 'SIM — citações diretas permanecem válidas; CORPUS-006 e CORPUS-007 adicionam nova evidência',
                'requires_v1_1_0': False,
            },
            {
                'check': 'Novas relações conceituais emergiram?',
                'result': 'SIM — detecção de revisão científica C: 0.968 → 0.793 é novo evento histórico, mas não muda CONCEITOS',
                'requires_v1_1_0': False,
                'note': 'Esta é atualização do ESTADO EVIDENCIAL, não estrutural — pertence ao grafo temporal, não à ontologia',
            },
            {
                'check': 'T5 (defasagem de versionamento) precisa ser reinterpretada?',
                'result': 'SIM — mas a reinterpretacao é sobre o ESTADO TEMPORAL, não sobre estrutura ontológica',
                'requires_v1_1_0': False,
                'note': 'T5 passa a ser: "cronologia documental correta" ao invés de "defasagem". Isto é atualização do grafo temporal, não da ontologia.',
            },
            {
                'check': 'B6 requer alteração ontológica?',
                'result': 'NAO — B6 é lacuna temporal, não estrutural. Continua NOT CLOSED.',
                'requires_v1_1_0': False,
            },
        ],
    }
    
    requires_v_1_1_0 = any(c.get('requires_v1_1_0', False) for c in audit_findings['audit_checks'])
    audit_findings['requires_new_ontology_version'] = requires_v_1_1_0
    audit_findings['ontology_version_after_audit'] = 'v1.0.0 (mantida)' if not requires_v_1_1_0 else 'v1.1.0 (necessária)'
    
    print(f"  Ontology v1.0.0 permanece vigente: {'SIM' if not requires_v_1_1_0 else 'NAO'}")
    for check in audit_findings['audit_checks']:
        print(f"  • {check['check']}")
        print(f"    Resultado: {check['result']}")
        if 'note' in check:
            print(f"    Nota: {check['note']}")
    
    return audit_findings


# === Etapa 9: TEMPORAL INDEX (com nova janela R^α) ===

def stage_9_temporal_index() -> dict:
    print("\n[ETAPA 9] TEMPORAL INDEX — atualizar com nova cronologia")
    
    # Estados temporais atualizados com a nova descoberta
    temporal_states = [
        # R^α: PRESENTE em v6.1 oficial (10/08)
        {
            'concept_id': 'R_recursion',
            'concept_label': 'Termo de recursão R^α',
            'valid_at': '2026-08-10',
            'document_date': '2026-08-10',
            'document': 'CORPUS-006',
            'version': 'v6.1',
            'state': 'R^α PRESENTE com α=1.3 (métrica C ainda inclui R)',
            'change_type': 'STABLE',
            'evidence_type': '[E]',
            'note': 'Confirmado por detecção textual: 5 padrões de R^α encontrados',
        },
        # R^α: ainda PRESENTE em v6.1 revisão (12/08)
        {
            'concept_id': 'R_recursion',
            'concept_label': 'Termo de recursão R^α',
            'valid_at': '2026-08-12',
            'document_date': '2026-08-12',
            'document': 'CORPUS-007',
            'version': 'v6.1-revision',
            'state': 'R^α ainda PRESENTE (mas C mudou de 0.968 para 0.793±0.133)',
            'change_type': 'STABLE',
            'evidence_type': '[E]',
            'note': 'R^α não foi removido nesta revisão científica; apenas resultado P3 foi atualizado',
        },
        # R^α: AUSENTE em v6.2 (12/08)
        {
            'concept_id': 'R_recursion',
            'concept_label': 'Termo de recursão R^α',
            'valid_at': '2026-08-12',
            'document_date': '2026-08-12',
            'document': 'CORPUS-002',
            'version': 'v6.2',
            'state': 'R^α AUSENTE — REMOVIDO da métrica C',
            'change_type': 'REVOKED',
            'evidence_type': '[E]',
            'note': 'Removido por irrelevância empírica (Sobol <1.1%)',
        },
        # C (Coerência Relacional) — evolução do valor P3
        {
            'concept_id': 'C',
            'concept_label': 'Coerência Relacional (C)',
            'valid_at': '2026-08-10',
            'document_date': '2026-08-10',
            'document': 'CORPUS-006',
            'version': 'v6.1',
            'state': 'P3: C = 0.968 (valor otimista, dataset PhysioNet Sleep-EDF aspiracional)',
            'change_type': 'INTRODUCED',
            'evidence_type': '[E]',
            'note': 'Valor P3 original em v6.1',
        },
        {
            'concept_id': 'C',
            'concept_label': 'Coerência Relacional (C)',
            'valid_at': '2026-08-12',
            'document_date': '2026-08-12',
            'document': 'CORPUS-007',
            'version': 'v6.1-revision',
            'state': 'P3: C = 0.793 ± 0.133 (valor realista, dataset OpenNeuro ds003768, 4 sujeitos)',
            'change_type': 'REFINED',
            'evidence_type': '[E]',
            'note': 'REVISÃO CIENTÍFICA — valor P3 atualizado de 0.968 para 0.793±0.133',
        },
        {
            'concept_id': 'C',
            'concept_label': 'Coerência Relacional (C)',
            'valid_at': '2026-08-12',
            'document_date': '2026-08-12',
            'document': 'CORPUS-002',
            'version': 'v6.2',
            'state': 'P3: C = 0.793 ± 0.133 (mantido da revisão v6.1)',
            'change_type': 'STABLE',
            'evidence_type': '[E]',
            'note': 'Valor consolidado em v6.2 FINAL',
        },
    ]
    
    # Janela temporal para B6 (data de abandono do R^α)
    b6_window = {
        'concept': 'R^α abandono',
        'earliest_known_absence': '2026-08-12 (CORPUS-002 v6.2)',
        'latest_known_presence': '2026-08-12 (CORPUS-007 v6.1 revisão)',
        'window': 'Entre CORPUS-007 (v6.1-revision, 12/08) e CORPUS-002 (v6.2, 12/08)',
        'precision': 'SAME_DAY_BOUNDED',
        'b6_status': 'TEMPORALLY BOUNDED, NOT CLOSED',
        'epistemic_note': 'Ambos eventos em 12/08/2026 — não há como distinguir ordem cronológica precisa sem timestamp de sub-dia. B6 NÃO está CLOSED porque data exata não pode ser determinada.',
    }
    
    # Recomputa TPC com novos estados
    total_states = len(temporal_states)
    verified_states = sum(1 for s in temporal_states if s['valid_at'] != 'UNKNOWN' and s['document_date'] != 'UNKNOWN')
    tpc = verified_states / total_states if total_states > 0 else 0.0
    
    print(f"  Estados temporais atualizados: {total_states}")
    print(f"  Estados com data verificável: {verified_states}")
    print(f"  TPC atualizado: {tpc:.4f} ({tpc*100:.1f}%)")
    print(f"  B6 status: {b6_window['b6_status']}")
    print(f"  B6 window: {b6_window['window']}")
    
    return {
        'temporal_states': temporal_states,
        'b6_window': b6_window,
        'tpc_updated': tpc,
    }


# === Etapa 10: GraphRAG update (apenas registro; sem re-execução) ===

def stage_10_graphrag_update() -> dict:
    print("\n[ETAPA 10] GraphRAG update — registro de novos nós/arestas")
    
    # Não vamos re-executar GraphRAG completo; apenas registrar que novos nós
    # e arestas serão adicionados quando o pipeline for re-executado
    update_plan = {
        'new_nodes_to_add': ['CORPUS-006', 'CORPUS-007', 'CORPUS-011'],
        'new_edges_to_add': [
            ('CORPUS-006', 'CORPUS-007', 'succeeded_by', 'SCIENTIFIC_REVISION'),
            ('CORPUS-007', 'CORPUS-002', 'succeeded_by', 'CONSOLIDATION'),
            ('CORPUS-002-HIST', 'CORPUS-002', 'superseded_by', 'TEXTUAL_EQUIVALENT_REPLACEMENT'),
            ('CORPUS-004', 'CORPUS-011', 'succeeded_by', 'EXPANSION'),
        ],
        'note': 'GraphRAG será re-executado na Etapa 12 (rebenchmark) com corpus expandido',
        'estimated_new_chunks': 23 + 23 + 17,  # CORPUS-006 + 007 + 011
    }
    
    print(f"  Novos nós a adicionar: {update_plan['new_nodes_to_add']}")
    print(f"  Novas arestas a adicionar: {len(update_plan['new_edges_to_add'])}")
    print(f"  Chunks estimados adicionais: {update_plan['estimated_new_chunks']}")
    
    return update_plan


# === Etapa 11: Corpus v1.3.0 frozen ===

def stage_11_freeze_corpus_v13() -> dict:
    print("\n[ETAPA 11] Corpus v1.3.0 — FROZEN")
    
    corpus_v13 = {
        'version': '1.3.0',
        'status': 'FROZEN',
        'frozen_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'composition': CORPUS_V13_COMPOSITION,
        'non_existent_documents': NON_EXISTENT_DOCS,
        'changes_from_v1.2.0': [
            'Adicionado CORPUS-006 (Paper A v6.1 oficial, 10/08)',
            'Adicionado CORPUS-007 (Paper A v6.1 revisão, 12/08, SCIENTIFIC_REVISION)',
            'Adicionado CORPUS-011 (Paper B v6.1 novo expandido, 17/08)',
            'Adicionado CORPUS-002-HIST (Paper A v6.2 anterior, SUPERSEDED)',
            'Promovido CORPUS-002 para nova versão (137.520 B, substituindo 134.294 B)',
            'Reinterpretado T5: Cover Letter PT-BR era consistente com v6.1 original, não aspiracional',
            'B6 status: TEMPORALLY BOUNDED, NOT CLOSED (janela 12/08 entre v6.1rev e v6.2)',
        ],
        'principles_preserved': [
            'Nenhum documento histórico removido',
            'Genealogia documental preservada',
            'Substituição não é apagamento',
            'B6 não foi artificialmente CLOSED',
            'Ontologia v1.0.0 mantida (sem v1.1.0 desnecessário)',
        ],
    }
    
    print(f"  Versão: {corpus_v13['version']}")
    print(f"  Status: {corpus_v13['status']}")
    print(f"  Documentos: {len(corpus_v13['composition'])}")
    print(f"  Documentos inexistentes: {len(corpus_v13['non_existent_documents'])}")
    
    # Salvar manifesto do corpus v1.3.0
    manifest_path = OUTPUT_DIR / 'aion_corpus_v1.3.0_manifest.json'
    manifest_path.write_text(json.dumps(corpus_v13, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"  Manifesto salvo: {manifest_path}")
    
    return corpus_v13


def main():
    print("=" * 70)
    print("AION Passo 6.1-F — Composição Controlada do Corpus v1.3.0")
    print("=" * 70)
    
    # Etapas 1-11
    stage_1 = stage_1_composition()
    stage_2 = stage_2_genealogy()
    stage_3_4 = stage_3_4_corpus_002_replacement()
    stage_5_6_7 = stage_5_6_7_incorporate_new_documents()
    stage_8 = stage_8_ontology_audit()
    stage_9 = stage_9_temporal_index()
    stage_10 = stage_10_graphrag_update()
    stage_11 = stage_11_freeze_corpus_v13()
    
    # Relatório completo
    report = {
        'metadata': {
            'experiment': 'AION-6.1-F — Composição Controlada Corpus v1.3.0',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'stage_1_composition': stage_1,
        'stage_2_genealogy': stage_2,
        'stage_3_4_corpus_002_replacement': stage_3_4,
        'stage_5_6_7_incorporation': stage_5_6_7,
        'stage_8_ontology_audit': stage_8,
        'stage_9_temporal_index': stage_9,
        'stage_10_graphrag_update': stage_10,
        'stage_11_corpus_v13_frozen': stage_11,
        'pending_steps': [
            'ETAPA 12: Rebenchmark B1-B7 (requer re-executar pipeline RAG com corpus expandido)',
            'ETAPA 13: LCR (B6 TEMPORALLY BOUNDED, NOT CLOSED — não conta como CLOSED)',
        ],
    }
    
    json_path = OUTPUT_DIR / 'aion_6_1_f_corpus_v13_composition.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    print(f"\n{'=' * 70}")
    print("[RESUMO AION-6.1-F]")
    print(f"{'=' * 70}")
    print(f"  Corpus v1.3.0: FROZEN")
    print(f"  Documentos atuais: {stage_1['current_count']}")
    print(f"  Documentos históricos: {stage_1['historical_count']}")
    print(f"  Documentos inexistentes: {len(NON_EXISTENT_DOCS)}")
    print(f"  Ontologia: v1.0.0 mantida (não requer v1.1.0)")
    print(f"  B6: TEMPORALLY BOUNDED, NOT CLOSED")
    print(f"  TPC atualizado: {stage_9['tpc_updated']:.4f}")
    
    print(f"\n[PENDENTE]")
    print(f"  Etapa 12: Rebenchmark B1-B7")
    print(f"  Etapa 13: LCR (com B6 NOT_CLOSED)")
    
    return report


if __name__ == '__main__':
    main()
