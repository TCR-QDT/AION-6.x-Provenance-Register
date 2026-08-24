#!/usr/bin/env python3
"""
AION Plano de Teste — Passo 4, Fase 3

Executa as 4 perguntas do Plano de Teste (P1-P4) contra o RAG proxy,
compara as respostas com a ontologia v1.0.0 (gabarito) e produz relatório
de conformidade.

Autor: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import List

# Adiciona scripts dir ao path
sys.path.insert(0, '/home/z/my-project/scripts')
from aion_rag_proxy import (
    TfidfVectorStore, CORPUS_FILES, CORPUS_DIR,
    parse_extracted_markdown, generate_answer
)

OUTPUT_DIR = Path('/home/z/my-project/download/rag')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# === Plano de Teste ===

TEST_PLAN = {
    'P1': {
        'tipo': 'controle',
        'pergunta': (
            "Quais são os principais conceitos presentes no Corpus AION-001 "
            "e em quais documentos cada conceito aparece? Liste os conceitos "
            "identificando o documento de origem (CORPUS-001 a 005)."
        ),
        'criterio_sucesso': (
            "Sistema deve retornar lista de conceitos, associando cada um a "
            "pelo menos um documento, com citações ou referências diretas. "
            "Não deve inventar conceitos nem documentos."
        ),
        'gabarito_conceitos_esperados': [
            'Coerência Relacional (C = I × S × Hβ)',
            'Integração (I)',
            'Simetria (S)',
            'Entropia Espectral (H)',
            'Functor Φcat',
            'Lema de Yoneda',
            'Tensor Qµν',
            'Equação de Einstein modificada',
            'Dinâmica Quântica Dissipativa (QDT)',
            'Complexo FMO / Power-law T₂',
            'Lakatos / Programa de pesquisa',
            'Conjectura / Proposta / Validação (tríade epistêmica)',
        ],
        'gabarito_docs_esperados': ['CORPUS-001', 'CORPUS-002', 'CORPUS-003', 'CORPUS-004', 'CORPUS-005'],
    },
    'P2': {
        'tipo': 'evolutiva',
        'pergunta': (
            "Como o conceito de 'consciência' ou 'campo primordial' é tratado "
            "no CORPUS-003 (Parte IV) e no CORPUS-002 (Paper A)? Há diferenças "
            "ou complementaridades?"
        ),
        'criterio_sucesso': (
            "Comparação com base nos textos, indicando diferenças de status "
            "(conjectura vs. framework quantitativo)."
        ),
        'gabarito_resolvido_T4': (
            "O termo 'consciência' NÃO aparece em nenhum dos 5 textos extraídos. "
            "O termo 'campo primordial' também não aparece no texto extraído da Parte IV. "
            "A referência a 'consciência' no Handoff original era inferência, não evidência. "
            "Única ponte conceitual: Paper A cita Tononi (Φ-IIT) como referência crítica na Introdução."
        ),
    },
    'P3': {
        'tipo': 'crítica',
        'pergunta': (
            "O que o CORPUS-005 (Cover Letter) e o CORPUS-002 (Paper A) "
            "apontam como limitações do programa TCR? Liste as limitações "
            "auto-declaradas em cada documento."
        ),
        'criterio_sucesso': (
            "Lista de limitações com citação direta. Deve incluir as 6 "
            "inconsistências catalogadas no Paper A e as limitações declaradas "
            "na Cover Letter."
        ),
        'gabarito_limitacoes_paper_a': [
            '6 inconsistências conhecidas catalogadas',
            '3 resolvidas em v6.2 (calibração LOOCV; P3 sintético→real; recursão R removida)',
            '3 diferidas (Inconsistência #3 ST extrapolation → Paper B; #5 η não confirmado → Paper B; #6 COSMO postdictions → Paper C)',
            'Fixtures sintéticos em P1/P2 (Watts-Strogatz, Barabasi-Albert)',
            'P3 com 4 sujeitos preliminares',
            'C não supera {I,S,H} como classificador',
        ],
        'gabarito_limitacoes_cover_letter': [
            'Fixtures sintéticos (transparência declarada)',
            'C não adiciona poder discriminativo',
            'β=0.5 não unicamente determinado',
            'Status: AINDA NÃO PRONTO PARA SUBMISSÃO (v6.1)',
        ],
    },
    'P4': {
        'tipo': 'consistência',
        'pergunta': (
            "Há contradições materiais entre declarações feitas em diferentes "
            "documentos do corpus AION-001? Liste cada contradição com citação "
            "direta e referência cruzada dos documentos envolvidos."
        ),
        'criterio_sucesso': (
            "Sistema deve identificar contradições com citação dupla. "
            "Deve priorizar contradições Cover Letter (CORPUS-005) ↔ Paper A (CORPUS-002)."
        ),
        'gabarito_contradicoes_esperadas': [
            ('C1', 'Versão do Paper A', 'Cover Letter: v6.1, AINDA NÃO PRONTO', 'Paper A: v6.2 FINAL, submetido ao PRE'),
            ('C2', 'Resultados P3', 'Cover Letter: PhysioNet Sleep-EDF, AUC 0.968, 91.2%', 'Paper A: OpenNeuro ds003768, AUC 0.793±0.133, 4 sujeitos'),
            ('C3', 'P1/P2 datasets', 'Cover Letter: conectomas empíricos (C. elegans→HCP, Drosophila)', 'Paper A: fixtures sintéticos (Watts-Strogatz, Barabasi-Albert)'),
            ('C4', 'Status Paper C', 'Cover Letter: submetido à Foundations of Physics em 10/08/2026', 'Paper A: "reserved for a companion paper"'),
        ],
    },
}


def rebuild_store() -> TfidfVectorStore:
    """Reconstrói o store a partir dos arquivos extraídos."""
    store = TfidfVectorStore()
    for filename, meta in CORPUS_FILES.items():
        path = CORPUS_DIR / filename
        if not path.exists():
            continue
        md_text = path.read_text(encoding='utf-8')
        chunks = parse_extracted_markdown(md_text, meta['id'])
        store.add_chunks(chunks)
    store.build_index()
    return store


def run_test(test_id: str, store: TfidfVectorStore) -> dict:
    """Executa um teste do plano."""
    test = TEST_PLAN[test_id]
    print(f"\n{'=' * 70}")
    print(f"[{test_id}] ({test['tipo']})")
    print(f"{'=' * 70}")
    print(f"\nPERGUNTA:\n{test['pergunta']}\n")
    
    # Retrieval
    retrieved = store.query(test['pergunta'], top_k=8)
    print(f"\n[RETRIEVAL] Top-8 chunks recuperados:")
    for r in retrieved:
        print(f"  #{r.rank} score={r.score:.3f} | {r.chunk.chunk_id} | {r.chunk.short_title} | {r.chunk.page} | {r.chunk.section}")
    
    # Geração
    print(f"\n[GERAÇÃO] Chamando z-ai LLM...")
    answer, prompt = generate_answer(test['pergunta'], retrieved[:5])
    
    print(f"\n[RESPOSTA DO SISTEMA]:")
    print(answer[:3000] + ("..." if len(answer) > 3000 else ""))
    
    return {
        'test_id': test_id,
        'tipo': test['tipo'],
        'pergunta': test['pergunta'],
        'criterio_sucesso': test['criterio_sucesso'],
        'retrieved_chunks': [
            {
                'rank': r.rank,
                'chunk_id': r.chunk.chunk_id,
                'corpus_id': r.chunk.corpus_id,
                'short_title': r.chunk.short_title,
                'page': r.chunk.page,
                'section': r.chunk.section,
                'score': r.score,
            } for r in retrieved
        ],
        'prompt_completo': prompt,
        'resposta_sistema': answer,
        'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }


def evaluate_test(test_id: str, result: dict) -> dict:
    """Avalia a resposta contra o gabarito da ontologia v1.0.0."""
    test = TEST_PLAN[test_id]
    answer = result['resposta_sistema'].lower()
    
    evaluation = {
        'test_id': test_id,
        'criterio_sucesso': test['criterio_sucesso'],
    }
    
    if test_id == 'P1':
        # Verifica se conceitos esperados aparecem na resposta
        conceitos_encontrados = []
        conceitos_ausentes = []
        for c in test['gabarito_conceitos_esperados']:
            # Busca termos-chave do conceito na resposta
            terms = extract_key_terms(c)
            if any(t.lower() in answer for t in terms):
                conceitos_encontrados.append(c)
            else:
                conceitos_ausentes.append(c)
        
        # Verifica se mencionou documentos
        docs_mencionados = [d.lower() for d in test['gabarito_docs_esperados'] if d.lower() in answer]
        
        evaluation['conceitos_esperados'] = test['gabarito_conceitos_esperados']
        evaluation['conceitos_encontrados'] = conceitos_encontrados
        evaluation['conceitos_ausentes'] = conceitos_ausentes
        evaluation['docs_esperados'] = test['gabarito_docs_esperados']
        evaluation['docs_mencionados'] = [d.upper() for d in docs_mencionados]
        evaluation['cobertura_conceitos'] = f"{len(conceitos_encontrados)}/{len(test['gabarito_conceitos_esperados'])}"
        evaluation['cobertura_docs'] = f"{len(docs_mencionados)}/{len(test['gabarito_docs_esperados'])}"
        evaluation['pass'] = len(conceitos_encontrados) >= 8 and len(docs_mencionados) >= 4
    
    elif test_id == 'P2':
        # Verifica se identificou que "consciência" não está nos textos
        identificou_ausencia = (
            ('não aparece' in answer) or
            ('não consta' in answer) or
            ('não está' in answer) or
            ('ausente' in answer) or
            ('não mencionado' in answer) or
            ('não encontrado' in answer)
        )
        # Verifica se mencionou Tononi
        mencionou_tononi = 'tononi' in answer
        
        evaluation['gabarito_T4'] = test['gabarito_resolvido_T4']
        evaluation['identificou_ausencia_consciencia'] = identificou_ausencia
        evaluation['mencionou_tononi'] = mencionou_tononi
        evaluation['pass'] = identificou_ausencia and mencionou_tononi
    
    elif test_id == 'P3':
        # Verifica se mencionou as 6 inconsistências
        mencionou_6_inconsistencias = '6 inconsis' in answer or 'seis inconsis' in answer
        mencionou_fixtures_sinteticos = 'sintét' in answer or 'synthetic' in answer
        mencionou_ablation = 'abla' in answer or 'c não supera' in answer or 'não adiciona' in answer
        mencionou_eta = 'η' in answer or 'eta' in answer or 'comensurab' in answer
        
        evaluation['mencionou_6_inconsistencias'] = mencionou_6_inconsistencias
        evaluation['mencionou_fixtures_sinteticos'] = mencionou_fixtures_sinteticos
        evaluation['mencionou_ablation'] = mencionou_ablation
        evaluation['mencionou_retracao_eta'] = mencionou_eta
        evaluation['pass'] = sum([
            mencionou_6_inconsistencias,
            mencionou_fixtures_sinteticos,
            mencionou_ablation,
        ]) >= 2
    
    elif test_id == 'P4':
        # Verifica se identificou contradições
        contradicoes_identificadas = []
        for cid, name, cl_evidence, pa_evidence in test['gabarito_contradicoes_esperadas']:
            # Termos chave para cada contradição
            keys = {
                'C1': ['v6.1', 'v6.2', 'pronto', 'final', 'submetido'],
                'C2': ['0.968', '0.793', '91.2', '4 sujeitos', '4 subjects', 'physionet', 'ds003768', 'openneuro'],
                'C3': ['sintét', 'synthetic', 'empírico', 'watts', 'barabasi', 'wormwiring', 'janelia'],
                'C4': ['foundations of physics', 'paper c', 'submetido', 'reserved', 'companion'],
            }
            found_keys = [k for k in keys[cid] if k.lower() in answer]
            if len(found_keys) >= 2:
                contradicoes_identificadas.append({
                    'contradicao_id': cid,
                    'nome': name,
                    'termos_encontrados': found_keys,
                })
        
        evaluation['contradicoes_esperadas'] = [
            {'id': c[0], 'nome': c[1]} for c in test['gabarito_contradicoes_esperadas']
        ]
        evaluation['contradicoes_identificadas'] = contradicoes_identificadas
        evaluation['cobertura'] = f"{len(contradicoes_identificadas)}/{len(test['gabarito_contradicoes_esperadas'])}"
        evaluation['pass'] = len(contradicoes_identificadas) >= 2
    
    return evaluation


def extract_key_terms(concept: str) -> List[str]:
    """Extrai termos-chave de um nome de conceito para busca."""
    # Para conceitos com símbolos matemáticos, usar formas alternativas
    alternatives = {
        'Coerência Relacional (C = I × S × Hβ)': ['coerência relacional', 'relational coherence', 'TCR', 'C = I'],
        'Integração (I)': ['integração', 'integration', 'I ='],
        'Simetria (S)': ['simetria', 'symmetry', 'S =', 'autormorfismo', 'automorphism'],
        'Entropia Espectral (H)': ['entropia', 'entropy', 'H =', 'spectral entropy'],
        'Functor Φcat': ['functor', 'Φcat', 'Φ_cat', 'Phicat', 'Hom_C'],
        'Lema de Yoneda': ['yoneda', 'lema'],
        'Tensor Qµν': ['tensor', 'Qµν', 'Q_mu', 'Qµ', 'Qµν'],
        'Equação de Einstein modificada': ['einstein', 'equação modificada', 'Gµν', 'G = 8πG'],
        'Dinâmica Quântica Dissipativa (QDT)': ['quântica dissipativa', 'quantum dissipative', 'QDT', 'dissipativa'],
        'Complexo FMO / Power-law T₂': ['FMO', 'fenna', 'power-law', 'T2', 'T₂', 'power law'],
        'Lakatos / Programa de pesquisa': ['lakatos', 'programa de pesquisa', 'research programme'],
        'Conjectura / Proposta / Validação (tríade epistêmica)': ['conjectura', 'proposta', 'validação', 'passo 16', 'passo 17', 'passo 18'],
    }
    return alternatives.get(concept, [concept[:30]])


def main():
    print("=" * 70)
    print("AION PLANO DE TESTE — Passo 4, Fase 3")
    print("=" * 70)
    
    # Reconstrói o store
    print("\n[SETUP] Reconstruindo índice RAG...")
    store = rebuild_store()
    
    # Executa os 4 testes
    results = {}
    evaluations = {}
    
    for test_id in ['P1', 'P2', 'P3', 'P4']:
        result = run_test(test_id, store)
        results[test_id] = result
        evaluation = evaluate_test(test_id, result)
        evaluations[test_id] = evaluation
        
        print(f"\n[AVALIAÇÃO {test_id}]")
        print(json.dumps(evaluation, ensure_ascii=False, indent=2))
    
    # Salva relatório completo
    report = {
        'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'rag_proxy': {
            'chunks_total': len(store.chunks),
            'vectorizer': 'TF-IDF (sklearn)',
            'matrix_shape': list(store.matrix.shape),
            'vocab_size': len(store.vectorizer.vocabulary_),
            'llm_backend': 'z-ai-web-dev-sdk CLI',
        },
        'test_plan': TEST_PLAN,
        'results': results,
        'evaluations': evaluations,
        'summary': {
            'P1': evaluations['P1'].get('pass', False),
            'P2': evaluations['P2'].get('pass', False),
            'P3': evaluations['P3'].get('pass', False),
            'P4': evaluations['P4'].get('pass', False),
        },
    }
    
    report_path = OUTPUT_DIR / 'plano_teste_resultados.json'
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print(f"\n{'=' * 70}")
    print("[RELATÓRIO FINAL]")
    print(f"{'=' * 70}")
    print(f"\nArquivo: {report_path}")
    print(f"\nResumo:")
    for tid, passed in report['summary'].items():
        status = '✅ PASS' if passed else '❌ FAIL'
        print(f"  {tid}: {status}")
    
    return report


if __name__ == '__main__':
    main()
