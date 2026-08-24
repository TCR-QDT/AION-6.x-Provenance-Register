#!/usr/bin/env python3
"""
AION Passo 6.2.6 — Diagnóstico Top-k + Experimentos E, F, G, H

Etapa 1: Diagnóstico Top-k do baseline (distinguir retrieval vs ranking)
Etapa 2: Experimento E — Remoção de stopwords
Etapa 3: Experimento F — N-grams (unigram, bigram, unigram+bigram)
Etapa 4: Experimento G — Boost de termos raros/estruturais
Etapa 5: Experimento H — Reranking híbrido

NÃO altera: corpus v1.3.0, GraphRAG, P-RESP-001 v0.3, AION-EVAL-002 v0.2

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from aion_rag_proxy import TfidfVectorStore, parse_extracted_markdown, RetrievedChunk
from aion_bench_001 import BENCH_TESTS
from aion_6_1_f_rebenchmark_lcr import CORPUS_V13_FILES

OUTPUT_DIR = Path('/home/z/my-project/download/rag')


# === Stopwords para Experimento E ===

# Stopwords em português + inglês (manual, sem dependência externa)
STOPWORDS = {
    # Português
    'a', 'o', 'as', 'os', 'de', 'da', 'do', 'das', 'dos', 'e', 'ou', 'que', 'com',
    'para', 'por', 'no', 'na', 'nos', 'nas', 'um', 'uma', 'uns', 'umas',
    'é', 'são', 'foi', 'ser', 'seu', 'sua', 'seus', 'suas', 'ao', 'aos',
    'à', 'às', 'pelo', 'pela', 'pelos', 'pelas', 'este', 'esta', 'estes',
    'estas', 'esse', 'essa', 'esses', 'essas', 'isto', 'isso', 'aquilo',
    'em', 'se', 'mas', 'como', 'também', 'já', 'não', 'sim', 'mais', 'menos',
    'muito', 'muita', 'muitos', 'muitas', 'todo', 'toda', 'todos', 'todas',
    'qual', 'quais', 'qualquer', 'quaisquer', 'algum', 'alguma', 'alguns',
    'algumas', 'nenhum', 'nenhuma', 'outro', 'outra', 'outros', 'outras',
    'sobre', 'após', 'entre', 'até', 'desde', 'quando', 'onde', 'porque',
    # Inglês
    'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
    'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
    'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
    'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
    'why', 'how', 'a', 'an', 'and', 'or', 'but', 'if', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
    'from', 'up', 'in', 'out', 'on', 'off', 'over', 'under',
}


# === Função utilitária: construir chunks base ===

def build_base_chunks():
    all_chunks = []
    for filename, meta in CORPUS_V13_FILES.items():
        path = meta['path']
        if not path.exists():
            continue
        md_text = path.read_text(encoding='utf-8')
        chunks = parse_extracted_markdown(md_text, meta['id'])
        all_chunks.extend(chunks)
    return all_chunks


# === Etapa 1: Diagnóstico Top-k ===

def diagnose_top_k(store, question: str, expected_prefix: str, k_values=[1, 3, 5, 10, 20]) -> dict:
    """Diagnóstico Top-k: onde está o chunk esperado no ranking?"""
    print(f"\n  Diagnóstico Top-k para B1:")
    print(f"    Chunk esperado: {expected_prefix}*")
    
    # Recupera top-20 (ou máximo disponível)
    max_k = max(k_values)
    retrieved = store.query(question, top_k=max_k)
    
    results = {}
    found_at_rank = None
    
    for k in k_values:
        top_k_chunks = retrieved[:k]
        hit = any(r.chunk.chunk_id.startswith(expected_prefix) for r in top_k_chunks)
        results[k] = hit
        if hit and found_at_rank is None:
            for r in top_k_chunks:
                if r.chunk.chunk_id.startswith(expected_prefix):
                    found_at_rank = r.rank
                    break
    
    # Identifica qual chunk CORPUS-002 foi recuperado (se algum)
    corpus_002_chunks_retrieved = []
    for r in retrieved:
        if r.chunk.corpus_id == 'CORPUS-002':
            corpus_002_chunks_retrieved.append({
                'rank': r.rank,
                'chunk_id': r.chunk.chunk_id,
                'score': r.score,
            })
    
    print(f"  Resultado por k:")
    for k in k_values:
        hit_emoji = '✅' if results[k] else '❌'
        print(f"    Top-{k}: {hit_emoji}")
    
    if found_at_rank:
        print(f"  >>> Chunk CORPUS-002#p1 encontrado no rank #{found_at_rank}")
    else:
        print(f"  >>> Nenhum chunk CORPUS-002#p1 encontrado no Top-{max_k}")
        if corpus_002_chunks_retrieved:
            print(f"  >>> Mas outros chunks CORPUS-002 foram recuperados:")
            for c in corpus_002_chunks_retrieved[:5]:
                print(f"      #{c['rank']} score={c['score']:.4f} | {c['chunk_id']}")
    
    return {
        'question': question,
        'expected_prefix': expected_prefix,
        'hits_by_k': results,
        'found_at_rank': found_at_rank,
        'corpus_002_chunks_retrieved': corpus_002_chunks_retrieved,
        'top1': {
            'chunk_id': retrieved[0].chunk.chunk_id if retrieved else None,
            'score': retrieved[0].score if retrieved else None,
        },
        'top10_all': [{'rank': r.rank, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id} for r in retrieved[:10]],
    }


# === Experimento E — Stopwords ===

class ExperimentE_Store:
    """TF-IDF com stopword filtering."""
    
    def __init__(self, chunks: list):
        self.chunks = chunks
        
        self.vectorizer = TfidfVectorizer(
            max_features=4096,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            token_pattern=r'(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9_]+\b',
            stop_words=list(STOPWORDS),  # NOVO: stopword filtering
        )
        texts = [c.text for c in self.chunks]
        self.matrix = self.vectorizer.fit_transform(texts)
        print(f"  [Exp E] Vocabulário: {len(self.vectorizer.vocabulary_)} termos")
        print(f"  [Exp E] Stopwords aplicadas: {len(STOPWORDS)}")
    
    def query(self, question: str, top_k: int = 8):
        q_vec = self.vectorizer.transform([question])
        scores = cosine_similarity(q_vec, self.matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for rank, idx in enumerate(top_indices, 1):
            r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
            results.append(r)
        return results


# === Experimento F — N-grams ===

class ExperimentF_Store:
    """Testa diferentes n-gram ranges. Vamos testar (1,1) e (2,2) separadamente."""
    
    def __init__(self, chunks: list, ngram_range=(1, 1)):
        self.chunks = chunks
        self.ngram_range = ngram_range
        
        self.vectorizer = TfidfVectorizer(
            max_features=4096,
            ngram_range=ngram_range,
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            token_pattern=r'(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9_]+\b',
        )
        texts = [c.text for c in self.chunks]
        self.matrix = self.vectorizer.fit_transform(texts)
        print(f"  [Exp F] n-gram range: {ngram_range}")
        print(f"  [Exp F] Vocabulário: {len(self.vectorizer.vocabulary_)} termos")
        # Verificar se "métrica tcr" está no vocabulário (bigram)
        if ngram_range == (2, 2):
            print(f"  [Exp F] 'métrica tcr' no vocabulário: {'métrica tcr' in self.vectorizer.vocabulary_}")
            print(f"  [Exp F] 'fonte exata' no vocabulário: {'fonte exata' in self.vectorizer.vocabulary_}")
    
    def query(self, question: str, top_k: int = 8):
        q_vec = self.vectorizer.transform([question])
        scores = cosine_similarity(q_vec, self.matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for rank, idx in enumerate(top_indices, 1):
            r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
            results.append(r)
        return results


# === Experimento G — Boost de termos raros/estruturais ===

class ExperimentG_Store:
    """TF-IDF com boost em tokens estruturais (tokens com símbolos =, ^, _)."""
    
    def __init__(self, chunks: list):
        self.chunks = chunks
        
        # Primeiro: TF-IDF padrão
        self.vectorizer = TfidfVectorizer(
            max_features=4096,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            token_pattern=r'(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9_]+\b',
        )
        texts = [c.text for c in self.chunks]
        self.matrix = self.vectorizer.fit_transform(texts)
        
        # Identificar tokens estruturais raros (DF baixo = raros)
        df_array = (self.matrix > 0).sum(axis=0).A1  # Document Frequency
        n_docs = len(self.chunks)
        
        # Tokens estruturais: aqueles com DF <= 2 (aparecem em poucos chunks)
        # Boost de 3x nesses tokens
        boost_mask = np.where(df_array <= 2, 3.0, 1.0)
        
        # Aplicar boost na matriz TF-IDF
        self.matrix_boosted = self.matrix.multiply(boost_mask).tocsr()
        
        print(f"  [Exp G] Vocabulário: {len(self.vectorizer.vocabulary_)} termos")
        print(f"  [Exp G] Tokens com boost (DF<=2): {(df_array <= 2).sum()}")
        print(f"  [Exp G] Tokens sem boost (DF>2): {(df_array > 2).sum()}")
    
    def query(self, question: str, top_k: int = 8):
        # Query normal
        q_vec = self.vectorizer.transform([question])
        # Converter para denso para aplicar boost
        q_array = q_vec.toarray()[0]
        df_array = (self.matrix > 0).sum(axis=0).A1
        boost_mask = np.where(df_array <= 2, 3.0, 1.0)
        q_boosted = q_array * boost_mask

        # Matriz boosted em denso (apenas para a query — matriz permanece sparse)
        # Calcular scores manualmente com produto escalar + norma
        # scores[i] = (q_boosted · matrix[i]) / (||q_boosted|| * ||matrix[i]||)
        # Mas para simplicidade, usar cosine_similarity com q_boosted como matriz densa
        from scipy.sparse import csr_matrix
        q_boosted_sparse = csr_matrix(q_boosted.reshape(1, -1))

        # Re-calcular scores com matriz boosted
        scores = cosine_similarity(q_boosted_sparse, self.matrix_boosted).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for rank, idx in enumerate(top_indices, 1):
            r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
            results.append(r)
        return results


# === Experimento H — Reranking híbrido ===

class ExperimentH_Store:
    """TF-IDF + reranking lexical/estrutural nos top-k candidatos."""
    
    def __init__(self, chunks: list):
        self.chunks = chunks
        
        # TF-IDF base (igual ao controle)
        self.vectorizer = TfidfVectorizer(
            max_features=4096,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            token_pattern=r'(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9_]+\b',
        )
        texts = [c.text for c in self.chunks]
        self.matrix = self.vectorizer.fit_transform(texts)
        print(f"  [Exp H] Vocabulário: {len(self.vectorizer.vocabulary_)} termos")
        print(f"  [Exp H] Reranking: Boost por termos estruturais nos top-k")
    
    def query(self, question: str, top_k: int = 8):
        # Passo 1: Recuperar top-20 candidatos com TF-IDF
        q_vec = self.vectorizer.transform([question])
        scores = cosine_similarity(q_vec, self.matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:min(20, len(scores))]
        
        # Passo 2: Reranking lexical/estrutural
        # Boosta chunks que contêm símbolos matemáticos da pergunta
        # Extrair símbolos matemáticos da pergunta
        math_symbols_in_question = set(re.findall(r'[=×βΦαµν∂∇∑∏]', question))
        
        reranked = []
        for rank, idx in enumerate(top_indices, 1):
            chunk = self.chunks[idx]
            original_score = float(scores[idx])
            
            # Calcular boost baseado em símbolos matemáticos compartilhados
            chunk_math_symbols = set(re.findall(r'[=×βΦαµν∂∇∑∏]', chunk.text))
            shared_math = math_symbols_in_question & chunk_math_symbols
            boost = 1.0 + 0.1 * len(shared_math)  # 10% boost por símbolo compartilhado
            
            # Calcular boost baseado em presença de fórmula (padrão X = ...)
            has_formula = bool(re.search(r'[A-Za-zβΦαµν]\s*=\s*[\d.]', chunk.text))
            if has_formula:
                boost += 0.2  # 20% boost extra
            
            reranked_score = original_score * boost
            
            reranked.append({
                'idx': idx,
                'chunk': chunk,
                'original_score': original_score,
                'boost': boost,
                'reranked_score': reranked_score,
                'shared_math_symbols': list(shared_math),
            })
        
        # Ordenar por reranked_score
        reranked.sort(key=lambda x: x['reranked_score'], reverse=True)
        
        # Retornar top-k
        results = []
        for rank, item in enumerate(reranked[:top_k], 1):
            r = RetrievedChunk(chunk=item['chunk'], score=item['reranked_score'], rank=rank)
            results.append(r)
        
        # Log do reranking (apenas top-5)
        if top_k >= 5:
            print(f"  [Exp H] Top-5 após reranking:")
            for i, item in enumerate(reranked[:5]):
                print(f"    #{i+1} reranked={item['reranked_score']:.4f} (orig={item['original_score']:.4f}, boost={item['boost']:.2f}) | {item['chunk'].chunk_id} | shared_math={item['shared_math_symbols']}")
        
        return results


# === Avaliação de B1 para cada experimento ===

def evaluate_b1(store, experiment_name: str, n_runs: int = 3) -> dict:
    """Avalia B1 com top-k diagnóstico."""
    test = BENCH_TESTS['B1']
    expected_prefix = 'CORPUS-002#p1'
    
    # Diagnóstico Top-k no primeiro run
    print(f"\n  Diagnóstico Top-k para {experiment_name}:")
    diagnosis = diagnose_top_k(store, test['pergunta'], expected_prefix, k_values=[1, 3, 5, 10, 20])
    
    # 3 runs para verificar determinismo
    runs = []
    for run_idx in range(1, n_runs + 1):
        retrieved = store.query(test['pergunta'], top_k=8)
        top3 = [{'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score} for i, r in enumerate(retrieved[:3])]
        hit_top3 = any(r['chunk_id'].startswith(expected_prefix) for r in top3)
        runs.append({
            'run_idx': run_idx,
            'top3_chunks': top3,
            'hit_top3': hit_top3,
        })
        if run_idx == 1:
            print(f"  Run 1 top-3:")
            for r in top3:
                marker = '✅' if r['chunk_id'].startswith(expected_prefix) else '  '
                print(f"    {marker} #{r['rank']} score={r['score']:.4f} | {r['chunk_id']}")
    
    hits = sum(1 for r in runs if r['hit_top3'])
    top3_sets = [tuple(r['chunk_id'] for r in run['top3_chunks']) for run in runs]
    deterministic = all(s == top3_sets[0] for s in top3_sets)
    
    return {
        'experiment': experiment_name,
        'top_k_diagnosis': diagnosis,
        'runs': runs,
        'hits_top3': hits,
        'retrieval_hit_rate': hits / n_runs,
        'deterministic': deterministic,
        'B1_status': 'PASS' if hits == n_runs else ('PARTIAL' if hits > 0 else 'FAIL-SYSTEM'),
    }


def main():
    print("=" * 70)
    print("AION Passo 6.2.6 — Diagnóstico Top-k + Experimentos E, F, G, H")
    print("=" * 70)
    
    # Constrói chunks base
    print("\n[SETUP] Construindo chunks base do corpus v1.3.0...")
    base_chunks = build_base_chunks()
    print(f"  Base chunks: {len(base_chunks)}")
    
    # === DIAGNÓSTICO TOP-K DO CONTROLE (baseline) ===
    print(f"\n{'=' * 70}")
    print("[DIAGNÓSTICO TOP-K — Baseline (Controle)]")
    print(f"{'=' * 70}")
    
    # Reconstrói store controle
    control_store = TfidfVectorStore()
    control_store.add_chunks(base_chunks)
    control_store.build_index()
    
    control_diagnosis = evaluate_b1(control_store, 'A (Controle) - Top-k', n_runs=3)
    
    # === EXPERIMENTO E — STOPWORDS ===
    print(f"\n{'=' * 70}")
    print("[6.2.6.E] EXPERIMENTO E — Remoção de stopwords")
    print(f"{'=' * 70}")
    
    exp_e_store = ExperimentE_Store(base_chunks)
    exp_e_result = evaluate_b1(exp_e_store, 'E (Stopwords)', n_runs=3)
    
    print(f"\n  Resultado E:")
    print(f"    Hits top-3: {exp_e_result['hits_top3']}/3")
    print(f"    B1: {exp_e_result['B1_status']}")
    
    # === EXPERIMENTO F1 — UNIGRAM ===
    print(f"\n{'=' * 70}")
    print("[6.2.6.F1] EXPERIMENTO F1 — Unigram apenas (n-gram range (1,1))")
    print(f"{'=' * 70}")
    
    exp_f1_store = ExperimentF_Store(base_chunks, ngram_range=(1, 1))
    exp_f1_result = evaluate_b1(exp_f1_store, 'F1 (Unigram)', n_runs=3)
    
    print(f"\n  Resultado F1:")
    print(f"    Hits top-3: {exp_f1_result['hits_top3']}/3")
    print(f"    B1: {exp_f1_result['B1_status']}")
    
    # === EXPERIMENTO F2 — BIGRAM ===
    print(f"\n{'=' * 70}")
    print("[6.2.6.F2] EXPERIMENTO F2 — Bigram apenas (n-gram range (2,2))")
    print(f"{'=' * 70}")
    
    exp_f2_store = ExperimentF_Store(base_chunks, ngram_range=(2, 2))
    exp_f2_result = evaluate_b1(exp_f2_store, 'F2 (Bigram)', n_runs=3)
    
    print(f"\n  Resultado F2:")
    print(f"    Hits top-3: {exp_f2_result['hits_top3']}/3")
    print(f"    B1: {exp_f2_result['B1_status']}")
    
    # === EXPERIMENTO G — BOOST ESTRUTURAL ===
    print(f"\n{'=' * 70}")
    print("[6.2.6.G] EXPERIMENTO G — Boost de termos raros/estruturais")
    print(f"{'=' * 70}")
    
    exp_g_store = ExperimentG_Store(base_chunks)
    exp_g_result = evaluate_b1(exp_g_store, 'G (Boost estrutural)', n_runs=3)
    
    print(f"\n  Resultado G:")
    print(f"    Hits top-3: {exp_g_result['hits_top3']}/3")
    print(f"    B1: {exp_g_result['B1_status']}")
    
    # === EXPERIMENTO H — RERANKING HÍBRIDO ===
    print(f"\n{'=' * 70}")
    print("[6.2.6.H] EXPERIMENTO H — Reranking híbrido")
    print(f"{'=' * 70}")
    
    exp_h_store = ExperimentH_Store(base_chunks)
    exp_h_result = evaluate_b1(exp_h_store, 'H (Reranking)', n_runs=3)
    
    print(f"\n  Resultado H:")
    print(f"    Hits top-3: {exp_h_result['hits_top3']}/3")
    print(f"    B1: {exp_h_result['B1_status']}")
    
    # === COMPARAÇÃO COMPLETA A/B/C/D/E/F1/F2/G/H ===
    print(f"\n{'=' * 70}")
    print("[COMPARAÇÃO COMPLETA — Todos os experimentos]")
    print(f"{'=' * 70}")
    
    # Carrega resultados anteriores (A, B, C, D)
    bcd_path = OUTPUT_DIR / 'aion_6_2_experiments_bcd.json'
    bcd_data = json.loads(bcd_path.read_text(encoding='utf-8'))
    
    comparison = {
        'A (Controle)': {
            'intervention': 'TF-IDF atual',
            'hits_top3': bcd_data['comparison']['A (Controle)']['hits_top3'],
            'B1_status': bcd_data['comparison']['A (Controle)']['B1_status'],
            'top_k_diagnosis': control_diagnosis['top_k_diagnosis'],
        },
        'B (Normalização)': {
            'intervention': 'Normalização matemática',
            'hits_top3': bcd_data['comparison']['B (Normalização)']['hits_top3'],
            'B1_status': bcd_data['comparison']['B (Normalização)']['B1_status'],
        },
        'C (Chunking)': {
            'intervention': 'Chunking matemático',
            'hits_top3': bcd_data['comparison']['C (Chunking)']['hits_top3'],
            'B1_status': bcd_data['comparison']['C (Chunking)']['B1_status'],
        },
        'D (Tokenização)': {
            'intervention': 'Token_pattern estendido',
            'hits_top3': bcd_data['comparison']['D (Tokenização)']['hits_top3'],
            'B1_status': bcd_data['comparison']['D (Tokenização)']['B1_status'],
        },
        'E (Stopwords)': {
            'intervention': 'Stopword filtering',
            'hits_top3': exp_e_result['hits_top3'],
            'B1_status': exp_e_result['B1_status'],
            'top_k_diagnosis': exp_e_result['top_k_diagnosis'],
        },
        'F1 (Unigram)': {
            'intervention': 'n-gram (1,1)',
            'hits_top3': exp_f1_result['hits_top3'],
            'B1_status': exp_f1_result['B1_status'],
            'top_k_diagnosis': exp_f1_result['top_k_diagnosis'],
        },
        'F2 (Bigram)': {
            'intervention': 'n-gram (2,2)',
            'hits_top3': exp_f2_result['hits_top3'],
            'B1_status': exp_f2_result['B1_status'],
            'top_k_diagnosis': exp_f2_result['top_k_diagnosis'],
        },
        'G (Boost)': {
            'intervention': 'Boost de termos raros',
            'hits_top3': exp_g_result['hits_top3'],
            'B1_status': exp_g_result['B1_status'],
            'top_k_diagnosis': exp_g_result['top_k_diagnosis'],
        },
        'H (Reranking)': {
            'intervention': 'Reranking híbrido',
            'hits_top3': exp_h_result['hits_top3'],
            'B1_status': exp_h_result['B1_status'],
            'top_k_diagnosis': exp_h_result['top_k_diagnosis'],
        },
    }
    
    print(f"\n{'Braço':<22} {'Intervention':<35} {'Hits':<8} {'B1':<15} {'Top-k diagnosis'}")
    print('-' * 110)
    for arm, data in comparison.items():
        hits = data['hits_top3']
        hits_str = f"{hits}/3"
        b1 = data['B1_status']
        
        # Top-k diagnosis (se disponível)
        if 'top_k_diagnosis' in data:
            diag = data['top_k_diagnosis']
            hits_by_k = diag['hits_by_k']
            k_str = ""
            for k in [1, 3, 5, 10, 20]:
                hit = hits_by_k.get(k, '?')
                k_str += f"{'✅' if hit else '❌' if hit is False else '?'}"
            if diag['found_at_rank']:
                k_str += f" (rank #{diag['found_at_rank']})"
        else:
            k_str = "N/A"
        
        print(f"{arm:<22} {data['intervention'][:33]:<35} {hits_str:<8} {b1:<15} {k_str}")
    
    # Identificar melhor braço
    best_arm = max(comparison.items(), key=lambda x: x[1]['hits_top3'])
    print(f"\n  Melhor braço: {best_arm[0]} ({best_arm[1]['hits_top3']}/3 hits)")
    
    # Análise do diagnóstico Top-k
    print(f"\n  Análise Top-k (onde está CORPUS-002#p1?):")
    for arm in ['A (Controle)', 'E (Stopwords)', 'F1 (Unigram)', 'F2 (Bigram)', 'G (Boost)', 'H (Reranking)']:
        if 'top_k_diagnosis' in comparison[arm]:
            diag = comparison[arm]['top_k_diagnosis']
            print(f"    {arm}:")
            for k in [1, 3, 5, 10, 20]:
                hit = diag['hits_by_k'].get(k, False)
                print(f"      Top-{k}: {'✅' if hit else '❌'}")
            if diag['found_at_rank']:
                print(f"      >>> Encontrado no rank #{diag['found_at_rank']}")
            else:
                print(f"      >>> NÃO encontrado em Top-20")
                if diag['corpus_002_chunks_retrieved']:
                    print(f"      >>> Mas outros chunks CORPUS-002 recuperados:")
                    for c in diag['corpus_002_chunks_retrieved'][:3]:
                        print(f"          #{c['rank']} score={c['score']:.4f} | {c['chunk_id']}")
    
    # Salvar relatório completo
    report = {
        'metadata': {
            'experiment': 'AION-6.2.6 — Diagnóstico Top-k + Experimentos E, F, G, H',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'control_top_k_diagnosis': control_diagnosis,
        'experiment_E_stopwords': exp_e_result,
        'experiment_F1_unigram': exp_f1_result,
        'experiment_F2_bigram': exp_f2_result,
        'experiment_G_boost': exp_g_result,
        'experiment_H_reranking': exp_h_result,
        'comparison_all': comparison,
        'best_arm': {
            'name': best_arm[0],
            'data': best_arm[1],
        },
    }
    
    json_path = OUTPUT_DIR / 'aion_6_2_6_diagnosis_top_k_efgh.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
