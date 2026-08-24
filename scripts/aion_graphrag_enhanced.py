#!/usr/bin/env python3
"""
AION GraphRAG Enhanced — Passo 5.5

Re-executa o Plano de Teste P1-P4 usando o grafo conceitual como
contexto adicional ao retrieval TF-IDF. Compara com o baseline
do Passo 4 (TF-IDF puro).

Autor: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.local/lib/python3.13/site-packages')

import networkx as nx
from aion_rag_proxy import (
    TfidfVectorStore, CORPUS_FILES, CORPUS_DIR,
    parse_extracted_markdown, generate_answer
)
from aion_test_plan import TEST_PLAN, evaluate_test, extract_key_terms
from aion_graphrag import build_graph, enrich_with_cooccurrence, CONCEPTS

OUTPUT_DIR = Path('/home/z/my-project/download/rag')


def rebuild_store_with_graph() -> tuple:
    """Reconstrói store + grafo enriquecido."""
    store = TfidfVectorStore()
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
    
    # Constrói grafo e enriquece
    G = build_graph()
    enrich_with_cooccurrence(G, all_chunks)
    
    return store, G


def get_concept_subgraph_context(G: nx.MultiDiGraph, concept_ids: list, max_depth: int = 1) -> str:
    """Extrai subgrafo de contexto para um conjunto de conceitos."""
    if not concept_ids:
        return ""
    
    # Nós vizinhos (depth 1)
    neighbors = set(concept_ids)
    for cid in concept_ids:
        if cid in G:
            neighbors.update(G.successors(cid))
            neighbors.update(G.predecessors(cid))
    
    lines = []
    lines.append(f"=== Contexto do grafo conceitual ===")
    lines.append(f"Conceitos vizinhos (depth {max_depth}): {sorted(neighbors)}")
    lines.append("")
    lines.append("Arestas ontológicas [E] relevantes:")
    
    seen_edges = set()
    for src in neighbors:
        if src not in G:
            continue
        for dst in G.successors(src):
            if dst not in neighbors:
                continue
            edge_data_dict = G.get_edge_data(src, dst)
            if not edge_data_dict:
                continue
            for key, data in edge_data_dict.items():
                if not isinstance(data, dict):
                    continue
                if data.get('source') == 'ontology_v1.0.0_E':
                    edge_key = (src, dst, data.get('type'))
                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        lines.append(f"  {src} --[{data.get('type')}]--> {dst}")
                        lines.append(f"    evidência: {data.get('evidence', '')}")
    
    return "\n".join(lines)


def detect_concepts_in_question(question: str) -> list:
    """Detecta conceitos da ontologia mencionados na pergunta."""
    from aion_graphrag import CONCEPT_PATTERNS
    import re
    found = []
    for concept_id, patterns in CONCEPT_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, question, re.IGNORECASE):
                found.append(concept_id)
                break
    return found


def generate_answer_with_graph(question: str, retrieved: list, graph_context: str) -> tuple:
    """Gera resposta via z-ai CLI usando chunks + grafo como contexto."""
    context_parts = []
    for r in retrieved:
        context_parts.append(
            f"[{r.chunk.chunk_id} | {r.chunk.short_title} | {r.chunk.page} | {r.chunk.section} | score={r.score:.3f}]\n"
            f"{r.chunk.text}\n"
        )
    chunks_context = "\n---\n".join(context_parts)
    
    system_prompt = (
        "Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido "
        "(chunks recuperados + grafo conceitual). Para cada afirmação, cite o chunk_id de origem "
        "ou a aresta do grafo. Se a informação não estiver no contexto, diga 'INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO'. "
        "Não invente. Não use conhecimento externo. Responda em português."
    )
    
    user_prompt = f"""CONTEXTO RECUPERADO (chunks):

{chunks_context}

{graph_context}

PERGUNTA: {question}

Responda usando apenas o contexto acima. Cada afirmação deve ter citação de chunk_id ou aresta do grafo."""
    
    try:
        result = subprocess.run(
            ['z-ai', 'chat',
             '--system', system_prompt,
             '--prompt', user_prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            return f"[ERRO z-ai: {result.stderr}]", user_prompt
        try:
            data = json.loads(result.stdout)
            answer = data.get('content') or data.get('response') or result.stdout
        except json.JSONDecodeError:
            answer = result.stdout.strip()
        return answer, user_prompt
    except subprocess.TimeoutExpired:
        return "[ERRO z-ai: timeout]", user_prompt
    except Exception as e:
        return f"[ERRO z-ai: {e}]", user_prompt


def run_test_enhanced(test_id: str, store, G) -> dict:
    """Executa um teste usando RAG + grafo."""
    test = TEST_PLAN[test_id]
    print(f"\n{'=' * 70}")
    print(f"[{test_id} ENHANCED] ({test['tipo']})")
    print(f"{'=' * 70}")
    print(f"\nPERGUNTA:\n{test['pergunta'][:200]}...\n")
    
    # Retrieval TF-IDF
    retrieved = store.query(test['pergunta'], top_k=8)
    
    # Detecta conceitos na pergunta
    concepts_in_q = detect_concepts_in_question(test['pergunta'])
    print(f"\n[CONCEITOS NA PERGUNTA]: {concepts_in_q}")
    
    # Expande conceitos com vizinhos do grafo
    expanded_concepts = set(concepts_in_q)
    for cid in concepts_in_q:
        if cid in G:
            expanded_concepts.update(G.successors(cid))
            expanded_concepts.update(G.predecessors(cid))
    print(f"[CONCEITOS EXPANDIDOS VIA GRAFO]: {len(expanded_concepts)} conceitos")
    
    # Contexto do grafo
    graph_context = get_concept_subgraph_context(G, list(expanded_concepts)[:10])
    
    # Geração com chunks + grafo
    print(f"\n[GERAÇÃO COM GRAFO] Chamando z-ai LLM...")
    answer, prompt = generate_answer_with_graph(test['pergunta'], retrieved[:5], graph_context)
    
    print(f"\n[RESPOSTA ENHANCED]:")
    print(answer[:2500] + ("..." if len(answer) > 2500 else ""))
    
    return {
        'test_id': test_id + '_enhanced',
        'tipo': test['tipo'],
        'pergunta': test['pergunta'],
        'criterio_sucesso': test['criterio_sucesso'],
        'concepts_in_question': concepts_in_q,
        'expanded_concepts_count': len(expanded_concepts),
        'retrieved_chunks': [
            {
                'rank': r.rank,
                'chunk_id': r.chunk.chunk_id,
                'corpus_id': r.chunk.corpus_id,
                'score': r.score,
            } for r in retrieved
        ],
        'graph_context_provided': graph_context[:2000],
        'prompt_completo': prompt,
        'resposta_sistema': answer,
        'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }


def main():
    print("=" * 70)
    print("AION GraphRAG Enhanced Test — Passo 5.5")
    print("=" * 70)
    
    # Carrega baseline (Passo 4)
    baseline_path = OUTPUT_DIR / 'plano_teste_resultados.json'
    baseline = json.loads(baseline_path.read_text(encoding='utf-8')) if baseline_path.exists() else None
    if baseline:
        print(f"\n[BASELINE carregado: Passo 4]")
    
    # Reconstrói store + grafo
    print("\n[SETUP] Reconstruindo índice RAG + grafo conceitual...")
    store, G = rebuild_store_with_graph()
    print(f"  Store: {len(store.chunks)} chunks")
    print(f"  Grafo: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")
    
    # Executa testes enhanced
    results = {}
    evaluations = {}
    
    for test_id in ['P1', 'P2', 'P3', 'P4']:
        result = run_test_enhanced(test_id, store, G)
        results[test_id] = result
        evaluation = evaluate_test(test_id, result)
        evaluations[test_id] = evaluation
        
        print(f"\n[AVALIAÇÃO {test_id} ENHANCED]")
        print(json.dumps(evaluation, ensure_ascii=False, indent=2))
    
    # Relatório comparativo
    comparison = {
        'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'baseline_passo4': {
            'P1': baseline['summary']['P1'] if baseline else None,
            'P2': baseline['summary']['P2'] if baseline else None,
            'P3': baseline['summary']['P3'] if baseline else None,
            'P4': baseline['summary']['P4'] if baseline else None,
        },
        'enhanced_passo5': {
            'P1': evaluations['P1'].get('pass', False),
            'P2': evaluations['P2'].get('pass', False),
            'P3': evaluations['P3'].get('pass', False),
            'P4': evaluations['P4'].get('pass', False),
        },
        'graph_stats': {
            'nodes': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'ontology_edges_E': sum(1 for _, _, d in G.edges(data=True) if d.get('source') == 'ontology_v1.0.0_E'),
            'cooccurrence_edges': sum(1 for _, _, d in G.edges(data=True) if d.get('source') == 'rag_cooccurrence_auto'),
        },
        'results': results,
        'evaluations': evaluations,
    }
    
    # Adiciona comparações detalhadas
    comparison['detailed_comparison'] = {}
    for tid in ['P1', 'P2', 'P3', 'P4']:
        baseline_ans = baseline['results'][tid]['resposta_sistema'][:500] if baseline else ""
        enhanced_ans = results[tid]['resposta_sistema'][:500]
        comparison['detailed_comparison'][tid] = {
            'baseline_pass': baseline['summary'][tid] if baseline else None,
            'enhanced_pass': evaluations[tid].get('pass', False),
            'baseline_answer_excerpt': baseline_ans,
            'enhanced_answer_excerpt': enhanced_ans,
        }
    
    report_path = OUTPUT_DIR / 'graphrag_enhanced_results.json'
    report_path.write_text(json.dumps(comparison, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print(f"\n{'=' * 70}")
    print("[RELATÓRIO COMPARATIVO]")
    print(f"{'=' * 70}")
    print(f"\nArquivo: {report_path}")
    print(f"\nResumo comparativo:")
    print(f"  {'Teste':<8} {'Passo 4 (baseline)':<22} {'Passo 5 (enhanced)':<22} {'Delta'}")
    for tid in ['P1', 'P2', 'P3', 'P4']:
        b = baseline['summary'][tid] if baseline else None
        e = evaluations[tid].get('pass', False)
        b_str = '✅ PASS' if b else '❌ FAIL'
        e_str = '✅ PASS' if e else '❌ FAIL'
        if b is None:
            delta = '—'
        elif b == e:
            delta = '='
        elif e and not b:
            delta = '↑ IMPROVED'
        else:
            delta = '↓ REGRESSED'
        print(f"  {tid:<8} {b_str:<22} {e_str:<22} {delta}")
    
    return comparison


if __name__ == '__main__':
    main()
