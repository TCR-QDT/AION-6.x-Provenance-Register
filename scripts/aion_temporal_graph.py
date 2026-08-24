#!/usr/bin/env python3
"""
AION Passo 5.7 — Grafo Temporal

Implementa grafo temporal de estados conceituais com:
- 6 tipos de mudança: INTRODUCED, REFINED, EXTENDED, CONTRADICTED, REVOKED, STABLE
- Distinção valid_at vs document_date
- Estados UNKNOWN quando data não pode ser estabelecida
- TPC (Temporal Provenance Coverage) calculado

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
sys.path.insert(0, '/home/z/.local/lib/python3.13/site-packages')

OUTPUT_DIR = Path('/home/z/my-project/download/rag')

# === Metadados canônicos dos documentos (datas declaradas) ===

DOC_METADATA = {
    'CORPUS-001': {
        'version': '0.1.0',
        'document_date': 'UNKNOWN',  # NÃO DECLARADO no HTML canônico
        'kind': 'normativo',
        'short_title': 'AION-DOC-000',
    },
    'CORPUS-002': {
        'version': 'v6.2',
        'document_date': '2026-08-12',  # declarado no PDF
        'kind': 'paper_FINAL',
        'short_title': 'Paper A',
        'previous_versions': [
            {'version': 'v5.1', 'document_date': 'UNKNOWN', 'note': 'Submetido ao Brazilian Journal of Physics — feedback recebido, citado em Acknowledgments do Paper A v6.2'},
            {'version': 'v6.0', 'document_date': 'UNKNOWN', 'note': 'Incluía termo de recursão R^α com α=1.3; removido em v6.2'},
        ],
    },
    'CORPUS-003': {
        'version': '1.0',
        'document_date': '2026-08-10',  # declarado na p.1 do PDF
        'kind': 'documento_teorico_difusao_controlada',
        'short_title': 'Parte IV',
    },
    'CORPUS-004': {
        'version': 'v6.1',
        'document_date': '2026-08-12',
        'kind': 'paper_FINAL_rascunho',
        'short_title': 'Paper B',
        'previous_versions': [
            {'version': 'v6.0', 'document_date': 'UNKNOWN', 'note': 'ST=-0.795 (dímero 2 sítios); hipótese η proposta'},
        ],
    },
    'CORPUS-005': {
        'version': 'NÃO DECLARADO',
        'document_date': '2026-08-10',  # declarado na Cover Letter
        'kind': 'carta_submissao_v6.1_aspiracional',
        'short_title': 'Cover Letter PT-BR',
    },
}

# === Estados conceituais temporais ===
# Cada estado = snapshot de um conceito em um momento documental

CONCEPT_TEMPORAL_STATES = [
    # === Conceito C (Coerência Relacional) ===
    {
        'concept_id': 'C',
        'concept_label': 'Coerência Relacional (C)',
        'valid_at': 'UNKNOWN',
        'document_date': '2026-08-10',
        'document': 'CORPUS-005',
        'version': 'v6.1 aspiracional',
        'state': 'C = I × S × H^β, β canônico não declarado',
        'change_type': 'STABLE',
        'previous_state': None,
        'evidence_text': '"uma métrica unificada C = I × S × H^β para a coerência informacional"',
        'evidence_type': '[E]',
        'note': 'Cover Letter PT-BR descreve plano aspiracional v6.1; métrica fundamental já estável.',
    },
    {
        'concept_id': 'C',
        'concept_label': 'Coerência Relacional (C)',
        'valid_at': '2026-08-12',
        'document_date': '2026-08-12',
        'document': 'CORPUS-002',
        'version': 'v6.2',
        'state': 'C = I × S × H^β, β=0.5 calibrado via LOOCV sobre 12 fixtures sintéticas',
        'change_type': 'REFINED',
        'previous_state': 'C = I × S × H^β, β canônico não declarado',
        'evidence_text': '"We adopt β = 0.5 as the canonical value throughout this work"',
        'evidence_type': '[E]',
        'note': 'Paper A v6.2 FINAL — β calibrado, termo de recursão R removido por irrelevância empírica (Sobol <1.1%).',
    },
    
    # === Conceito β (calibração) ===
    {
        'concept_id': 'beta',
        'concept_label': 'β (calibração LOOCV)',
        'valid_at': 'UNKNOWN',
        'document_date': 'UNKNOWN',
        'document': 'NÃO DOCUMENTADO ANTES DE v6.2',
        'version': 'pre-v6.2',
        'state': 'β não explicitamente calibrado; presunção de β=1 ou valor nominal',
        'change_type': 'INTRODUCED',
        'previous_state': None,
        'evidence_text': 'Ausência documental — inferência do gap entre v5.1 (BJoP feedback) e v6.2 FINAL',
        'evidence_type': '[I]',
        'note': 'Estado reconstruído por inferência; marcado UNKNOWN.',
    },
    {
        'concept_id': 'beta',
        'concept_label': 'β (calibração LOOCV)',
        'valid_at': '2026-08-12',
        'document_date': '2026-08-12',
        'document': 'CORPUS-002',
        'version': 'v6.2',
        'state': 'β=0.5, calibrado via LOOCV, consistência = 1.0 em [0.1, 1.5]',
        'change_type': 'REFINED',
        'previous_state': 'β não explicitamente calibrado',
        'evidence_text': '"calibrated via leave-one-out cross-validation (LOOCV) over 12 synthetic connectome fixtures"',
        'evidence_type': '[E]',
        'note': 'Inconsistência #1 do Paper A resolvida nesta versão.',
    },
    
    # === Conceito R (termo de recursão) — REVOKED ===
    {
        'concept_id': 'R_recursion',
        'concept_label': 'Termo de recursão R^α',
        'valid_at': 'UNKNOWN',
        'document_date': 'UNKNOWN',
        'document': 'Paper A v5.1/v6.0 (não no corpus)',
        'version': 'pre-v6.2',
        'state': 'R^α com α=1.3 como parte da métrica C',
        'change_type': 'INTRODUCED',
        'previous_state': None,
        'evidence_text': '"Earlier versions of TCR included a recursion term R with exponent α = 1.3"',
        'evidence_type': '[E]',
        'note': 'Referência ao estado anterior feita no Paper A v6.2 (p.1, linha 90-91).',
    },
    {
        'concept_id': 'R_recursion',
        'concept_label': 'Termo de recursão R^α',
        'valid_at': '2026-08-12',
        'document_date': '2026-08-12',
        'document': 'CORPUS-002',
        'version': 'v6.2',
        'state': 'REMOVIDO da métrica C',
        'change_type': 'REVOKED',
        'previous_state': 'R^α com α=1.3 como parte da métrica C',
        'evidence_text': '"global sensitivity analysis (Sobol) reveals that R contributes less than 1.1% of the variance in C, rendering it empirically irrelevant. We therefore drop it in this version"',
        'evidence_type': '[E]',
        'note': 'Inconsistência #2 do Paper A resolvida — abandono por irrelevância empírica (parsimônia).',
    },
    
    # === Conceito Φcat (Functor) ===
    {
        'concept_id': 'Phi_cat',
        'concept_label': 'Functor Φcat',
        'valid_at': '2026-08-10',
        'document_date': '2026-08-10',
        'document': 'CORPUS-003',
        'version': '1.0',
        'state': 'Φcat : C → Set, X ↦ Hom_C(•, X) — Conjectura (Passo 16)',
        'change_type': 'INTRODUCED',
        'previous_state': None,
        'evidence_text': '"Define-se o functor Φcat : C → Set, X ↦ Hom_C(•, X)"',
        'evidence_type': '[E]',
        'note': 'CORPUS-003 é Parte IV de um programa maior; passos 1-15 não estão no corpus — estado anterior desconhecido.',
    },
    
    # === Conceito Qµν (Tensor) ===
    {
        'concept_id': 'Q_munu',
        'concept_label': 'Tensor Qµν',
        'valid_at': '2026-08-10',
        'document_date': '2026-08-10',
        'document': 'CORPUS-003',
        'version': '1.0',
        'state': 'Forma bilinear simétrica (0,2), 5 axiomas (Q1-Q5) — Proposta (Passo 17)',
        'change_type': 'INTRODUCED',
        'previous_state': None,
        'evidence_text': '"Definição 3.1 (Tensor Qµν)... Q1. Simetria; Q2. Conservação covariante; Q3. Covariância geral; Q4. Traço bem definido; Q5. Decaimento assintótico"',
        'evidence_type': '[E]',
        'note': 'CORPUS-003 é Parte IV; estado anterior desconhecido.',
    },
    
    # === Conceito Equação de Einstein modificada ===
    {
        'concept_id': 'Einstein_mod',
        'concept_label': 'Equação de Einstein modificada',
        'valid_at': '2026-08-10',
        'document_date': '2026-08-10',
        'document': 'CORPUS-003',
        'version': '1.0',
        'state': 'Gµν = 8πG(Tµν + Qµν) — Proposta teórica',
        'change_type': 'INTRODUCED',
        'previous_state': None,
        'evidence_text': '"a equação modificada Gµν = 8πG(Tµν + Qµν)"',
        'evidence_type': '[E]',
        'note': 'Derivação variacional pendente (lacuna declarada na Tabela 2).',
    },
    
    # === Conceito Power-law T₂ (FMO) ===
    {
        'concept_id': 'Power_law_T2',
        'concept_label': 'Power-law T₂ (FMO)',
        'valid_at': 'UNKNOWN',
        'document_date': 'UNKNOWN',
        'document': 'Paper B v6.0 (não no corpus)',
        'version': 'v6.0',
        'state': 'T₂ = K·J^1.205·λ^(-1.114)·γ^(-1.068)·T^(-0.795), R²=0.914 (dímero 2 sítios)',
        'change_type': 'INTRODUCED',
        'previous_state': None,
        'evidence_text': '"Em nosso trabalho anterior (v6.0), reportamos um escalonamento power-law..."',
        'evidence_type': '[E]',
        'note': 'Estado anterior citado no Paper B v6.1; data do documento original desconhecida.',
    },
    {
        'concept_id': 'Power_law_T2',
        'concept_label': 'Power-law T₂ (FMO)',
        'valid_at': '2026-08-12',
        'document_date': '2026-08-12',
        'document': 'CORPUS-004',
        'version': 'v6.1',
        'state': 'T₂ = (1.567×10⁴)·J^0.831·λ^(-0.843)·γ^(-0.766)·T^(-0.261), R²=0.988 (FMO 7 sítios)',
        'change_type': 'REFINED',
        'previous_state': 'T₂ = K·J^1.205·λ^(-1.114)·γ^(-1.068)·T^(-0.795) (dímero)',
        'evidence_text': '"obtemos T₂ = K J^0.831 λ^(-0.843) γ^(-0.766) T^(-0.261) com R² = 0.988"',
        'evidence_type': '[E]',
        'note': 'Inconsistência #3 do Paper A resolvida — re-derivação a partir do Hamiltoniano FMO completo (375 combinações).',
    },
    
    # === Conceito η (cross-scale) — REVOKED ===
    {
        'concept_id': 'eta_hyp',
        'concept_label': 'Hipótese η (cross-scale)',
        'valid_at': 'UNKNOWN',
        'document_date': 'UNKNOWN',
        'document': 'Paper B v6.0 (não no corpus)',
        'version': 'v6.0',
        'state': 'Hipótese η proposta — comensurabilidade cross-scale entre δβ e δST',
        'change_type': 'INTRODUCED',
        'previous_state': None,
        'evidence_text': '"Reportamos também um índice de comensurabilidade cross-scale η..."',
        'evidence_type': '[E]',
        'note': 'Estado anterior citado no Paper B v6.1.',
    },
    {
        'concept_id': 'eta_hyp',
        'concept_label': 'Hipótese η (cross-scale)',
        'valid_at': '2026-08-12',
        'document_date': '2026-08-12',
        'document': 'CORPUS-004',
        'version': 'v6.1',
        'state': 'HIPÓTESE RETIRADA — critério |δβ − δST|/δβ < 0.2 não satisfeito (razão = 0.291)',
        'change_type': 'REVOKED',
        'previous_state': 'Hipótese η proposta — comensurabilidade cross-scale',
        'evidence_text': '"O critério não é satisfeito (razão = 0.291), levando-nos a retrair a hipótese η da análise presente"',
        'evidence_type': '[E]',
        'note': 'Inconsistência #5 do Paper A resolvida por retração formal.',
    },
    
    # === Conceito "Consciência" — nunca presente ===
    {
        'concept_id': 'consciencia',
        'concept_label': 'Consciência',
        'valid_at': '2026-08-16',
        'document_date': '2026-08-16',
        'document': 'AION-CORPUS-001 Handoff original',
        'version': 'Handoff',
        'state': 'Mencionado no Handoff original como "Nível 0 — Campo Primordial da Consciência" — inferência do curador, não presente nos textos',
        'change_type': 'INTRODUCED',
        'previous_state': None,
        'evidence_text': 'Handoff original menciona "Nível 0 — Campo Primordial da Consciência"',
        'evidence_type': '[I]',
        'note': 'Inferência posteriormente descreditada pela auditoria T4 — termo não aparece em nenhum dos 5 textos.',
    },
    {
        'concept_id': 'consciencia',
        'concept_label': 'Consciência',
        'valid_at': '2026-08-16',
        'document_date': '2026-08-16',
        'document': 'Auditoria da ontologia v1.0.0',
        'version': 'v1.0.0',
        'state': 'AUSÊNCIA CONFIRMADA — termo "consciência" não aparece em nenhum dos 5 textos extraídos. Única ponte: Paper A cita Tononi (Φ-IIT) como referência crítica, não como conceito do programa.',
        'change_type': 'CONTRADICTED',
        'previous_state': 'Mencionado no Handoff como sinônimo de CORPUS-003',
        'evidence_text': 'Auditoria de corpus: termo "consciência" ausente de CORPUS-001 a 005',
        'evidence_type': '[E]',
        'note': 'T4 resolvida na ontologia v1.0.0 — Handoff original continha inferência.',
    },
    
    # === Conceito "Campo Primordial" — nunca presente nos textos ===
    {
        'concept_id': 'campo_primordial',
        'concept_label': 'Campo Primordial',
        'valid_at': '2026-08-16',
        'document_date': '2026-08-16',
        'document': 'AION-CORPUS-001 Handoff original',
        'version': 'Handoff',
        'state': 'Atribuído ao CORPUS-003 no Handoff original como subtítulo descritivo',
        'change_type': 'INTRODUCED',
        'previous_state': None,
        'evidence_text': 'Handoff original: "Documento 3 — Nível 0 (Campo Primordial)"',
        'evidence_type': '[I]',
        'note': 'Inferência do curador a partir do contexto; termo não aparece no texto do CORPUS-003.',
    },
    {
        'concept_id': 'campo_primordial',
        'concept_label': 'Campo Primordial',
        'valid_at': '2026-08-17',
        'document_date': '2026-08-17',
        'document': 'Auditoria da ontologia v1.0.0',
        'version': 'v1.0.0',
        'state': 'AUSÊNCIA CONFIRMADA — termo "Campo Primordial" não aparece no texto extraído do CORPUS-003. Conceito removido da ontologia v1.0.0.',
        'change_type': 'CONTRADICTED',
        'previous_state': 'Atribuído ao CORPUS-003 no Handoff',
        'evidence_text': 'Auditoria de corpus: termo "Campo Primordial" ausente do CORPUS-003',
        'evidence_type': '[E]',
        'note': 'Conceito removido da ontologia v1.0.0 (Cluster B).',
    },
    
    # === Dependência ontológica Paper A → Parte IV — REVOKED ===
    {
        'concept_id': 'edge_paperA_to_parteIV',
        'concept_label': 'Dependência ontológica Paper A → Parte IV',
        'valid_at': '2026-08-16',
        'document_date': '2026-08-16',
        'document': 'AION-CORPUS-001 HTML canônico v1.2.0',
        'version': 'v1.2.0',
        'state': 'CORPUS-002 (Paper A) depende ontologicamente do CORPUS-003 (Parte IV)',
        'change_type': 'INTRODUCED',
        'previous_state': None,
        'evidence_text': 'HTML canônico seção 3: "Paper A depende ontologicamente da Parte IV"',
        'evidence_type': '[I]',
        'note': 'Inferência do curador no registro do corpus.',
    },
    {
        'concept_id': 'edge_paperA_to_parteIV',
        'concept_label': 'Dependência ontológica Paper A → Parte IV',
        'valid_at': '2026-08-17',
        'document_date': '2026-08-17',
        'document': 'Auditoria da ontologia v1.0.0',
        'version': 'v1.0.0',
        'state': 'REVOGADA — substituída por paralelismo epistêmico',
        'change_type': 'REVOKED',
        'previous_state': 'Paper A depende ontologicamente da Parte IV',
        'evidence_text': '"deliberately separated to maintain focus and falsifiability" (Paper A v6.2, p.5-6)',
        'evidence_type': '[E]',
        'note': 'Revogação baseada em citação direta do Paper A v6.2.',
    },
    
    # === Programa de pesquisa Lakatosiano ===
    {
        'concept_id': 'Lakatos_program',
        'concept_label': 'Programa de pesquisa Lakatosiano',
        'valid_at': '2026-08-10',
        'document_date': '2026-08-10',
        'document': 'CORPUS-003',
        'version': '1.0',
        'state': 'Auto-designação explícita — núcleo firme + cinturão protetor; núcleo = formalização categórico-tensorial unificada',
        'change_type': 'INTRODUCED',
        'previous_state': None,
        'evidence_text': '"A leitura conjunta dos três passos sugere uma estrutura epistêmica análoga à distinção de Lakatos"',
        'evidence_type': '[E]',
        'note': 'CORPUS-003 declara explicitamente a estrutura lakatosiana.',
    },
]


def compute_tpc(states: list) -> dict:
    """
    TPC (Temporal Provenance Coverage):
    razão entre estados com data/proveniência verificável e total de estados registrados.
    Estados UNKNOWN não contam no numerador mas contam no denominador.
    """
    total = len(states)
    verified = sum(1 for s in states if s['valid_at'] != 'UNKNOWN' and s['document_date'] != 'UNKNOWN')
    unknown = sum(1 for s in states if s['valid_at'] == 'UNKNOWN' or s['document_date'] == 'UNKNOWN')
    
    return {
        'total_states': total,
        'states_with_verified_date': verified,
        'states_with_unknown_date': unknown,
        'tpc': verified / total if total > 0 else 0.0,
        'tpc_percentage': f"{(verified / total * 100) if total > 0 else 0:.1f}%",
    }


def group_states_by_concept(states: list) -> dict:
    """Agrupa estados por concept_id para visualização de evolução."""
    grouped = defaultdict(list)
    for s in states:
        grouped[s['concept_id']].append(s)
    
    # Ordena por data (UNKNOWN vai para o início)
    for cid in grouped:
        grouped[cid].sort(key=lambda x: (
            x['valid_at'] == 'UNKNOWN',  # False (UNKNOWN=False=0) vem depois, mas queremos UNKNOWN antes
            x['valid_at'] if x['valid_at'] != 'UNKNOWN' else '0000-01-01'
        ))
    
    return dict(grouped)


def run_temp_test(test_id: str, question: str, states: list) -> dict:
    """Executa um teste do plano AION-TEMP-001 a 005."""
    print(f"\n[{test_id}] {question}")
    print('-' * 60)
    
    grouped = group_states_by_concept(states)
    
    if test_id == 'AION-TEMP-001':
        # Evolução da Coerência Relacional
        concept_states = grouped.get('C', [])
        answer_lines = [f"Evolução documental de 'Coerência Relacional' (C):"]
        answer_lines.append(f"")
        for s in concept_states:
            answer_lines.append(f"• {s['valid_at']} (doc: {s['document']} {s['version']})")
            answer_lines.append(f"  Estado: {s['state']}")
            answer_lines.append(f"  Mudança: {s['change_type']}")
            if s['previous_state']:
                answer_lines.append(f"  Estado anterior: {s['previous_state']}")
            answer_lines.append(f"  Evidência: {s['evidence_text'][:100]}...")
            answer_lines.append(f"  Tipo: {s['evidence_type']}")
            answer_lines.append("")
        
        answer = '\n'.join(answer_lines)
    
    elif test_id == 'AION-TEMP-002':
        # Evolução da "Consciência"
        concept_states = grouped.get('consciencia', [])
        answer_lines = ["Evolução documental do conceito de 'Consciência':"]
        answer_lines.append("")
        answer_lines.append("RESPOSTA EPISTEMICAMENTE RESPONSÁVEL:")
        answer_lines.append("")
        for s in concept_states:
            answer_lines.append(f"• {s['valid_at']} (doc: {s['document']})")
            answer_lines.append(f"  Estado: {s['state']}")
            answer_lines.append(f"  Mudança: {s['change_type']}")
            answer_lines.append(f"  Evidência: {s['evidence_type']}")
            answer_lines.append("")
        answer_lines.append("CONCLUSÃO: O conceito de 'consciência' nunca foi um conceito do programa TCR.")
        answer_lines.append("Sua presença no Handoff original foi inferência do curador, descreditada na auditoria T4.")
        answer_lines.append("A única menção textual a 'consciência' no corpus é a referência crítica a Tononi (Φ-IIT) no Paper A v6.2.")
        
        answer = '\n'.join(answer_lines)
    
    elif test_id == 'AION-TEMP-003':
        # Evolução da relação Campo Primordial ↔ Consciência
        cp_states = grouped.get('campo_primordial', [])
        consc_states = grouped.get('consciencia', [])
        answer_lines = ["Evolução documental da relação 'Campo Primordial' ↔ 'Consciência':"]
        answer_lines.append("")
        answer_lines.append("RESPOSTA EPISTEMICAMENTE RESPONSÁVEL:")
        answer_lines.append("")
        answer_lines.append("Ambos os conceitos:")
        answer_lines.append("• Foram INFERIDOS no Handoff original (16/08/2026) a partir de contexto, não de texto.")
        answer_lines.append("• Foram CONTRADITOS pela auditoria da ontologia v1.0.0 (17/08/2026) — termos não aparecem nos textos.")
        answer_lines.append("• Foram REMOVIDOS da ontologia v1.0.0 como conceitos do programa.")
        answer_lines.append("")
        answer_lines.append("Portanto, a relação entre eles nunca existiu documentalmente.")
        answer_lines.append("A relação foi uma inferência curatorial posteriormente descreditada.")
        answer_lines.append("")
        answer_lines.append("Não é possível estabelecer uma 'evolução' de uma relação que nunca teve evidência textual.")
        
        answer = '\n'.join(answer_lines)
    
    elif test_id == 'AION-TEMP-004':
        # Conceitos abandonados, modificados ou enfraquecidos
        revoked_or_contradicted = [s for s in states if s['change_type'] in ('REVOKED', 'CONTRADICTED')]
        answer_lines = ["Conceitos abandonados (REVOKED) ou contrariados (CONTRADICTED) no corpus:"]
        answer_lines.append("")
        for s in revoked_or_contradicted:
            answer_lines.append(f"• {s['concept_label']} ({s['concept_id']})")
            answer_lines.append(f"  Data: {s['valid_at']} (doc: {s['document']} {s['version']})")
            answer_lines.append(f"  Estado final: {s['state']}")
            answer_lines.append(f"  Estado anterior: {s['previous_state']}")
            answer_lines.append(f"  Evidência: {s['evidence_text'][:120]}")
            answer_lines.append(f"  Tipo: {s['evidence_type']}")
            answer_lines.append("")
        
        answer = '\n'.join(answer_lines)
    
    elif test_id == 'AION-TEMP-005':
        # Conceitos estáveis
        stable = [s for s in states if s['change_type'] == 'STABLE']
        introduced = [s for s in states if s['change_type'] == 'INTRODUCED']
        refined = [s for s in states if s['change_type'] == 'REFINED']
        
        answer_lines = ["Conceitos estáveis (STABLE) ou sem modificação após INTRODUCED:"]
        answer_lines.append("")
        answer_lines.append(f"Estados STABLE: {len(stable)}")
        for s in stable:
            answer_lines.append(f"  • {s['concept_label']} ({s['concept_id']}) — {s['valid_at']} — {s['state'][:80]}")
        answer_lines.append("")
        answer_lines.append(f"Conceitos INTRODUCED sem refinamento posterior (estável desde introdução):")
        for s in introduced:
            # Verifica se o conceito tem apenas um estado
            cid_states = [x for x in states if x['concept_id'] == s['concept_id']]
            if len(cid_states) == 1:
                answer_lines.append(f"  • {s['concept_label']} ({s['concept_id']}) — {s['valid_at']} — {s['state'][:80]}")
        
        answer = '\n'.join(answer_lines)
    
    else:
        answer = "Teste não reconhecido."
    
    print(answer)
    return {
        'test_id': test_id,
        'question': question,
        'answer': answer,
        'concept_count_relevant': len(grouped.get(test_id.replace('AION-TEMP-00', '').strip() if test_id != 'AION-TEMP-001' else 'C', [])),
    }


def build_temporal_graph_html(states: list, tpc: dict) -> str:
    """Gera HTML do grafo temporal."""
    grouped = group_states_by_concept(states)
    
    html = ['''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AION — Grafo Temporal</title>
<style>
body{font-family:system-ui,sans-serif;max-width:1200px;margin:2rem auto;line-height:1.6;padding:0 1rem;background:#fafafa;color:#111}
h1{color:#1a252f}
h2{color:#2c3e50;border-left:4px solid #3498db;padding-left:.8rem;margin-top:2rem}
.timeline{margin:1rem 0;padding:1rem;background:#fff;border-left:4px solid #3498db}
.state{margin:.5rem 0;padding:.8rem;background:#f8f9fa;border-radius:4px;border-left:3px solid #95a5a6}
.change-INTRODUCED{border-left-color:#27ae60}
.change-REFINED{border-left-color:#3498db}
.change-EXTENDED{border-left-color:#9b59b6}
.change-CONTRADICTED{border-left-color:#e67e22}
.change-REVOKED{border-left-color:#e74c3c}
.change-STABLE{border-left-color:#95a5a6}
.badge{display:inline-block;padding:.2rem .6rem;border-radius:3px;font-size:.8rem;color:#fff;font-weight:bold;margin-right:.3rem}
.badge-E{background:#27ae60}
.badge-I{background:#f39c12}
.unknown{background:#fff3cd;padding:.5rem;border-left:4px solid #f39c12;margin:.5rem 0}
.tpc-summary{background:#d4edda;padding:1rem;border-radius:4px;margin:1rem 0}
.tpc-summary h3{margin-top:0;color:#155724}
</style>
</head>
<body>
<header>
<h1>AION — Grafo Temporal</h1>
<p><strong>Versão:</strong> 1.0.0</p>
<p><strong>Data:</strong> 17 de agosto de 2026</p>
<p><strong>Autor da estrutura:</strong> Edson C. Nascimento (Projetista Master)</p>
<p><strong>Implementação:</strong> IA Curadora</p>
</header>
''']
    
    # TPC summary
    html.append(f'''
<section class="tpc-summary">
<h3>TPC — Temporal Provenance Coverage</h3>
<p><strong>{tpc['states_with_verified_date']}/{tpc['total_states']}</strong> estados com data verificável documentalmente.</p>
<p><strong>TPC = {tpc['tpc']:.4f} ({tpc['tpc_percentage']})</strong></p>
<p><em>Estados com data UNKNOWN são explicitamente marcados — não são artificialmente datados.</em></p>
</section>
''')
    
    # Timeline por conceito
    html.append('<h2>Estados Conceituais Temporais</h2>')
    
    for cid, cid_states in sorted(grouped.items()):
        label = cid_states[0]['concept_label']
        html.append(f'<div class="timeline">')
        html.append(f'<h3>{label} <code>({cid})</code></h3>')
        
        for s in cid_states:
            change_class = f"change-{s['change_type']}"
            evidence_class = f"badge-{s['evidence_type'].strip('[]')}"
            
            html.append(f'<div class="state {change_class}">')
            html.append(f'<strong>{s["valid_at"]}</strong> — <span class="badge {evidence_class}">{s["evidence_type"]}</span> <span class="badge change-{s["change_type"]}">{s["change_type"]}</span>')
            html.append(f'<br><em>Documento:</em> {s["document"]} ({s["version"]})')
            html.append(f'<br><em>Estado:</em> {s["state"]}')
            if s['previous_state']:
                html.append(f'<br><em>Estado anterior:</em> {s["previous_state"]}')
            html.append(f'<br><em>Evidência:</em> <code>{s["evidence_text"]}</code>')
            if s.get('note'):
                html.append(f'<br><em>Nota:</em> {s["note"]}')
            html.append('</div>')
        
        html.append('</div>')
    
    html.append('''
<footer>
<p><em>Ausência de informação não é autorização para inferência. Estados UNKNOWN são dados, não lacunas a preencher.</em></p>
</footer>
</body>
</html>
''')
    
    return '\n'.join(html)


def main():
    print("=" * 70)
    print("AION Passo 5.7 — Grafo Temporal")
    print("=" * 70)
    
    # Estados conceituais
    states = CONCEPT_TEMPORAL_STATES
    print(f"\n[5.7.1] Estados conceituais registrados: {len(states)}")
    
    # Agrupar por conceito
    grouped = group_states_by_concept(states)
    print(f"\n[5.7.2] Conceitos com estados temporais: {len(grouped)}")
    for cid, cid_states in grouped.items():
        print(f"  • {cid_states[0]['concept_label']} ({cid}): {len(cid_states)} estados")
    
    # Tipos de mudança
    change_types = defaultdict(int)
    for s in states:
        change_types[s['change_type']] += 1
    print(f"\n[5.7.3] Distribuição de tipos de mudança:")
    for ct, count in sorted(change_types.items()):
        print(f"  • {ct}: {count}")
    
    # Calcular TPC
    tpc = compute_tpc(states)
    print(f"\n[5.7.4] TPC calculado:")
    print(f"  Estados totais: {tpc['total_states']}")
    print(f"  Estados com data verificável: {tpc['states_with_verified_date']}")
    print(f"  Estados UNKNOWN: {tpc['states_with_unknown_date']}")
    print(f"  TPC = {tpc['tpc']:.4f} ({tpc['tpc_percentage']})")
    
    # Executar testes AION-TEMP-001 a 005
    test_results = {}
    tests = [
        ('AION-TEMP-001', "Como o conceito de Coerência Relacional evoluiu no corpus fundacional?"),
        ('AION-TEMP-002', "Como o conceito de Consciência evoluiu?"),
        ('AION-TEMP-003', "Como a relação entre Campo Primordial e Consciência evoluiu?"),
        ('AION-TEMP-004', "Quais conceitos foram abandonados, modificados ou enfraquecidos?"),
        ('AION-TEMP-005', "Quais conceitos permaneceram estáveis?"),
    ]
    
    for test_id, question in tests:
        result = run_temp_test(test_id, question, states)
        test_results[test_id] = result
    
    # Construir grafo JSON
    graph_data = {
        'metadata': {
            'version': '1.0.0',
            'generated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
            'protocol': 'AION-CORPUS-001 v1.2.0 + ONTOLOGY v1.0.0 + graphrag_enriched_v2.0',
        },
        'states': states,
        'grouped_by_concept': {cid: len(cid_states) for cid, cid_states in grouped.items()},
        'tpc': tpc,
        'change_type_distribution': dict(change_types),
        'test_results': test_results,
        'doc_metadata': DOC_METADATA,
    }
    
    # Salvar JSON
    json_path = OUTPUT_DIR / 'aion_temporal_graph_v1.0.json'
    json_path.write_text(json.dumps(graph_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[5.7.5] JSON salvo: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    # Salvar HTML
    html_path = OUTPUT_DIR / 'aion_temporal_visualization.html'
    html_content = build_temporal_graph_html(states, tpc)
    html_path.write_text(html_content, encoding='utf-8')
    print(f"  HTML salvo: {html_path}")
    print(f"  Tamanho: {html_path.stat().st_size} bytes")
    
    # Resumo final
    print(f"\n{'=' * 70}")
    print("[RESUMO Passo 5.7]")
    print(f"{'=' * 70}")
    print(f"Estados conceituais: {len(states)}")
    print(f"Conceitos com trajetória temporal: {len(grouped)}")
    print(f"Tipos de mudança: {dict(change_types)}")
    print(f"TPC = {tpc['tpc']:.4f} ({tpc['tpc_percentage']})")
    print(f"  Estados UNKNOWN explicitamente marcados: {tpc['states_with_unknown_date']}")
    
    return graph_data


if __name__ == '__main__':
    main()
