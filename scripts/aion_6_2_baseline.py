#!/usr/bin/env python3
"""
AION Passo 6.2 — Resolução Experimental de B1

Etapa 6.2.0: Congelamento do baseline v1.3.0
Etapa 6.2.1: Reprodução determinística de B1 (3 runs para estabelecer baseline)
Etapa 6.2.2: Experimento A — Controle (TF-IDF atual, sem alteração)

NÃO altera: corpus v1.3.0, GraphRAG, P-RESP-001 v0.3, AION-EVAL-002 v0.2

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import sys
import time
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

from aion_rag_proxy import TfidfVectorStore, parse_extracted_markdown
from aion_bench_001 import BENCH_TESTS
from aion_p_resp_001_v02 import (
    P_RESP_001_V02_SYSTEM_PROMPT, CONTROL_SYSTEM_PROMPT,
    evaluate_with_eval002_v02, generate_answer, clean_answer,
)
from aion_p_resp_001_v03 import ProvenanceValidator
from aion_6_1_f_rebenchmark_lcr import CORPUS_V13_FILES

OUTPUT_DIR = Path('/home/z/my-project/download/rag')


# === Etapa 6.2.0 — Congelamento do baseline ===

def stage_6_2_0_freeze_baseline() -> dict:
    """Registra snapshot do baseline antes dos experimentos."""
    print("=" * 70)
    print("[ETAPA 6.2.0] Congelamento do baseline v1.3.0")
    print("=" * 70)
    
    baseline = {
        'snapshot_timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'frozen_components': {
            'corpus': 'v1.3.0 (9 registros documentais + 2 inexistentes)',
            'graphrag': 'v1.0.0 (22 nós, 187 arestas)',
            'p_resp_001': 'v0.3 (validator determinístico)',
            'aion_eval_002': 'v0.2 (FAIL-SYSTEM vs FAIL-EVALUATOR)',
            'aion_dify_001': 'APROVADO',
        },
        'baseline_benchmarks': {
            'B1': 'FAIL-SYSTEM',
            'B2': 'PASS-SEMANTIC',
            'B3': 'FAIL-SYSTEM',
            'B4': 'PARTIAL',
            'B5': 'PASS-SEMANTIC',
            'B6': 'PARTIAL (TEMPORALLY BOUNDED, NOT CLOSED)',
            'B7': 'PASS-SEMANTIC',
        },
        'restraint_principles': [
            'NÃO alterar corpus v1.3.0',
            'NÃO alterar GraphRAG',
            'NÃO alterar P-RESP-001 v0.3',
            'NÃO alterar AION-EVAL-002 v0.2',
            'NÃO alterar AION-DIFY-001',
            'NÃO mascarar B1 como PASS artificial',
            'Intervir SOMENTE entre EVIDÊNCIA e RETRIEVAL/REPRESENTAÇÃO',
        ],
    }
    
    # Hash do snapshot para auditoria
    baseline_hash = hashlib.sha256(
        json.dumps(baseline, sort_keys=True).encode()
    ).hexdigest()
    baseline['snapshot_hash'] = baseline_hash
    
    print(f"\n  Componentes congelados:")
    for k, v in baseline['frozen_components'].items():
        print(f"    • {k}: {v}")
    
    print(f"\n  Baseline benchmarks:")
    for k, v in baseline['baseline_benchmarks'].items():
        print(f"    • {k}: {v}")
    
    print(f"\n  Restraint principles:")
    for p in baseline['restraint_principles']:
        print(f"    • {p}")
    
    print(f"\n  Snapshot hash: {baseline_hash[:32]}...")
    
    return baseline


# === Etapa 6.2.1 — Reprodução determinística de B1 ===

def stage_6_2_1_reproduce_b1(store, validator, n_runs=3) -> dict:
    """Executa B1 N vezes para estabelecer baseline determinístico."""
    print(f"\n{'=' * 70}")
    print(f"[ETAPA 6.2.1] Reprodução determinística de B1 ({n_runs} runs)")
    print(f"{'=' * 70}")
    
    test = BENCH_TESTS['B1']
    runs = []
    
    for run_idx in range(1, n_runs + 1):
        print(f"\n  --- Run {run_idx}/{n_runs} ---")
        
        # Retrieval (TF-IDF atual, sem alteração)
        retrieved = store.query(test['pergunta'], top_k=8)
        retrieved_for_eval = [
            {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
            for i, r in enumerate(retrieved)
        ]
        
        # Top-3 chunks recuperados
        print(f"  Top-3 chunks recuperados:")
        for r in retrieved_for_eval[:3]:
            print(f"    #{r['rank']} score={r['score']:.4f} | {r['chunk_id']:<30} | {r['corpus_id']}")
        
        # Verificar se chunk esperado (CORPUS-002#p1) está no top-3
        expected_prefix = 'CORPUS-002#p1'
        expected_in_top3 = any(r['chunk_id'].startswith(expected_prefix) for r in retrieved_for_eval[:3])
        expected_in_top5 = any(r['chunk_id'].startswith(expected_prefix) for r in retrieved_for_eval[:5])
        expected_rank = None
        for r in retrieved_for_eval:
            if r['chunk_id'].startswith(expected_prefix):
                expected_rank = r['rank']
                break
        
        print(f"  Chunk esperado (CORPUS-002#p1) no top-3: {'SIM' if expected_in_top3 else 'NAO'}")
        if expected_rank:
            print(f"    Rank: #{expected_rank}")
        else:
            print(f"    NAO recuperado em top-8")
        
        # Métricas detalhadas (sem LLM — apenas retrieval)
        run_result = {
            'run_idx': run_idx,
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'pergunta': test['pergunta'],
            'retrieval': {
                'top3_chunks': retrieved_for_eval[:3],
                'top5_chunks': retrieved_for_eval[:5],
                'expected_chunk_prefix': expected_prefix,
                'expected_in_top3': expected_in_top3,
                'expected_in_top5': expected_in_top5,
                'expected_rank': expected_rank,
                'retrieval_hit': expected_in_top3,
            },
            'B1_status_retrieval_only': 'PASS' if expected_in_top3 else 'FAIL-SYSTEM',
        }
        
        runs.append(run_result)
        print(f"  B1 (retrieval only): {run_result['B1_status_retrieval_only']}")
    
    # Análise de estabilidade
    print(f"\n  --- Análise de estabilidade ---")
    hits = sum(1 for r in runs if r['retrieval']['retrieval_hit'])
    print(f"  Hits em {n_runs} runs: {hits}/{n_runs}")
    
    # Verifica se todos os runs recuperaram os mesmos top-3 chunks
    top3_sets = [tuple(r['retrieval']['top3_chunks'][i]['chunk_id'] for i in range(3)) for r in runs]
    all_identical = all(s == top3_sets[0] for s in top3_sets)
    print(f"  Top-3 chunks idênticos em todos os runs: {'SIM' if all_identical else 'NAO'}")
    
    if all_identical:
        print(f"  >>> Retrieval é DETERMINÍSTICO")
        deterministic = True
    else:
        print(f"  >>> Retrieval é NÃO-DETERMINÍSTICO — variabilidade entre runs")
        deterministic = False
        for i, ts in enumerate(top3_sets):
            print(f"    Run {i+1}: {ts}")
    
    return {
        'runs': runs,
        'n_runs': n_runs,
        'hits': hits,
        'deterministic': deterministic,
        'top3_sets': top3_sets,
        'baseline_B1': 'FAIL-SYSTEM' if hits == 0 else 'PASS',
        'baseline_retrieval_hit_rate': hits / n_runs,
    }


# === Etapa 6.2.2 — Experimento A (Controle) ===

def stage_6_2_2_experiment_A_control(store, validator, baseline_b1) -> dict:
    """Experimento A: TF-IDF atual, sem alteração. Estabelece controle."""
    print(f"\n{'=' * 70}")
    print(f"[ETAPA 6.2.2] Experimento A — Controle (TF-IDF atual)")
    print(f"{'=' * 70}")
    
    # Já executado na Etapa 6.2.1 (3 runs)
    # Aqui apenas consolidamos como Experimento A
    
    experiment_A = {
        'name': 'A — Controle',
        'description': 'TF-IDF atual (sklearn TfidfVectorizer), sem alteração',
        'intervention': 'NENHUMA',
        'baseline_b1': baseline_b1['baseline_B1'],
        'retrieval_hit_rate': baseline_b1['baseline_retrieval_hit_rate'],
        'deterministic': baseline_b1['deterministic'],
        'runs': baseline_b1['runs'],
    }
    
    print(f"  Intervention: {experiment_A['intervention']}")
    print(f"  Baseline B1: {experiment_A['baseline_b1']}")
    print(f"  Retrieval hit rate: {experiment_A['retrieval_hit_rate']:.2%}")
    print(f"  Deterministic: {experiment_A['deterministic']}")
    
    return experiment_A


# === Diagnóstico aprofundado de B1 (para entender o gargalo) ===

def diagnose_b1_root_cause(store) -> dict:
    """Diagnóstico aprofundado do gargalo de B1."""
    print(f"\n{'=' * 70}")
    print(f"[DIAGNÓSTICO] Análise aprofundada do gargalo de B1")
    print(f"{'=' * 70}")
    
    test = BENCH_TESTS['B1']
    question = test['pergunta']
    
    # 1. Tokeniza a pergunta
    print(f"\n  Pergunta: {question}")
    
    # Extrai tokens da pergunta
    import re
    question_tokens = re.findall(r'\w+', question.lower())
    print(f"  Tokens da pergunta ({len(question_tokens)}): {question_tokens}")
    
    # Símbolos matemáticos na pergunta
    math_symbols_q = re.findall(r'[=×βΦαµν∂∇∑∏]', question)
    print(f"  Símbolos matemáticos na pergunta: {math_symbols_q}")
    
    # 2. Verifica o chunk esperado (CORPUS-002#p1_01 ou similar)
    print(f"\n  Chunk esperado: CORPUS-002#p1 (Paper A, Abstract)")
    
    # Encontra chunk esperado
    expected_chunks = [c for c in store.chunks if c.chunk_id.startswith('CORPUS-002#p1')]
    if expected_chunks:
        expected_chunk = expected_chunks[0]
        print(f"  Chunk encontrado: {expected_chunk.chunk_id}")
        print(f"  Conteúdo (primeiros 300 chars):")
        print(f"    {expected_chunk.text[:300]}")
        
        # Símbolos matemáticos no chunk esperado
        math_symbols_chunk = re.findall(r'[=×βΦαµν∂∇∑∏]', expected_chunk.text)
        print(f"  Símbolos matemáticos no chunk esperado: {math_symbols_chunk}")
        
        # Tokens do chunk
        chunk_tokens = re.findall(r'\w+', expected_chunk.text.lower())
        print(f"  Tokens do chunk ({len(chunk_tokens)}): primeiros 20 = {chunk_tokens[:20]}")
        
        # Tokens compartilhados entre pergunta e chunk
        shared_tokens = set(question_tokens) & set(chunk_tokens)
        print(f"  Tokens compartilhados (pergunta ∩ chunk): {len(shared_tokens)}")
        print(f"    {shared_tokens}")
        
        # Símbolos matemáticos compartilhados
        shared_math = set(math_symbols_q) & set(math_symbols_chunk)
        print(f"  Símbolos matemáticos compartilhados: {shared_math}")
    
    # 3. Comparar com chunk que está sendo recuperado no top-1
    retrieved = store.query(question, top_k=3)
    if retrieved:
        top1 = retrieved[0]
        print(f"\n  Top-1 recuperado: {top1.chunk.chunk_id}")
        print(f"  Conteúdo (primeiros 300 chars):")
        print(f"    {top1.chunk.text[:300]}")
        
        # Símbolos matemáticos no top-1
        math_symbols_top1 = re.findall(r'[=×βΦαµν∂∇∑∏]', top1.chunk.text)
        print(f"  Símbolos matemáticos no top-1: {math_symbols_top1}")
        
        # Tokens do top-1
        top1_tokens = re.findall(r'\w+', top1.chunk.text.lower())
        print(f"  Tokens do top-1 ({len(top1_tokens)}): primeiros 20 = {top1_tokens[:20]}")
        
        # Tokens compartilhados entre pergunta e top-1
        shared_tokens_top1 = set(question_tokens) & set(top1_tokens)
        print(f"  Tokens compartilhados (pergunta ∩ top-1): {len(shared_tokens_top1)}")
        print(f"    {shared_tokens_top1}")
    
    # 4. Análise do tokenizador TF-IDF
    print(f"\n  Tokenizador TF-IDF atual:")
    print(f"    token_pattern: {store.vectorizer.token_pattern}")
    print(f"    ngram_range: {store.vectorizer.ngram_range}")
    print(f"    Vocabulário size: {len(store.vectorizer.vocabulary_)}")
    
    # Verifica se "β" está no vocabulário
    vocab = store.vectorizer.vocabulary_
    print(f"  'β' no vocabulário: {'SIM' if 'β' in vocab else 'NAO'}")
    print(f"  'C' no vocabulário: {'SIM' if 'c' in vocab else 'NAO'}")
    print(f"  'tcr' no vocabulário: {'SIM' if 'tcr' in vocab else 'NAO'}")
    print(f"  'coerência' no vocabulário: {'SIM' if 'coerência' in vocab else 'NAO'}")
    print(f"  'relacional' no vocabulário: {'SIM' if 'relacional' in vocab else 'NAO'}")
    
    # 5. Diagnóstico
    diagnosis = {
        'question_tokens_count': len(question_tokens),
        'question_math_symbols': math_symbols_q,
        'expected_chunk_id': expected_chunk.chunk_id if expected_chunks else 'NOT_FOUND',
        'expected_chunk_math_symbols': math_symbols_chunk if expected_chunks else [],
        'expected_chunk_tokens_count': len(chunk_tokens) if expected_chunks else 0,
        'shared_tokens_question_expected': len(shared_tokens) if expected_chunks else 0,
        'shared_math_symbols': list(shared_math) if expected_chunks else [],
        'top1_chunk_id': retrieved[0].chunk.chunk_id if retrieved else 'NONE',
        'top1_chunk_math_symbols': math_symbols_top1 if retrieved else [],
        'top1_shared_tokens': len(shared_tokens_top1) if retrieved else 0,
        'tfidf_token_pattern': store.vectorizer.token_pattern,
        'tfidf_vocab_size': len(vocab),
        'beta_in_vocab': 'β' in vocab,
        'tcr_in_vocab': 'tcr' in vocab,
    }
    
    # Hipótese diagnóstica
    print(f"\n  >>> HIPÓTESE DIAGNÓSTICA:")
    if not shared_math and shared_tokens:
        print(f"    Símbolos matemáticos NÃO compartilhados → falha lexical específica")
        diagnosis['hypothesis'] = 'LEXICAL_MATH_SYMBOLS_NOT_TOKENIZED'
    elif len(shared_tokens) < 3:
        print(f"    Poucos tokens compartilhados → falha lexical geral")
        diagnosis['hypothesis'] = 'LEXICAL_GENERAL_FAILURE'
    else:
        print(f"    Tokens compartilhados suficientes mas chunk esperado não recuperado")
        print(f"    → possível problema de peso/normalização TF-IDF")
        diagnosis['hypothesis'] = 'TFIDF_WEIGHTING_ISSUE'
    
    return diagnosis


def main():
    print("=" * 70)
    print("AION Passo 6.2 — Resolução Experimental de B1")
    print("Etapas 6.2.0, 6.2.1, 6.2.2")
    print("=" * 70)
    
    # Etapa 6.2.0: Congelar baseline
    baseline = stage_6_2_0_freeze_baseline()
    
    # Reconstrói store com corpus v1.3.0 (igual ao 6.1-F)
    print(f"\n[SETUP] Reconstruindo TF-IDF store com corpus v1.3.0...")
    store = TfidfVectorStore()
    all_chunks = []
    
    for filename, meta in CORPUS_V13_FILES.items():
        path = meta['path']
        if not path.exists():
            continue
        md_text = path.read_text(encoding='utf-8')
        chunks = parse_extracted_markdown(md_text, meta['id'])
        store.add_chunks(chunks)
        all_chunks.extend(chunks)
    
    store.build_index()
    print(f"  Store: {len(store.chunks)} chunks, vocab size: {len(store.vectorizer.vocabulary_)}")
    
    # Inicializa validator
    validator = ProvenanceValidator(all_chunks)
    print(f"  Validator CORPUS_INDEX: {len(validator.corpus_index)} chunks")
    
    # Etapa 6.2.1: Reprodução determinística de B1 (3 runs)
    baseline_b1 = stage_6_2_1_reproduce_b1(store, validator, n_runs=3)
    
    # Etapa 6.2.2: Experimento A (Controle)
    experiment_A = stage_6_2_2_experiment_A_control(store, validator, baseline_b1)
    
    # Diagnóstico aprofundado
    diagnosis = diagnose_b1_root_cause(store)
    
    # Salvar relatório
    report = {
        'metadata': {
            'experiment': 'AION-6.2 Etapas 6.2.0, 6.2.1, 6.2.2',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'stage_6_2_0_baseline': baseline,
        'stage_6_2_1_b1_reproduction': baseline_b1,
        'stage_6_2_2_experiment_A_control': experiment_A,
        'diagnosis': diagnosis,
        'next_steps': [
            '6.2.3 — Experimento B: Normalização matemática',
            '6.2.4 — Experimento C: Chunking matemático',
            '6.2.5 — Experimento D: Tokenização matemática',
            '6.2.6 — Comparação estatística/diagnóstica',
            '6.2.7 — Rebenchmark B1-B7 da melhor intervenção',
            '6.2.8 — Veredito (RESOLVED / PARTIALLY RESOLVED / KNOWN LIMITATION)',
        ],
    }
    
    json_path = OUTPUT_DIR / 'aion_6_2_baseline_diagnosis.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    # Resumo
    print(f"\n{'=' * 70}")
    print("[RESUMO AION-6.2 Etapas 6.2.0-6.2.2]")
    print(f"{'=' * 70}")
    print(f"\nBaseline congelado:")
    print(f"  Corpus: v1.3.0 (9 registros)")
    print(f"  Chunks: {len(store.chunks)}")
    print(f"  Vocabulário TF-IDF: {len(store.vectorizer.vocabulary_)} termos")
    
    print(f"\nReprodução B1 (3 runs):")
    print(f"  Hits: {baseline_b1['hits']}/3")
    print(f"  Determinístico: {baseline_b1['deterministic']}")
    print(f"  Baseline B1: {baseline_b1['baseline_B1']}")
    
    print(f"\nDiagnóstico:")
    print(f"  Hipótese: {diagnosis['hypothesis']}")
    print(f"  Tokens compartilhados (pergunta ∩ chunk esperado): {diagnosis['shared_tokens_question_expected']}")
    print(f"  Símbolos matemáticos compartilhados: {diagnosis['shared_math_symbols']}")
    print(f"  'β' no vocabulário TF-IDF: {diagnosis['beta_in_vocab']}")
    print(f"  'tcr' no vocabulário TF-IDF: {diagnosis['tcr_in_vocab']}")
    
    return report


if __name__ == '__main__':
    main()
