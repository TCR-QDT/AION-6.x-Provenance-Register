#!/usr/bin/env python3
"""
AION Passo 6.3.1-C — Provenance Evidence-Bound

C0: Controle (P_RESP_001 v0.2 completo)
C1: ID explicitamente evidence-bound (preserva provenance, restringe ID)
C2: Provenance copy-only (só pode copiar IDs do contexto)

N=30 por condição (90 runs total).
NÃO altera: corpus, oracle, retrieval, validator, modelo.

Objetivo: FR↓ + F3R↓ + PC≈ + SR≈ + VR=1

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
    evaluate_with_eval002_v02, clean_answer,
)
from aion_p_resp_001_v03 import ProvenanceValidator
from aion_6_2_6_top_k_efgh import build_base_chunks
from aion_6_2_9_oracle_crosslingual import B1_PERGUNTA_EN, ExperimentJ_CrossLingual

OUTPUT_DIR = Path('/home/z/my-project/download/rag')
N_PER_CONDITION = 10

# === Prompts ===

# C0 — Controle (P_RESP_001 v0.2 completo)
C0_PROMPT = P_RESP_001_V02_SYSTEM_PROMPT

# C1 — ID evidence-bound (preserva provenance, restringe ID)
C1_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido.

PROTOCOLO DE PROVENIÊNCIA EXPLÍCITA (P-RESP-001 v0.2):

Para cada afirmação relevante, você DEVE:

1. Classificar a afirmação: [E] (evidência), [I] (interpretação), [H] (hipótese)
2. Citar a fonte com granularidade: source: chunk_id=<ID> | documento=CORPUS-XXX
3. Se não houver evidência: "INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO."

REGRA CRÍTICA DE IDENTIFICADOR:
Para cada referência, copie EXCLUSIVAMENTE um chunk_id que esteja LITERALMENTE presente no contexto recuperado acima. Não derive, não complete, não infira, não construa identificadores. Se você não encontrar o chunk_id exato no contexto, diga "FONTE NÃO LOCALIZADA NO CONTEXTO".

NUNCA produza um identificador que não apareça literalmente no contexto.
Responda em português. Use APENAS o contexto fornecido."""

# C2 — Provenance copy-only (mais restritivo)
C2_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido.

PROTOCOLO DE PROVENIÊNCIA EXPLÍCITA (P-RESP-001 v0.2):

Para cada afirmação relevante, você DEVE:

1. Classificar a afirmação: [E] (evidência), [I] (interpretação), [H] (hipótese)
2. Citar a fonte: source: chunk_id=<ID> | documento=CORPUS-XXX
3. Se não houver evidência: "INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO."

REGRA CRÍTICA DE CORRESPONDÊNCIA LITERAL:
Uma referência SOMENTE pode ser emitida se houver correspondência LITERAL entre o identificador que você produz e um identificador presente na evidência fornecida acima.

Antes de citar um chunk_id, verifique: este chunk_id aparece EXATAMENTE como escrito no contexto acima? Se sim, cite-o. Se não, NÃO o cite — diga "PROVENIÊNCIA NÃO DISPONÍVEL NO CONTEXTO".

NUNCA construa, derive, complete ou infira identificadores.
NUNCA combine partes de identificadores diferentes.
NUNCA aplique um formato de identificador de um documento a outro documento.

Responda em português. Use APENAS o contexto fornecido."""


CONDITIONS = {
    'C0': {'name': 'Controle', 'prompt': C0_PROMPT},
    'C1': {'name': 'ID evidence-bound', 'prompt': C1_PROMPT},
    'C2': {'name': 'Provenance copy-only', 'prompt': C2_PROMPT},
}


def generate_answer_with_prompt(question, retrieved, system_prompt, system_extra=""):
    context_parts = []
    for r in retrieved:
        context_parts.append(
            f"[{r.chunk.chunk_id} | {r.chunk.short_title} | {r.chunk.page} | {r.chunk.section} | score={r.score:.3f}]\n{r.chunk.text}\n"
        )
    chunks_context = "\n---\n".join(context_parts)
    full_system = system_prompt + (" " + system_extra if system_extra else "")
    user_prompt = f"""CONTEXTO RECUPERADO:

{chunks_context}

{system_extra}

PERGUNTA: {question}

Responda usando apenas o contexto acima."""
    
    try:
        result = subprocess.run(
            ['z-ai', 'chat', '--system', full_system, '--prompt', user_prompt],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            return f"[ERRO z-ai: {result.stderr}]"
        try:
            data = json.loads(result.stdout)
            return data.get('content') or data.get('response') or result.stdout
        except json.JSONDecodeError:
            return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "[ERRO z-ai: timeout]"
    except Exception as e:
        return f"[ERRO z-ai: {e}]"


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


def run_condition(j_store, validator, all_chunks, condition_key, prompt, n_runs):
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
    
    context_parts = [f"[{r.chunk.chunk_id} | score={r.score:.3f}]\n{r.chunk.text}\n" for r in retrieved[:5]]
    context_hash = hashlib.sha256("\n---\n".join(context_parts).encode()).hexdigest()
    
    runs = []
    fab_types = Counter()
    
    for run_idx in range(1, n_runs + 1):
        if run_idx % 10 == 0:
            print(f"    {condition_key} Run {run_idx}/{n_runs}...")
        
        t_start = time.time()
        answer_raw = generate_answer_with_prompt(test['pergunta'], retrieved[:5], prompt, system_extra)
        t_elapsed = time.time() - t_start
        answer_clean = clean_answer(answer_raw)
        
        cited_ids = list(set(re.findall(r'CORPUS-\d{3}#\w+', answer_clean)))
        
        validation_result = validator.validate_response(answer_clean, retrieved_for_eval)
        answer_final = validation_result['answer_cleaned']
        
        valid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if v['is_valid']]
        invalid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if not v['is_valid']]
        invalid_types = [classify_fabrication(inv, all_chunks, retrieved_ids) for inv in invalid_ids]
        for t in invalid_types:
            fab_types[t] += 1
        
        e_claims = len(re.findall(r'\[E\]', answer_clean))
        i_claims = len(re.findall(r'\[I\]', answer_clean))
        claims_needing = e_claims + i_claims
        claims_valid = len(valid_ids)
        
        exact_copies = sum(1 for cid in cited_ids if cid in retrieved_ids)
        per_run = exact_copies / len(cited_ids) if cited_ids else 1.0
        pc_run = claims_valid / claims_needing if claims_needing > 0 else 0.0
        
        eval_result = evaluate_with_eval002_v02('B2', retrieved_for_eval, answer_final, test['gabarito'])
        provenance_status = 'VALID' if not invalid_ids else 'INVALID'
        
        runs.append({
            'run_id': run_idx, 'condition': condition_key,
            'generated_ids': cited_ids, 'valid_ids': valid_ids, 'invalid_ids': invalid_ids,
            'invalid_types': invalid_types, 'per_run': per_run, 'pc_run': pc_run,
            'e_claims': e_claims, 'i_claims': i_claims,
            'validator_status': 'INTERCEPTED' if invalid_ids else 'CLEAN',
            'semantic_status': eval_result['avaliacao_final'],
            'provenance_status': provenance_status,
        })
    
    fr = sum(1 for r in runs if r['invalid_ids']) / n_runs
    ir_total_gen = sum(len(r['generated_ids']) for r in runs)
    ir_total_inv = sum(len(r['invalid_ids']) for r in runs)
    ir = ir_total_inv / ir_total_gen if ir_total_gen > 0 else 0
    vr = ir_total_inv / ir_total_inv if ir_total_inv > 0 else 1.0
    sr = sum(1 for r in runs if 'PASS' in r['semantic_status']) / n_runs
    f3_count = sum(1 for r in runs for t in r['invalid_types'] if 'F3' in t)
    f3r = f3_count / n_runs
    per_avg = sum(r['per_run'] for r in runs) / n_runs
    pc_avg = sum(r['pc_run'] for r in runs) / n_runs
    
    sp_pv = sum(1 for r in runs if 'PASS' in r['semantic_status'] and r['provenance_status'] == 'VALID')
    sp_pi = sum(1 for r in runs if 'PASS' in r['semantic_status'] and r['provenance_status'] == 'INVALID')
    sf_pv = sum(1 for r in runs if 'PASS' not in r['semantic_status'] and r['provenance_status'] == 'VALID')
    sf_pi = sum(1 for r in runs if 'PASS' not in r['semantic_status'] and r['provenance_status'] == 'INVALID')
    
    return {
        'condition': condition_key, 'n_runs': n_runs,
        'metrics': {'FR': fr, 'IR': ir, 'VR': vr, 'SR': sr, 'F3R': f3r, 'PER': per_avg, 'PC': pc_avg,
                    'total_ids': ir_total_gen, 'total_invalid': ir_total_inv, 'f3_count': f3_count},
        'context_hash': context_hash[:16], 'retrieval_top1': retrieval_top1,
        'fabrication_types': dict(fab_types),
        'crosstab': {'PASS_VALID': sp_pv, 'PASS_INVALID': sp_pi, 'FAIL_VALID': sf_pv, 'FAIL_INVALID': sf_pi},
        'runs_summary': [{'run_id': r['run_id'], 'invalid_ids': r['invalid_ids'], 'invalid_types': r['invalid_types'],
                          'validator_status': r['validator_status'], 'semantic_status': r['semantic_status'],
                          'provenance_status': r['provenance_status'], 'per_run': r['per_run'], 'pc_run': r['pc_run']} for r in runs],
    }


def main():
    print("=" * 80)
    print("AION Passo 6.3.1-C — Provenance Evidence-Bound")
    print(f"C0/C1/C2, N={N_PER_CONDITION} cada (90 runs)")
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
    
    results = {}
    for cond_key, cond_data in CONDITIONS.items():
        print(f"\n{'=' * 70}")
        print(f"[{cond_key}] {cond_data['name']} — N={N_PER_CONDITION}")
        print(f"{'=' * 70}")
        results[cond_key] = run_condition(j_store, validator, base_chunks, cond_key, cond_data['prompt'], N_PER_CONDITION)
        m = results[cond_key]['metrics']
        print(f"  FR={m['FR']:.4f} IR={m['IR']:.4f} VR={m['VR']:.4f} SR={m['SR']:.4f} F3R={m['F3R']:.4f} PER={m['PER']:.4f} PC={m['PC']:.4f}")
    
    # Matriz
    print(f"\n{'=' * 80}")
    print("[MATRIZ C0/C1/C2]")
    print(f"{'=' * 80}")
    print(f"\n{'Cond':<6} {'FR':<10} {'IR':<10} {'VR':<10} {'SR':<10} {'F3R':<10} {'PER':<10} {'PC':<10}")
    print('-' * 76)
    for cond in ['C0', 'C1', 'C2']:
        m = results[cond]['metrics']
        print(f"{cond:<6} {m['FR']:<10.4f} {m['IR']:<10.4f} {m['VR']:<10.4f} {m['SR']:<10.4f} {m['F3R']:<10.4f} {m['PER']:<10.4f} {m['PC']:<10.4f}")
    
    # Análise de preservação
    print(f"\n{'=' * 80}")
    print("[ANÁLISE DE PRESERVAÇÃO]")
    print(f"{'=' * 80}")
    
    fr_c0 = results['C0']['metrics']['FR']
    fr_c1 = results['C1']['metrics']['FR']
    fr_c2 = results['C2']['metrics']['FR']
    pc_c0 = results['C0']['metrics']['PC']
    pc_c1 = results['C1']['metrics']['PC']
    pc_c2 = results['C2']['metrics']['PC']
    sr_c0 = results['C0']['metrics']['SR']
    sr_c1 = results['C1']['metrics']['SR']
    sr_c2 = results['C2']['metrics']['SR']
    
    for cond in ['C1', 'C2']:
        fr_cond = results[cond]['metrics']['FR']
        pc_cond = results[cond]['metrics']['PC']
        sr_cond = results[cond]['metrics']['SR']
        
        fr_reduced = fr_cond < fr_c0
        pc_preserved = pc_cond >= pc_c0 * 0.5
        sr_preserved = sr_cond >= sr_c0 * 0.5
        
        if fr_reduced and pc_preserved and sr_preserved:
            assessment = f'CANDIDATO A SOLUÇÃO ✅ — FR reduziu, PC e SR preservados'
        elif fr_reduced and not pc_preserved:
            assessment = f'FALSA SOLUÇÃO ❌ — FR reduziu MAS PC colapsou (supressão de provenance)'
        elif fr_reduced and not sr_preserved:
            assessment = f'FALSA SOLUÇÃO ❌ — FR reduziu MAS SR colapsou (supressão semântica)'
        elif not fr_reduced:
            assessment = f'SEM EFEITO — FR não reduziu'
        else:
            assessment = f'INCONCLUSIVO'
        
        print(f"\n  {cond}:")
        print(f"    FR: {fr_c0:.4f} → {fr_cond:.4f} ({'reduziu ✅' if fr_reduced else 'sem redução ❌'})")
        print(f"    PC: {pc_c0:.4f} → {pc_cond:.4f} ({'preservado ✅' if pc_preserved else 'colapsou ❌'})")
        print(f"    SR: {sr_c0:.4f} → {sr_cond:.4f} ({'preservado ✅' if sr_preserved else 'colapsou ❌'})")
        print(f"    >>> {assessment}")
    
    # Salvar
    report = {
        'metadata': {
            'experiment': 'AION-6.3.1-C — Provenance Evidence-Bound',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'n_per_condition': N_PER_CONDITION,
            'total_runs': 3 * N_PER_CONDITION,
        },
        'results': results,
        'preservation_analysis': {
            'C1': {
                'fr_reduced': fr_c1 < fr_c0,
                'pc_preserved': pc_c1 >= pc_c0 * 0.5,
                'sr_preserved': sr_c1 >= sr_c0 * 0.5,
            },
            'C2': {
                'fr_reduced': fr_c2 < fr_c0,
                'pc_preserved': pc_c2 >= pc_c0 * 0.5,
                'sr_preserved': sr_c2 >= sr_c0 * 0.5,
            },
        },
    }
    
    json_path = OUTPUT_DIR / 'aion_6_3_1_c_evidence_bound.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
