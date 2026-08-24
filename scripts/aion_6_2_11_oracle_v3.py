#!/usr/bin/env python3
"""
AION Passo 6.2.11 — Oracle v3 + Rebenchmark Controlado

Etapa 1: Promover Oracle v3 a ACTIVE (7 chunks)
Etapa 2: Executar J + Oracle v3 (3 runs determinísticos)
Etapa 3: Medir Top-1/3/5/10/20 + identificar qual chunk recuperado
Etapa 4: Teste de não-regressão B2-B7
Etapa 5: Veredito (RESOLVED se Top-3=3/3 + não-regressão)

NÃO executa J+E ainda.

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import sys
import re
import time
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from aion_rag_proxy import TfidfVectorStore, parse_extracted_markdown, RetrievedChunk
from aion_bench_001 import BENCH_TESTS
from aion_p_resp_001_v02 import (
    P_RESP_001_V02_SYSTEM_PROMPT,
    evaluate_with_eval002_v02, generate_answer, clean_answer,
)
from aion_p_resp_001_v03 import ProvenanceValidator
from aion_6_1_f_rebenchmark_lcr import CORPUS_V13_FILES
from aion_6_2_6_top_k_efgh import build_base_chunks
from aion_6_2_9_oracle_crosslingual import B1_ORACLE_V1, B1_ORACLE_V2, B1_PERGUNTA_EN, ExperimentJ_CrossLingual

OUTPUT_DIR = Path('/home/z/my-project/download/rag')


# === ETAPA 1: Oracle v3 — ACTIVE ===

B1_ORACLE_V3 = {
    'version': 'v3',
    'status': 'ACTIVE',
    'promoted_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    'acceptable_chunks': [
        # v2 (5 chunks em CORPUS-002)
        'CORPUS-002#p1_01',  # Abstract (v6.2)
        'CORPUS-002#p1_02',  # Abstract (v6.2)
        'CORPUS-002#p2_01',  # Sec. II (v6.2)
        'CORPUS-002#p5_01',  # Sec. V (v6.2)
        'CORPUS-002#p5_02',  # Sec. V (v6.2)
        # v3 extensão (2 chunks EQUIVALENT em CORPUS-006/007)
        'CORPUS-006#p1_01',  # Abstract (v6.1 oficial) — EQUIVALENT
        'CORPUS-007#p1_01',  # Abstract (v6.1 revisão) — EQUIVALENT
    ],
    'description': 'Conjunto de 7 chunks com evidência primária equivalente (interversional)',
    'rationale': 'Auditoria AION-6.2.10 demonstrou EQUIVALENT entre CORPUS-002/006/007 para a fórmula C = I × S × H^β',
    'audit_source': 'aion_6_2_10_equivalencia_interversional.json',
    'methodological_rule': 'Extensão baseada em equivalência documental demonstrada, não em resultado de retrieval',
    'preservation': 'v1 e v2 permanecem como históricos para reprodução',
}


# === ETAPA 2: J + Oracle v3 (3 runs determinísticos) ===

def evaluate_j_with_oracle_v3(j_store, oracle_chunks: list, n_runs: int = 3) -> dict:
    """Avalia B1 com braço J (cross-lingual) + Oracle v3."""
    test = BENCH_TESTS['B1']
    
    print(f"\n  Pergunta B1 (PT-BR): {test['pergunta'][:80]}...")
    print(f"  Pergunta B1 (EN traduzida): {B1_PERGUNTA_EN[:80]}...")
    print(f"  Oracle v3 aceitável: {oracle_chunks}")
    
    runs = []
    
    for run_idx in range(1, n_runs + 1):
        # J usa a pergunta TRADUZIDA (EN)
        retrieved = j_store.query(test['pergunta'], top_k=20)
        
        # Top-k diagnosis com oracle v3
        top_k_results = {}
        for k in [1, 3, 5, 10, 20]:
            top_k_chunks = retrieved[:k]
            hit = any(r.chunk.chunk_id in oracle_chunks for r in top_k_chunks)
            top_k_results[k] = hit
        
        # Identifica qual chunk do oracle foi recuperado (se algum)
        oracle_chunk_found = None
        oracle_rank = None
        for r in retrieved:
            if r.chunk.chunk_id in oracle_chunks:
                oracle_chunk_found = r.chunk.chunk_id
                oracle_rank = r.rank
                break
        
        # Top-3 detalhado
        top3_detail = [
            {
                'rank': i+1,
                'chunk_id': r.chunk.chunk_id,
                'corpus_id': r.chunk.corpus_id,
                'score': r.score,
                'in_oracle_v3': r.chunk.chunk_id in oracle_chunks,
            } for i, r in enumerate(retrieved[:3])
        ]
        
        # Top-5 detalhado
        top5_detail = [
            {
                'rank': i+1,
                'chunk_id': r.chunk.chunk_id,
                'corpus_id': r.chunk.corpus_id,
                'score': r.score,
                'in_oracle_v3': r.chunk.chunk_id in oracle_chunks,
            } for i, r in enumerate(retrieved[:5])
        ]
        
        # Todos chunks oracle em Top-20
        all_oracle_in_top20 = [
            {
                'rank': r.rank,
                'chunk_id': r.chunk.chunk_id,
                'score': r.score,
            } for r in retrieved if r.chunk.chunk_id in oracle_chunks
        ]
        
        run_result = {
            'run_idx': run_idx,
            'top_k_hits': top_k_results,
            'oracle_chunk_found': oracle_chunk_found,
            'oracle_rank': oracle_rank,
            'top3_detail': top3_detail,
            'top5_detail': top5_detail,
            'all_oracle_chunks_in_top20': all_oracle_in_top20,
            'top1_chunk': retrieved[0].chunk.chunk_id if retrieved else None,
            'top1_score': retrieved[0].score if retrieved else None,
        }
        runs.append(run_result)
        
        if run_idx == 1:
            print(f"\n  Run 1 — Top-k hits (ORACLE v3):")
            for k in [1, 3, 5, 10, 20]:
                hit = top_k_results[k]
                print(f"    Top-{k}: {'✅' if hit else '❌'}")
            
            if oracle_chunk_found:
                print(f"    >>> Primeiro chunk oracle recuperado: {oracle_chunk_found} (rank #{oracle_rank})")
            
            print(f"\n  Top-5 detalhado:")
            for t in top5_detail:
                marker = '✅ ORACLE' if t['in_oracle_v3'] else '  '
                print(f"    {marker} #{t['rank']} score={t['score']:.4f} | {t['chunk_id']:<30} | {t['corpus_id']}")
            
            if all_oracle_in_top20:
                print(f"\n  Todos chunks oracle em Top-20:")
                for o in all_oracle_in_top20:
                    print(f"    #{o['rank']} score={o['score']:.4f} | {o['chunk_id']}")
    
    # Estatísticas
    hits_by_k = {k: sum(1 for r in runs if r['top_k_hits'][k]) for k in [1, 3, 5, 10, 20]}
    
    # Determinismo
    top3_full = [tuple((t['chunk_id'] for t in run['top3_detail'])) for run in runs]
    deterministic = all(s == top3_full[0] for s in top3_full)
    
    # Todos chunks oracle recuperados em qualquer run
    all_oracle_found = list(set(r['oracle_chunk_found'] for r in runs if r['oracle_chunk_found']))
    
    return {
        'oracle_version': 'v3',
        'oracle_chunks': oracle_chunks,
        'runs': runs,
        'hits_by_k': hits_by_k,
        'deterministic': deterministic,
        'oracle_chunks_found_in_any_run': all_oracle_found,
    }


# === ETAPA 4: Teste de não-regressão B2-B7 ===

def rebenchmark_b2_b7(j_store, validator) -> dict:
    """Teste de não-regressão: B2-B7 com braço J (cross-lingual)."""
    print(f"\n  Teste de não-regressão B2-B7 (com braço J cross-lingual):")
    
    # Para B2-B7, precisamos traduzir as perguntas também (cross-lingual)
    # Mas as perguntas B2-B7 já são em PT-BR e os documentos são mistos (PT-BR + EN)
    # Para manter consistência com o controle, usamos a pergunta original (PT-BR)
    # para B2-B7, pois estas não têm o problema específico de B1
    
    results = {}
    
    for test_id in ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        test = BENCH_TESTS[test_id]
        
        # Para B2-B7, usar pergunta original (não traduzida)
        # porque o problema cross-lingual é específico de B1
        # (pergunta em PT-BR sobre documento em EN)
        retrieved = j_store.query_original(test['pergunta'], top_k=8)
        retrieved_for_eval = [
            {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
            for i, r in enumerate(retrieved)
        ]
        
        # System extra
        system_extra = ""
        if test_id == 'B2':
            temporal_data = json.loads((OUTPUT_DIR / 'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
            temporal_context = json.dumps(temporal_data['states'][:5], ensure_ascii=False, indent=2)[:2000]
            system_extra = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{temporal_context}"
        elif test_id == 'B6':
            hist_data = json.loads((OUTPUT_DIR / 'aion_hist_001_reconciliacao.json').read_text(encoding='utf-8'))
            negative_context = json.dumps(hist_data['negative_memory']['DESCONHECIDO'], ensure_ascii=False, indent=2)[:2000]
            system_extra = f"\n\nMEMÓRIA NEGATIVA:\n{negative_context}"
        
        # Geração
        t_start = time.time()
        answer_raw = generate_answer(
            test['pergunta'], retrieved[:5], P_RESP_001_V02_SYSTEM_PROMPT, system_extra
        )
        t_elapsed = time.time() - t_start
        answer_clean = clean_answer(answer_raw)
        
        # Validator
        validation_result = validator.validate_response(answer_clean, retrieved_for_eval)
        answer_final = validation_result['answer_cleaned']
        
        # Avaliação
        eval_result = evaluate_with_eval002_v02(test_id, retrieved_for_eval, answer_final, test['gabarito'])
        
        results[test_id] = {
            'test_id': test_id,
            'categoria': test['categoria'],
            'eval_002_v02': eval_result,
            'invalid_count': validation_result['invalid_count'],
            'valid_count': validation_result['valid_count'],
            'evidence_status': validation_result['evidence_category'],
        }
        
        status = eval_result['avaliacao_final']
        invalid = validation_result['invalid_count']
        print(f"    {test_id}: {status} | invalid={invalid}")
    
    return results


def main():
    print("=" * 80)
    print("AION Passo 6.2.11 — Oracle v3 + Rebenchmark Controlado")
    print("=" * 80)
    
    # === ETAPA 1: Promover Oracle v3 ===
    print(f"\n{'=' * 80}")
    print("[ETAPA 1] Oracle v3 — PROMOVIDO A ACTIVE")
    print(f"{'=' * 80}")
    
    print(f"\n  Oracle versioning completo:")
    print(f"\n  v1 (FROZEN — historical):")
    print(f"    Chunks: {B1_ORACLE_V1['acceptable_chunks']}")
    print(f"    Status: {B1_ORACLE_V1['status']}")
    
    print(f"\n  v2 (FROZEN — metodologicamente corrigido):")
    print(f"    Chunks: {B1_ORACLE_V2['acceptable_chunks']}")
    print(f"    Status: {B1_ORACLE_V2['status']}")
    
    print(f"\n  v3 (ACTIVE — extensão interversional):")
    print(f"    Chunks: {B1_ORACLE_V3['acceptable_chunks']}")
    print(f"    Status: {B1_ORACLE_V3['status']}")
    print(f"    Rationale: {B1_ORACLE_V3['rationale']}")
    print(f"    Preservation: {B1_ORACLE_V3['preservation']}")
    
    # Constrói chunks base
    print(f"\n[SETUP] Construindo chunks base do corpus v1.3.0...")
    base_chunks = build_base_chunks()
    print(f"  Base chunks: {len(base_chunks)}")
    
    # Inicializa validator
    validator = ProvenanceValidator(base_chunks)
    print(f"  Validator CORPUS_INDEX: {len(validator.corpus_index)} chunks")
    
    # === ETAPA 2: J + Oracle v3 ===
    print(f"\n{'=' * 80}")
    print("[ETAPA 2] J + Oracle v3 (3 runs determinísticos)")
    print(f"{'=' * 80}")
    
    # Adiciona método query_original ao ExperimentJ_CrossLingual
    class ExperimentJ_V3(ExperimentJ_CrossLingual):
        """J com método query_original para B2-B7 (usa pergunta PT-BR original)."""
        def query_original(self, question: str, top_k: int = 8):
            q_vec = self.vectorizer.transform([question])
            scores = cosine_similarity(q_vec, self.matrix).flatten()
            top_indices = np.argsort(scores)[::-1][:top_k]
            results = []
            for rank, idx in enumerate(top_indices, 1):
                r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
                results.append(r)
            return results
    
    j_v3_store = ExperimentJ_V3(base_chunks, B1_PERGUNTA_EN)
    
    j_v3_result = evaluate_j_with_oracle_v3(j_v3_store, B1_ORACLE_V3['acceptable_chunks'], n_runs=3)
    
    print(f"\n  Resultado J + Oracle v3:")
    print(f"    Hits por k:")
    for k in [1, 3, 5, 10, 20]:
        hits = j_v3_result['hits_by_k'][k]
        print(f"      Top-{k}: {hits}/3 runs")
    print(f"    Determinístico: {j_v3_result['deterministic']}")
    print(f"    Chunks oracle recuperados: {j_v3_result['oracle_chunks_found_in_any_run']}")
    
    # === ETAPA 3: Resultado detalhado ===
    print(f"\n{'=' * 80}")
    print("[ETAPA 3] RESULTADO DETALHADO")
    print(f"{'=' * 80}")
    
    top1_hits = j_v3_result['hits_by_k'][1]
    top3_hits = j_v3_result['hits_by_k'][3]
    
    print(f"\n  Top-1 hits: {top1_hits}/3")
    print(f"  Top-3 hits: {top3_hits}/3")
    print(f"  Top-5 hits: {j_v3_result['hits_by_k'][5]}/3")
    print(f"  Top-10 hits: {j_v3_result['hits_by_k'][10]}/3")
    print(f"  Top-20 hits: {j_v3_result['hits_by_k'][20]}/3")
    print(f"  Determinístico: {j_v3_result['deterministic']}")
    
    if j_v3_result['oracle_chunks_found_in_any_run']:
        print(f"\n  Chunks oracle recuperados (em qualquer run):")
        for chunk in j_v3_result['oracle_chunks_found_in_any_run']:
            print(f"    • {chunk}")
    
    # Mostra top-5 de cada run
    for run in j_v3_result['runs']:
        print(f"\n  Run {run['run_idx']} — Top-5:")
        for t in run['top5_detail']:
            marker = '✅ ORACLE' if t['in_oracle_v3'] else '  '
            print(f"    {marker} #{t['rank']} score={t['score']:.4f} | {t['chunk_id']:<30} | {t['corpus_id']}")
    
    # === ETAPA 4: Teste de não-regressão B2-B7 ===
    print(f"\n{'=' * 80}")
    print("[ETAPA 4] TESTE DE NÃO-REGRESSÃO B2-B7")
    print(f"{'=' * 80}")
    
    b2_b7_results = rebenchmark_b2_b7(j_v3_store, validator)
    
    # Análise de regressão
    baseline_hierarchy = {'PASS': 5, 'PASS-SEMANTIC': 4, 'PARTIAL': 3, 'FAIL-EVALUATOR': 2, 'FAIL-MIXED': 1, 'FAIL-SYSTEM': 0}
    baseline_b2_b7 = {
        'B2': 'PASS-SEMANTIC',
        'B3': 'FAIL-SYSTEM',
        'B4': 'PARTIAL',
        'B5': 'PASS-SEMANTIC',
        'B6': 'PARTIAL',
        'B7': 'PASS-SEMANTIC',
    }
    
    regressions = []
    for test_id in ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        baseline_status = baseline_b2_b7[test_id]
        v3_status = b2_b7_results[test_id]['eval_002_v02']['avaliacao_final']
        
        baseline_score = baseline_hierarchy.get(baseline_status, 0)
        v3_score = baseline_hierarchy.get(v3_status, 0)
        
        if v3_score < baseline_score:
            regressions.append({
                'test': test_id,
                'baseline_status': baseline_status,
                'v3_status': v3_status,
            })
    
    no_regression = len(regressions) == 0
    all_valid = all(b2_b7_results[tid]['invalid_count'] == 0 for tid in ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'])
    
    print(f"\n  Regressões: {len(regressions)}")
    if regressions:
        for r in regressions:
            print(f"    ⚠️ {r['test']}: {r['baseline_status']} → {r['v3_status']}")
    else:
        print(f"    ✅ Nenhuma regressão")
    
    print(f"  Todas proveniências válidas: {'SIM' if all_valid else 'NAO'}")
    
    # === ETAPA 5: VEREDITO ===
    print(f"\n{'=' * 80}")
    print("[ETAPA 5] VEREDITO AION-6.2.11")
    print(f"{'=' * 80}")
    
    # Critério: Top-1 = 3/3 + Top-3 = 3/3 + não-regressão B2-B7
    top1_pass = top1_hits == 3
    top3_pass = top3_hits == 3
    deterministic_pass = j_v3_result['deterministic']
    no_regression_pass = no_regression
    all_valid_pass = all_valid
    
    print(f"\n  Critérios para B1 RESOLVED:")
    print(f"    Top-1 = 3/3: {'✅' if top1_pass else '❌'} ({top1_hits}/3)")
    print(f"    Top-3 = 3/3: {'✅' if top3_pass else '❌'} ({top3_hits}/3)")
    print(f"    Determinístico: {'✅' if deterministic_pass else '❌'}")
    print(f"    Não-regressão B2-B7: {'✅' if no_regression_pass else '❌'}")
    print(f"    Proveniências válidas B2-B7: {'✅' if all_valid_pass else '❌'}")
    
    all_criteria = top1_pass and top3_pass and deterministic_pass and no_regression_pass and all_valid_pass
    
    if all_criteria:
        verdict = 'B1 RESOLVED / ROBUST'
        b1_final_status = 'RESOLVED'
        next_action = 'AION-6.2 pode ser encerrado formalmente'
    elif top3_pass and deterministic_pass:
        verdict = 'B1 PARTIALLY RESOLVED — Top-3 OK mas outro critério falhou'
        b1_final_status = 'PARTIALLY_RESOLVED'
        next_action = 'Investigar critério falhado'
    elif top3_hits > 0:
        verdict = 'B1 PARTIALLY RESOLVED — melhora mas não robusto'
        b1_final_status = 'PARTIALLY_RESOLVED'
        next_action = 'Investigar J+E ou próxima intervenção'
    else:
        verdict = 'B1 NOT RESOLVED'
        b1_final_status = 'FAIL-SYSTEM'
        next_action = 'Investigar próxima causa contribuinte'
    
    print(f"\n  >>> VEREDITO: {verdict}")
    print(f"  >>> B1 status: {b1_final_status}")
    print(f"  >>> Próxima ação: {next_action}")
    
    # Salvar relatório
    report = {
        'metadata': {
            'experiment': 'AION-6.2.11 — Oracle v3 + Rebenchmark Controlado',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'oracle_v1': B1_ORACLE_V1,
        'oracle_v2': B1_ORACLE_V2,
        'oracle_v3': B1_ORACLE_V3,
        'etapa_2_j_oracle_v3': j_v3_result,
        'etapa_3_resultado_detalhado': {
            'top1_hits': top1_hits,
            'top3_hits': top3_hits,
            'top5_hits': j_v3_result['hits_by_k'][5],
            'top10_hits': j_v3_result['hits_by_k'][10],
            'top20_hits': j_v3_result['hits_by_k'][20],
            'deterministic': j_v3_result['deterministic'],
            'oracle_chunks_found': j_v3_result['oracle_chunks_found_in_any_run'],
        },
        'etapa_4_nao_regressao_b2_b7': b2_b7_results,
        'etapa_5_veredito': {
            'criteria': {
                'top1_pass': top1_pass,
                'top3_pass': top3_pass,
                'deterministic_pass': deterministic_pass,
                'no_regression_pass': no_regression_pass,
                'all_valid_pass': all_valid_pass,
            },
            'all_criteria_met': all_criteria,
            'verdict': verdict,
            'b1_final_status': b1_final_status,
            'next_action': next_action,
        },
    }
    
    json_path = OUTPUT_DIR / 'aion_6_2_11_oracle_v3_rebenchmark.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
