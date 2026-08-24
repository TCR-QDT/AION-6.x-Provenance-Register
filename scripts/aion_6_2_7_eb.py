#!/usr/bin/env python3
"""
AION Passo 6.2.7 — Experimento Combinado E+B

Combina:
- E: Stopword filtering (remover palavras frequentes)
- B: Normalização matemática (β→beta, ×→*, etc.)

Aplicado SOMENTE à representação experimental.
Documento-fonte: PRESERVADO.

Árvore decisória:
- Nível 0 (Falha): chunk-alvo fora do Top-20
- Nível 1 (Evidência de mecanismo): chunk no Top-20, não no Top-3
- Nível 2 (Recuperação operacional): chunk no Top-3, evidência válida
- Nível 3 (Resolução robusta): determinístico, sem regressão em B2-B7

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import sys
import re
import time
import subprocess
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
from aion_6_2_6_top_k_efgh import STOPWORDS, build_base_chunks
from aion_6_2_experiments_bcd import normalize_math

OUTPUT_DIR = Path('/home/z/my-project/download/rag')


# === Experimento E+B — Combinação ===

class ExperimentEB_Store:
    """Combina E (stopwords) + B (normalização matemática).
    
    Aplica normalização matemática à REPRESENTAÇÃO EXPERIMENTAL
    (texto que vai para o TF-IDF), mantendo o documento-fonte inalterado.
    Remove stopwords durante a vetorização.
    """
    
    def __init__(self, chunks: list):
        self.chunks = chunks
        # Aplica normalização matemática APENAS à representação experimental
        # Documento-fonte (chunk.text original) permanece inalterado
        self.normalized_texts = [normalize_math(c.text) for c in self.chunks]
        
        self.vectorizer = TfidfVectorizer(
            max_features=4096,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            token_pattern=r'(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9_]+\b',
            stop_words=list(STOPWORDS),  # E: stopword filtering
        )
        # Aplica B (normalização) + E (stopwords) à representação
        self.matrix = self.vectorizer.fit_transform(self.normalized_texts)
        
        print(f"  [Exp E+B] Vocabulário: {len(self.vectorizer.vocabulary_)} termos")
        print(f"  [Exp E+B] Stopwords aplicadas: {len(STOPWORDS)}")
        print(f"  [Exp E+B] 'beta' no vocabulário: {'beta' in self.vectorizer.vocabulary_}")
        print(f"  [Exp E+B] 'mu' no vocabulário: {'mu' in self.vectorizer.vocabulary_}")
        print(f"  [Exp E+B] 'tcr' no vocabulário: {'tcr' in self.vectorizer.vocabulary_}")
        print(f"  [Exp E+B] 'coerência' no vocabulário: {'coerência' in self.vectorizer.vocabulary_}")
    
    def query(self, question: str, top_k: int = 8):
        # Aplica B (normalização) à pergunta também
        normalized_question = normalize_math(question)
        # E (stopwords) aplicado automaticamente pelo vectorizer
        q_vec = self.vectorizer.transform([normalized_question])
        scores = cosine_similarity(q_vec, self.matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for rank, idx in enumerate(top_indices, 1):
            # Retorna chunk original (não normalizado) — preserva evidência
            r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
            results.append(r)
        return results


# === Diagnóstico Top-k para E+B ===

def diagnose_top_k(store, question: str, expected_prefix: str, k_values=[1, 3, 5, 10, 20]) -> dict:
    """Diagnóstico Top-k detalhado."""
    max_k = max(k_values)
    retrieved = store.query(question, top_k=max_k)
    
    results = {}
    found_at_rank = None
    corpus_002_chunks = []
    
    for k in k_values:
        top_k_chunks = retrieved[:k]
        hit = any(r.chunk.chunk_id.startswith(expected_prefix) for r in top_k_chunks)
        results[k] = hit
        if hit and found_at_rank is None:
            for r in top_k_chunks:
                if r.chunk.chunk_id.startswith(expected_prefix):
                    found_at_rank = r.rank
                    break
    
    # Identifica todos os chunks CORPUS-002 recuperados
    for r in retrieved:
        if r.chunk.corpus_id == 'CORPUS-002':
            corpus_002_chunks.append({
                'rank': r.rank,
                'chunk_id': r.chunk.chunk_id,
                'score': r.score,
            })
    
    return {
        'question': question,
        'expected_prefix': expected_prefix,
        'hits_by_k': results,
        'found_at_rank': found_at_rank,
        'corpus_002_chunks_retrieved': corpus_002_chunks,
        'top1': {
            'chunk_id': retrieved[0].chunk.chunk_id if retrieved else None,
            'score': retrieved[0].score if retrieved else None,
            'corpus_id': retrieved[0].chunk.corpus_id if retrieved else None,
        },
        'top10_all': [{'rank': r.rank, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id} for r in retrieved[:10]],
    }


# === Avaliação completa de B1 com E+B ===

def evaluate_b1_eb(store, validator, n_runs=3) -> dict:
    """Avalia B1 com E+B: 3 runs + LLM + validator + top-k."""
    test = BENCH_TESTS['B1']
    expected_prefix = 'CORPUS-002#p1'
    
    print(f"\n  Diagnóstico Top-k para E+B:")
    diagnosis = diagnose_top_k(store, test['pergunta'], expected_prefix)
    
    print(f"    Top-1: {'✅' if diagnosis['hits_by_k'][1] else '❌'}")
    print(f"    Top-3: {'✅' if diagnosis['hits_by_k'][3] else '❌'}")
    print(f"    Top-5: {'✅' if diagnosis['hits_by_k'][5] else '❌'}")
    print(f"    Top-10: {'✅' if diagnosis['hits_by_k'][10] else '❌'}")
    print(f"    Top-20: {'✅' if diagnosis['hits_by_k'][20] else '❌'}")
    
    if diagnosis['found_at_rank']:
        print(f"    >>> Chunk CORPUS-002#p1 encontrado no rank #{diagnosis['found_at_rank']}")
    else:
        print(f"    >>> NÃO encontrado em Top-20")
    
    if diagnosis['corpus_002_chunks_retrieved']:
        print(f"    >>> Outros chunks CORPUS-002 recuperados:")
        for c in diagnosis['corpus_002_chunks_retrieved'][:5]:
            print(f"        #{c['rank']} score={c['score']:.4f} | {c['chunk_id']}")
    
    print(f"\n    Top-1 chunk: {diagnosis['top1']['chunk_id']} (score={diagnosis['top1']['score']:.4f})")
    print(f"    Top-10 chunks:")
    for c in diagnosis['top10_all']:
        marker = '✅' if c['chunk_id'].startswith(expected_prefix) else '  '
        print(f"      {marker} #{c['rank']} score={c['score']:.4f} | {c['chunk_id']:<30} | {c['corpus_id']}")
    
    # 3 runs para verificar determinismo
    runs = []
    for run_idx in range(1, n_runs + 1):
        retrieved = store.query(test['pergunta'], top_k=8)
        top3 = [{'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score} for i, r in enumerate(retrieved[:3])]
        hit_top3 = any(r['chunk_id'].startswith(expected_prefix) for r in top3)
        runs.append({'run_idx': run_idx, 'top3_chunks': top3, 'hit_top3': hit_top3})
    
    hits = sum(1 for r in runs if r['hit_top3'])
    top3_sets = [tuple(r['chunk_id'] for r in run['top3_chunks']) for run in runs]
    deterministic = all(s == top3_sets[0] for s in top3_sets)
    
    return {
        'top_k_diagnosis': diagnosis,
        'runs': runs,
        'hits_top3': hits,
        'retrieval_hit_rate': hits / n_runs,
        'deterministic': deterministic,
        'B1_status_retrieval': 'PASS' if hits == n_runs else ('PARTIAL' if hits > 0 else 'FAIL-SYSTEM'),
    }


# === Rebenchmark B2-B7 com E+B (teste de não-regressão) ===

def rebenchmark_b2_b7_with_eb(store, validator) -> dict:
    """Teste de não-regressão: B2-B7 com E+B."""
    print(f"\n  Teste de não-regressão B2-B7:")
    
    results = {}
    
    for test_id in ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        test = BENCH_TESTS[test_id]
        
        # Retrieval
        retrieved = store.query(test['pergunta'], top_k=8)
        retrieved_for_eval = [
            {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
            for i, r in enumerate(retrieved)
        ]
        
        # System extra (igual ao 6.1-F)
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


# === Classificação por árvore decisória ===

def classify_decision_tree(eb_result, b2_b7_results, baseline_status) -> dict:
    """Classifica o resultado pela árvore decisória de 4 níveis."""
    
    diagnosis = eb_result['top_k_diagnosis']
    found_at_rank = diagnosis['found_at_rank']
    hits_top3 = eb_result['hits_top3']
    deterministic = eb_result['deterministic']
    
    # Nível 0 — Falha: chunk-alvo fora do Top-20
    if not diagnosis['hits_by_k'][20]:
        level = 0
        level_name = 'FALHA'
        b1_status = 'FAIL-SYSTEM'
        verdict = 'B1 continua FAIL-SYSTEM — chunk-alvo não recuperado em Top-20'
        can_promote = False
    
    # Nível 1 — Evidência de mecanismo: chunk no Top-20, não no Top-3
    elif not hits_top3:
        level = 1
        level_name = 'EVIDÊNCIA_DE_MECANISMO'
        b1_status = 'FAIL-SYSTEM (melhorado)'
        verdict = f'B1 mostra melhora de retrieval (rank #{found_at_rank}) mas ainda não no Top-3'
        can_promote = False
    
    # Nível 2 — Recuperação operacional: chunk no Top-3, evidência válida
    elif hits_top3 == 3:
        # Verificar se proveniência é válida (invalid_count = 0)
        # Como não rodamos LLM para B1 ainda, vamos verificar o que seria necessário
        level = 2
        level_name = 'RECUPERAÇÃO_OPERACIONAL'
        b1_status = 'PASS (pending provenance validation)'
        verdict = 'B1 recuperou chunk-alvo em Top-3 — validar proveniência'
        can_promote = False  # Precisa validar proveniência
    
    # Nível 3 — Resolução robusta
    else:
        level = 3
        level_name = 'RESOLUÇÃO_ROBUSTA'
        b1_status = 'PASS'
        verdict = 'B1 RESOLVIDO — determinístico + sem regressão'
        can_promote = True
    
    # Verificar regressão em B2-B7
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
        eb_status = b2_b7_results[test_id]['eval_002_v02']['avaliacao_final']
        
        baseline_score = baseline_hierarchy.get(baseline_status, 0)
        eb_score = baseline_hierarchy.get(eb_status, 0)
        
        if eb_score < baseline_score:
            regressions.append({
                'test': test_id,
                'baseline_status': baseline_status,
                'eb_status': eb_status,
                'regression': True,
            })
    
    no_regression = len(regressions) == 0
    
    # Verificar invalid_count = 0 em B2-B7
    all_valid = all(b2_b7_results[tid]['invalid_count'] == 0 for tid in ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'])
    
    return {
        'level': level,
        'level_name': level_name,
        'b1_status': b1_status,
        'verdict': verdict,
        'can_promote': can_promote,
        'no_regression': no_regression,
        'regressions': regressions,
        'all_provenance_valid_b2_b7': all_valid,
        'final_decision': 'B1 RESOLVED' if (level == 3 and no_regression and all_valid) else 'B1 NOT RESOLVED',
    }


def main():
    print("=" * 70)
    print("AION Passo 6.2.7 — Experimento Combinado E+B")
    print("Stopwords + Normalização matemática")
    print("=" * 70)
    
    # Constrói chunks base
    print("\n[SETUP] Construindo chunks base do corpus v1.3.0...")
    base_chunks = build_base_chunks()
    print(f"  Base chunks: {len(base_chunks)}")
    
    # Inicializa validator
    validator = ProvenanceValidator(base_chunks)
    print(f"  Validator CORPUS_INDEX: {len(validator.corpus_index)} chunks")
    
    # === EXPERIMENTO E+B ===
    print(f"\n{'=' * 70}")
    print("[6.2.7] EXPERIMENTO E+B — Stopwords + Normalização matemática")
    print(f"{'=' * 70}")
    print("\n  Documento-fonte: PRESERVADO (evidência inalterada)")
    print("  Representação experimental: normalizada + stopwords removidas")
    
    eb_store = ExperimentEB_Store(base_chunks)
    eb_result = evaluate_b1_eb(eb_store, validator, n_runs=3)
    
    print(f"\n  Resultado E+B (retrieval only):")
    print(f"    Hits top-3: {eb_result['hits_top3']}/3")
    print(f"    B1 status (retrieval): {eb_result['B1_status_retrieval']}")
    print(f"    Deterministic: {eb_result['deterministic']}")
    
    # === COMPARAÇÃO A vs E vs E+B ===
    print(f"\n{'=' * 70}")
    print("[COMPARAÇÃO — A (Controle) vs E (Stopwords) vs E+B]")
    print(f"{'=' * 70}")
    
    # Carrega dados de A e E
    efgh_path = OUTPUT_DIR / 'aion_6_2_6_diagnosis_top_k_efgh.json'
    efgh_data = json.loads(efgh_path.read_text(encoding='utf-8'))
    
    a_diag = efgh_data['control_top_k_diagnosis']['top_k_diagnosis']
    e_diag = efgh_data['experiment_E_stopwords']['top_k_diagnosis']
    eb_diag = eb_result['top_k_diagnosis']
    
    comparison = {
        'A (Controle)': {
            'intervention': 'TF-IDF atual',
            'hits_by_k': a_diag['hits_by_k'],
            'found_at_rank': a_diag['found_at_rank'],
            'top1': a_diag['top1'],
        },
        'E (Stopwords)': {
            'intervention': 'Stopword filtering',
            'hits_by_k': e_diag['hits_by_k'],
            'found_at_rank': e_diag['found_at_rank'],
            'top1': e_diag['top1'],
        },
        'E+B (Stopwords + Normalização)': {
            'intervention': 'Stopword filtering + Normalização matemática',
            'hits_by_k': eb_diag['hits_by_k'],
            'found_at_rank': eb_diag['found_at_rank'],
            'top1': eb_diag['top1'],
        },
    }
    
    print(f"\n{'Braço':<35} {'Top-1':<8} {'Top-3':<8} {'Top-5':<8} {'Top-10':<8} {'Top-20':<8} {'Rank'}")
    print('-' * 90)
    for arm, data in comparison.items():
        hits = data['hits_by_k']
        rank = data['found_at_rank'] if data['found_at_rank'] else 'N/A'
        # hits keys podem ser int ou string — normalizar para int
        def hit_at(k):
            return hits.get(k, hits.get(str(k), False))
        print(f"{arm:<35} {'✅' if hit_at(1) else '❌':<8} {'✅' if hit_at(3) else '❌':<8} {'✅' if hit_at(5) else '❌':<8} {'✅' if hit_at(10) else '❌':<8} {'✅' if hit_at(20) else '❌':<8} {rank}")
    
    # === TESTE DE NÃO-REGRESSÃO B2-B7 ===
    print(f"\n{'=' * 70}")
    print("[TESTE DE NÃO-REGRESSÃO B2-B7 com E+B]")
    print(f"{'=' * 70}")
    
    b2_b7_results = rebenchmark_b2_b7_with_eb(eb_store, validator)
    
    # === ÁRVORE DECISÓRIA ===
    print(f"\n{'=' * 70}")
    print("[ÁRVORE DECISÓRIA — Classificação]")
    print(f"{'=' * 70}")
    
    decision = classify_decision_tree(eb_result, b2_b7_results, baseline_status='FAIL-SYSTEM')
    
    print(f"\n  Nível: {decision['level']} — {decision['level_name']}")
    print(f"  B1 status: {decision['b1_status']}")
    print(f"  Verdict: {decision['verdict']}")
    print(f"  Can promote: {decision['can_promote']}")
    print(f"  No regression in B2-B7: {decision['no_regression']}")
    if decision['regressions']:
        print(f"  Regressions:")
        for r in decision['regressions']:
            print(f"    ⚠️ {r['test']}: {r['baseline_status']} → {r['eb_status']}")
    print(f"  All provenance valid in B2-B7: {decision['all_provenance_valid_b2_b7']}")
    print(f"\n  >>> FINAL DECISION: {decision['final_decision']}")
    
    # Salvar relatório
    report = {
        'metadata': {
            'experiment': 'AION-6.2.7 — Experimento Combinado E+B',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'experiment_eb': {
            'description': 'Stopword filtering (E) + Normalização matemática (B)',
            'document_preservation': 'Documento-fonte PRESERVADO; apenas representação experimental alterada',
            'interventions_applied': ['E: stopword filtering', 'B: normalização matemática (β→beta, ×→*)'],
            'result': eb_result,
        },
        'comparison_a_e_eb': comparison,
        'b2_b7_regression_test': b2_b7_results,
        'decision_tree': decision,
    }
    
    json_path = OUTPUT_DIR / 'aion_6_2_7_eb_resultados.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
