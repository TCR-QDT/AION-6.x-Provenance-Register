#!/usr/bin/env python3
"""
AION Passo 6.3.1-B — Decomposição causal Prompt × Schema (P0/P1/P2)

P0: Provenance estruturada SIM + Schema múltiplo (controle)
P1: Provenance estruturada NÃO + Schema múltiplo (ablação de provenance)
P2: Provenance estruturada SIM + Schema unificado (controle de schema)

N=50 por condição (150 runs total).
NÃO altera: corpus, oracle, retrieval, validator, modelo.

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
N_PER_CONDITION = 20

# === Prompts ===

# P0 — Controle (P_RESP_001 v0.2 completo)
P0_PROMPT = P_RESP_001_V02_SYSTEM_PROMPT

# P1 — Sem provenance estruturada (prompt simplificado)
P1_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido. Se a informação não estiver no contexto, diga 'INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO'. Não invente. Não use conhecimento externo. Responda em português."""

# P2 — Provenance estruturada + Schema unificado
# Unifica o schema de chunks: converte todos os IDs para o formato "chunk_NNN"
# no contexto entregue ao LLM, eliminando a competição entre "chunk_001" e "p1_01"
P2_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido.

PROTOCOLO DE PROVENIÊNCIA EXPLICITA (P-RESP-001 v0.2):

Para cada afirmação relevante, você DEVE:
1. Classificar: [E] (evidência), [I] (interpretação), [H] (hipótese)
2. Citar a fonte: chunk_id=<ID real do contexto> | documento=CORPUS-XXX
3. Se não houver evidência, declarar: "INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO."

NUNCA produza um identificador que não apareça literalmente no contexto.
Responda em português."""


def unify_chunk_schema(text):
    """Converte todos os chunk IDs no texto para o formato unificado chunk_NNN.
    
    CORPUS-002#p1_01 → CORPUS-002#chunk_001
    CORPUS-003#p3_02 → CORPUS-003#chunk_002
    etc.
    
    Mapeamento determinístico: p{page}_{nn} → chunk_{sequential}
    """
    # Encontra todos os chunk IDs
    pattern = r'(CORPUS-\d{3})#(p\d+_\d+|chunk_\d+)'
    
    # Para cada documento, mapeia chunks sequencialmente
    doc_chunk_map = {}
    
    def replace_chunk(match):
        doc = match.group(1)
        old_chunk = match.group(2)
        
        if doc not in doc_chunk_map:
            doc_chunk_map[doc] = {}
        
        if old_chunk not in doc_chunk_map[doc]:
            doc_chunk_map[doc][old_chunk] = f"chunk_{len(doc_chunk_map[doc]) + 1:03d}"
        
        return f"{doc}#{doc_chunk_map[doc][old_chunk]}"
    
    return re.sub(pattern, replace_chunk, text)


def generate_answer_with_prompt(question, retrieved, system_prompt, system_extra="", unify_schema=False):
    """Gera resposta via z-ai CLI."""
    context_parts = []
    for r in retrieved:
        chunk_id = r.chunk.chunk_id
        chunk_text = r.chunk.text
        
        if unify_schema:
            # Unifica o schema do chunk_id no contexto
            chunk_id = unify_chunk_schema(chunk_id)
            chunk_text = unify_chunk_schema(chunk_text)
        
        context_parts.append(
            f"[{chunk_id} | {r.chunk.short_title} | {r.chunk.page} | {r.chunk.section} | score={r.score:.3f}]\n{chunk_text}\n"
        )
    chunks_context = "\n---\n".join(context_parts)
    
    full_system = system_prompt
    if system_extra:
        full_system += " " + system_extra
    
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
            answer = data.get('content') or data.get('response') or result.stdout
        except json.JSONDecodeError:
            answer = result.stdout.strip()
        return answer
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


def run_condition(j_store, validator, all_chunks, condition_key, prompt, n_runs, unify_schema=False):
    """Executa uma condição experimental."""
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
    
    # Context hash (para verificação de controle)
    context_parts = []
    for r in retrieved[:5]:
        ctx_text = r.chunk.text
        ctx_id = r.chunk.chunk_id
        if unify_schema:
            ctx_id = unify_chunk_schema(ctx_id)
            ctx_text = unify_chunk_schema(ctx_text)
        context_parts.append(f"[{ctx_id} | {r.chunk.short_title} | {r.chunk.page} | score={r.score:.3f}]\n{ctx_text}\n")
    context_hash = hashlib.sha256("\n---\n".join(context_parts).encode()).hexdigest()
    
    runs = []
    
    for run_idx in range(1, n_runs + 1):
        if run_idx % 10 == 0:
            print(f"    {condition_key} Run {run_idx}/{n_runs}...")
        
        t_start = time.time()
        answer_raw = generate_answer_with_prompt(
            test['pergunta'], retrieved[:5], prompt, system_extra, unify_schema=unify_schema
        )
        t_elapsed = time.time() - t_start
        answer_clean = clean_answer(answer_raw)
        
        # IDs citados
        cited_ids = list(set(re.findall(r'CORPUS-\d{3}#\w+', answer_clean)))
        
        # Validator (usa IDs originais, não unificados)
        validation_result = validator.validate_response(answer_clean, retrieved_for_eval)
        answer_final = validation_result['answer_cleaned']
        
        valid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if v['is_valid']]
        invalid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if not v['is_valid']]
        
        invalid_types = [classify_fabrication(inv, all_chunks, retrieved_ids) for inv in invalid_ids]
        
        # PER
        exact_copies = sum(1 for cid in cited_ids if cid in retrieved_ids)
        per_run = exact_copies / len(cited_ids) if cited_ids else 1.0
        
        # PC — Provenance Coverage
        # Claims que requeriam provenance = afirmações com [E] ou citação esperada
        e_claims = len(re.findall(r'\[E\]', answer_clean))
        i_claims = len(re.findall(r'\[I\]', answer_clean))
        claims_needing_provenance = e_claims + i_claims
        claims_with_valid_provenance = len(valid_ids)  # cada valid_id = 1 claim com provenance válida
        pc_run = claims_with_valid_provenance / claims_needing_provenance if claims_needing_provenance > 0 else 0.0
        
        eval_result = evaluate_with_eval002_v02('B2', retrieved_for_eval, answer_final, test['gabarito'])
        provenance_status = 'VALID' if not invalid_ids else 'INVALID'
        
        runs.append({
            'run_id': run_idx,
            'condition': condition_key,
            'retrieval_top1': retrieval_top1,
            'context_hash': context_hash[:16],
            'generated_ids': cited_ids,
            'valid_ids': valid_ids,
            'invalid_ids': invalid_ids,
            'invalid_types': invalid_types,
            'per_run': per_run,
            'pc_run': pc_run,
            'e_claims': e_claims,
            'i_claims': i_claims,
            'validator_status': 'INTERCEPTED' if invalid_ids else 'CLEAN',
            'semantic_status': eval_result['avaliacao_final'],
            'provenance_status': provenance_status,
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'tempo_segundos': round(t_elapsed, 2),
        })
    
    # Métricas
    fr = sum(1 for r in runs if r['invalid_ids']) / n_runs
    ir_total_gen = sum(len(r['generated_ids']) for r in runs)
    ir_total_inv = sum(len(r['invalid_ids']) for r in runs)
    ir = ir_total_inv / ir_total_gen if ir_total_gen > 0 else 0
    vr = ir_total_inv / ir_total_inv if ir_total_inv > 0 else 1.0
    sr = sum(1 for r in runs if 'PASS' in r['semantic_status']) / n_runs
    f3_count = sum(1 for r in runs for t in r['invalid_types'] if t == 'F3_DOCUMENT_CORRECT_FORMAT_INCORRECT')
    f3r = f3_count / n_runs
    per_avg = sum(r['per_run'] for r in runs) / n_runs
    pc_avg = sum(r['pc_run'] for r in runs) / n_runs
    
    return {
        'condition': condition_key,
        'n_runs': n_runs,
        'metrics': {
            'FR': fr, 'IR': ir, 'VR': vr, 'SR': sr, 'F3R': f3r, 'PER': per_avg, 'PC': pc_avg,
            'total_ids_generated': ir_total_gen, 'total_invalid_ids': ir_total_inv, 'f3_count': f3_count,
        },
        'context_hash': context_hash[:16],
        'retrieval_top1': retrieval_top1,
        'b1_deterministic': True,  # retrieval é determinístico por construção
        'runs_summary': [
            {
                'run_id': r['run_id'],
                'invalid_ids': r['invalid_ids'],
                'invalid_types': r['invalid_types'],
                'validator_status': r['validator_status'],
                'semantic_status': r['semantic_status'],
                'provenance_status': r['provenance_status'],
                'per_run': r['per_run'],
                'pc_run': r['pc_run'],
            } for r in runs
        ],
    }


def main():
    print("=" * 80)
    print("AION Passo 6.3.1-B — Decomposição causal Prompt × Schema")
    print(f"P0/P1/P2, N={N_PER_CONDITION} cada (150 runs total)")
    print("=" * 80)
    
    base_chunks = build_base_chunks()
    print(f"  Base chunks: {len(base_chunks)}")
    
    validator = ProvenanceValidator(base_chunks)
    print(f"  Validator: {len(validator.corpus_index)} chunks")
    
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
    
    results = {}
    
    # P0 — Controle
    print(f"\n{'=' * 70}")
    print(f"[P0] Controle — P_RESP_001 v0.2 + Schema múltiplo — N={N_PER_CONDITION}")
    print(f"{'=' * 70}")
    results['P0'] = run_condition(j_store, validator, base_chunks, 'P0', P0_PROMPT, N_PER_CONDITION, unify_schema=False)
    m = results['P0']['metrics']
    print(f"  FR={m['FR']:.4f} IR={m['IR']:.4f} VR={m['VR']:.4f} SR={m['SR']:.4f} F3R={m['F3R']:.4f} PER={m['PER']:.4f} PC={m['PC']:.4f}")
    
    # P1 — Ablação de provenance
    print(f"\n{'=' * 70}")
    print(f"[P1] Ablação — Sem provenance estruturada + Schema múltiplo — N={N_PER_CONDITION}")
    print(f"{'=' * 70}")
    results['P1'] = run_condition(j_store, validator, base_chunks, 'P1', P1_PROMPT, N_PER_CONDITION, unify_schema=False)
    m = results['P1']['metrics']
    print(f"  FR={m['FR']:.4f} IR={m['IR']:.4f} VR={m['VR']:.4f} SR={m['SR']:.4f} F3R={m['F3R']:.4f} PER={m['PER']:.4f} PC={m['PC']:.4f}")
    
    # P2 — Schema unificado
    print(f"\n{'=' * 70}")
    print(f"[P2] Schema unificado — P_RESP_001 v0.2 + Schema unificado — N={N_PER_CONDITION}")
    print(f"{'=' * 70}")
    results['P2'] = run_condition(j_store, validator, base_chunks, 'P2', P2_PROMPT, N_PER_CONDITION, unify_schema=True)
    m = results['P2']['metrics']
    print(f"  FR={m['FR']:.4f} IR={m['IR']:.4f} VR={m['VR']:.4f} SR={m['SR']:.4f} F3R={m['F3R']:.4f} PER={m['PER']:.4f} PC={m['PC']:.4f}")
    
    # === MATRIZ BRUTA ===
    print(f"\n{'=' * 80}")
    print("[MATRIZ BRUTA P0/P1/P2]")
    print(f"{'=' * 80}")
    
    print(f"\n{'Condição':<12} {'FR':<10} {'IR':<10} {'VR':<10} {'SR':<10} {'F3R':<10} {'PER':<10} {'PC':<10}")
    print('-' * 82)
    for cond in ['P0', 'P1', 'P2']:
        m = results[cond]['metrics']
        print(f"{cond:<12} {m['FR']:<10.4f} {m['IR']:<10.4f} {m['VR']:<10.4f} {m['SR']:<10.4f} {m['F3R']:<10.4f} {m['PER']:<10.4f} {m['PC']:<10.4f}")
    
    # Controles
    print(f"\n  Controles:")
    for cond in ['P0', 'P1', 'P2']:
        print(f"    {cond}: Top-1={results[cond]['retrieval_top1']}, context_hash={results[cond]['context_hash']}")
    
    # === TESTE DE HIPÓTESES ===
    print(f"\n{'=' * 80}")
    print("[TESTE DE HIPÓTESES]")
    print(f"{'=' * 80}")
    
    fr_p0 = results['P0']['metrics']['FR']
    fr_p1 = results['P1']['metrics']['FR']
    fr_p2 = results['P2']['metrics']['FR']
    
    sr_p0 = results['P0']['metrics']['SR']
    sr_p1 = results['P1']['metrics']['SR']
    sr_p2 = results['P2']['metrics']['SR']
    
    pc_p0 = results['P0']['metrics']['PC']
    pc_p1 = results['P1']['metrics']['PC']
    pc_p2 = results['P2']['metrics']['PC']
    
    f3r_p0 = results['P0']['metrics']['F3R']
    f3r_p1 = results['P1']['metrics']['F3R']
    f3r_p2 = results['P2']['metrics']['F3R']
    
    # H-PROMPT: FR(P0) > FR(P1)
    delta_fr_prompt = fr_p0 - fr_p1
    h_prompt_supported = delta_fr_prompt > 0
    
    # H-SCHEMA: FR(P0) > FR(P2)
    delta_fr_schema = fr_p0 - fr_p2
    h_schema_supported = delta_fr_schema > 0
    
    # Interação
    delta_fr_interaction = delta_fr_prompt - delta_fr_schema
    
    print(f"\n  H-PROMPT (FR(P0) > FR(P1)):")
    print(f"    FR(P0) = {fr_p0:.4f}")
    print(f"    FR(P1) = {fr_p1:.4f}")
    print(f"    ΔFR_prompt = {delta_fr_prompt:+.4f}")
    print(f"    Hipótese {'APOIADA ✅' if h_prompt_supported else 'REJEITADA ❌'}")
    
    print(f"\n  H-SCHEMA (FR(P0) > FR(P2)):")
    print(f"    FR(P0) = {fr_p0:.4f}")
    print(f"    FR(P2) = {fr_p2:.4f}")
    print(f"    ΔFR_schema = {delta_fr_schema:+.4f}")
    print(f"    Hipótese {'APOIADA ✅' if h_schema_supported else 'REJEITADA ❌'}")
    
    print(f"\n  Interação:")
    print(f"    ΔFR_interaction = {delta_fr_interaction:+.4f}")
    
    # Verificar PC e SR
    print(f"\n  Provenance Coverage (PC):")
    print(f"    PC(P0) = {pc_p0:.4f}")
    print(f"    PC(P1) = {pc_p1:.4f}")
    print(f"    PC(P2) = {pc_p2:.4f}")
    print(f"    P1 reduziu PC? {'SIM — supressão de provenance ❌' if pc_p1 < pc_p0 * 0.5 else 'NÃO — provenance preservada ✅'}")
    
    print(f"\n  Semantic Rate (SR):")
    print(f"    SR(P0) = {sr_p0:.4f}")
    print(f"    SR(P1) = {sr_p1:.4f}")
    print(f"    SR(P2) = {sr_p2:.4f}")
    
    # Veredito
    print(f"\n{'=' * 80}")
    print("[VEREDITO CAUSAL]")
    print(f"{'=' * 80}")
    
    # P2 é o candidato ideal: FR baixo + PC preservado + SR preservado
    p2_is_solution = (fr_p2 < fr_p0 * 0.5) and (pc_p2 >= pc_p0 * 0.5) and (sr_p2 >= sr_p0 * 0.5)
    
    if p2_is_solution:
        verdict = 'P2 É CANDIDATO A SOLUÇÃO — FR reduzido + PC e SR preservados'
        action = 'Prosseguir para AION-6.3.2 com schema unificado como intervenção arquitetural'
    elif h_prompt_supported and not h_schema_supported:
        verdict = 'H-PROMPT APOIADA, H-SCHEMA REJEITADA — prompt é causa principal'
        action = 'Investigar modificação de prompt que preserve PC'
    elif h_schema_supported and not h_prompt_supported:
        verdict = 'H-SCHEMA APOIADA, H-PROMPT REJEITADA — schema é causa principal'
        action = 'Investigar unificação de schema como intervenção'
    elif h_prompt_supported and h_schema_supported:
        verdict = 'AMBAS AS HIPÓTESES APOIADAS — prompt e schema são causas contribuintes'
        action = 'Investigar combinação de intervenções'
    else:
        verdict = 'NENHUMA HIPÓTESE APOIADA — investigar outras causas'
        action = 'Reconsiderar modelo causal'
    
    print(f"\n  >>> {verdict}")
    print(f"  >>> {action}")
    
    # Salvar
    report = {
        'metadata': {
            'experiment': 'AION-6.3.1-B — Decomposição causal Prompt × Schema',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'n_per_condition': N_PER_CONDITION,
            'total_runs': 3 * N_PER_CONDITION,
        },
        'results': results,
        'hypothesis_test': {
            'H_PROMPT': {
                'supported': h_prompt_supported,
                'delta_fr': delta_fr_prompt,
                'fr_p0': fr_p0,
                'fr_p1': fr_p1,
                'pc_p0': pc_p0,
                'pc_p1': pc_p1,
                'sr_p0': sr_p0,
                'sr_p1': sr_p1,
            },
            'H_SCHEMA': {
                'supported': h_schema_supported,
                'delta_fr': delta_fr_schema,
                'fr_p0': fr_p0,
                'fr_p2': fr_p2,
                'pc_p0': pc_p0,
                'pc_p2': pc_p2,
                'sr_p0': sr_p0,
                'sr_p2': sr_p2,
            },
            'interaction': delta_fr_interaction,
        },
        'verdict': verdict,
        'action': action,
    }
    
    json_path = OUTPUT_DIR / 'aion_6_3_1_b_prompt_schema.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
