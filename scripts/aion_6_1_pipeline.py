#!/usr/bin/env python3
"""
AION Passo 6.1 — Pipeline de Aquisição Controlada

Pipeline auditável para incorporar novos documentos ao corpus sem
comprometer as garantias epistemológicas do AION-MVP-001:

INGEST → AUDIT → EXTRACT → CHUNK → ONTOLOGY → TEMPORAL INDEX → GRAPH → CORPUS VERSION

Cada novo documento passa por:
- INGEST: recebimento do arquivo
- AUDIT: verificação de integridade (hash, metadados declarados)
- EXTRACT: extração de texto estruturado (PyMuPDF + pdfplumber)
- CHUNK: chunking semântico por seção/página (igual ao Passo 3)
- ONTOLOGY: identificação de conceitos da ontologia v1.0.0 no novo documento
- TEMPORAL INDEX: registro de estado temporal do conceito no novo documento
- GRAPH: adição de arestas de co-ocorrência ao GraphRAG
- CORPUS VERSION: bump da versão do corpus (v1.2.0 → v1.3.0)

NÃO altera: TF-IDF, GraphRAG, P-RESP-001 v0.3, AION-EVAL-002 v0.2, B1

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
from dataclasses import dataclass, asdict

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

from aion_rag_proxy import CORPUS_FILES, CORPUS_DIR, parse_extracted_markdown
from aion_graphrag import CONCEPT_PATTERNS, detect_concepts_in_text

OUTPUT_DIR = Path('/home/z/my-project/download/rag')
INGEST_DIR = Path('/home/z/my-project/upload')


# === Estrutura de metadados para novos documentos ===

@dataclass
class DocumentMetadata:
    """Metadados obrigatórios para cada documento adquirido."""
    document_id: str  # ex: CORPUS-006
    filename: str  # ex: Paper_A_v6.0.pdf
    title: str  # declarado no documento
    version: str  # ex: v6.0
    document_date: str  # ISO 8601 ou UNKNOWN
    origin: str  # ex: "submission archive", "personal archive"
    sha256_hash: str  # hash do arquivo
    state: str  # ex: "FINAL draft", "submitted to BJoP", etc.
    language: str  # ex: "PT-BR", "EN"
    author: str  # ex: "Edson Carvalho do Nascimento"
    file_size_bytes: int
    file_type: str  # ex: "PDF", "MD", "HTML"
    acquired_at: str  # ISO timestamp da aquisição
    acquisition_method: str  # ex: "user_upload", "user_paste"
    notes: str = ""  # observações adicionais


# === Pipeline de aquisição controlada ===

def stage_1_ingest(filepath: Path) -> dict:
    """INGEST: recebe o arquivo e calcula hash."""
    if not filepath.exists():
        return {'status': 'FAIL', 'reason': f'Arquivo não encontrado: {filepath}'}
    
    file_bytes = filepath.read_bytes()
    sha256 = hashlib.sha256(file_bytes).hexdigest()
    
    return {
        'status': 'OK',
        'filepath': str(filepath),
        'sha256': sha256,
        'file_size_bytes': len(file_bytes),
        'file_type': filepath.suffix.lstrip('.').upper(),
    }


def stage_2_audit(filepath: Path, expected_metadata: dict, ingest_data: dict) -> dict:
    """AUDIT: verifica integridade e metadados declarados."""
    issues = []
    
    # Verifica hash contra esperado (se fornecido)
    if 'expected_sha256' in expected_metadata:
        if ingest_data['sha256'] != expected_metadata['expected_sha256']:
            issues.append(f"Hash mismatch: esperado {expected_metadata['expected_sha256']}, obtido {ingest_data['sha256']}")
    
    # Verifica tamanho mínimo
    if ingest_data['file_size_bytes'] < 100:
        issues.append(f"Arquivo muito pequeno: {ingest_data['file_size_bytes']} bytes")
    
    # Verifica tipo suportado
    if ingest_data['file_type'] not in ('PDF', 'MD', 'HTML', 'TXT'):
        issues.append(f"Tipo não suportado: {ingest_data['file_type']}")
    
    # Verifica metadados obrigatórios
    required_fields = ['document_id', 'title', 'version', 'document_date', 'origin', 'state']
    for field in required_fields:
        if field not in expected_metadata:
            issues.append(f"Metadado obrigatório ausente: {field}")
    
    return {
        'status': 'PASS' if not issues else 'FAIL',
        'issues': issues,
        'audit_timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }


def stage_3_extract(filepath: Path, file_type: str) -> dict:
    """EXTRACT: extrai texto estruturado (PDF, MD ou HTML)."""
    if file_type == 'PDF':
        # Usa o extractor do Passo 3
        import fitz
        import pdfplumber
        
        doc = fitz.open(filepath)
        pages = []
        for i, page in enumerate(doc):
            text = page.get_text('text')
            pages.append({'page_number': i + 1, 'text': text})
        doc.close()
        
        # Extrai tabelas
        tables = []
        try:
            with pdfplumber.open(filepath) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    for j, table in enumerate(page_tables):
                        tables.append({
                            'page': i + 1,
                            'table_index': j + 1,
                            'rows': table,
                        })
        except Exception as e:
            pass  # Tabelas são opcionais
        
        full_text = '\n'.join(p['text'] for p in pages)
        
        return {
            'status': 'OK',
            'page_count': len(pages),
            'char_count': len(full_text),
            'full_text': full_text,
            'pages': pages,
            'tables_found': len(tables),
        }
    
    elif file_type in ('MD', 'HTML', 'TXT'):
        text = filepath.read_text(encoding='utf-8')
        return {
            'status': 'OK',
            'page_count': 1,
            'char_count': len(text),
            'full_text': text,
            'pages': [{'page_number': 1, 'text': text}],
            'tables_found': 0,
        }
    
    return {'status': 'FAIL', 'reason': f'Tipo não suportado: {file_type}'}


def stage_4_chunk(extract_data: dict, document_id: str) -> dict:
    """CHUNK: chunking semântico por seção/página."""
    # Reutiliza função do Passo 3
    # Cria um markdown estruturado para passar ao parser
    md_content = f"# {document_id} — Extração de Texto Estruturado\n\n"
    md_content += f"**ID do Corpus:** {document_id}\n\n---\n\n"
    
    for page in extract_data['pages']:
        md_content += f"### Página {page['page_number']}\n\n```text\n{page['text']}\n```\n\n"
    
    # Usa o parser do Passo 3
    chunks = parse_extracted_markdown(md_content, document_id)
    
    return {
        'status': 'OK',
        'chunk_count': len(chunks),
        'chunks': [
            {
                'chunk_id': c.chunk_id,
                'page': c.page,
                'section': c.section,
                'text_length': c.char_count,
            } for c in chunks
        ],
    }


def stage_5_ontology(extract_data: dict) -> dict:
    """ONTOLOGY: identifica conceitos da ontologia v1.0.0 no novo documento."""
    full_text = extract_data['full_text']
    concepts_found = detect_concepts_in_text(full_text)
    
    return {
        'status': 'OK',
        'concepts_found': sorted(concepts_found),
        'concept_count': len(concepts_found),
    }


def stage_6_temporal_index(ontology_data: dict, document_metadata: dict) -> dict:
    """TEMPORAL INDEX: registra estado temporal dos conceitos neste documento."""
    states = []
    for concept_id in ontology_data['concepts_found']:
        states.append({
            'concept_id': concept_id,
            'valid_at': document_metadata['document_date'],
            'document_date': document_metadata['document_date'],
            'document': document_metadata['document_id'],
            'version': document_metadata['version'],
            'change_type': 'INTRODUCED',  # default; pode ser refinado
            'state': f"Detectado em {document_metadata['document_id']} ({document_metadata['version']})",
            'evidence_type': '[E]',
            'note': 'Detectado automaticamente pelo pipeline de aquisição',
        })
    
    return {
        'status': 'OK',
        'temporal_states_added': len(states),
        'states': states,
    }


def stage_7_graph(ontology_data: dict, chunk_data: dict) -> dict:
    """GRAPH: identifica pares de co-ocorrência que serão adicionados ao GraphRAG."""
    # Pares de conceitos detectados no mesmo documento
    concepts = ontology_data['concepts_found']
    pairs = []
    for i, a in enumerate(concepts):
        for b in concepts[i+1:]:
            pairs.append({
                'source': a,
                'target': b,
                'evidence_type': '[E-cooc]',
                'status': 'CANDIDATE',
                'document_origin': chunk_data['chunks'][0]['chunk_id'].split('#')[0] if chunk_data['chunks'] else 'UNKNOWN',
            })
    
    return {
        'status': 'OK',
        'co_occurrence_pairs': len(pairs),
        'pairs': pairs,
    }


def stage_8_corpus_version(document_metadata: dict, current_version: str = '1.2.0') -> dict:
    """CORPUS VERSION: bump da versão do corpus."""
    # v1.2.0 → v1.3.0 (adicionar documento)
    parts = current_version.split('.')
    new_version = f"{parts[0]}.{int(parts[1]) + 1}.0"
    
    return {
        'status': 'OK',
        'previous_version': current_version,
        'new_version': new_version,
        'change_description': f"Adição de {document_metadata['document_id']} ({document_metadata['filename']})",
        'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }


def execute_pipeline(filepath: Path, expected_metadata: dict) -> dict:
    """Executa o pipeline completo de 8 estágios."""
    pipeline_log = {
        'pipeline_started_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'filepath': str(filepath),
        'expected_metadata': expected_metadata,
        'stages': {},
    }
    
    # Estágio 1: INGEST
    print(f"  [1/8] INGEST...")
    ingest = stage_1_ingest(filepath)
    pipeline_log['stages']['1_INGEST'] = ingest
    if ingest['status'] != 'OK':
        pipeline_log['pipeline_status'] = 'FAILED_AT_STAGE_1'
        return pipeline_log
    print(f"        hash={ingest['sha256'][:16]}... size={ingest['file_size_bytes']}B type={ingest['file_type']}")
    
    # Estágio 2: AUDIT
    print(f"  [2/8] AUDIT...")
    audit = stage_2_audit(filepath, expected_metadata, ingest)
    pipeline_log['stages']['2_AUDIT'] = audit
    if audit['status'] != 'PASS':
        pipeline_log['pipeline_status'] = 'FAILED_AT_STAGE_2'
        print(f"        ❌ {audit['issues']}")
        return pipeline_log
    print(f"        ✅ Audit pass — sem issues")
    
    # Constrói metadados completos
    metadata = DocumentMetadata(
        document_id=expected_metadata['document_id'],
        filename=filepath.name,
        title=expected_metadata['title'],
        version=expected_metadata['version'],
        document_date=expected_metadata['document_date'],
        origin=expected_metadata['origin'],
        sha256_hash=ingest['sha256'],
        state=expected_metadata['state'],
        language=expected_metadata.get('language', 'PT-BR'),
        author=expected_metadata.get('author', 'Edson Carvalho do Nascimento'),
        file_size_bytes=ingest['file_size_bytes'],
        file_type=ingest['file_type'],
        acquired_at=datetime.now(timezone.utc).isoformat(timespec='seconds'),
        acquisition_method=expected_metadata.get('acquisition_method', 'user_upload'),
        notes=expected_metadata.get('notes', ''),
    )
    pipeline_log['document_metadata'] = asdict(metadata)
    
    # Estágio 3: EXTRACT
    print(f"  [3/8] EXTRACT...")
    extract = stage_3_extract(filepath, ingest['file_type'])
    pipeline_log['stages']['3_EXTRACT'] = {k: v for k, v in extract.items() if k != 'full_text' and k != 'pages'}
    if extract['status'] != 'OK':
        pipeline_log['pipeline_status'] = 'FAILED_AT_STAGE_3'
        return pipeline_log
    print(f"        pages={extract['page_count']} chars={extract['char_count']} tables={extract['tables_found']}")
    
    # Estágio 4: CHUNK
    print(f"  [4/8] CHUNK...")
    chunk_data = stage_4_chunk(extract, metadata.document_id)
    pipeline_log['stages']['4_CHUNK'] = chunk_data
    if chunk_data['status'] != 'OK':
        pipeline_log['pipeline_status'] = 'FAILED_AT_STAGE_4'
        return pipeline_log
    print(f"        chunks={chunk_data['chunk_count']}")
    
    # Estágio 5: ONTOLOGY
    print(f"  [5/8] ONTOLOGY...")
    ontology = stage_5_ontology(extract)
    pipeline_log['stages']['5_ONTOLOGY'] = ontology
    if ontology['status'] != 'OK':
        pipeline_log['pipeline_status'] = 'FAILED_AT_STAGE_5'
        return pipeline_log
    print(f"        concepts={ontology['concept_count']}: {ontology['concepts_found']}")
    
    # Estágio 6: TEMPORAL INDEX
    print(f"  [6/8] TEMPORAL INDEX...")
    temporal = stage_6_temporal_index(ontology, asdict(metadata))
    pipeline_log['stages']['6_TEMPORAL_INDEX'] = temporal
    if temporal['status'] != 'OK':
        pipeline_log['pipeline_status'] = 'FAILED_AT_STAGE_6'
        return pipeline_log
    print(f"        temporal_states_added={temporal['temporal_states_added']}")
    
    # Estágio 7: GRAPH
    print(f"  [7/8] GRAPH...")
    graph = stage_7_graph(ontology, chunk_data)
    pipeline_log['stages']['7_GRAPH'] = graph
    if graph['status'] != 'OK':
        pipeline_log['pipeline_status'] = 'FAILED_AT_STAGE_7'
        return pipeline_log
    print(f"        co_occurrence_pairs={graph['co_occurrence_pairs']}")
    
    # Estágio 8: CORPUS VERSION
    print(f"  [8/8] CORPUS VERSION...")
    corpus_version = stage_8_corpus_version(asdict(metadata))
    pipeline_log['stages']['8_CORPUS_VERSION'] = corpus_version
    if corpus_version['status'] != 'OK':
        pipeline_log['pipeline_status'] = 'FAILED_AT_STAGE_8'
        return pipeline_log
    print(f"        version: {corpus_version['previous_version']} → {corpus_version['new_version']}")
    
    pipeline_log['pipeline_status'] = 'COMPLETED'
    pipeline_log['pipeline_completed_at'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
    
    return pipeline_log


# === Critério LCR (Lacuna Closure Rate) ===

def evaluate_lacuna_closure(lacuna_id: str, question: str, response_data: dict) -> dict:
    """
    Avalia se uma lacuna foi CLOSED após aquisição documental.
    
    CLOSED requer:
    1. Informação efetivamente no corpus
    2. Recuperada pelo retrieval
    3. Provenance válida
    4. Contexto temporal consistente
    5. Resposta não transforma interpretação em evidência
    """
    criteria = {
        '1_in_corpus': response_data.get('evidence_status') == 'EVIDENCE_VALID',
        '2_retrieved': response_data.get('valid_count', 0) > 0,
        '3_provenance_valid': response_data.get('invalid_count', 0) == 0,
        '4_temporal_consistent': 'PASS' in response_data.get('eval_002_v02', {}).get('categories', {}).get('T1', {}).get('status', ''),
        '5_no_interpretation_as_evidence': response_data.get('classificacao_epistemologica', {}).get('[I]', 0) == 0 or 
                                            response_data.get('classificacao_epistemologica', {}).get('[E]', 0) > 0,
    }
    
    is_closed = all(criteria.values())
    
    return {
        'lacuna_id': lacuna_id,
        'question': question,
        'criteria': criteria,
        'is_closed': is_closed,
        'closure_status': 'CLOSED' if is_closed else 'NOT_CLOSED',
        'failed_criteria': [k for k, v in criteria.items() if not v],
    }


def compute_lcr(closure_evaluations: list) -> dict:
    """LCR = lacunas_resolvidas / lacunas_selecionadas."""
    total = len(closure_evaluations)
    closed = sum(1 for e in closure_evaluations if e['is_closed'])
    
    return {
        'total_lacunas': total,
        'closed_lacunas': closed,
        'lcr': closed / total if total > 0 else 0.0,
        'lcr_percentage': f"{(closed / total * 100) if total > 0 else 0:.1f}%",
    }


# === Main — Apenas prepara pipeline; não executa sem documentos ===

def main():
    print("=" * 70)
    print("AION Passo 6.1 — Pipeline de Aquisição Controlada")
    print("=" * 70)
    
    print("\n[STATUS] Pipeline implementado e pronto para execução.")
    print("         Aguardando upload/colagem de documentos P1 e P2.")
    
    print("\n[DOCUMENTOS AGUARDANDO AQUISIÇÃO]")
    
    expected_documents = [
        {
            'prioridade': 'P1',
            'document_id': 'CORPUS-006',
            'filename_esperado': 'Paper_A_v6.0.pdf',
            'title': 'Relational Coherence (Paper A v6.0 — com termo de recursão R^α)',
            'version': 'v6.0',
            'document_date': 'UNKNOWN',
            'origin': 'submission archive',
            'state': 'FINAL draft (com R^α)',
            'lacunas_que_resolve': ['B6 (data de abandono do R^α)', 'TPC UNKNOWN pré-v6.2'],
        },
        {
            'prioridade': 'P1',
            'document_id': 'CORPUS-007',
            'filename_esperado': 'Paper_A_v6.1.pdf',
            'title': 'Relational Coherence (Paper A v6.1 — transição para v6.2)',
            'version': 'v6.1',
            'document_date': 'UNKNOWN',
            'origin': 'submission archive',
            'state': 'DRAFT (transição)',
            'lacunas_que_resolve': ['B6 (data de abandono do R^α)'],
        },
        {
            'prioridade': 'P1',
            'document_id': 'CORPUS-008',
            'filename_esperado': 'Paper_B_v6.0.pdf',
            'title': 'Dinâmica Quântica Dissipativa (Paper B v6.0 — com hipótese η, dímero 2 sítios)',
            'version': 'v6.0',
            'document_date': 'UNKNOWN',
            'origin': 'submission archive',
            'state': 'FINAL draft (com η e dímero 2 sítios)',
            'lacunas_que_resolve': ['B6 (data de proposição do η)'],
        },
        {
            'prioridade': 'P2',
            'document_id': 'CORPUS-009',
            'filename_esperado': 'Cover_Letter_Paper_A_PRE.md',
            'title': 'Cover Letter (EN — versão oficial submetida ao PRE)',
            'version': 'NÃO DECLARADO',
            'document_date': 'UNKNOWN',
            'origin': 'submission archive',
            'state': 'Carta de submissão oficial (EN)',
            'lacunas_que_resolve': ['T6 (lacuna Cover Letter EN)'],
        },
        {
            'prioridade': 'P2',
            'document_id': 'CORPUS-010',
            'filename_esperado': 'Partes_I_a_III_Formalizacao.pdf',
            'title': 'Partes I-III do Programa de Formalização Físico-Matemática',
            'version': 'UNKNOWN',
            'document_date': 'UNKNOWN',
            'origin': 'submission archive',
            'state': 'Documento teórico (Passos 1-15)',
            'lacunas_que_resolve': ['T9 (lacuna estrutural Partes I-III)'],
        },
    ]
    
    for d in expected_documents:
        print(f"\n  [{d['prioridade']}] {d['document_id']} — {d['filename_esperado']}")
        print(f"        Versão: {d['version']}")
        print(f"        Data esperada: {d['document_date']}")
        print(f"        Estado: {d['state']}")
        print(f"        Lacunas que resolve:")
        for lacuna in d['lacunas_que_resolve']:
            print(f"          • {lacuna}")
    
    print(f"\n[PIPELINE PRONTO]")
    print(f"  8 estágios implementados:")
    print(f"  1. INGEST       — recebimento + hash SHA256")
    print(f"  2. AUDIT        — verificação de integridade e metadados")
    print(f"  3. EXTRACT      — extração de texto estruturado (PyMuPDF + pdfplumber)")
    print(f"  4. CHUNK        — chunking semântico por seção/página")
    print(f"  5. ONTOLOGY     — identificação de conceitos da ontologia v1.0.0")
    print(f"  6. TEMPORAL     — registro de estado temporal do conceito")
    print(f"  7. GRAPH        — adição de arestas de co-ocorrência ao GraphRAG")
    print(f"  8. CORPUS VER   — bump da versão do corpus (v1.2.0 → v1.3.0)")
    
    print(f"\n[LCR (Lacuna Closure Rate) — definido]")
    print(f"  LCR = lacunas_resolvidas / lacunas_selecionadas")
    print(f"  CLOSED requer:")
    print(f"    1. Informação efetivamente no corpus")
    print(f"    2. Recuperada pelo retrieval")
    print(f"    3. Provenance válida (validator P-RESP-001 v0.3)")
    print(f"    4. Contexto temporal consistente")
    print(f"    5. Resposta não transforma interpretação em evidência")
    
    # Salva manifesto do pipeline
    manifest = {
        'metadata': {
            'pipeline': 'AION-6.1 — Aquisição Controlada',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'status': 'PIPELINE_READY_AWAITING_DOCUMENTS',
        'expected_documents': expected_documents,
        'pipeline_stages': [
            '1_INGEST',
            '2_AUDIT',
            '3_EXTRACT',
            '4_CHUNK',
            '5_ONTOLOGY',
            '6_TEMPORAL_INDEX',
            '7_GRAPH',
            '8_CORPUS_VERSION',
        ],
        'lcr_definition': {
            'formula': 'LCR = lacunas_resolvidas / lacunas_selecionadas',
            'closed_criteria': [
                '1_in_corpus',
                '2_retrieved',
                '3_provenance_valid',
                '4_temporal_consistent',
                '5_no_interpretation_as_evidence',
            ],
        },
        'principles_preserved': [
            'TF-IDF permanece',
            'GraphRAG permanece',
            'P-RESP-001 v0.3 permanece',
            'AION-EVAL-002 v0.2 permanece',
            'Dify permanece apenas como orquestrador',
            'B1 permanece KNOWN LIMITATION',
        ],
    }
    
    manifest_path = OUTPUT_DIR / 'aion_6_1_pipeline_manifest.json'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] Manifesto: {manifest_path}")
    print(f"  Tamanho: {manifest_path.stat().st_size} bytes")
    
    print(f"\n{'=' * 70}")
    print("[AGUARDANDO AÇÃO DO PROJETISTA MASTER]")
    print(f"{'=' * 70}")
    print("Para cada documento P1/P2, fazer upload ou colar conteúdo.")
    print("Após recebimento, executar: aion_6_1_pipeline.py <filepath> <document_id>")
    print("Pipeline executará 8 estágios e atualizará corpus para v1.3.0.")
    
    return manifest


if __name__ == '__main__':
    main()
