#!/usr/bin/env python3
"""
AION Passo 5.9 — AION-BENCH-001 (Benchmark de Valor Tecnológico)

Executa 7 testes B1-B7 sobre o sistema atual para estabelecer baseline.
Prepara estrutura A/B para avaliar componentes candidatos (AnythingLLM, etc.).

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
sys.path.insert(0, '/home/z/.local/lib/python3.13/site-packages')

from aion_rag_proxy import TfidfVectorStore, CORPUS_FILES, CORPUS_DIR, parse_extracted_markdown
from aion_graphrag import build_graph, enrich_with_cooccurrence
from aion_provenance_granular import EDGE_LOCATIONS

OUTPUT_DIR = Path('/home/z/my-project/download/rag')

# Carrega dados pré-computados
TEMPORAL = json.loads((OUTPUT_DIR / 'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
HIST = json.loads((OUTPUT_DIR / 'aion_hist_001_reconciliacao.json').read_text(encoding='utf-8'))
GRAPH_V2 = json.loads((OUTPUT_DIR / 'graphrag_enriched_v2.0.json').read_text(encoding='utf-8'))


# === Bench B1-B7 ===

BENCH_TESTS = {
    'B1': {
        'categoria': 'Proveniência',
        'pergunta': "Qual é a fonte exata da afirmação de que a métrica TCR é C = I × S × H^β?",
        'gabarito': {
            'documento': 'CORPUS-002',
            'versao': 'v6.2',
            'secao': 'Abstract, p.1',
            'linha': 46,
            'chunk_id': 'CORPUS-002#p1_01',
            'evidence_type': '[E]',
        },
    },
    'B2': {
        'categoria': 'Temporalidade',
        'pergunta': "Quando a métrica C = I × S × H^β apareceu pela primeira vez no corpus e qual foi sua última modificação documentada?",
        'gabarito': {
            'introduced_at': '2026-08-10 (Cover Letter v6.1 aspiracional)',
            'last_refined_at': '2026-08-12 (Paper A v6.2 — β calibrado)',
            'change_type': 'STABLE → REFINED',
        },
    },
    'B3': {
        'categoria': 'Revogação',
        'pergunta': "A hipótese de comensurabilidade cross-scale η continua válida ou foi posteriormente abandonada?",
        'gabarito': {
            'status': 'REVOKED',
            'data_revogacao': '2026-08-12',
            'documento_revogacao': 'CORPUS-004 (Paper B v6.1)',
            'evidence': 'razão |δβ − δST|/δβ = 0.291 > 0.2 não satisfeito',
        },
    },
    'B4': {
        'categoria': 'Ausência',
        'pergunta': "O corpus contém evidência de que Edson defende o conceito de 'consciência' como parte do programa TCR?",
        'gabarito': {
            'resposta_esperada': 'NÃO',
            'razao': 'Termo "consciência" não aparece em nenhum dos 5 textos extraídos. Única referência: Paper A cita Tononi (Φ-IIT) como referência externa, não como conceito do programa.',
            'evidence_type': '[E] — ausência confirmada por auditoria T4',
        },
    },
    'B5': {
        'categoria': 'Contradição',
        'pergunta': "Existem documentos do corpus que apresentam posições incompatíveis sobre os resultados P3 do Paper A?",
        'gabarito': {
            'contradicao_identificada': 'SIM — C2',
            'doc1': 'CORPUS-005 Cover Letter PT-BR: AUC 0.968, 91.2% acurácia, PhysioNet Sleep-EDF',
            'doc2': 'CORPUS-002 Paper A v6.2: AUC 0.793±0.133, 4 sujeitos, OpenNeuro ds003768',
            'interpretacao': 'Defasagem de versionamento — Cover Letter é rascunho v6.1 aspiracional',
        },
    },
    'B6': {
        'categoria': 'Lacuna',
        'pergunta': "O que seria necessário consultar para responder com maior confiança quando Edson abandonou o termo de recursão R^α?",
        'gabarito': {
            'documento_necessario': 'Versões v6.0 e v6.1 do Paper A (não no corpus)',
            'razao': 'Não há documento intermediário entre v5.1 (com R) e v6.2 (sem R)',
            'tipo_lacuna': 'T9 (estrutural) + lacuna documental de versão',
        },
    },
    'B7': {
        'categoria': 'Síntese',
        'pergunta': "Reconstrua a evolução do conceito de Power-law T₂ sem misturar versões.",
        'gabarito': {
            'estado_v6.0': 'T₂ = K·J^1.205·λ^(-1.114)·γ^(-1.068)·T^(-0.795), R²=0.914 (dímero 2 sítios)',
            'estado_v6.1': 'T₂ = (1.567×10⁴)·J^0.831·λ^(-0.843)·γ^(-0.766)·T^(-0.261), R²=0.988 (FMO 7 sítios)',
            'change_type': 'REFINED',
            'data_refinamento': '2026-08-12',
            'razao_refinamento': 'Re-derivação a partir do Hamiltoniano FMO completo (375 combinações)',
        },
    },
}


def rebuild_store_and_graph():
    """Reconstrói store + grafo para uso no benchmark."""
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
    
    G = build_graph()
    enrich_with_cooccurrence(G, all_chunks)
    
    return store, G, all_chunks


def generate_answer_via_llm(question: str, retrieved: list, system_extra: str = "") -> tuple:
    """Gera resposta via z-ai CLI."""
    context_parts = []
    for r in retrieved:
        context_parts.append(
            f"[{r.chunk.chunk_id} | {r.chunk.short_title} | {r.chunk.page} | {r.chunk.section} | score={r.score:.3f}]\n"
            f"{r.chunk.text}\n"
        )
    chunks_context = "\n---\n".join(context_parts)
    
    system_prompt = (
        "Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido. "
        "Para cada afirmação, cite o chunk_id de origem. "
        "Se a informação não estiver no contexto, diga 'INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO'. "
        "Não invente. Não use conhecimento externo. Responda em português."
    )
    if system_extra:
        system_prompt += " " + system_extra
    
    user_prompt = f"""CONTEXTO RECUPERADO:

{chunks_context}

PERGUNTA: {question}

Responda usando apenas o contexto acima. Cada afirmação deve ter citação de chunk_id."""
    
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


def evaluate_bench(test_id: str, answer: str, retrieved: list) -> dict:
    """Avalia resposta do bench B1-B7 contra gabarito."""
    answer_lower = answer.lower()
    test = BENCH_TESTS[test_id]
    gabarito = test['gabarito']
    
    evaluation = {
        'test_id': test_id,
        'categoria': test['categoria'],
        'criterion_pass': False,
        'evidence_found': [],
    }
    
    if test_id == 'B1':
        # Proveniência: deve citar CORPUS-002, p.1, Abstract
        found_corpus_002 = 'corpus-002' in answer_lower
        found_p1 = 'p.1' in answer_lower or 'página 1' in answer_lower or 'abstract' in answer_lower
        found_chunk = 'corpus-002#p1' in answer_lower or any('CORPUS-002' in r.chunk.chunk_id for r in retrieved)
        
        if found_corpus_002 and (found_p1 or found_chunk):
            evaluation['criterion_pass'] = True
            evaluation['evidence_found'] = ['CORPUS-002', 'p.1/Abstract', 'chunk_id']
    
    elif test_id == 'B2':
        # Temporalidade: deve mencionar 2026-08-10 (introdução) e 2026-08-12 (refinamento)
        found_intro = '2026-08-10' in answer or '10 de agosto' in answer_lower or '10/08' in answer
        found_refine = '2026-08-12' in answer or '12 de agosto' in answer_lower or '12/08' in answer
        found_stable_refined = 'stable' in answer_lower or 'refin' in answer_lower
        
        if found_intro and found_refine and found_stable_refined:
            evaluation['criterion_pass'] = True
            evaluation['evidence_found'] = ['2026-08-10', '2026-08-12', 'STABLE→REFINED']
    
    elif test_id == 'B3':
        # Revogação: deve dizer que η foi REVOKED em 2026-08-12
        found_revoked = 'revoked' in answer_lower or 'retrat' in answer_lower or 'retirad' in answer_lower or 'abandonad' in answer_lower
        found_date = '2026-08-12' in answer or '12 de agosto' in answer_lower or '12/08' in answer
        found_reason = '0.291' in answer or '0.2' in answer or 'critério' in answer_lower
        
        if found_revoked and found_date:
            evaluation['criterion_pass'] = True
            evaluation['evidence_found'] = ['REVOKED', '2026-08-12']
            if found_reason:
                evaluation['evidence_found'].append('razão quantitativa')
    
    elif test_id == 'B4':
        # Ausência: deve dizer NÃO (consciência não está no corpus)
        found_no = 'não' in answer_lower and ('consciência' in answer_lower or 'ausente' in answer_lower or 'não encontrado' in answer_lower)
        found_tononi = 'tononi' in answer_lower
        found_auditoria = 'auditoria' in answer_lower or 't4' in answer_lower
        
        if found_no:
            evaluation['criterion_pass'] = True
            evaluation['evidence_found'] = ['ausência confirmada']
            if found_tononi:
                evaluation['evidence_found'].append('referência Tononi')
    
    elif test_id == 'B5':
        # Contradição: deve identificar C2 com citação dupla
        found_aucs = '0.968' in answer and '0.793' in answer
        found_datasets = 'physionet' in answer_lower and ('ds003768' in answer_lower or 'openneuro' in answer_lower)
        found_corpus_005 = 'corpus-005' in answer_lower
        found_corpus_002 = 'corpus-002' in answer_lower
        
        if (found_aucs or found_datasets) and found_corpus_005 and found_corpus_002:
            evaluation['criterion_pass'] = True
            evaluation['evidence_found'] = ['contradição identificada', 'citação dupla']
    
    elif test_id == 'B6':
        # Lacuna: deve identificar v6.0/v6.1 do Paper A como necessário
        found_v60 = 'v6.0' in answer or 'v6.1' in answer
        found_paper_a = 'paper a' in answer_lower
        found_necessario = 'necessário' in answer_lower or 'necessaria' in answer_lower or 'precisa' in answer_lower or 'precisaria' in answer_lower
        
        if found_v60 and found_paper_a:
            evaluation['criterion_pass'] = True
            evaluation['evidence_found'] = ['documento necessário identificado']
    
    elif test_id == 'B7':
        # Síntese: deve distinguir v6.0 (dímero) de v6.1 (FMO 7 sítios)
        found_dimer = 'dímero' in answer_lower or 'dimero' in answer_lower or '2 sítios' in answer_lower or '2 sitios' in answer_lower
        found_fmo7 = '7 sítios' in answer_lower or '7 sitios' in answer_lower or 'fmo completo' in answer_lower
        found_v60 = 'v6.0' in answer
        found_v61 = 'v6.1' in answer
        found_refined = 'refin' in answer_lower
        
        if found_dimer and found_fmo7 and found_v60 and found_v61:
            evaluation['criterion_pass'] = True
            evaluation['evidence_found'] = ['v6.0 (dímero)', 'v6.1 (FMO 7 sítios)', 'distinção mantida']
            if found_refined:
                evaluation['evidence_found'].append('REFINED')
    
    return evaluation


def run_bench_system_A(store, G) -> dict:
    """Executa bench no Sistema A (AION atual: TF-IDF + grafo + temporal + memória negativa)."""
    results = {}
    
    for test_id, test in BENCH_TESTS.items():
        print(f"\n{'=' * 60}")
        print(f"[{test_id}] ({test['categoria']}) — Sistema A")
        print(f"{'=' * 60}")
        print(f"PERGUNTA: {test['pergunta'][:200]}...")
        
        # Retrieval
        retrieved = store.query(test['pergunta'], top_k=8)
        
        # Adiciona contexto do grafo e temporal para algumas perguntas
        system_extra = ""
        if test_id == 'B2':
            # Adiciona contexto temporal
            temporal_context = json.dumps(TEMPORAL['states'][:5], ensure_ascii=False, indent=2)[:2000]
            system_extra = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{temporal_context}"
        elif test_id == 'B6':
            # Adiciona memória negativa
            negative_context = json.dumps(HIST['negative_memory']['DESCONHECIDO'], ensure_ascii=False, indent=2)[:2000]
            system_extra = f"\n\nMEMÓRIA NEGATIVA (perguntas não respondíveis):\n{negative_context}"
        
        # Geração
        t_start = time.time()
        answer, _ = generate_answer_via_llm(test['pergunta'], retrieved[:5], system_extra)
        t_elapsed = time.time() - t_start
        
        print(f"\nRESPOSTA ({t_elapsed:.1f}s):")
        print(answer[:1500] + ("..." if len(answer) > 1500 else ""))
        
        # Avaliação
        evaluation = evaluate_bench(test_id, answer, retrieved)
        print(f"\nAVALIAÇÃO: {'✅ PASS' if evaluation['criterion_pass'] else '❌ FAIL'}")
        print(f"  Evidence found: {evaluation['evidence_found']}")
        
        results[test_id] = {
            'test_id': test_id,
            'categoria': test['categoria'],
            'pergunta': test['pergunta'],
            'resposta': answer,
            'tempo_segundos': round(t_elapsed, 2),
            'retrieved_chunks_count': len(retrieved),
            'retrieved_chunks_top5': [
                {'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
                for r in retrieved[:5]
            ],
            'evaluation': evaluation,
            'gabarito': test['gabarito'],
        }
    
    return results


def compute_ab_matrix(results_A: dict) -> dict:
    """Computa matriz A/B (Sistema B ainda não implementado, deixa placeholder)."""
    matrix = {
        'criterios': [
            'Recuperação correta',
            'Proveniência',
            'Respeito à temporalidade',
            'Detecção de contradições',
            'Tratamento de ausência',
            'Reconstrução histórica',
            'Latência (s)',
            'Complexidade operacional',
        ],
        'sistema_A': {},
        'sistema_B_candidato': {c: 'PENDENTE' for c in [
            'Recuperação correta',
            'Proveniência',
            'Respeito à temporalidade',
            'Detecção de contradições',
            'Tratamento de ausência',
            'Reconstrução histórica',
            'Latência (s)',
            'Complexidade operacional',
        ]},
    }
    
    # Conta passes por categoria
    pass_count = sum(1 for r in results_A.values() if r['evaluation']['criterion_pass'])
    total_count = len(results_A)
    
    # Latência média
    avg_latency = sum(r['tempo_segundos'] for r in results_A.values()) / total_count
    
    matrix['sistema_A']['Recuperação correta'] = f"{pass_count}/{total_count} ({pass_count/total_count*100:.0f}%)"
    matrix['sistema_A']['Proveniência'] = '✅' if results_A['B1']['evaluation']['criterion_pass'] else '❌'
    matrix['sistema_A']['Respeito à temporalidade'] = '✅' if results_A['B2']['evaluation']['criterion_pass'] else '❌'
    matrix['sistema_A']['Detecção de contradições'] = '✅' if results_A['B5']['evaluation']['criterion_pass'] else '❌'
    matrix['sistema_A']['Tratamento de ausência'] = '✅' if results_A['B4']['evaluation']['criterion_pass'] else '❌'
    matrix['sistema_A']['Reconstrução histórica'] = '✅' if results_A['B7']['evaluation']['criterion_pass'] else '❌'
    matrix['sistema_A']['Latência (s)'] = f"{avg_latency:.1f}s médios"
    matrix['sistema_A']['Complexidade operacional'] = "BAIXA (proxy Python + z-ai CLI, sem Docker)"
    
    return matrix


def main():
    print("=" * 70)
    print("AION Passo 5.9 — AION-BENCH-001")
    print("Benchmark de Valor Tecnológico")
    print("=" * 70)
    
    # Reconstrói store + grafo
    print("\n[SETUP] Reconstruindo índice + grafo...")
    store, G, all_chunks = rebuild_store_and_graph()
    print(f"  Store: {len(store.chunks)} chunks")
    print(f"  Grafo: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")
    
    # Executa bench no Sistema A
    print("\n[SISTEMA A] Executando bench no AION atual...")
    results_A = run_bench_system_A(store, G)
    
    # Computa matriz A/B
    print("\n[MATRIZ A/B]")
    matrix = compute_ab_matrix(results_A)
    for crit in matrix['criterios']:
        a = matrix['sistema_A'].get(crit, 'N/A')
        b = matrix['sistema_B_candidato'].get(crit, 'PENDENTE')
        print(f"  {crit:<35} A: {a:<25} B: {b}")
    
    # Estrutura final
    report = {
        'metadata': {
            'version': '1.0.0',
            'generated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
            'protocol': 'AION-BENCH-001',
        },
        'bench_definition': BENCH_TESTS,
        'sistema_A': {
            'description': 'AION atual: TF-IDF + GraphRAG + temporal + memória negativa + LLM z-ai',
            'results': results_A,
        },
        'sistema_B_candidato': {
            'description': 'PENDENTE — candidato a ser avaliado (AnythingLLM real com embeddings semânticos, ou outra arquitetura)',
            'status': 'AGUARDANDO DECISÃO DO PROJETISTA MASTER',
            'prerequisite': 'Apenas proceder com Sistema B se Sistema A falhar em critério crítico identificado pelo Projetista Master',
        },
        'ab_matrix': matrix,
        'recommendation': {
            'sistema_A_pass_count': sum(1 for r in results_A.values() if r['evaluation']['criterion_pass']),
            'sistema_A_total': len(results_A),
            'veredito': 'PENDENTE — aguarda análise do Projetista Master sobre se há critério crítico falhando',
        },
    }
    
    # Salvar JSON
    json_path = OUTPUT_DIR / 'aion_bench_001_resultados.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    # Resumo final
    print(f"\n{'=' * 70}")
    print("[RESUMO Passo 5.9 — AION-BENCH-001]")
    print(f"{'=' * 70}")
    pass_count = report['recommendation']['sistema_A_pass_count']
    total = report['recommendation']['sistema_A_total']
    print(f"Sistema A (AION atual): {pass_count}/{total} testes PASS")
    
    print(f"\nDetalhes por teste:")
    for tid, r in results_A.items():
        status = '✅ PASS' if r['evaluation']['criterion_pass'] else '❌ FAIL'
        print(f"  {tid} ({r['categoria']:<15}) {status}  ({r['tempo_segundos']}s)")
    
    avg_latency = sum(r['tempo_segundos'] for r in results_A.values()) / len(results_A)
    print(f"\nLatência média: {avg_latency:.1f}s por pergunta")
    
    return report


if __name__ == '__main__':
    main()
