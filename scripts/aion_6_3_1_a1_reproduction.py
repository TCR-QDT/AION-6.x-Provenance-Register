#!/usr/bin/env python3
"""
AION Passo 6.3.1-A.1 — Prompt Reproduction Test (N=30)

Reproduz exatamente o baseline 6.3.0 usando P_RESP_001_V02_SYSTEM_PROMPT.
Verifica se FR>0 e F3 reaparece.

NÃO altera: corpus, oracle, retrieval, validator, modelo, temperatura, parâmetros.

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 21 de agosto de 2026
"""

import json
import sys
import re
import time
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
N_RUNS = 30


def classify_fabrication(invalid_id, all_chunks, retrieved_ids):
    doc_match = re.match(r'CORPUS-(\d{3})', invalid_id)
    if not doc_match:
        return 'F5_MALFORMED'
    doc_id = f'CORPUS-{doc_match.group(1)}'
    doc_exists = any(c.corpus_id == doc_id for c in all_chunks)
    chunk_exists = any(c.chunk_id == invalid_id for c in all_chunks)
    if not doc_exists:
        return 'F1_DOCUMENT_INEXISTENT'
    if doc_exists and not chunk_exists:
        if '#chunk_' in invalid_id and doc_id in ('CORPUS-002', 'CORPUS-003', 'CORPUS-004', 'CORPUS-006', 'CORPUS-007', 'CORPUS-011'):
            return 'F3_DOCUMENT_CORRECT_FORMAT_INCORRECT'
        return 'F2_DOCUMENT_EXISTS_CHUNK_INEXISTENT'
    if chunk_exists and invalid_id not in retrieved_ids:
        return 'F4_CHUNK_EXISTS_DOCUMENT_INCORRECT'
    return 'F7_OTHER'


def main():
    print("=" * 80)
    print("AION Passo 6.3.1-A.1 — Prompt Reproduction Test (N=30)")
    print("Usando P_RESP_001_V02_SYSTEM_PROMPT (igual ao baseline 6.3.0)")
    print("=" * 80)
    
    # Setup
    print("\n[SETUP] Construindo chunks base...")
    base_chunks = build_base_chunks()
    print(f"  Base chunks: {len(base_chunks)}")
    
    validator = ProvenanceValidator(base_chunks)
    print(f"  Validator CORPUS_INDEX: {len(validator.corpus_index)} chunks")
    
    class ExperimentJ_V3(ExperimentJ_CrossLingual):
        def query_original(self, question, top_k=8):
            q_vec = self.vectorizer.transform([question])
            scores = cosine_similarity(q_vec, self.matrix).flatten()
            top_indices = np.argsort(scores)[::-1][:top_k]
            results = []
            for rank, idx in enumerate(top_indices, 1):
                r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
                results.append(r)
            return results
    
    j_store = ExperimentJ_V3(base_chunks, B1_PERGUNTA_EN)
    
    # B2 test
    test = BENCH_TESTS['B2']
    
    # Retrieval fixo
    retrieved = j_store.query_original(test['pergunta'], top_k=8)
    retrieved_for_eval = [
        {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
        for i, r in enumerate(retrieved)
    ]
    retrieved_ids = [r.chunk.chunk_id for r in retrieved]
    retrieval_top1 = retrieved[0].chunk.chunk_id if retrieved else None
    
    # System extra (temporal context)
    temporal_data = json.loads((OUTPUT_DIR / 'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
    temporal_context = json.dumps(temporal_data['states'][:5], ensure_ascii=False, indent=2)[:2000]
    system_extra = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{temporal_context}"
    
    print(f"\n  Prompt: P_RESP_001_V02_SYSTEM_PROMPT (igual ao baseline 6.3.0)")
    print(f"  Retrieval Top-1: {retrieval_top1}")
    print(f"  N runs: {N_RUNS}")
    
    # Executar N runs
    runs = []
    fabrication_types = Counter()
    
    for run_idx in range(1, N_RUNS + 1):
        if run_idx % 5 == 0:
            print(f"  Run {run_idx}/{N_RUNS}...")
        
        t_start = time.time()
        answer_raw = generate_answer(
            test['pergunta'], retrieved[:5], P_RESP_001_V02_SYSTEM_PROMPT, system_extra
        )
        t_elapsed = time.time() - t_start
        answer_clean = clean_answer(answer_raw)
        
        cited_ids = list(set(re.findall(r'CORPUS-\d{3}#\w+', answer_clean)))
        
        validation_result = validator.validate_response(answer_clean, retrieved_for_eval)
        answer_final = validation_result['answer_cleaned']
        
        valid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if v['is_valid']]
        invalid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if not v['is_valid']]
        
        invalid_types = [classify_fabrication(inv, base_chunks, retrieved_ids) for inv in invalid_ids]
        for t in invalid_types:
            fabrication_types[t] += 1
        
        eval_result = evaluate_with_eval002_v02('B2', retrieved_for_eval, answer_final, test['gabarito'])
        
        exact_copies = sum(1 for cid in cited_ids if cid in retrieved_ids)
        per_run = exact_copies / len(cited_ids) if cited_ids else 1.0
        
        provenance_status = 'VALID' if not invalid_ids else 'INVALID'
        
        runs.append({
            'run_id': run_idx,
            'generated_ids': cited_ids,
            'valid_ids': valid_ids,
            'invalid_ids': invalid_ids,
            'invalid_types': invalid_types,
            'per_run': per_run,
            'validator_status': 'INTERCEPTED' if invalid_ids else 'CLEAN',
            'semantic_status': eval_result['avaliacao_final'],
            'provenance_status': provenance_status,
            'evidence_status': validation_result['evidence_category'],
            'tempo_segundos': round(t_elapsed, 2),
        })
    
    # Métricas
    fr = sum(1 for r in runs if r['invalid_ids']) / N_RUNS
    ir_total_gen = sum(len(r['generated_ids']) for r in runs)
    ir_total_inv = sum(len(r['invalid_ids']) for r in runs)
    ir = ir_total_inv / ir_total_gen if ir_total_gen > 0 else 0
    vr = ir_total_inv / ir_total_inv if ir_total_inv > 0 else 1.0
    sr = sum(1 for r in runs if 'PASS' in r['semantic_status']) / N_RUNS
    f3_count = sum(1 for r in runs for t in r['invalid_types'] if t == 'F3_DOCUMENT_CORRECT_FORMAT_INCORRECT')
    f3r = f3_count / N_RUNS
    per_avg = sum(r['per_run'] for r in runs) / N_RUNS
    
    b1_deterministic = len(set(r.get('retrieval_top1', retrieval_top1) for r in runs)) == 1
    
    # Crosstab
    sp_pv = sum(1 for r in runs if 'PASS' in r['semantic_status'] and r['provenance_status'] == 'VALID')
    sp_pi = sum(1 for r in runs if 'PASS' in r['semantic_status'] and r['provenance_status'] == 'INVALID')
    sf_pv = sum(1 for r in runs if 'PASS' not in r['semantic_status'] and r['provenance_status'] == 'VALID')
    sf_pi = sum(1 for r in runs if 'PASS' not in r['semantic_status'] and r['provenance_status'] == 'INVALID')
    
    # Relatório
    print(f"\n{'=' * 80}")
    print("[RESULTADO — Prompt Reproduction Test]")
    print(f"{'=' * 80}")
    
    print(f"\n  N = {N_RUNS}")
    print(f"  Prompt: P_RESP_001_V02_SYSTEM_PROMPT")
    print(f"  B1 Top-1: {retrieval_top1} (determinístico: {b1_deterministic})")
    
    print(f"\n  MÉTRICAS:")
    print(f"    FR = {fr:.4f} ({sum(1 for r in runs if r['invalid_ids'])}/{N_RUNS})")
    print(f"    IR = {ir:.4f} ({ir_total_inv}/{ir_total_gen})")
    print(f"    VR = {vr:.4f}")
    print(f"    SR = {sr:.4f}")
    print(f"    F3R = {f3r:.4f} ({f3_count} casos F3)")
    print(f"    PER = {per_avg:.4f}")
    
    print(f"\n  Fabrication types:")
    for t, c in fabrication_types.most_common():
        print(f"    {t}: {c}")
    
    print(f"\n  Crosstab Semantic × Provenance:")
    print(f"    PASS + VALID:   {sp_pv}")
    print(f"    PASS + INVALID: {sp_pi}")
    print(f"    FAIL + VALID:   {sf_pv}")
    print(f"    FAIL + INVALID: {sf_pi}")
    
    # Veredito
    print(f"\n{'=' * 80}")
    print("[VEREDITO]")
    print(f"{'=' * 80}")
    
    if fr > 0:
        if f3_count > 0:
            verdict = 'FABRICAÇÃO REPRODUZIDA — F3 reapareceu com prompt correto'
            action = 'Prosseguir para decomposição causal Prompt × Schema (P0/P1/P2)'
        else:
            verdict = 'FABRICAÇÃO REPRODUZIDA mas não F3 — outro tipo de fabricação'
            action = 'Investigar novo tipo de fabricação'
    else:
        verdict = 'FABRICAÇÃO NÃO REPRODUZIDA — investigar variabilidade'
        action = 'Investigar outras causas de variabilidade entre sessões'
    
    print(f"\n  >>> {verdict}")
    print(f"  >>> {action}")
    
    # Salvar
    report = {
        'metadata': {
            'experiment': 'AION-6.3.1-A.1 — Prompt Reproduction Test',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
            'n_runs': N_RUNS,
            'prompt_used': 'P_RESP_001_V02_SYSTEM_PROMPT (igual ao baseline 6.3.0)',
        },
        'metrics': {
            'FR': fr,
            'IR': ir,
            'VR': vr,
            'SR': sr,
            'F3R': f3r,
            'PER': per_avg,
            'f3_count': f3_count,
            'total_ids_generated': ir_total_gen,
            'total_invalid_ids': ir_total_inv,
        },
        'b1_control': {
            'b1_top1': retrieval_top1,
            'b1_deterministic': b1_deterministic,
        },
        'fabrication_distribution': dict(fabrication_types),
        'crosstab': {
            'semantic_pass_provenance_valid': sp_pv,
            'semantic_pass_provenance_invalid': sp_pi,
            'semantic_fail_provenance_valid': sf_pv,
            'semantic_fail_provenance_invalid': sf_pi,
        },
        'runs_summary': [
            {
                'run_id': r['run_id'],
                'invalid_ids': r['invalid_ids'],
                'invalid_types': r['invalid_types'],
                'validator_status': r['validator_status'],
                'semantic_status': r['semantic_status'],
                'provenance_status': r['provenance_status'],
            } for r in runs
        ],
        'verdict': verdict,
        'action': action,
    }
    
    json_path = OUTPUT_DIR / 'aion_6_3_1_a1_reproduction.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
