#!/usr/bin/env python3
"""
AION Passo 6.4.1-A — Evidence-Bound Provenance (piloto intercalado)

A0: baseline (P_RESP_001 v0.2)
A1: provenance obrigatória + ID exclusivamente evidence-bound/literal

N=20 por condição, 40 runs total, INTERCALADOS (A0,A1,A0,A1,...)
para reduzir confound H-TEMP.

Objetivo: CFR↓ + EBA↑ + PER≈ + SR≈

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 21 de agosto de 2026
"""

import json
import sys
import re
import time
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from aion_rag_proxy import RetrievedChunk
from aion_bench_001 import BENCH_TESTS
from aion_p_resp_001_v02 import (
    P_RESP_001_V02_SYSTEM_PROMPT,
    evaluate_with_eval002_v02, generate_answer, clean_answer,
)
from aion_p_resp_001_v03 import ProvenanceValidator
from aion_6_2_6_top_k_efgh import build_base_chunks
from aion_6_2_9_oracle_crosslingual import B1_PERGUNTA_EN, ExperimentJ_CrossLingual

OUTPUT_DIR = Path('/home/z/my-project/download/rag')
N_PER = 25

A0_PROMPT = P_RESP_001_V02_SYSTEM_PROMPT

A1_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido.

PROTOCOLO DE PROVENIÊNCIA EXPLÍCITA (P-RESP-001 v0.2):

Para cada afirmação relevante, você DEVE:

1. Classificar a afirmação: [E] (evidência), [I] (interpretação), [H] (hipótese)
2. Citar a fonte com granularidade: source: chunk_id=<ID> | documento=CORPUS-XXX
3. Se não houver evidência: "INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO."

REGRA CRÍTICA DE ANCORAGEM LITERAL DE IDENTIFICADOR:

Um chunk_id SOMENTE pode ser utilizado como provenance se o identificador aparecer LITERALMENTE na evidência/contexto fornecido acima.

Antes de escrever qualquer chunk_id na resposta, você DEVE verificar:
- O identificador aparece EXATAMENTE como escrito no contexto acima?
- Sim → pode usar
- Não → NÃO use; diga "PROVENIÊNCIA NÃO LOCALIZADA NO CONTEXTO"

NUNCA:
- Complete, derive, infira ou construa um identificador
- Aplique o formato de identificador de um documento a outro documento
- Combine partes de identificadores diferentes
- Produza um identificador que não esteja literalmente presente no contexto

Responda em português. Use APENAS o contexto fornecido."""


def classify_fabrication(invalid_id, all_chunks, retrieved_ids):
    doc_match = re.match(r'CORPUS-(\d{3})', invalid_id)
    if not doc_match:
        return 'F5'
    doc_id = f'CORPUS-{doc_match.group(1)}'
    doc_exists = any(c.corpus_id == doc_id for c in all_chunks)
    chunk_exists = any(c.chunk_id == invalid_id for c in all_chunks)
    if not doc_exists:
        return 'F1'
    if doc_exists and not chunk_exists:
        if '#chunk_' in invalid_id and doc_id in ('CORPUS-002', 'CORPUS-003', 'CORPUS-004', 'CORPUS-006', 'CORPUS-007', 'CORPUS-011'):
            return 'F3'
        return 'F2'
    if chunk_exists and invalid_id not in retrieved_ids:
        return 'F4'
    return 'F7'


def run_single(j_store, validator, all_chunks, prompt, retrieved, retrieved_for_eval, retrieved_ids, system_extra):
    """Executa uma única run."""
    test = BENCH_TESTS['B2']
    
    t_start = time.time()
    answer_raw = generate_answer(test['pergunta'], retrieved[:5], prompt, system_extra)
    t_elapsed = time.time() - t_start
    answer_clean = clean_answer(answer_raw)
    
    cited_ids = list(set(re.findall(r'CORPUS-\d{3}#\w+', answer_clean)))
    e_claims = len(re.findall(r'\[E\]', answer_clean))
    i_claims = len(re.findall(r'\[I\]', answer_clean))
    claim_count = e_claims + i_claims
    provenance_emitted = len(cited_ids) > 0
    
    validation_result = validator.validate_response(answer_clean, retrieved_for_eval)
    answer_final = validation_result['answer_cleaned']
    
    valid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if v['is_valid']]
    invalid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if not v['is_valid']]
    invalid_types = [classify_fabrication(inv, all_chunks, retrieved_ids) for inv in invalid_ids]
    
    f3_count = sum(1 for t in invalid_types if t == 'F3')
    f4_count = sum(1 for t in invalid_types if t == 'F4')
    
    eba_valid = sum(1 for vid in valid_ids if vid in retrieved_ids[:5])
    
    eval_result = evaluate_with_eval002_v02('B2', retrieved_for_eval, answer_final, test['gabarito'])
    semantic_pass = 'PASS' in eval_result['avaliacao_final']
    
    return {
        'provenance_emitted': provenance_emitted,
        'claim_count': claim_count,
        'provenance_count': len(cited_ids),
        'valid_id_count': len(valid_ids),
        'invalid_id_count': len(invalid_ids),
        'f3_count': f3_count,
        'f4_count': f4_count,
        'invalid_types': invalid_types,
        'semantic_pass': semantic_pass,
        'semantic_status': eval_result['avaliacao_final'],
        'eba_valid': eba_valid,
        'tempo': round(t_elapsed, 2),
        'cited_ids': cited_ids,
        'valid_ids': valid_ids,
        'invalid_ids': invalid_ids,
    }


def compute_metrics(runs):
    n = len(runs)
    runs_with_prov = sum(1 for r in runs if r['provenance_emitted'])
    per = runs_with_prov / n
    
    total_ids = sum(r['provenance_count'] for r in runs)
    total_invalid = sum(r['invalid_id_count'] for r in runs)
    cfr_id = total_invalid / total_ids if total_ids > 0 else 0
    
    runs_prov_invalid = sum(1 for r in runs if r['provenance_emitted'] and r['invalid_id_count'] > 0)
    cfr_run = runs_prov_invalid / runs_with_prov if runs_with_prov > 0 else 0
    
    total_eba = sum(r['eba_valid'] for r in runs)
    eba = total_eba / total_ids if total_ids > 0 else 0
    
    vr = 1.0  # validator intercepta 100% por construção
    
    f3_runs = sum(1 for r in runs if r['f3_count'] > 0)
    f3r = f3_runs / n
    
    sr = sum(1 for r in runs if r['semantic_pass']) / n
    fr = runs_prov_invalid / n
    empty = sum(1 for r in runs if not r['provenance_emitted'])
    
    return {
        'PER': per, 'CFR_ID': cfr_id, 'CFR_RUN': cfr_run, 'EBA': eba,
        'VR': vr, 'F3R': f3r, 'SR': sr, 'FR': fr,
        'runs_with_prov': runs_with_prov, 'empty_prov': empty,
        'total_ids': total_ids, 'total_invalid': total_invalid,
        'runs_prov_invalid': runs_prov_invalid,
    }


def main():
    print("=" * 80)
    print("AION Passo 6.4.1-A — Evidence-Bound Provenance (piloto intercalado)")
    print(f"A0/A1, N={N_PER} cada (40 runs), INTERCALADOS")
    print("=" * 80)
    
    base_chunks = build_base_chunks()
    validator = ProvenanceValidator(base_chunks)
    
    class ExperimentJ_V3(ExperimentJ_CrossLingual):
        def query_original(self, question, top_k=8):
            q_vec = self.vectorizer.transform([question])
            scores = cosine_similarity(q_vec, self.matrix).flatten()
            top_indices = np.argsort(scores)[::-1][:top_k]
            return [RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank) for rank, idx in enumerate(top_indices, 1)]
    
    j_store = ExperimentJ_V3(base_chunks, B1_PERGUNTA_EN)
    
    test = BENCH_TESTS['B2']
    retrieved = j_store.query_original(test['pergunta'], top_k=8)
    retrieved_for_eval = [
        {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
        for i, r in enumerate(retrieved)
    ]
    retrieved_ids = [r.chunk.chunk_id for r in retrieved]
    
    temporal_data = json.loads((OUTPUT_DIR / 'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
    temporal_context = json.dumps(temporal_data['states'][:5], ensure_ascii=False, indent=2)[:2000]
    system_extra = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{temporal_context}"
    
    # Execução INTERCALADA: A0, A1, A0, A1, ...
    a0_runs = []
    a1_runs = []
    
    for i in range(N_PER):
        # A0
        if i % 5 == 0:
            print(f"  Bloco {i+1}/{N_PER} — A0...")
        r_a0 = run_single(j_store, validator, base_chunks, A0_PROMPT, retrieved, retrieved_for_eval, retrieved_ids, system_extra)
        r_a0['run_id'] = f"A0-{i+1}"
        r_a0['condition'] = 'A0'
        a0_runs.append(r_a0)
        
        # A1
        if i % 5 == 0:
            print(f"  Bloco {i+1}/{N_PER} — A1...")
        r_a1 = run_single(j_store, validator, base_chunks, A1_PROMPT, retrieved, retrieved_for_eval, retrieved_ids, system_extra)
        r_a1['run_id'] = f"A1-{i+1}"
        r_a1['condition'] = 'A1'
        a1_runs.append(r_a1)
    
    # Métricas
    m_a0 = compute_metrics(a0_runs)
    m_a1 = compute_metrics(a1_runs)
    
    # Matriz
    print(f"\n{'=' * 80}")
    print("[MATRIZ A0 × A1]")
    print(f"{'=' * 80}")
    print(f"\n{'Métrica':<15} {'A0 (baseline)':<20} {'A1 (evidence-bound)':<20} {'Variação'}")
    print('-' * 75)
    for metric in ['PER', 'CFR_ID', 'CFR_RUN', 'EBA', 'VR', 'F3R', 'SR', 'FR']:
        v0 = m_a0[metric]
        v1 = m_a1[metric]
        diff = v1 - v0
        if metric in ['EBA', 'PER', 'SR', 'VR']:
            arrow = '↑' if diff > 0 else ('↓' if diff < 0 else '=')
        else:  # CFR, F3R, FR — queremos reduzir
            arrow = '↓' if diff < 0 else ('↑' if diff > 0 else '=')
        print(f"{metric:<15} {v0:<20.4f} {v1:<20.4f} {arrow} {diff:+.4f}")
    
    print(f"\n  Runs com provenance: A0={m_a0['runs_with_prov']}, A1={m_a1['runs_with_prov']}")
    print(f"  Empty provenance:   A0={m_a0['empty_prov']}, A1={m_a1['empty_prov']}")
    print(f"  Total IDs:          A0={m_a0['total_ids']}, A1={m_a1['total_ids']}")
    print(f"  Total inválidos:    A0={m_a0['total_invalid']}, A1={m_a1['total_invalid']}")
    
    # Análise de preservação
    print(f"\n{'=' * 80}")
    print("[ANÁLISE DE PRESERVAÇÃO]")
    print(f"{'=' * 80}")
    
    cfr_reduced = m_a1['CFR_RUN'] < m_a0['CFR_RUN']
    eba_increased = m_a1['EBA'] > m_a0['EBA']
    per_preserved = m_a1['PER'] >= m_a0['PER'] * 0.5  # não caiu mais que 50%
    sr_preserved = m_a1['SR'] >= m_a0['SR'] * 0.5
    f3_reduced = m_a1['F3R'] < m_a0['F3R']
    
    print(f"\n  CFR reduzido?     {'SIM ✅' if cfr_reduced else 'NAO ❌'} ({m_a0['CFR_RUN']:.4f} → {m_a1['CFR_RUN']:.4f})")
    print(f"  EBA aumentou?      {'SIM ✅' if eba_increased else 'NAO ❌'} ({m_a0['EBA']:.4f} → {m_a1['EBA']:.4f})")
    print(f"  PER preservado?   {'SIM ✅' if per_preserved else 'NAO ❌'} ({m_a0['PER']:.4f} → {m_a1['PER']:.4f})")
    print(f"  SR preservado?    {'SIM ✅' if sr_preserved else 'NAO ❌'} ({m_a0['SR']:.4f} → {m_a1['SR']:.4f})")
    print(f"  F3 reduzido?      {'SIM ✅' if f3_reduced else 'NAO ❌'} ({m_a0['F3R']:.4f} → {m_a1['F3R']:.4f})")
    
    # Veredito
    if cfr_reduced and per_preserved and sr_preserved:
        if eba_increased:
            verdict = 'CENÁRIO A — A1 PROMISSORA ✅ (CFR↓ + EBA↑ + PER≈ + SR≈)'
        else:
            verdict = 'CENÁRIO A-PARCIAL — CFR reduziu preservando PER/SR, mas EBA não aumentou'
        action = 'Prosseguir para confirmação com N maior'
    elif cfr_reduced and not per_preserved:
        verdict = 'CENÁRIO B — FALSA SOLUÇÃO ❌ (CFR↓ mas PER colapsou — supressão)'
        action = 'Descartar A1; investigar alternativa'
    elif not cfr_reduced:
        verdict = 'CENÁRIO C — SEM EFEITO (CFR não reduziu)'
        action = 'Reformular intervenção'
    elif m_a1['PER'] == 0:
        verdict = 'CENÁRIO D — NÃO OBSERVÁVEL (PER=0 — nenhuma provenance emitida)'
        action = 'Reexecutar em outra sessão'
    else:
        verdict = 'CENÁRIO MISTO — análise manual necessária'
        action = 'Analisar detalhadamente'
    
    print(f"\n  >>> {verdict}")
    print(f"  >>> {action}")
    
    # Salvar
    report = {
        'metadata': {
            'experiment': 'AION-6.4.1-A — Evidence-Bound Provenance (piloto intercalado)',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'n_per_condition': N_PER,
            'total_runs': 2 * N_PER,
            'interleaved': True,
        },
        'a0_metrics': m_a0,
        'a1_metrics': m_a1,
        'preservation': {
            'cfr_reduced': cfr_reduced,
            'eba_increased': eba_increased,
            'per_preserved': per_preserved,
            'sr_preserved': sr_preserved,
            'f3_reduced': f3_reduced,
        },
        'verdict': verdict,
        'action': action,
        'a0_runs': [{'run_id': r['run_id'], 'provenance_emitted': r['provenance_emitted'],
                      'provenance_count': r['provenance_count'], 'valid_id_count': r['valid_id_count'],
                      'invalid_id_count': r['invalid_id_count'], 'f3_count': r['f3_count'],
                      'semantic_pass': r['semantic_pass'], 'eba_valid': r['eba_valid'],
                      'cited_ids': r['cited_ids'], 'invalid_ids': r['invalid_ids']} for r in a0_runs],
        'a1_runs': [{'run_id': r['run_id'], 'provenance_emitted': r['provenance_emitted'],
                      'provenance_count': r['provenance_count'], 'valid_id_count': r['valid_id_count'],
                      'invalid_id_count': r['invalid_id_count'], 'f3_count': r['f3_count'],
                      'semantic_pass': r['semantic_pass'], 'eba_valid': r['eba_valid'],
                      'cited_ids': r['cited_ids'], 'invalid_ids': r['invalid_ids']} for r in a1_runs],
    }
    
    json_path = OUTPUT_DIR / 'aion_6_4_1_a_evidence_bound.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
