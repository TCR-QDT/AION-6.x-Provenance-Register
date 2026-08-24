#!/usr/bin/env python3
"""
AION Passo 5.12.1 — AION-B1-DIAG-001

Auditoria diagnóstica de B1: testa se o gargalo é retrieval capability 
ou query formulation. Não altera arquitetura, não altera modelo de avaliação.

3 variantes de consulta × 2 retrievers = 6 condições experimentais.
Apenas análise de retrieval (sem geração de resposta, sem LLM).

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, '/home/z/my-project/scripts')
# sentence-transformers + transformers instalados em paths específicos
for p in [
    '/home/z/.venv/lib/python3.12/site-packages',
    '/home/z/.local/lib/python3.12/site-packages',
]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Verifica imports críticos
try:
    import torch
    print(f"  [Setup] torch {torch.__version__} OK")
except ImportError:
    print("  [Setup] torch NÃO disponível")
try:
    import transformers
    print(f"  [Setup] transformers {transformers.__version__} OK")
except ImportError:
    print("  [Setup] transformers NÃO disponível")

from aion_rag_proxy import (
    TfidfVectorStore, CORPUS_FILES, CORPUS_DIR, parse_extracted_markdown
)
from aion_h_rag_001 import SemanticVectorStore

OUTPUT_DIR = Path('/home/z/my-project/download/rag')

# === 3 variantes da pergunta B1 ===

B1_VARIANTS = {
    'Q1_natural': {
        'descricao': 'Pergunta original do benchmark (formulação natural)',
        'pergunta': "Qual é a fonte exata da afirmação de que a métrica TCR é C = I × S × H^β?",
        'hipotese': 'Testa capacidade do retriever de mapear pergunta natural ao chunk correto',
    },
    'Q2_enriquecida': {
        'descricao': 'Pergunta lexicalmente enriquecida com termos do domínio',
        'pergunta': "Qual é a fonte documental exata da definição da métrica TCR (Teoria da Coerência Relacional), que combina integração I, simetria S e entropia espectral H com expoente β?",
        'hipotese': 'Testa se sinais lexicais adicionais melhoram retrieval',
    },
    'Q3_explicita': {
        'descricao': 'Pergunta contendo explicitamente a fórmula/termo técnico',
        'pergunta': "Qual documento define textualmente a métrica C = I × S × H^β com β calibrado via LOOCV? Procure pela fórmula exata.",
        'hipotese': 'Testa se presença explícita da fórmula resolve retrieval',
    },
}

# Critério de sucesso do retrieval: chunk esperado deve estar no top-3
EXPECTED_CHUNK_PREFIX = 'CORPUS-002#p1'  # Paper A, p.1, Abstract
EXPECTED_DOC = 'CORPUS-002'

# Adicionalmente, chunks aceitáveis (também definem a métrica TCR)
ACCEPTABLE_CHUNKS = [
    'CORPUS-002#p1_01',  # Abstract, p.1
    'CORPUS-002#p2_01',  # Sec. II, p.2 (Eq. 2 - mesma fórmula)
    'CORPUS-005#chunk_001',  # Cover Letter (também menciona a fórmula, mas é rascunho aspiracional)
]


def evaluate_retrieval(retrieved: list, query_id: str) -> dict:
    """Avalia se o chunk esperado foi recuperado."""
    expected_in_top3 = False
    expected_in_top5 = False
    expected_rank = None
    acceptable_in_top3 = False
    acceptable_rank = None
    
    for r in retrieved:
        chunk_id = r.get('chunk_id', '') if isinstance(r, dict) else r.chunk.chunk_id
        rank = r.get('rank', 0) if isinstance(r, dict) else r.rank
        
        if chunk_id.startswith(EXPECTED_CHUNK_PREFIX):
            if rank <= 3:
                expected_in_top3 = True
            if rank <= 5:
                expected_in_top5 = True
            expected_rank = rank
            break
        
        for acceptable in ACCEPTABLE_CHUNKS:
            if chunk_id.startswith(acceptable.split('#')[0]) and chunk_id == acceptable:
                if rank <= 3:
                    acceptable_in_top3 = True
                acceptable_rank = rank
                break
    
    return {
        'expected_in_top3': expected_in_top3,
        'expected_in_top5': expected_in_top5,
        'expected_rank': expected_rank,
        'acceptable_in_top3': acceptable_in_top3,
        'acceptable_rank': acceptable_rank,
        'pass': expected_in_top3,
    }


def run_retrieval_diagnostic(store_tfidf, store_embedding) -> dict:
    """Executa 6 condições experimentais (3 queries × 2 retrievers)."""
    results = {}
    
    for query_id, query_data in B1_VARIANTS.items():
        pergunta = query_data['pergunta']
        print(f"\n[{query_id}] {query_data['descricao']}")
        print(f"  Pergunta: {pergunta[:120]}...")
        
        # TF-IDF
        retrieved_tfidf = store_tfidf.query(pergunta, top_k=8)
        tfidf_for_eval = [
            {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
            for i, r in enumerate(retrieved_tfidf)
        ]
        eval_tfidf = evaluate_retrieval(tfidf_for_eval, query_id)
        
        # Embedding
        retrieved_emb = store_embedding.query(pergunta, top_k=8)
        emb_for_eval = [
            {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
            for i, r in enumerate(retrieved_emb)
        ]
        eval_emb = evaluate_retrieval(emb_for_eval, query_id)
        
        print(f"  TF-IDF top-3:")
        for r in tfidf_for_eval[:3]:
            marker = '✅' if r['chunk_id'].startswith(EXPECTED_CHUNK_PREFIX) else '  '
            print(f"    {marker} #{r['rank']} score={r['score']:.4f} | {r['chunk_id']:<30} | {r['corpus_id']}")
        print(f"    Resultado: {'PASS' if eval_tfidf['pass'] else 'FAIL'} (rank esperado: {eval_tfidf['expected_rank']})")
        
        print(f"  Embedding top-3:")
        for r in emb_for_eval[:3]:
            marker = '✅' if r['chunk_id'].startswith(EXPECTED_CHUNK_PREFIX) else '  '
            print(f"    {marker} #{r['rank']} score={r['score']:.4f} | {r['chunk_id']:<30} | {r['corpus_id']}")
        print(f"    Resultado: {'PASS' if eval_emb['pass'] else 'FAIL'} (rank esperado: {eval_emb['expected_rank']})")
        
        results[query_id] = {
            'descricao': query_data['descricao'],
            'pergunta': pergunta,
            'hipotese': query_data['hipotese'],
            'tfidf': {
                'retrieved': tfidf_for_eval,
                'evaluation': eval_tfidf,
            },
            'embedding': {
                'retrieved': emb_for_eval,
                'evaluation': eval_emb,
            },
        }
    
    return results


def compute_diagnostic_matrix(results: dict) -> dict:
    """Computa matriz diagnóstica 3×2."""
    matrix = []
    for query_id, r in results.items():
        matrix.append({
            'query': query_id,
            'tfidf_pass': r['tfidf']['evaluation']['pass'],
            'tfidf_rank': r['tfidf']['evaluation']['expected_rank'],
            'embedding_pass': r['embedding']['evaluation']['pass'],
            'embedding_rank': r['embedding']['evaluation']['expected_rank'],
        })
    
    # Diagnóstico
    q1_tfidf = matrix[0]['tfidf_pass']
    q1_emb = matrix[0]['embedding_pass']
    q3_tfidf = matrix[2]['tfidf_pass']
    q3_emb = matrix[2]['embedding_pass']
    
    if not q1_tfidf and not q1_emb and q3_tfidf and q3_emb:
        diagnosis = "PROBLEMA DE FORMULAÇÃO DE CONSULTA — ambos retrievers falham em Q1 mas passam em Q3"
        implication = "Solução: query reformulation / query expansion, não trocar retriever"
    elif not q1_tfidf and q1_emb and q3_tfidf and q3_emb:
        diagnosis = "PROBLEMA DE RETRIEVER (TF-IDF) — embedding resolve Q1, TF-IDF não"
        implication = "Solução: manter embeddings (mas H-RAG-001 já mostrou regressões)"
    elif not q1_tfidf and not q1_emb and not q3_tfidf and not q3_emb:
        diagnosis = "PROBLEMA DE RETRIEVER + REPRESENTAÇÃO DOCUMENTAL — ambos falham mesmo com Q3 explícita"
        implication = "Solução: revisar chunking ou representação documental"
    elif q1_tfidf and q1_emb:
        diagnosis = "B1 RESOLVIDO EM AMBOS OS RETRIEVERS — falha original era sazonal/aleatória"
        implication = "Revisar avaliação original; B1 pode ter sido falso negativo"
    else:
        diagnosis = "DIAGNÓSTICO MISTO — ver detalhes por query"
        implication = "Análise caso a caso necessária"
    
    return {
        'matrix': matrix,
        'diagnosis': diagnosis,
        'implication': implication,
    }


def main():
    print("=" * 70)
    print("AION Passo 5.12.1 — AION-B1-DIAG-001")
    print("Auditoria diagnóstica de B1")
    print("=" * 70)
    
    # Reconstrói ambos os stores
    print("\n[SETUP] Reconstruindo TF-IDF store...")
    store_tfidf = TfidfVectorStore()
    all_chunks = []
    for filename, meta in CORPUS_FILES.items():
        path = CORPUS_DIR / filename
        if not path.exists():
            continue
        md_text = path.read_text(encoding='utf-8')
        chunks = parse_extracted_markdown(md_text, meta['id'])
        store_tfidf.add_chunks(chunks)
        all_chunks.extend(chunks)
    store_tfidf.build_index()
    print(f"  TF-IDF: {len(store_tfidf.chunks)} chunks")
    
    print("\n[SETUP] Reconstruindo Embedding store...")
    store_embedding = SemanticVectorStore()
    store_embedding.add_chunks(all_chunks)
    store_embedding.build_index()
    print(f"  Embedding: {len(store_embedding.chunks)} chunks")
    
    # Executa diagnóstico
    print("\n[DIAGNÓSTICO] Executando 6 condições experimentais (3 queries × 2 retrievers)...")
    results = run_retrieval_diagnostic(store_tfidf, store_embedding)
    
    # Computa matriz diagnóstica
    print("\n[MATRIZ DIAGNÓSTICA]")
    diagnostic = compute_diagnostic_matrix(results)
    
    print(f"\n{'Query':<20} {'TF-IDF':<15} {'Embedding':<15}")
    print(f"{'-' * 50}")
    for m in diagnostic['matrix']:
        t = f"{'PASS' if m['tfidf_pass'] else 'FAIL'} (rank={m['tfidf_rank']})"
        e = f"{'PASS' if m['embedding_pass'] else 'FAIL'} (rank={m['embedding_rank']})"
        print(f"{m['query']:<20} {t:<15} {e:<15}")
    
    print(f"\n[DIAGNÓSTICO]")
    print(f"  {diagnostic['diagnosis']}")
    print(f"  {diagnostic['implication']}")
    
    # Salva relatório
    report = {
        'metadata': {
            'experiment': 'AION-B1-DIAG-001',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
            'protocol': 'AION-EVAL-002 v1.0.0 (apenas retrieval, sem geração)',
        },
        'objective': 'Diagnosticar se B1 falha por retrieval capability ou query formulation',
        'variants': B1_VARIANTS,
        'expected_chunk_prefix': EXPECTED_CHUNK_PREFIX,
        'acceptable_chunks': ACCEPTABLE_CHUNKS,
        'results': results,
        'diagnostic_matrix': diagnostic,
        'diagnosis': diagnostic['diagnosis'],
        'implication': diagnostic['implication'],
    }
    
    json_path = OUTPUT_DIR / 'aion_b1_diag_001_resultados.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
