#!/usr/bin/env python3
"""
AION Passo 6.2.9 — Correção formal do Oracle + Benchmark Cross-Lingual

Etapa 1: Congelar B1_ORACLE_v1 (historical)
Etapa 2: Registrar B1_ORACLE_v2 (5 chunks PRIMARY em CORPUS-002)
Etapa 3: Rebenchmark baseline A usando ORACLE_v2 (TF-IDF atual, novo oracle)
Etapa 4: Executar braço cross-lingual J (tradução PT-BR → EN da pergunta)
Etapa 5: Comparar A(v2) × J(v2) com Top-k detalhado
Etapa 6: Veredito

Separação fundamental:
- B1_ORACLE_v1 (não apagado) — historical benchmark
- B1_ORACLE_v2 (ativo) — oracle metodologicamente corrigido
- Braço A: TF-IDF atual + ORACLE_v2
- Braço J: Cross-lingual (query traduzida PT-BR → EN) + ORACLE_v2

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

OUTPUT_DIR = Path('/home/z/my-project/download/rag')


# === ETAPA 1+2: B1_ORACLE_v1 (frozen) + B1_ORACLE_v2 (active) ===

B1_ORACLE_V1 = {
    'version': 'v1',
    'status': 'FROZEN — historical benchmark',
    'frozen_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    'acceptable_chunks': ['CORPUS-002#p1_01'],
    'description': 'Alvo único — Abstract do Paper A v6.2',
    'rationale': 'Oracle original do Passo 4 (AION-BENCH-001)',
    'preservation_rule': 'NÃO apagado — preservado para reprodução de resultados anteriores',
}

B1_ORACLE_V2 = {
    'version': 'v2',
    'status': 'ACTIVE — oracle metodologicamente corrigido',
    'registered_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    'acceptable_chunks': [
        'CORPUS-002#p1_01',  # Abstract — "we introduce"
        'CORPUS-002#p1_02',  # Abstract — "we introduce"
        'CORPUS-002#p2_01',  # Sec. II — "we define", "the metric is", "metric c as"
        'CORPUS-002#p5_01',  # Sec. V — discussão com definição
        'CORPUS-002#p5_02',  # Sec. V — discussão com definição
    ],
    'description': 'Conjunto de 5 chunks com evidência primária equivalente',
    'rationale': 'Auditoria AION-6.2.8 demonstrou documentalmente que o oracle v1 era excessivamente restritivo. 5 chunks em CORPUS-002 contêm definição/introdução da fórmula C = I × S × H^β.',
    'audit_source': 'aion_6_2_8_audit_gabarito.json',
    'methodological_rule': 'Oracle ampliado a partir da estrutura documental da evidência, NÃO a partir do resultado dos experimentos de retrieval.',
}


# === ETAPA 3: Rebenchmark baseline A usando ORACLE_v2 ===

def evaluate_with_oracle_v2(store, oracle_chunks: list, n_runs: int = 3) -> dict:
    """Avalia B1 usando ORACLE_v2 (5 chunks aceitáveis) em vez de ORACLE_v1 (1 chunk)."""
    test = BENCH_TESTS['B1']
    question = test['pergunta']
    
    print(f"\n  Pergunta B1: {question[:80]}...")
    print(f"  Oracle v2 aceitável: {oracle_chunks}")
    
    runs = []
    
    for run_idx in range(1, n_runs + 1):
        retrieved = store.query(question, top_k=20)
        
        # Top-k diagnosis com oracle v2
        top_k_results = {}
        for k in [1, 3, 5, 10, 20]:
            top_k_chunks = retrieved[:k]
            # Verifica se algum chunk do oracle v2 está no top-k
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
                'in_oracle_v2': r.chunk.chunk_id in oracle_chunks,
            } for i, r in enumerate(retrieved[:3])
        ]
        
        # Top-20 com todos os chunks do oracle que apareceram
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
            'all_oracle_chunks_in_top20': all_oracle_in_top20,
            'top1_chunk': retrieved[0].chunk.chunk_id if retrieved else None,
            'top1_score': retrieved[0].score if retrieved else None,
        }
        runs.append(run_result)
        
        if run_idx == 1:
            print(f"\n  Run 1 — Top-k hits (ORACLE v2):")
            for k in [1, 3, 5, 10, 20]:
                hit = top_k_results[k]
                print(f"    Top-{k}: {'✅' if hit else '❌'}")
            
            if oracle_chunk_found:
                print(f"    >>> Primeiro chunk oracle recuperado: {oracle_chunk_found} (rank #{oracle_rank})")
            else:
                print(f"    >>> Nenhum chunk oracle recuperado em Top-20")
            
            print(f"\n  Top-3 detalhado:")
            for t in top3_detail:
                marker = '✅ ORACLE' if t['in_oracle_v2'] else '  '
                print(f"    {marker} #{t['rank']} score={t['score']:.4f} | {t['chunk_id']}")
            
            if all_oracle_in_top20:
                print(f"\n  Todos chunks oracle em Top-20:")
                for o in all_oracle_in_top20:
                    print(f"    #{o['rank']} score={o['score']:.4f} | {o['chunk_id']}")
    
    # Estatísticas
    hits_by_k = {k: sum(1 for r in runs if r['top_k_hits'][k]) for k in [1, 3, 5, 10, 20]}
    
    # Determinismo
    top3_sets = [tuple(r['top1_chunk'] for r in [run]) for run in runs]
    # Mais robusto: comparar top-3 completo
    top3_full = [tuple((t['chunk_id'] for t in run['top3_detail'])) for run in runs]
    deterministic = all(s == top3_full[0] for s in top3_full)
    
    return {
        'oracle_version': 'v2',
        'oracle_chunks': oracle_chunks,
        'runs': runs,
        'hits_by_k': hits_by_k,
        'deterministic': deterministic,
        'oracle_chunks_found_in_any_run': list(set(r['oracle_chunk_found'] for r in runs if r['oracle_chunk_found'])),
    }


# === ETAPA 4: Braço J — Cross-lingual (PT-BR → EN) ===

# Tradução manual da pergunta B1 de PT-BR para EN
# (não usamos tradução automática para evitar variabilidade)
B1_PERGUNTA_EN = "What is the exact source of the statement that the TCR metric is C = I × S × H^β?"

# Mapeamento de tradução para auditoria
TRANSLATION_MAP = {
    'qual': 'what',
    'é': 'is',
    'a': 'the',
    'fonte': 'source',
    'exata': 'exact',
    'da': 'of the',
    'afirmação': 'statement',
    'de': 'of',
    'que': 'that',
    'métrica': 'metric',
    'tcr': 'TCR',
    # 'c', 'i', 's', 'h', 'β' = mesmos (matemáticos)
}


class ExperimentJ_CrossLingual:
    """Braço J: traduz pergunta PT-BR para EN antes do retrieval."""
    
    def __init__(self, chunks: list, translated_question: str):
        self.chunks = chunks
        self.translated_question = translated_question
        self.original_question = BENCH_TESTS['B1']['pergunta']
        
        # TF-IDF padrão (igual ao controle)
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
        print(f"  [Exp J] Vocabulário: {len(self.vectorizer.vocabulary_)} termos")
        print(f"  [Exp J] Pergunta original (PT-BR): {self.original_question[:60]}...")
        print(f"  [Exp J] Pergunta traduzida (EN): {self.translated_question[:60]}...")
        
        # Verificar tokens da pergunta traduzida no vocabulário
        en_tokens = re.findall(r'\w+', self.translated_question.lower())
        tokens_in_vocab = [t for t in en_tokens if t in self.vectorizer.vocabulary_]
        tokens_not_in_vocab = [t for t in en_tokens if t not in self.vectorizer.vocabulary_]
        print(f"  [Exp J] Tokens EN da pergunta: {en_tokens}")
        print(f"  [Exp J] Tokens EN no vocabulário: {tokens_in_vocab}")
        print(f"  [Exp J] Tokens EN NÃO no vocabulário: {tokens_not_in_vocab}")
    
    def query(self, question: str, top_k: int = 8):
        # Usa a pergunta TRADUZIDA (EN) em vez da original (PT-BR)
        q_vec = self.vectorizer.transform([self.translated_question])
        scores = cosine_similarity(q_vec, self.matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for rank, idx in enumerate(top_indices, 1):
            r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
            results.append(r)
        return results


# === Veredito ===

def classify_verdict_a_vs_j(a_result: dict, j_result: dict) -> dict:
    """Classifica o veredito A(v2) × J(v2) conforme critérios A/B/C/D."""
    
    a_hits = a_result['hits_by_k']
    j_hits = j_result['hits_by_k']
    
    # Resultado A: Cross-lingual não recupera nenhum dos cinco
    if not j_hits[20]:
        return {
            'result': 'A',
            'description': 'Cross-lingual não recupera nenhum dos cinco chunks do oracle',
            'interpretation': 'Assimetria linguística testada e não explica suficientemente o problema',
            'b1_status': 'FAIL-SYSTEM',
            'next_action': 'B1 permanece FAIL-SYSTEM; investigar próxima causa',
        }
    
    # Resultado B: Recupera um ou mais no Top-20, mas não no Top-3
    if j_hits[20] and not j_hits[3]:
        return {
            'result': 'B',
            'description': 'Cross-lingual recupera chunk do oracle no Top-20 mas não no Top-3',
            'interpretation': 'Evidência de que componente cross-lingual é causalmente relevante',
            'b1_status': 'FAIL-SYSTEM (com evidência de mecanismo)',
            'next_action': 'Não é resolução operacional; mas identifica mecanismo',
        }
    
    # Resultado C: Recupera chunk do oracle no Top-3
    if j_hits[3]:
        # Verificar determinismo
        if not j_result['deterministic']:
            return {
                'result': 'C_PARTIAL',
                'description': 'Cross-lingual recupera chunk do oracle no Top-3 mas não é determinístico',
                'interpretation': 'Recuperação operacional mas instável',
                'b1_status': 'PARTIAL',
                'next_action': 'Investigar estabilidade',
            }
        
        return {
            'result': 'C',
            'description': 'Cross-lingual recupera chunk do oracle no Top-3 de forma determinística',
            'interpretation': 'B1 operacionalmente recuperável',
            'b1_status': 'PASS (pending provenance + non-regression)',
            'next_action': 'Rebenchmark B1-B7 completo + teste de não-regressão',
        }
    
    # Resultado D: Top-1/Top-3 robusto
    if j_hits[1] and j_result['deterministic']:
        return {
            'result': 'D',
            'description': 'Cross-lingual recupera chunk do oracle no Top-1 de forma determinística',
            'interpretation': 'Candidato a B1 RESOLVED (requer não-regressão B2-B7)',
            'b1_status': 'PASS (pending full benchmark)',
            'next_action': 'Rebenchmark B1-B7 + não-regressão',
        }
    
    return {
        'result': 'INCONCLUSIVE',
        'description': 'Resultado não se encaixa em nenhuma categoria',
        'interpretation': 'Necessária análise adicional',
        'b1_status': 'UNKNOWN',
        'next_action': 'Análise manual',
    }


def main():
    print("=" * 70)
    print("AION Passo 6.2.9 — Correção formal do Oracle + Benchmark Cross-Lingual")
    print("=" * 70)
    
    # === ETAPA 1+2: Congelar v1, registrar v2 ===
    print(f"\n{'=' * 70}")
    print("[ETAPA 1+2] B1_ORACLE_v1 (frozen) + B1_ORACLE_v2 (active)")
    print(f"{'=' * 70}")
    
    print(f"\n  B1_ORACLE_v1 (FROZEN — historical):")
    print(f"    Status: {B1_ORACLE_V1['status']}")
    print(f"    Acceptable chunks: {B1_ORACLE_V1['acceptable_chunks']}")
    print(f"    Description: {B1_ORACLE_V1['description']}")
    print(f"    Preservation rule: {B1_ORACLE_V1['preservation_rule']}")
    
    print(f"\n  B1_ORACLE_v2 (ACTIVE — metodologicamente corrigido):")
    print(f"    Status: {B1_ORACLE_V2['status']}")
    print(f"    Acceptable chunks: {B1_ORACLE_V2['acceptable_chunks']}")
    print(f"    Description: {B1_ORACLE_V2['description']}")
    print(f"    Rationale: {B1_ORACLE_V2['rationale']}")
    print(f"    Methodological rule: {B1_ORACLE_V2['methodological_rule']}")
    
    # Constrói chunks base
    print(f"\n[SETUP] Construindo chunks base do corpus v1.3.0...")
    base_chunks = build_base_chunks()
    print(f"  Base chunks: {len(base_chunks)}")
    
    # === ETAPA 3: Rebenchmark baseline A usando ORACLE_v2 ===
    print(f"\n{'=' * 70}")
    print("[ETAPA 3] Rebenchmark baseline A usando ORACLE_v2 (TF-IDF atual)")
    print(f"{'=' * 70}")
    
    control_store = TfidfVectorStore()
    control_store.add_chunks(base_chunks)
    control_store.build_index()
    
    a_v2_result = evaluate_with_oracle_v2(control_store, B1_ORACLE_V2['acceptable_chunks'], n_runs=3)
    
    print(f"\n  Resultado A(v2) — TF-IDF atual + ORACLE_v2:")
    print(f"    Hits por k:")
    for k in [1, 3, 5, 10, 20]:
        hits = a_v2_result['hits_by_k'][k]
        print(f"      Top-{k}: {hits}/3 runs")
    print(f"    Determinístico: {a_v2_result['deterministic']}")
    if a_v2_result['oracle_chunks_found_in_any_run']:
        print(f"    Chunks oracle recuperados: {a_v2_result['oracle_chunks_found_in_any_run']}")
    else:
        print(f"    Nenhum chunk oracle recuperado em nenhuma run")
    
    # === ETAPA 4: Braço J — Cross-lingual ===
    print(f"\n{'=' * 70}")
    print("[ETAPA 4] Braço J — Cross-lingual (PT-BR → EN)")
    print(f"{'=' * 70}")
    
    j_store = ExperimentJ_CrossLingual(base_chunks, B1_PERGUNTA_EN)
    j_v2_result = evaluate_with_oracle_v2(j_store, B1_ORACLE_V2['acceptable_chunks'], n_runs=3)
    
    print(f"\n  Resultado J(v2) — Cross-lingual + ORACLE_v2:")
    print(f"    Hits por k:")
    for k in [1, 3, 5, 10, 20]:
        hits = j_v2_result['hits_by_k'][k]
        print(f"      Top-{k}: {hits}/3 runs")
    print(f"    Determinístico: {j_v2_result['deterministic']}")
    if j_v2_result['oracle_chunks_found_in_any_run']:
        print(f"    Chunks oracle recuperados: {j_v2_result['oracle_chunks_found_in_any_run']}")
    else:
        print(f"    Nenhum chunk oracle recuperado em nenhuma run")
    
    # === ETAPA 5: Comparação A(v2) × J(v2) ===
    print(f"\n{'=' * 70}")
    print("[ETAPA 5] Comparação A(v2) × J(v2)")
    print(f"{'=' * 70}")
    
    print(f"\n{'Métrica':<30} {'A (TF-IDF atual)':<25} {'J (Cross-lingual)':<25}")
    print('-' * 80)
    for k in [1, 3, 5, 10, 20]:
        a_hits = a_v2_result['hits_by_k'][k]
        j_hits = j_v2_result['hits_by_k'][k]
        a_str = f"{a_hits}/3"
        j_str = f"{j_hits}/3"
        diff = j_hits - a_hits
        if diff > 0:
            j_str += f" ↑{diff}"
        elif diff < 0:
            j_str += f" ↓{diff}"
        print(f"  {'Top-' + str(k) + ' hits':<28} {a_str:<25} {j_str:<25}")
    
    print(f"\n  {'Determinístico':<28} {a_v2_result['deterministic']!s:<25} {j_v2_result['deterministic']!s:<25}")
    
    a_chunks = a_v2_result['oracle_chunks_found_in_any_run']
    j_chunks = j_v2_result['oracle_chunks_found_in_any_run']
    print(f"  {'Chunks oracle recuperados':<28} {a_chunks!s:<25} {j_chunks!s:<25}")
    
    # === ETAPA 6: Veredito ===
    print(f"\n{'=' * 70}")
    print("[ETAPA 6] VEREDITO AION-6.2.9")
    print(f"{'=' * 70}")
    
    verdict = classify_verdict_a_vs_j(a_v2_result, j_v2_result)
    
    print(f"\n  Resultado: {verdict['result']}")
    print(f"  Descrição: {verdict['description']}")
    print(f"  Interpretação: {verdict['interpretation']}")
    print(f"  B1 status: {verdict['b1_status']}")
    print(f"  Próxima ação: {verdict['next_action']}")
    
    # Salvar relatório
    report = {
        'metadata': {
            'experiment': 'AION-6.2.9 — Correção do Oracle + Benchmark Cross-Lingual',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'b1_oracle_v1': B1_ORACLE_V1,
        'b1_oracle_v2': B1_ORACLE_V2,
        'translation_map': TRANSLATION_MAP,
        'b1_pergunta_pt_br': BENCH_TESTS['B1']['pergunta'],
        'b1_pergunta_en': B1_PERGUNTA_EN,
        'etapa_3_baseline_a_oracle_v2': a_v2_result,
        'etapa_4_cross_lingual_j_oracle_v2': j_v2_result,
        'etapa_5_comparison': {
            'a_v2_hits_by_k': a_v2_result['hits_by_k'],
            'j_v2_hits_by_k': j_v2_result['hits_by_k'],
            'a_v2_oracle_chunks_found': a_v2_result['oracle_chunks_found_in_any_run'],
            'j_v2_oracle_chunks_found': j_v2_result['oracle_chunks_found_in_any_run'],
        },
        'etapa_6_verdict': verdict,
    }
    
    json_path = OUTPUT_DIR / 'aion_6_2_9_oracle_v2_crosslingual.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
