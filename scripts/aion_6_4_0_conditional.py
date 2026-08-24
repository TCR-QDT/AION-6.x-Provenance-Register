#!/usr/bin/env python3
"""
AION Passo 6.4.0 — Provenance Conditional Reliability Baseline

Baseline observacional (sem intervenção).
Mede PER, CFR-ID, CFR-RUN, EBA, VR, F3R, SR separadamente.

NÃO altera: corpus, oracle, retrieval, validator, prompt, modelo.

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
N_RUNS = 100


def classify_fabrication(invalid_id, all_chunks, retrieved_ids):
    doc_match = re.match(r'CORPUS-(\d{3})', invalid_id)
    if not doc_match:
        return 'F5_MALFORMED'
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


def main():
    print("=" * 80)
    print("AION Passo 6.4.0 — Provenance Conditional Reliability Baseline")
    print(f"N = {N_RUNS} runs observacionais (sem intervenção)")
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
    retrieval_top1 = retrieved[0].chunk.chunk_id if retrieved else None
    
    temporal_data = json.loads((OUTPUT_DIR / 'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
    temporal_context = json.dumps(temporal_data['states'][:5], ensure_ascii=False, indent=2)[:2000]
    system_extra = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{temporal_context}"
    
    context_parts = [f"[{r.chunk.chunk_id}|score={r.score:.3f}]\n{r.chunk.text}" for r in retrieved[:5]]
    context_hash = hashlib.sha256("\n---\n".join(context_parts).encode()).hexdigest()
    
    print(f"\n  Retrieval Top-1: {retrieval_top1}")
    print(f"  Context hash: {context_hash[:16]}...")
    print(f"  Prompt: P_RESP_001_V02_SYSTEM_PROMPT (sem intervenção)")
    print(f"  N runs: {N_RUNS}")
    
    runs = []
    
    for run_idx in range(1, N_RUNS + 1):
        if run_idx % 10 == 0:
            print(f"  Run {run_idx}/{N_RUNS}...")
        
        t_start = time.time()
        answer_raw = generate_answer(test['pergunta'], retrieved[:5], P_RESP_001_V02_SYSTEM_PROMPT, system_extra)
        t_elapsed = time.time() - t_start
        answer_clean = clean_answer(answer_raw)
        
        # IDs citados
        cited_ids = list(set(re.findall(r'CORPUS-\d{3}#\w+', answer_clean)))
        
        # Claims com [E] ou [I]
        e_claims = len(re.findall(r'\[E\]', answer_clean))
        i_claims = len(re.findall(r'\[I\]', answer_clean))
        claim_count = e_claims + i_claims
        
        # Provenance emitida?
        provenance_emitted = len(cited_ids) > 0
        provenance_count = len(cited_ids)
        
        # Validator
        validation_result = validator.validate_response(answer_clean, retrieved_for_eval)
        answer_final = validation_result['answer_cleaned']
        
        valid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if v['is_valid']]
        invalid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if not v['is_valid']]
        
        # Classificar fabricações
        invalid_types = [classify_fabrication(inv, base_chunks, retrieved_ids) for inv in invalid_ids]
        f3_count = sum(1 for t in invalid_types if t == 'F3')
        f4_count = sum(1 for t in invalid_types if t == 'F4')
        other_fab = sum(1 for t in invalid_types if t not in ('F3', 'F4'))
        
        # EBA — Evidence-Bound Accuracy
        # ID válido E corresponde à evidência recuperada (está nos retrieved_ids top-5)
        eba_valid = sum(1 for vid in valid_ids if vid in retrieved_ids[:5])
        
        # Avaliação semântica
        eval_result = evaluate_with_eval002_v02('B2', retrieved_for_eval, answer_final, test['gabarito'])
        semantic_pass = 'PASS' in eval_result['avaliacao_final']
        
        # Validator interceptou?
        validator_intercepted = len(invalid_ids) > 0
        
        runs.append({
            'run_id': run_idx,
            'context_hash': context_hash[:16],
            'retrieval_top1': retrieval_top1,
            'retrieval_top5': retrieved_ids[:5],
            'semantic_pass': semantic_pass,
            'semantic_status': eval_result['avaliacao_final'],
            'provenance_emitted': provenance_emitted,
            'claim_count': claim_count,
            'e_claims': e_claims,
            'i_claims': i_claims,
            'provenance_count': provenance_count,
            'generated_ids': cited_ids,
            'valid_id_count': len(valid_ids),
            'invalid_id_count': len(invalid_ids),
            'valid_ids': valid_ids,
            'invalid_ids': invalid_ids,
            'f3_count': f3_count,
            'f4_count': f4_count,
            'other_fabrication_count': other_fab,
            'invalid_types': invalid_types,
            'validator_intercepted': validator_intercepted,
            'eba_valid': eba_valid,
            'eba_total_valid': len(valid_ids),
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'tempo_segundos': round(t_elapsed, 2),
        })
    
    # === MÉTRICAS ===
    
    n = len(runs)
    
    # PER — Provenance Emission Rate
    runs_with_provenance = sum(1 for r in runs if r['provenance_emitted'])
    per = runs_with_provenance / n
    
    # CFR-ID — Conditional Fabrication Rate (por referência)
    total_ids_produced = sum(r['provenance_count'] for r in runs)
    total_invalid_ids = sum(r['invalid_id_count'] for r in runs)
    cfr_id = total_invalid_ids / total_ids_produced if total_ids_produced > 0 else 0
    
    # CFR-RUN — Conditional Fabrication Rate (por run)
    runs_with_provenance_and_invalid = sum(1 for r in runs if r['provenance_emitted'] and r['invalid_id_count'] > 0)
    cfr_run = runs_with_provenance_and_invalid / runs_with_provenance if runs_with_provenance > 0 else 0
    
    # VR — Validation Rate
    total_invalid = sum(r['invalid_id_count'] for r in runs)
    total_intercepted = sum(1 for r in runs if r['validator_intercepted'])  # validator intercepta todos
    vr = total_intercepted / runs_with_provenance_and_invalid if runs_with_provenance_and_invalid > 0 else 1.0
    
    # F3R — F3 Rate (por run)
    f3_runs = sum(1 for r in runs if r['f3_count'] > 0)
    f3r = f3_runs / n
    
    # F3-ID — F3 como proporção de inválidos
    f3_total = sum(r['f3_count'] for r in runs)
    f3_id_ratio = f3_total / total_invalid if total_invalid > 0 else 0
    
    # SR — Semantic Rate
    sr = sum(1 for r in runs if r['semantic_pass']) / n
    
    # FR — Fabrication Rate (clássico)
    fr = runs_with_provenance_and_invalid / n
    
    # EBA — Evidence-Bound Accuracy
    total_eba_valid = sum(r['eba_valid'] for r in runs)
    eba = total_eba_valid / total_ids_produced if total_ids_produced > 0 else 0
    
    # Empty provenance
    empty_provenance = sum(1 for r in runs if not r['provenance_emitted'])
    
    # Relação PER × SR
    sp_with_prov = sum(1 for r in runs if r['semantic_pass'] and r['provenance_emitted'])
    sp_without_prov = sum(1 for r in runs if r['semantic_pass'] and not r['provenance_emitted'])
    
    # Relação PER × CFR
    # (já calculado acima)
    
    # === RELATÓRIO ===
    print(f"\n{'=' * 80}")
    print("[RELATÓRIO — AION-6.4.0 Provenance Conditional Reliability]")
    print(f"{'=' * 80}")
    
    print(f"\n  N = {n}")
    print(f"  Runs com provenance emitida: {runs_with_provenance} ({per*100:.1f}%)")
    print(f"  Runs sem provenance (empty): {empty_provenance} ({(1-per)*100:.1f}%)")
    
    print(f"\n  === MÉTRICAS PRIMÁRIAS ===")
    print(f"  PER  (Provenance Emission Rate):     {per:.4f} ({runs_with_provenance}/{n})")
    print(f"  CFR-ID (Cond. Fab. Rate por ID):     {cfr_id:.4f} ({total_invalid_ids}/{total_ids_produced})")
    print(f"  CFR-RUN (Cond. Fab. Rate por run):   {cfr_run:.4f} ({runs_with_provenance_and_invalid}/{runs_with_provenance})")
    print(f"  EBA  (Evidence-Bound Accuracy):      {eba:.4f} ({total_eba_valid}/{total_ids_produced})")
    print(f"  VR   (Validation Rate):              {vr:.4f}")
    print(f"  F3R  (F3 Rate por run):              {f3r:.4f} ({f3_runs}/{n})")
    print(f"  F3-ID (F3 / inválidos):              {f3_id_ratio:.4f} ({f3_total}/{total_invalid})")
    print(f"  SR   (Semantic Rate):                {sr:.4f}")
    print(f"  FR   (Fabrication Rate clássico):     {fr:.4f}")
    
    print(f"\n  === RELAÇÕES ===")
    print(f"  PER × SR:")
    print(f"    Semantic PASS com provenance:     {sp_with_prov}")
    print(f"    Semantic PASS sem provenance:    {sp_without_prov}")
    print(f"    Semantic FAIL com provenance:    {runs_with_provenance - sp_with_prov}")
    print(f"    Semantic FAIL sem provenance:    {empty_provenance - sp_without_prov}")
    
    print(f"\n  PER × CFR:")
    print(f"    FR = PER × CFR_RUN = {per:.4f} × {cfr_run:.4f} = {per * cfr_run:.4f}")
    print(f"    FR observado = {fr:.4f}")
    print(f"    (devem ser approximately iguais)")
    
    print(f"\n  === DISTRIBUIÇÃO DE FABRICAÇÃO ===")
    fab_dist = Counter()
    for r in runs:
        for t in r['invalid_types']:
            fab_dist[t] += 1
    for t, c in fab_dist.most_common():
        print(f"    {t}: {c}")
    
    # Resposta às 9 perguntas
    print(f"\n{'=' * 80}")
    print("[RESPOSTAS ÀS 9 PERGUNTAS]")
    print(f"{'=' * 80}")
    
    answers = {
        '1_PER': f'{per:.4f} ({per*100:.1f}%)',
        '2_CFR_ID': f'{cfr_id:.4f} ({total_invalid_ids}/{total_ids_produced})',
        '3_CFR_RUN': f'{cfr_run:.4f} ({runs_with_provenance_and_invalid}/{runs_with_provenance})',
        '4_EBA': f'{eba:.4f} ({total_eba_valid}/{total_ids_produced})',
        '5_VR': f'{vr:.4f}',
        '6_F3_F4_ratio': f'F3={f3_total}, F4={sum(r["f4_count"] for r in runs)}, other={sum(r["other_fabrication_count"] for r in runs)}',
        '7_PER_vs_SR': f'PASS com prov={sp_with_prov}, PASS sem prov={sp_without_prov}',
        '8_PER_vs_CFR': f'PER={per:.4f}, CFR_RUN={cfr_run:.4f}, FR={per*cfr_run:.4f} (observado={fr:.4f})',
        '9_variabilidade': f'PER={"ALTA" if per < 0.3 or per > 0.7 else "MODERADA"}, CFR={"ALTA" if cfr_run > 0.3 else "BAIXA"} → variabilidade concentrada em {"PER" if abs(per - 0.5) > abs(cfr_run - 0.5) else "CFR"}',
    }
    
    for q, a in answers.items():
        print(f"  {q}: {a}")
    
    # Salvar
    report = {
        'metadata': {
            'experiment': 'AION-6.4.0 — Provenance Conditional Reliability Baseline',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'n_runs': n,
        },
        'metrics': {
            'PER': per,
            'CFR_ID': cfr_id,
            'CFR_RUN': cfr_run,
            'EBA': eba,
            'VR': vr,
            'F3R': f3r,
            'F3_ID': f3_id_ratio,
            'SR': sr,
            'FR': fr,
            'runs_with_provenance': runs_with_provenance,
            'empty_provenance': empty_provenance,
            'total_ids_produced': total_ids_produced,
            'total_invalid_ids': total_invalid_ids,
            'total_eba_valid': total_eba_valid,
        },
        'relations': {
            'semantic_pass_with_provenance': sp_with_prov,
            'semantic_pass_without_provenance': sp_without_prov,
            'per_x_cfr': per * cfr_run,
            'fr_observed': fr,
        },
        'fabrication_distribution': dict(fab_dist),
        'answers_to_9_questions': answers,
        'runs_summary': [
            {
                'run_id': r['run_id'],
                'provenance_emitted': r['provenance_emitted'],
                'provenance_count': r['provenance_count'],
                'valid_id_count': r['valid_id_count'],
                'invalid_id_count': r['invalid_id_count'],
                'f3_count': r['f3_count'],
                'f4_count': r['f4_count'],
                'semantic_pass': r['semantic_pass'],
                'eba_valid': r['eba_valid'],
            } for r in runs
        ],
    }
    
    json_path = OUTPUT_DIR / 'aion_6_4_0_conditional_reliability.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
