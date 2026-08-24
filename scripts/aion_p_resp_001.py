#!/usr/bin/env python3
"""
AION Passo 5.13 — P-RESP-001 (Proveniência de Resposta)

Hipótese P-RESP-001: um protocolo explícito de geração que obrigue o sistema
a associar cada afirmação relevante a um chunk_id e classificá-la como [E]/[I]/[H]
melhora a proveniência comunicada em respostas sobre lacunas sem degradar H1.

Matriz experimental:
- Sistema A (controle): prompt atual
- Sistema B (P-RESP-001): prompt com protocolo de proveniência explícita

Não alterar: retrieval, GraphRAG, chunking, corpus, modelo de embedding.
Foco exclusivo: proveniência comunicada na resposta.

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

from aion_rag_proxy import TfidfVectorStore, CORPUS_FILES, CORPUS_DIR, parse_extracted_markdown
from aion_bench_001 import BENCH_TESTS
from aion_bench_001_eval002 import evaluate_with_eval002

OUTPUT_DIR = Path('/home/z/my-project/download/rag')


# === Protocolo P-RESP-001 ===

P_RESP_001_SYSTEM_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido.

PROTOCOLO DE PROVENIÊNCIA EXPLÍCITA (P-RESP-001):

Para cada afirmação relevante na sua resposta, você DEVE:

1. Classificar a afirmação com uma tag epistemológica:
   [E] — afirmação diretamente sustentada por texto do corpus (citação literal ou quase-literal)
   [I] — interpretação derivada da evidência, mas não literalmente no corpus
   [H] — hipótese/inferência não estabelecida, proposta pelo sistema

2. Citar a fonte com granularidade:
   source: chunk_id=CORPUS-XXX#pY_ZZ | document=CORPUS-XXX | section=... | page=...

3. Se a informação não estiver no contexto, responder EXATAMENTE:
   "INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO."
   E explicar qual documento seria necessário (se aplicável).

4. NUNCA fabricar chunk_id, documento, página ou evidência.
   Se você não sabe a fonte, diga "ORIGEM NÃO ESTABELECIDA".

5. Estados UNKNOWN (data desconhecida) devem ser marcados como UNKNOWN.
   NUNCA artificialmente date uma afirmação.

FORMATO DE RESPOSTA:

[afirmação 1] [E] [source: chunk_id=CORPUS-XXX#pY_ZZ | doc=CORPUS-XXX | p=Y]
[afirmação 2] [I] [source: chunk_id=... | doc=... | rationale=...]
[afirmação 3] [H] [source: NÃO ESTABELECIDA | rationale=...]

NÃO use conhecimento externo. Responda em português. Não invente."""

CONTROL_SYSTEM_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido. Para cada afirmação, cite o chunk_id de origem. Se a informação não estiver no contexto, diga 'INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO'. Não invente. Não use conhecimento externo. Responda em português."""


def generate_answer(question: str, retrieved: list, system_prompt: str, system_extra: str = "") -> tuple:
    """Gera resposta via z-ai CLI com prompt específico."""
    context_parts = []
    for r in retrieved:
        context_parts.append(
            f"[{r.chunk.chunk_id} | {r.chunk.short_title} | {r.chunk.page} | {r.chunk.section} | score={r.score:.3f}]\n"
            f"{r.chunk.text}\n"
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
            ['z-ai', 'chat',
             '--system', full_system,
             '--prompt', user_prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            return f"[ERRO z-ai: {result.stderr}]", 0
        try:
            data = json.loads(result.stdout)
            answer = data.get('content') or data.get('response') or result.stdout
        except json.JSONDecodeError:
            answer = result.stdout.strip()
        return answer, len(answer)
    except subprocess.TimeoutExpired:
        return "[ERRO z-ai: timeout]", 0
    except Exception as e:
        return f"[ERRO z-ai: {e}]", 0


def clean_answer(answer: str) -> str:
    """Limpa prefixos do z-ai CLI."""
    if '🚀' in answer:
        try:
            json_start = answer.find('{')
            if json_start >= 0:
                json_str = answer[json_start:]
                data = json.loads(json_str)
                return data['choices'][0]['message']['content']
        except:
            pass
    return answer


def run_sistema_test(test_id: str, store, system_prompt: str, system_name: str) -> dict:
    """Executa um teste com prompt específico (controle ou P-RESP-001)."""
    test = BENCH_TESTS[test_id]
    print(f"\n  [{test_id}] ({test['categoria']}) — Sistema {system_name}")
    
    retrieved = store.query(test['pergunta'], top_k=8)
    
    system_extra = ""
    if test_id == 'B2':
        temporal_data = json.loads((OUTPUT_DIR / 'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
        temporal_context = json.dumps(temporal_data['states'][:5], ensure_ascii=False, indent=2)[:2000]
        system_extra = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{temporal_context}"
    elif test_id == 'B6':
        hist_data = json.loads((OUTPUT_DIR / 'aion_hist_001_reconciliacao.json').read_text(encoding='utf-8'))
        negative_context = json.dumps(hist_data['negative_memory']['DESCONHECIDO'], ensure_ascii=False, indent=2)[:2000]
        system_extra = f"\n\nMEMÓRIA NEGATIVA (perguntas não respondíveis):\n{negative_context}"
    
    t_start = time.time()
    answer, _ = generate_answer(test['pergunta'], retrieved[:5], system_prompt, system_extra)
    t_elapsed = time.time() - t_start
    
    answer_clean = clean_answer(answer)
    
    retrieved_for_eval = [
        {
            'rank': i + 1,
            'chunk_id': r.chunk.chunk_id,
            'score': r.score,
            'corpus_id': r.chunk.corpus_id,
        } for i, r in enumerate(retrieved)
    ]
    
    eval_result = evaluate_with_eval002(test_id, retrieved_for_eval, answer_clean, test['gabarito'])
    
    return {
        'test_id': test_id,
        'categoria': test['categoria'],
        'pergunta': test['pergunta'],
        'resposta': answer_clean,
        'tempo_segundos': round(t_elapsed, 2),
        'retrieved_chunks_top5': retrieved_for_eval[:5],
        'eval_002': eval_result,
        'gabarito': test['gabarito'],
        'sistema': system_name,
    }


def evaluate_p_resp_001_metrics(answer: str) -> dict:
    """Métricas específicas do P-RESP-001: contagem de tags [E]/[I]/[H] e chunk_ids."""
    import re
    
    # Conta tags epistemológicas
    e_count = len(re.findall(r'\[E\]', answer))
    i_count = len(re.findall(r'\[I\]', answer))
    h_count = len(re.findall(r'\[H\]', answer))
    
    # Conta chunk_ids citados
    chunk_ids = re.findall(r'CORPUS-\d{3}#\w+', answer)
    unique_chunk_ids = list(set(chunk_ids))
    
    # Verifica se declarou "INFORMAÇÃO NÃO ENCONTRADA" ou "ORIGEM NÃO ESTABELECIDA"
    declared_unknown = (
        'INFORMAÇÃO NÃO ENCONTRADA' in answer or
        'ORIGEM NÃO ESTABELECIDA' in answer or
        'UNKNOWN' in answer
    )
    
    # Verifica se há source: estruturado
    has_source_structured = bool(re.search(r'source:.*chunk_id=', answer, re.IGNORECASE))
    
    return {
        'e_count': e_count,
        'i_count': i_count,
        'h_count': h_count,
        'chunk_ids_cited': unique_chunk_ids,
        'chunk_ids_count': len(unique_chunk_ids),
        'declared_unknown': declared_unknown,
        'has_source_structured': has_source_structured,
    }


def check_fabrication(answer: str, retrieved: list) -> dict:
    """Verifica se a resposta fabricou chunk_ids ou documentos."""
    import re
    
    # Chunk_ids válidos (recuperados)
    valid_chunks = set()
    for r in retrieved[:5]:
        valid_chunks.add(r['chunk_id'])
    
    # Chunk_ids citados na resposta
    cited_chunks = set(re.findall(r'CORPUS-\d{3}#\w+', answer))
    
    # Fabricados: citados mas não recuperados
    fabricated = cited_chunks - valid_chunks
    
    # Documentos válidos (CORPUS-001 a 005)
    valid_docs = {f'CORPUS-{i:03d}' for i in range(1, 6)}
    cited_docs = set(re.findall(r'CORPUS-\d{3}', answer))
    fabricated_docs = cited_docs - valid_docs
    
    return {
        'cited_chunks': list(cited_chunks),
        'valid_chunks': list(valid_chunks),
        'fabricated_chunks': list(fabricated),
        'fabrication_detected': len(fabricated) > 0 or len(fabricated_docs) > 0,
    }


def main():
    print("=" * 70)
    print("AION Passo 5.13 — P-RESP-001 (Proveniência de Resposta)")
    print("Hipótese: protocolo explícito melhora proveniência sem degradar H1")
    print("=" * 70)
    
    # Reconstrói store
    print("\n[SETUP] Reconstruindo TF-IDF store...")
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
    print(f"  Store: {len(store.chunks)} chunks")
    
    # Executa ambos os sistemas em B1-B7
    print("\n[SISTEMA A — Controle] Executando B1-B7...")
    results_A = {}
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        results_A[test_id] = run_sistema_test(test_id, store, CONTROL_SYSTEM_PROMPT, 'A (controle)')
    
    print("\n[SISTEMA B — P-RESP-001] Executando B1-B7...")
    results_B = {}
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        results_B[test_id] = run_sistema_test(test_id, store, P_RESP_001_SYSTEM_PROMPT, 'B (P-RESP-001)')
    
    # Métricas P-RESP-001 específicas
    print("\n[MÉTRICAS P-RESP-001]")
    metrics_A = {}
    metrics_B = {}
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        metrics_A[test_id] = evaluate_p_resp_001_metrics(results_A[test_id]['resposta'])
        metrics_B[test_id] = evaluate_p_resp_001_metrics(results_B[test_id]['resposta'])
    
    # Verificação de fabricação
    print("\n[VERIFICAÇÃO DE FABRICAÇÃO]")
    fabrication_A = {}
    fabrication_B = {}
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        fabrication_A[test_id] = check_fabrication(results_A[test_id]['resposta'], results_A[test_id]['retrieved_chunks_top5'])
        fabrication_B[test_id] = check_fabrication(results_B[test_id]['resposta'], results_B[test_id]['retrieved_chunks_top5'])
    
    # Matriz comparativa
    print(f"\n{'=' * 70}")
    print("[MATRIZ COMPARATIVA — Controle × P-RESP-001]")
    print(f"{'=' * 70}")
    print(f"\n{'Teste':<8} {'Categoria':<15} {'A (controle)':<22} {'B (P-RESP-001)':<22} {'Variação'}")
    print('-' * 80)
    
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        a_status = results_A[test_id]['eval_002']['avaliacao_final']
        b_status = results_B[test_id]['eval_002']['avaliacao_final']
        cat = results_A[test_id]['categoria']
        
        # Hierarquia: PASS > PASS-SEMANTIC > PARTIAL > FAIL
        hierarchy = {'PASS': 4, 'PASS-SEMANTIC': 3, 'PARTIAL': 2, 'FAIL': 1}
        diff = hierarchy.get(b_status, 0) - hierarchy.get(a_status, 0)
        if diff > 0:
            variation = f'↑ MELHOROU'
        elif diff < 0:
            variation = f'↓ REGREDIU'
        else:
            variation = '= (mantido)'
        
        a_emoji = {'PASS': '✅', 'PASS-SEMANTIC': '🟡', 'PARTIAL': '⚠️', 'FAIL': '❌'}.get(a_status, '?')
        b_emoji = {'PASS': '✅', 'PASS-SEMANTIC': '🟡', 'PARTIAL': '⚠️', 'FAIL': '❌'}.get(b_status, '?')
        
        print(f"{test_id:<8} {cat:<15} {a_emoji} {a_status:<19} {b_emoji} {b_status:<19} {variation}")
    
    # B6 em detalhe (foco do experimento)
    print(f"\n{'=' * 70}")
    print("[DETALHE B6 — Foco do experimento]")
    print(f"{'=' * 70}")
    print(f"\nSistema A (controle):")
    print(f"  Avaliação: {results_A['B6']['eval_002']['avaliacao_final']}")
    print(f"  Resposta (primeiros 800 chars):")
    print(f"  {results_A['B6']['resposta'][:800]}")
    print(f"\n  Métricas P-RESP-001: {metrics_A['B6']}")
    print(f"  Fabricação detectada: {fabrication_A['B6']['fabrication_detected']}")
    
    print(f"\nSistema B (P-RESP-001):")
    print(f"  Avaliação: {results_B['B6']['eval_002']['avaliacao_final']}")
    print(f"  Resposta (primeiros 800 chars):")
    print(f"  {results_B['B6']['resposta'][:800]}")
    print(f"\n  Métricas P-RESP-001: {metrics_B['B6']}")
    print(f"  Fabricação detectada: {fabrication_B['B6']['fabrication_detected']}")
    
    # Avaliação dos 7 critérios de aprovação
    print(f"\n{'=' * 70}")
    print("[CRITÉRIOS DE APROVAÇÃO]")
    print(f"{'=' * 70}")
    
    criteria = {
        '1_B6_melhora': (
            hierarchy.get(results_B['B6']['eval_002']['avaliacao_final'], 0) >= 
            hierarchy.get(results_A['B6']['eval_002']['avaliacao_final'], 0)
        ),
        '2_proveniencia_identificavel': (
            metrics_B['B6']['chunk_ids_count'] > metrics_A['B6']['chunk_ids_count'] or
            metrics_B['B6']['has_source_structured']
        ),
        '3_tags_EIH_diferenciadas': (
            metrics_B['B6']['e_count'] + metrics_B['B6']['i_count'] + metrics_B['B6']['h_count'] > 0
        ),
        '4_UNKNOWN_nao_preenchido': not fabrication_B['B6']['fabrication_detected'],
        '5_H1_PASS': results_B['B6']['eval_002']['categories']['H1']['status'] in ('PASS', 'PASS-SEMANTIC'),
        '6_sem_regressao_B1_B7': all(
            hierarchy.get(results_B[tid]['eval_002']['avaliacao_final'], 0) >= 
            hierarchy.get(results_A[tid]['eval_002']['avaliacao_final'], 0)
            for tid in ['B1', 'B2', 'B3', 'B4', 'B5', 'B7']
        ),
        '7_sem_fabricacao': all(not fabrication_B[tid]['fabrication_detected'] for tid in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']),
    }
    
    for crit, passed in criteria.items():
        print(f"  {'✅' if passed else '❌'} {crit}")
    
    pass_count = sum(criteria.values())
    total_count = len(criteria)
    print(f"\nTotal: {pass_count}/{total_count} critérios atendidos")
    
    # Veredito
    if pass_count == total_count:
        verdict = 'P-RESP-001 APROVADO — incorporar ao AION'
        decision = 'INCORPORAR protocolo P-RESP-001 como prompt padrão do sistema'
    elif pass_count >= 5:
        verdict = 'P-RESP-001 PARCIALMENTE APROVADO — incorporar com ressalvas'
        decision = 'INCORPORAR com revisão dos critérios falhados'
    else:
        verdict = 'P-RESP-001 REJEITADO'
        decision = 'MANTER prompt de controle (atual)'
    
    print(f"\n[VEREDITO]")
    print(f"  >>> {verdict}")
    print(f"  >>> {decision}")
    
    # Salva relatório completo
    report = {
        'metadata': {
            'experiment': 'P-RESP-001',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
            'protocol': 'AION-EVAL-002 v1.0.0',
        },
        'hipotese': 'Protocolo explícito de geração melhora proveniência comunicada sem degradar H1.',
        'sistema_A_controle': {
            'description': 'Prompt atual (sem P-RESP-001)',
            'system_prompt': CONTROL_SYSTEM_PROMPT,
            'results': results_A,
            'metrics': metrics_A,
            'fabrication_check': fabrication_A,
        },
        'sistema_B_p_resp_001': {
            'description': 'Prompt com protocolo P-RESP-001',
            'system_prompt': P_RESP_001_SYSTEM_PROMPT,
            'results': results_B,
            'metrics': metrics_B,
            'fabrication_check': fabrication_B,
        },
        'criteria_evaluation': criteria,
        'pass_count': pass_count,
        'total_count': total_count,
        'verdict': verdict,
        'decision': decision,
    }
    
    json_path = OUTPUT_DIR / 'aion_p_resp_001_resultados.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
