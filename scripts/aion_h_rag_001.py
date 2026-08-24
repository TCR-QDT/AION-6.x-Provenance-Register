#!/usr/bin/env python3
"""
AION Passo 5.12 — Experimento H-RAG-001 (Retrieval Semântico)

Teste controlado: substitui apenas o retrieval TF-IDF por embeddings semânticos,
mantendo todo o resto (chunking, GraphRAG, LLM) idêntico ao Sistema A.

H-RAG-001: embeddings semânticos melhoram a recuperação do documento-fonte 
correto para B1, mantendo ou melhorando o desempenho dos demais testes.

Regra de não-regressão: B1_embedding > B1_tfidf E perf_global_embedding >= perf_global_tfidf

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.local/lib/python3.12/site-packages')

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from aion_rag_proxy import CORPUS_FILES, CORPUS_DIR, parse_extracted_markdown
from aion_bench_001 import BENCH_TESTS, generate_answer_via_llm
from aion_bench_001_eval002 import evaluate_with_eval002

OUTPUT_DIR = Path('/home/z/my-project/download/rag')

# Modelo de embedding semântico (leve para ambiente sem GPU)
EMBEDDING_MODEL = 'paraphrase-MiniLM-L3-v2'  # 384 dims, ~120MB


class SemanticVectorStore:
    """Vector store baseado em embeddings semânticos (substituto do TfidfVectorStore)."""
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        print(f"  [Embedding] Carregando modelo {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.chunks = []
        self.embeddings = None
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"  [Embedding] Modelo carregado. Dim={self.embedding_dim}")
    
    def add_chunks(self, chunks):
        self.chunks.extend(chunks)
    
    def build_index(self):
        """Constrói índice de embeddings."""
        if not self.chunks:
            raise ValueError("Nenhum chunk para indexar")
        
        texts = [c.text for c in self.chunks]
        print(f"  [Embedding] Gerando embeddings para {len(texts)} chunks...")
        self.embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,  # para cosine similarity = dot product
        )
        print(f"  [Embedding] Índice construído. Shape: {self.embeddings.shape}")
    
    def query(self, question: str, top_k: int = 5):
        """Retorna top_k chunks mais similares à pergunta."""
        if self.embeddings is None:
            raise RuntimeError("Índice não construído")
        
        q_emb = self.model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        # cosine similarity (com normalize=True, é equivalente a dot product)
        scores = (self.embeddings @ q_emb.T).flatten()
        
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for rank, idx in enumerate(top_indices, 1):
            chunk = self.chunks[idx]
            # Emula RetrievedChunk interface
            class RetrievedChunk:
                pass
            r = RetrievedChunk()
            r.chunk = chunk
            r.score = float(scores[idx])
            r.rank = rank
            results.append(r)
        return results
    
    def save_state(self, path):
        np.save(path, self.embeddings)
        # Salva também chunks
        chunks_data = [c.chunk_id for c in self.chunks]
        Path(str(path) + '.meta.json').write_text(
            json.dumps({
                'embedding_dim': self.embedding_dim,
                'chunk_count': len(self.chunks),
                'chunk_ids': chunks_data,
                'model': EMBEDDING_MODEL,
            }, indent=2),
            encoding='utf-8'
        )


def rebuild_semantic_store():
    """Reconstrói store semântico a partir dos chunks."""
    store = SemanticVectorStore()
    all_chunks = []
    for filename, meta in CORPUS_FILES.items():
        path = CORPUS_DIR / filename
        if not path.exists():
            continue
        md_text = path.read_text(encoding='utf-8')
        chunks = parse_extracted_markdown(md_text, meta['id'])
        store.add_chunks(chunks)
        all_chunks.extend(chunks)
    store.build_index()
    return store, all_chunks


def run_bench_sistema_B(store) -> dict:
    """Executa bench B1-B7 no Sistema B (embeddings semânticos)."""
    results = {}
    
    for test_id, test in BENCH_TESTS.items():
        print(f"\n{'=' * 60}")
        print(f"[{test_id}] ({test['categoria']}) — Sistema B (Embeddings)")
        print(f"{'=' * 60}")
        print(f"PERGUNTA: {test['pergunta'][:200]}...")
        
        # Retrieval via embeddings semânticos
        retrieved = store.query(test['pergunta'], top_k=8)
        
        # Adiciona contexto temporal/memória negativa para B2, B6 (mesmo Sistema A)
        system_extra = ""
        if test_id == 'B2':
            temporal_data = json.loads((OUTPUT_DIR / 'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
            temporal_context = json.dumps(temporal_data['states'][:5], ensure_ascii=False, indent=2)[:2000]
            system_extra = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{temporal_context}"
        elif test_id == 'B6':
            hist_data = json.loads((OUTPUT_DIR / 'aion_hist_001_reconciliacao.json').read_text(encoding='utf-8'))
            negative_context = json.dumps(hist_data['negative_memory']['DESCONHECIDO'], ensure_ascii=False, indent=2)[:2000]
            system_extra = f"\n\nMEMÓRIA NEGATIVA (perguntas não respondíveis):\n{negative_context}"
        
        # Geração (mesmo LLM, mesmo prompt do Sistema A)
        t_start = time.time()
        answer, _ = generate_answer_via_llm(test['pergunta'], retrieved[:5], system_extra)
        t_elapsed = time.time() - t_start
        
        print(f"\nRESPOSTA ({t_elapsed:.1f}s):")
        print(answer[:1500] + ("..." if len(answer) > 1500 else ""))
        
        # Limpa resposta (remove prefixos do z-ai CLI)
        answer_clean = answer
        if '🚀' in answer:
            try:
                json_start = answer.find('{')
                if json_start >= 0:
                    json_str = answer[json_start:]
                    data = json.loads(json_str)
                    answer_clean = data['choices'][0]['message']['content']
            except:
                pass
        
        # Avaliação com AION-EVAL-002 (mesmo protocolo)
        retrieved_for_eval = [
            {
                'rank': i + 1,
                'chunk_id': r.chunk.chunk_id,
                'score': r.score,
                'corpus_id': r.chunk.corpus_id,
            } for i, r in enumerate(retrieved)
        ]
        eval_result = evaluate_with_eval002(test_id, retrieved_for_eval, answer_clean, test['gabarito'])
        
        print(f"\nAVALIAÇÃO (EVAL-002): {eval_result['avaliacao_final']}")
        for cat, cat_result in eval_result['categories'].items():
            print(f"  {cat}: {cat_result['status']:<18} — {cat_result['reason'][:80]}")
        
        results[test_id] = {
            'test_id': test_id,
            'categoria': test['categoria'],
            'pergunta': test['pergunta'],
            'resposta': answer_clean,
            'tempo_segundos': round(t_elapsed, 2),
            'retrieved_chunks_count': len(retrieved),
            'retrieved_chunks_top5': retrieved_for_eval[:5],
            'eval_002': eval_result,
            'gabarito': test['gabarito'],
            'sistema': 'B (embeddings semânticos)',
        }
    
    return results


def compute_comparative_matrix(results_A_path: Path, results_B: dict) -> dict:
    """Computa matriz comparativa A vs B com regra de não-regressão."""
    results_A = json.loads(results_A_path.read_text(encoding='utf-8'))
    
    matrix = {
        'criterios': [
            'B1 (Proveniência — crítico)',
            'B2 (Temporalidade)',
            'B3 (Revogação)',
            'B4 (Ausência)',
            'B5 (Contradição)',
            'B6 (Lacuna)',
            'B7 (Síntese)',
            'PASS count (estrito + semântico)',
            'PASS estrito',
            'PARTIAL count',
            'FAIL count',
            'Latência média (s)',
        ],
        'sistema_A_tfidf': {},
        'sistema_B_embedding': {},
    }
    
    # Reavalia Sistema A com EVAL-002 também (consistência)
    eval002_A_path = OUTPUT_DIR / 'aion_bench_001_eval002_resultados.json'
    eval002_A = json.loads(eval002_A_path.read_text(encoding='utf-8'))
    
    pass_count_A = sum(1 for r in eval002_A['results'].values() 
                       if r['eval_002']['avaliacao_final'] in ('PASS', 'PASS-SEMANTIC'))
    pass_strict_A = sum(1 for r in eval002_A['results'].values() 
                        if r['eval_002']['avaliacao_final'] == 'PASS')
    partial_A = sum(1 for r in eval002_A['results'].values() 
                    if r['eval_002']['avaliacao_final'] == 'PARTIAL')
    fail_A = sum(1 for r in eval002_A['results'].values() 
                 if r['eval_002']['avaliacao_final'] == 'FAIL')
    
    pass_count_B = sum(1 for r in results_B.values() 
                       if r['eval_002']['avaliacao_final'] in ('PASS', 'PASS-SEMANTIC'))
    pass_strict_B = sum(1 for r in results_B.values() 
                        if r['eval_002']['avaliacao_final'] == 'PASS')
    partial_B = sum(1 for r in results_B.values() 
                    if r['eval_002']['avaliacao_final'] == 'PARTIAL')
    fail_B = sum(1 for r in results_B.values() 
                 if r['eval_002']['avaliacao_final'] == 'FAIL')
    
    # Latências
    latency_A = sum(r['tempo_segundos'] for r in results_A['sistema_A']['results'].values()) / 7
    latency_B = sum(r['tempo_segundos'] for r in results_B.values()) / 7
    
    for tid in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        cat_name = next(t['categoria'] for k, t in BENCH_TESTS.items() if k == tid)
        # Encontra a categoria correspondente para A e B
        a_result = eval002_A['results'][tid]['eval_002']['avaliacao_final']
        b_result = results_B[tid]['eval_002']['avaliacao_final']
        
        # Converte para emoji para visualização
        emoji = lambda r: {'PASS': '✅', 'PASS-SEMANTIC': '🟡', 'PARTIAL': '⚠️', 'FAIL': '❌'}.get(r, '?')
        matrix['sistema_A_tfidf'][f'{tid} ({cat_name})'] = f"{emoji(a_result)} {a_result}"
        matrix['sistema_B_embedding'][f'{tid} ({cat_name})'] = f"{emoji(b_result)} {b_result}"
    
    matrix['sistema_A_tfidf']['PASS count (estrito + semântico)'] = f"{pass_count_A}/7"
    matrix['sistema_B_embedding']['PASS count (estrito + semântico)'] = f"{pass_count_B}/7"
    
    matrix['sistema_A_tfidf']['PASS estrito'] = f"{pass_strict_A}/7"
    matrix['sistema_B_embedding']['PASS estrito'] = f"{pass_strict_B}/7"
    
    matrix['sistema_A_tfidf']['PARTIAL count'] = f"{partial_A}/7"
    matrix['sistema_B_embedding']['PARTIAL count'] = f"{partial_B}/7"
    
    matrix['sistema_A_tfidf']['FAIL count'] = f"{fail_A}/7"
    matrix['sistema_B_embedding']['FAIL count'] = f"{fail_B}/7"
    
    matrix['sistema_A_tfidf']['Latência média (s)'] = f"{latency_A:.1f}s"
    matrix['sistema_B_embedding']['Latência média (s)'] = f"{latency_B:.1f}s"
    
    # Avaliação da regra de não-regressão
    b1_A = eval002_A['results']['B1']['eval_002']['avaliacao_final']
    b1_B = results_B['B1']['eval_002']['avaliacao_final']
    
    # Critério 1: B1_embedding > B1_tfidf
    b1_improved = False
    if b1_B in ('PASS', 'PASS-SEMANTIC') and b1_A == 'FAIL':
        b1_improved = True
    elif b1_B == 'PASS' and b1_A in ('PASS-SEMANTIC', 'PARTIAL'):
        b1_improved = True
    
    # Critério 2: perf_global_embedding >= perf_global_tfidf
    # Não pode haver regressões em testes que passavam
    regressions = []
    for tid in ['B2', 'B3', 'B4', 'B5', 'B7']:  # B6 era PARTIAL no Sistema A
        a_status = eval002_A['results'][tid]['eval_002']['avaliacao_final']
        b_status = results_B[tid]['eval_002']['avaliacao_final']
        
        # Hierarquia: PASS > PASS-SEMANTIC > PARTIAL > FAIL
        hierarchy = {'PASS': 4, 'PASS-SEMANTIC': 3, 'PARTIAL': 2, 'FAIL': 1}
        if hierarchy.get(b_status, 0) < hierarchy.get(a_status, 0):
            regressions.append({
                'test': tid,
                'tfidf_status': a_status,
                'embedding_status': b_status,
            })
    
    no_regression = len(regressions) == 0
    
    # Classificação do veredito
    if b1_improved and no_regression:
        verdict = 'CASO A — Embeddings vencem'
        decision = 'INCORPORAR embeddings ao AION'
    elif b1_improved and regressions:
        verdict = 'CASO C — Regressão'
        decision = 'REJEITAR substituição (embeddings causaram regressões)'
    elif not b1_improved and no_regression and pass_count_B >= pass_count_A:
        verdict = 'CASO B — Empate'
        decision = 'MANTER TF-IDF por enquanto (sem melhoria significativa)'
    elif not b1_improved and not no_regression:
        verdict = 'CASO C — Regressão + B1 não melhorou'
        decision = 'REJEITAR substituição'
    else:
        verdict = 'CASO B — Empate'
        decision = 'MANTER TF-IDF'
    
    return {
        'matrix': matrix,
        'b1_status_A': b1_A,
        'b1_status_B': b1_B,
        'b1_improved': b1_improved,
        'regressions': regressions,
        'no_regression': no_regression,
        'pass_count_A': pass_count_A,
        'pass_count_B': pass_count_B,
        'verdict': verdict,
        'decision': decision,
    }


def main():
    print("=" * 70)
    print("AION Passo 5.12 — H-RAG-001 (Retrieval Semântico)")
    print("Experimento controlado: TF-IDF vs Embeddings")
    print("=" * 70)
    
    # Reconstrói store semântico
    print("\n[SISTEMA B] Construindo índice semântico...")
    store, all_chunks = rebuild_semantic_store()
    
    # Executa bench no Sistema B
    print("\n[SISTEMA B] Executando B1-B7...")
    results_B = run_bench_sistema_B(store)
    
    # Computa matriz comparativa
    print("\n[MATRIZ COMPARATIVA A vs B]")
    results_A_path = OUTPUT_DIR / 'aion_bench_001_resultados.json'
    comparison = compute_comparative_matrix(results_A_path, results_B)
    
    for crit in comparison['matrix']['criterios']:
        a = comparison['matrix']['sistema_A_tfidf'].get(crit, 'N/A')
        b = comparison['matrix']['sistema_B_embedding'].get(crit, 'N/A')
        print(f"  {crit:<40} A: {a:<25} B: {b}")
    
    print(f"\n[VEREDITO]")
    print(f"  B1 status A (TF-IDF):     {comparison['b1_status_A']}")
    print(f"  B1 status B (Embedding):  {comparison['b1_status_B']}")
    print(f"  B1 melhorou:              {comparison['b1_improved']}")
    print(f"  Regressões:               {len(comparison['regressions'])}")
    if comparison['regressions']:
        for reg in comparison['regressions']:
            print(f"    ⚠️ {reg['test']}: {reg['tfidf_status']} → {reg['embedding_status']}")
    print(f"  Sem regressões:           {comparison['no_regression']}")
    print(f"  PASS count A: {comparison['pass_count_A']}/7  →  B: {comparison['pass_count_B']}/7")
    print(f"\n  >>> {comparison['verdict']}")
    print(f"  >>> {comparison['decision']}")
    
    # Salva relatório completo
    report = {
        'metadata': {
            'experiment': 'H-RAG-001',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
            'protocol': 'AION-EVAL-002 v1.0.0',
        },
        'hipotese': 'Embeddings semânticos melhoram a recuperação do documento-fonte correto para B1, mantendo ou melhorando o desempenho dos demais testes.',
        'regra_nao_regressao': 'B1_embedding > B1_tfidf E perf_global_embedding >= perf_global_tfidf',
        'sistema_A': {
            'description': 'TF-IDF (sklearn) + GraphRAG + LLM z-ai',
            'results_source': 'aion_bench_001_resultados.json + aion_bench_001_eval002_resultados.json',
        },
        'sistema_B': {
            'description': f'Embeddings semânticos ({EMBEDDING_MODEL}, {store.embedding_dim} dims) + GraphRAG + LLM z-ai',
            'results': results_B,
        },
        'comparison': comparison,
        'verdict': comparison['verdict'],
        'decision': comparison['decision'],
    }
    
    json_path = OUTPUT_DIR / 'aion_h_rag_001_resultados.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
