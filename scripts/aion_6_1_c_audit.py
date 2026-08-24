#!/usr/bin/env python3
"""
AION Passo 6.1-C — Auditoria de Aquisição

Executa auditoria detalhada dos 4 PDFs recebidos:
1. Verificação de identidade interna (título, autor, data declarada)
2. Hash SHA256 de cada arquivo
3. Comparação entre versões (v6.1 vs v6.2; Paper B antigo vs novo)
4. Identificação de duplicatas e variantes
5. Decisão de ingestão seletiva

Estabelece distinção crítica:
- DOCUMENTO NÃO EXISTENTE (Paper A v6.0, Paper B v6.0) — estado permanente
- DOCUMENTO AUSENTE DO CORPUS — pode ser adquirido no futuro

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import hashlib
import re
from pathlib import Path
from datetime import datetime, timezone
import sys

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

import fitz  # PyMuPDF

INGEST_DIR = Path('/home/z/my-project/upload')
OUTPUT_DIR = Path('/home/z/my-project/download/rag')


# === Identificações curatorialmente declaradas ===

IDENTIFICATION = {
    'Paper_A_v6.1_REVTeX_COMPLETE.pdf': {
        'curatorial_id': 'Paper A v6.1 oficial',
        'document_id': 'CORPUS-006',
        'version': 'v6.1',
        'language': 'EN',
        'state': 'DRAFT (transição para v6.2)',
    },
    'Paper_A_v6.1_REVTeX_COMPLETE .pdf': {  # COM ESPAÇO no nome
        'curatorial_id': 'Paper A v6.1 revisão posterior',
        'document_id': 'CORPUS-007',
        'version': 'v6.1-revision',
        'language': 'EN',
        'state': 'REVISÃO POSTERIOR (data posterior ao v6.2)',
    },
    'Paper_B_QDT_v6.1_PT.pdf': {
        'curatorial_id': 'Paper B v6.1 PT (novo, 5 págs)',
        'document_id': 'CORPUS-011',
        'version': 'v6.1',
        'language': 'PT-BR',
        'state': 'NOVO Paper B v6.1 expandido',
    },
    'Paper_A_v6.2_FINAL.pdf': {
        'curatorial_id': 'Paper A v6.2 FINAL (substituto do v6.2 anterior)',
        'document_id': 'CORPUS-002-NEW',
        'version': 'v6.2',
        'language': 'EN',
        'state': 'SUBSTITUI o v6.2 anteriormente auditado',
    },
}

# Documentos declarados como NÃO EXISTENTES
NON_EXISTENT_DOCUMENTS = [
    {
        'document_id': 'CORPUS-006-PREVIOUS-ATTEMPT',
        'name': 'Paper A v6.0',
        'state': 'DOCUMENTO NÃO EXISTENTE / NÃO DISPONÍVEL NO HISTÓRICO DOCUMENTAL DECLARADO',
        'note': 'Projetista Master declarou em 17/08/2026 que esta versão não existe.',
        'lacunas_afetadas': ['B6 (data exata de abandono do R^α)'],
        'epistemic_implication': 'B6 NÃO pode ser CLOSED por esta via; restará apenas janela temporal v6.1→v6.2',
    },
    {
        'document_id': 'CORPUS-008-PREVIOUS-ATTEMPT',
        'name': 'Paper B v6.0',
        'state': 'DOCUMENTO NÃO EXISTENTE / NÃO DISPONÍVEL NO HISTÓRICO DOCUMENTAL DECLARADO',
        'note': 'Projetista Master declarou em 17/08/2026 que esta versão não existe.',
        'lacunas_afetadas': ['B6 (data exata de proposição do η)'],
        'epistemic_implication': 'B6 NÃO pode ser CLOSED por esta via; restará apenas inferência a partir de menção textual no v6.1',
    },
]


def compute_sha256(filepath: Path) -> str:
    """Calcula hash SHA256 do arquivo."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def extract_pdf_metadata(filepath: Path) -> dict:
    """Extrai metadados internos do PDF."""
    doc = fitz.open(filepath)
    meta = dict(doc.metadata)
    page_count = len(doc)
    
    # Extrai texto da primeira página para auditoria interna
    first_page_text = doc[0].get_text()
    
    # Procura por data declarada no texto
    date_patterns = [
        r'Dated:\s*([A-Z][a-z]+ \d{1,2}, \d{4})',
        r'\((\d{1,2} de [A-Z][a-z]+ de \d{4})\)',
        r'(\d{1,2}/\d{1,2}/\d{4})',
    ]
    declared_date_in_text = None
    for pattern in date_patterns:
        match = re.search(pattern, first_page_text)
        if match:
            declared_date_in_text = match.group(1)
            break
    
    # Procura por versão no texto
    version_patterns = [
        r'v(\d+\.\d+)',
        r'Versão:\s*(\d+\.\d+)',
        r'Version:\s*(\d+\.\d+)',
    ]
    declared_version_in_text = None
    for pattern in version_patterns:
        match = re.search(pattern, first_page_text, re.IGNORECASE)
        if match:
            declared_version_in_text = match.group(1)
            break
    
    # Procura por título
    title_in_text = None
    first_lines = first_page_text.strip().split('\n')[:3]
    for line in first_lines:
        if len(line.strip()) > 20 and not line.strip().startswith('Edson'):
            title_in_text = line.strip()
            break
    
    # Verifica presença de R^α (para distinguir versões do Paper A)
    has_recursion_R = bool(re.search(r'R\s*\^?\s*α|R\^\\alpha|R\s*com\s*expoente', first_page_text, re.IGNORECASE))
    
    # Verifica presença de η (para distinguir versões do Paper B)
    has_eta_hypothesis = bool(re.search(r'η|\\eta|comensurabilidade', first_page_text, re.IGNORECASE))
    
    doc.close()
    
    return {
        'pdf_metadata': {
            'title': meta.get('title', ''),
            'author': meta.get('author', ''),
            'subject': meta.get('subject', ''),
            'creator': meta.get('creator', ''),
            'producer': meta.get('producer', ''),
            'creationDate': meta.get('creationDate', ''),
            'modDate': meta.get('modDate', ''),
        },
        'page_count': page_count,
        'declared_date_in_text': declared_date_in_text,
        'declared_version_in_text': declared_version_in_text,
        'title_in_first_page': title_in_text,
        'has_recursion_R_alpha': has_recursion_R,
        'has_eta_hypothesis': has_eta_hypothesis,
        'first_page_excerpt': first_page_text[:500],
    }


def audit_single_pdf(filepath: Path, identification: dict) -> dict:
    """Executa auditoria completa de um PDF."""
    print(f"\n  Auditing: {filepath.name}")
    
    # Hash
    sha256 = compute_sha256(filepath)
    file_size = filepath.stat().st_size
    print(f"    SHA256: {sha256[:32]}...")
    print(f"    Size: {file_size} bytes")
    
    # Metadados internos
    pdf_meta = extract_pdf_metadata(filepath)
    
    # Verificação de identidade interna
    identity_checks = {
        'title_match': bool(pdf_meta['pdf_metadata']['title']),
        'author_match': 'Edson' in pdf_meta['pdf_metadata']['author'] or 'Nascimento' in pdf_meta['pdf_metadata']['author'],
        'date_in_text': pdf_meta['declared_date_in_text'] is not None,
        'version_in_text': pdf_meta['declared_version_in_text'] is not None,
    }
    
    # Comparação com identificação curatorial
    curatorial_match = {
        'expected_version': identification['version'],
        'version_in_pdf_metadata': pdf_meta['declared_version_in_text'],
        'version_match': pdf_meta['declared_version_in_text'] == identification['version'].replace('-revision', ''),
        'expected_language': identification['language'],
    }
    
    # Determina se é Paper A ou B
    if 'Paper_A' in filepath.name:
        document_type = 'Paper A'
        # Verifica presença de R^α
        document_specific = {
            'has_R_alpha': pdf_meta['has_recursion_R_alpha'],
            'note': 'R^α presente = versão pré-v6.2; R^α ausente = v6.2 ou posterior',
        }
    elif 'Paper_B' in filepath.name:
        document_type = 'Paper B'
        document_specific = {
            'has_eta_hypothesis': pdf_meta['has_eta_hypothesis'],
            'note': 'η presente = versão pré-v6.1 final; η ausente = v6.1 final (retratada)',
        }
    else:
        document_type = 'Unknown'
        document_specific = {}
    
    audit_result = {
        'filename': filepath.name,
        'filepath': str(filepath),
        'curatorial_identification': identification,
        'sha256': sha256,
        'file_size_bytes': file_size,
        'pdf_metadata': pdf_meta,
        'identity_checks': identity_checks,
        'curatorial_match': curatorial_match,
        'document_type': document_type,
        'document_specific': document_specific,
        'audit_timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }
    
    print(f"    Document type: {document_type}")
    print(f"    Identity checks: {identity_checks}")
    if document_specific:
        print(f"    Document specific: {document_specific}")
    
    return audit_result


def compare_pdfs(audit_results: dict) -> dict:
    """Compara PDFs para identificar duplicatas e variantes."""
    comparisons = []
    
    # Comparar Paper A v6.1 (138KB) vs Paper A v6.1 revisão (326KB)
    pa_v61 = audit_results.get('Paper_A_v6.1_REVTeX_COMPLETE.pdf')
    pa_v61_rev = audit_results.get('Paper_A_v6.1_REVTeX_COMPLETE .pdf')
    if pa_v61 and pa_v61_rev:
        comparisons.append({
            'comparison': 'Paper A v6.1 (138KB) vs Paper A v6.1 revisão (326KB)',
            'file_a': pa_v61['filename'],
            'file_b': pa_v61_rev['filename'],
            'same_sha256': pa_v61['sha256'] == pa_v61_rev['sha256'],
            'different_size': pa_v61['file_size_bytes'] != pa_v61_rev['file_size_bytes'],
            'creation_dates': {
                'a': pa_v61['pdf_metadata']['pdf_metadata']['creationDate'],
                'b': pa_v61_rev['pdf_metadata']['pdf_metadata']['creationDate'],
            },
            'R_alpha_presence': {
                'a': pa_v61['document_specific'].get('has_R_alpha', 'N/A'),
                'b': pa_v61_rev['document_specific'].get('has_R_alpha', 'N/A'),
            },
            'verdict': 'ARQUIVOS DIFERENTES' if pa_v61['sha256'] != pa_v61_rev['sha256'] else 'IDÊNTICOS',
        })
    
    # Comparar Paper A v6.2 atual (no corpus, 134.294 B) vs Paper A v6.2 FINAL (137.520 B)
    pa_v62_new = audit_results.get('Paper_A_v6.2_FINAL.pdf')
    # Não temos acesso direto ao Paper A v6.2 do corpus original aqui, mas podemos registrar
    if pa_v62_new:
        comparisons.append({
            'comparison': 'Paper A v6.2 FINAL (novo, 137.520 B) vs Paper A v6.2 (corpus atual, 134.294 B)',
            'file_a': 'Paper_A_v6.2_FINAL.pdf (novo upload)',
            'file_b': 'Paper_A_v6.2_FINAL.pdf (corpus atual, do Passo 3)',
            'size_difference_bytes': 137520 - 134294,
            'verdict': 'VARIANTES — substituição requer confirmação explícita',
            'note': 'Tamanhos diferentes indicam que não são idênticos. Auditoria textual necessária antes da substituição.',
        })
    
    # Comparar Paper B antigo (3 págs, do corpus) vs Paper B novo (5 págs)
    pb_new = audit_results.get('Paper_B_QDT_v6.1_PT.pdf')
    if pb_new:
        comparisons.append({
            'comparison': 'Paper B v6.1 PT (novo, 5 págs) vs Paper B v6.1 PT-BR (corpus atual, 3 págs)',
            'file_a': 'Paper_B_QDT_v6.1_PT.pdf (novo upload)',
            'file_b': 'Paper_B_QDT_JCP_v6.1_PT-BR.pdf (corpus atual, do Passo 3)',
            'page_count_a': pb_new['pdf_metadata']['page_count'],
            'page_count_b': 3,
            'page_difference': pb_new['pdf_metadata']['page_count'] - 3,
            'verdict': 'VARIANTES EXPANDIDAS — Paper B novo tem 2 páginas a mais',
            'note': 'NÃO substituir automaticamente. Auditoria textual necessária para verificar se é revisão expandida ou documento diferente.',
        })
    
    return {'comparisons': comparisons}


def main():
    print("=" * 70)
    print("AION Passo 6.1-C — Auditoria de Aquisição")
    print("=" * 70)
    
    # Auditoria de cada PDF
    audit_results = {}
    for filename, identification in IDENTIFICATION.items():
        filepath = INGEST_DIR / filename
        if not filepath.exists():
            print(f"\n  ❌ NOT FOUND: {filename}")
            continue
        audit_results[filename] = audit_single_pdf(filepath, identification)
    
    # Comparação entre versões
    print(f"\n{'=' * 70}")
    print("[COMPARAÇÃO DE VERSÕES]")
    print(f"{'=' * 70}")
    comparison_results = compare_pdfs(audit_results)
    for c in comparison_results['comparisons']:
        print(f"\n  {c['comparison']}")
        for k, v in c.items():
            if k != 'comparison':
                print(f"    {k}: {v}")
    
    # Registrar documentos não-existentes
    print(f"\n{'=' * 70}")
    print("[DOCUMENTOS DECLARADOS NÃO EXISTENTES]")
    print(f"{'=' * 70}")
    for doc in NON_EXISTENT_DOCUMENTS:
        print(f"\n  {doc['name']} ({doc['document_id']})")
        print(f"    State: {doc['state']}")
        print(f"    Note: {doc['note']}")
        print(f"    Lacunas afetadas: {doc['lacunas_afetadas']}")
        print(f"    Implicação epistêmica: {doc['epistemic_implication']}")
    
    # Decisão de ingestão seletiva
    print(f"\n{'=' * 70}")
    print("[DECISÃO DE INGESTÃO SELETIVA]")
    print(f"{'=' * 70}")
    
    ingestion_decisions = []
    
    # Paper A v6.1 (138KB) — ingest
    pa_v61 = audit_results.get('Paper_A_v6.1_REVTeX_COMPLETE.pdf')
    if pa_v61:
        decision = {
            'filename': 'Paper_A_v6.1_REVTeX_COMPLETE.pdf',
            'document_id': 'CORPUS-006',
            'decision': 'INGEST',
            'rationale': 'Paper A v6.1 oficial, data 10/08/2026, anterior ao v6.2 final (12/08). Documento crítico para delimitação temporal do abandono do R^α.',
            'audit_passed': all(pa_v61['identity_checks'].values()),
            'pre_conditions': [
                'Verificar se R^α está presente no texto (esperado: SIM, pois v6.2 já não tem)',
                'Verificar coerência temporal com v6.2 (já no corpus)',
            ],
        }
        ingestion_decisions.append(decision)
        print(f"\n  ✅ INGEST: {decision['filename']} → {decision['document_id']}")
        print(f"     Rationale: {decision['rationale']}")
        print(f"     Audit passed: {decision['audit_passed']}")
    
    # Paper A v6.1 revisão (326KB) — ingest como CORPUS-007
    pa_v61_rev = audit_results.get('Paper_A_v6.1_REVTeX_COMPLETE .pdf')
    if pa_v61_rev:
        decision = {
            'filename': 'Paper_A_v6.1_REVTeX_COMPLETE .pdf',
            'document_id': 'CORPUS-007',
            'decision': 'INGEST (com ressalva)',
            'rationale': 'Revisão posterior do Paper A v6.1, data 12/08/2026 (igual ao v6.2). Documento legítimo mas de identidade ambígua — revisão posterior rotulada como v6.1.',
            'audit_passed': all(pa_v61_rev['identity_checks'].values()),
            'pre_conditions': [
                'Verificar se contém R^α ou não (distinguindo de v6.2)',
                'Registrar explicitamente como "v6.1 revisão posterior" no grafo temporal',
                'Não confundir com v6.1 oficial (CORPUS-006)',
            ],
        }
        ingestion_decisions.append(decision)
        print(f"\n  ⚠️ INGEST (com ressalva): {decision['filename']} → {decision['document_id']}")
        print(f"     Rationale: {decision['rationale']}")
        print(f"     Pre-conditions: {decision['pre_conditions']}")
    
    # Paper B v6.1 PT (novo) — ingest como CORPUS-011
    pb_new = audit_results.get('Paper_B_QDT_v6.1_PT.pdf')
    if pb_new:
        decision = {
            'filename': 'Paper_B_QDT_v6.1_PT.pdf',
            'document_id': 'CORPUS-011',
            'decision': 'INGEST (como novo documento, não substituição)',
            'rationale': 'Paper B v6.1 expandido (5 págs vs 3 anteriores). Documento distinto do Paper_B_QDT_JCP_v6.1_PT-BR.pdf já no corpus. Mantém o antigo como CORPUS-004.',
            'audit_passed': all(pb_new['identity_checks'].values()),
            'pre_conditions': [
                'Não substituir CORPUS-004 (Paper B antigo, 3 págs)',
                'Registrar como CORPUS-011 (novo)',
                'Verificar relação temporal com CORPUS-004',
            ],
        }
        ingestion_decisions.append(decision)
        print(f"\n  ✅ INGEST (novo): {decision['filename']} → {decision['document_id']}")
        print(f"     Rationale: {decision['rationale']}")
        print(f"     Pre-conditions: {decision['pre_conditions']}")
    
    # Paper A v6.2 FINAL (137.520 B) — substituição requer confirmação
    pa_v62_new = audit_results.get('Paper_A_v6.2_FINAL.pdf')
    if pa_v62_new:
        decision = {
            'filename': 'Paper_A_v6.2_FINAL.pdf',
            'document_id': 'CORPUS-002 (substituição)',
            'decision': 'HOLD — substituição requer confirmação explícita',
            'rationale': 'Tamanho diferente do v6.2 já auditado (137.520 B vs 134.294 B = 3.226 B de diferença). Substituição silenciosa comprometeria integridade do corpus. Auditoria textual necessária antes de substituir.',
            'audit_passed': all(pa_v62_new['identity_checks'].values()),
            'pre_conditions': [
                'Comparar texto extraído do novo v6.2 com v6.2 já no corpus',
                'Identificar diferenças (3.226 B pode indicar pequena revisão)',
                'Confirmar com Projetista Master se substituição é desejada',
            ],
        }
        ingestion_decisions.append(decision)
        print(f"\n  ⏸️ HOLD: {decision['filename']} → {decision['document_id']}")
        print(f"     Rationale: {decision['rationale']}")
        print(f"     Pre-conditions: {decision['pre_conditions']}")
    
    # Salvar relatório de auditoria
    report = {
        'metadata': {
            'experiment': 'AION-6.1-C — Auditoria de Aquisição',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'identification_curatorial': IDENTIFICATION,
        'non_existent_documents': NON_EXISTENT_DOCUMENTS,
        'audit_results': audit_results,
        'comparison_results': comparison_results,
        'ingestion_decisions': ingestion_decisions,
        'next_step': 'Ingestão seletiva dos 3 documentos aprovados (CORPUS-006, CORPUS-007, CORPUS-011) após confirmação do Projetista Master. CORPUS-002 (substituição) permanece em HOLD até auditoria textual.',
    }
    
    json_path = OUTPUT_DIR / 'aion_6_1_c_audit_results.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    # Resumo
    print(f"\n{'=' * 70}")
    print("[RESUMO DA AUDITORIA]")
    print(f"{'=' * 70}")
    
    ingest_count = sum(1 for d in ingestion_decisions if 'INGEST' in d['decision'])
    hold_count = sum(1 for d in ingestion_decisions if 'HOLD' in d['decision'])
    non_existent_count = len(NON_EXISTENT_DOCUMENTS)
    
    print(f"\nDocumentos para INGEST: {ingest_count}")
    for d in ingestion_decisions:
        if 'INGEST' in d['decision']:
            print(f"  • {d['filename']} → {d['document_id']} ({d['decision']})")
    
    print(f"\nDocumentos em HOLD: {hold_count}")
    for d in ingestion_decisions:
        if 'HOLD' in d['decision']:
            print(f"  • {d['filename']} → {d['document_id']}")
    
    print(f"\nDocumentos NÃO EXISTENTES: {non_existent_count}")
    for doc in NON_EXISTENT_DOCUMENTS:
        print(f"  • {doc['name']} — {doc['state']}")
    
    print(f"\n[PRÓXIMO PASSO]")
    print(f"  Confirmar com Projetista Master a ingestão dos 3 documentos aprovados.")
    print(f"  CORPUS-002 (substituição) permanece em HOLD até auditoria textual.")
    print(f"  Após confirmação: executar pipeline 8 estágios para cada documento.")
    
    return report


if __name__ == '__main__':
    main()
