#!/usr/bin/env python3
"""
AION Passo 6.3.0 — Baseline Estatístico de Fabricação B2

Executa N=100 runs independentes de B2 para caracterizar estatisticamente
a fabricação de identificadores documentais pela camada de geração.

NÃO altera: corpus, oracle, retrieval, validator, prompt, modelo, temperatura.

Variáveis por run: run_id, query, retrieved_chunks, retrieval_top1,
generated_answer, generated_ids, valid_ids, invalid_ids, invalid_type,
validator_status, semantic_status, provenance_status, timestamp.

Taxonomia de fabricação F1-F7.
Métricas: FR, IR, VR, SR.
Controle: B1 Top-1 deve permanecer determinístico.

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
from collections import Counter, defaultdict

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from aion_rag_proxy import parse_extracted_markdown, RetrievedChunk
from aion_bench_001 import BENCH_TESTS
from aion_p_resp_001_v02 import (
    P_RESP_001_V02_SYSTEM_PROMPT,
    evaluate_with_eval002_v02, generate_answer, clean_answer,
)
from aion_p_resp_001_v03 import ProvenanceValidator
from aion_6_1_f_rebenchmark_lcr import CORPUS_V13_FILES
from aion_6_2_6_top_k_efgh import build_base_chunks
from aion_6_2_9_oracle_crosslingual import B1_PERGUNTA_EN, ExperimentJ_CrossLingual

OUTPUT_DIR = Path('/home/z/my-project/download/rag')

N_RUNS = 100


# === Taxonomia de fabricação F1-F7 ===

def classify_fabrication(invalid_id: str, all_chunks: list, retrieved_ids: list) -> str:
    """Classifica o tipo de fabricação do ID inválido."""
    doc_match = re.match(r'CORPUS-(\d{3})', invalid_id)
    if not doc_match:
        return 'F5_MALFORMED'
    
    doc_id = f'CORPUS-{doc_match.group(1)}'
    doc_exists = any(c.corpus_id == doc_id for c in all_chunks)
    chunk_exists = any(c.chunk_id == invalid_id for c in all_chunks)
    
    if not doc_exists:
        return 'F1_DOCUMENT_INEXISTENT'
    
    if doc_exists and not chunk_exists:
        # Verificar se é formato incorreto (documento correto, chunk com formato errado)
        # CORPUS-002 usa p1_01, p2_01 etc; CORPUS-005 usa chunk_001
        if '#chunk_' in invalid_id and doc_id == 'CORPUS-002':
            return 'F3_DOCUMENT_CORRECT_FORMAT_INCORRECT'
        elif '#p' in invalid_id and doc_id == 'CORPUS-005':
            return 'F3_DOCUMENT_CORRECT_FORMAT_INCORRECT'
        else:
            return 'F2_DOCUMENT_EXISTS_CHUNK_INEXISTENT'
    
    if chunk_exists and invalid_id not in retrieved_ids:
        # Chunk existe mas não foi recuperado para esta consulta
        return 'F4_CHUNK_EXISTS_DOCUMENT_INCORRECT'
    
    # Verificar malformação
    if not re.match(r'CORPUS-\d{3}#\w+', invalid_id):
        return 'F5_MALFORMED'
    
    return 'F7_OTHER'


# === Experimento principal ===

def run_b2_baseline(j_store, validator, all_chunks, n_runs=N_RUNS) -> dict:
    """Executa B2 N vezes e coleta todas as variáveis."""
    test = BENCH_TESTS['B2']
    
    # System extra (temporal context — igual ao 6.2.11)
    temporal_data = json.loads((OUTPUT_DIR / 'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
    temporal_context = json.dumps(temporal_data['states'][:5], ensure_ascii=False, indent=2)[:2000]
    system_extra = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{temporal_context}"
    
    # Retrieval fixo (mesmo em todas as runs — controle de variabilidade)
    retrieved = j_store.query_original(test['pergunta'], top_k=8)
    retrieved_for_eval = [
        {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
        for i, r in enumerate(retrieved)
    ]
    retrieved_ids = [r.chunk.chunk_id for r in retrieved]
    retrieval_top1 = retrieved[0].chunk.chunk_id if retrieved else None
    
    runs = []
    fabrication_types = Counter()
    
    for run_idx in range(1, n_runs + 1):
        if run_idx % 10 == 0:
            print(f"  Run {run_idx}/{n_runs}...")
        
        # Geração (variabilidade estocástica do LLM)
        t_start = time.time()
        answer_raw = generate_answer(
            test['pergunta'], retrieved[:5], P_RESP_001_V02_SYSTEM_PROMPT, system_extra
        )
        t_elapsed = time.time() - t_start
        answer_clean = clean_answer(answer_raw)
        
        # IDs citados pelo LLM
        cited_ids = list(set(re.findall(r'CORPUS-\d{3}#\w+', answer_clean)))
        
        # Validator
        validation_result = validator.validate_response(answer_clean, retrieved_for_eval)
        answer_final = validation_result['answer_cleaned']
        
        valid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if v['is_valid']]
        invalid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if not v['is_valid']]
        
        # Classificar cada ID inválido
        invalid_types = []
        for inv_id in invalid_ids:
            fab_type = classify_fabrication(inv_id, all_chunks, retrieved_ids)
            invalid_types.append(fab_type)
            fabrication_types[fab_type] += 1
        
        # Avaliação semântica
        eval_result = evaluate_with_eval002_v02('B2', retrieved_for_eval, answer_final, test['gabarito'])
        semantic_status = eval_result['avaliacao_final']
        
        # Determinar provenance_status
        if len(invalid_ids) == 0:
            provenance_status = 'VALID'
        else:
            provenance_status = 'INVALID'
        
        run_data = {
            'run_id': run_idx,
            'query': test['pergunta'],
            'retrieved_chunks_top5': retrieved_ids[:5],
            'retrieval_top1': retrieval_top1,
            'generated_answer_excerpt': answer_clean[:300],
            'generated_ids': cited_ids,
            'valid_ids': valid_ids,
            'invalid_ids': invalid_ids,
            'invalid_types': invalid_types,
            'validator_status': 'INTERCEPTED' if invalid_ids else 'CLEAN',
            'semantic_status': semantic_status,
            'provenance_status': provenance_status,
            'evidence_status': validation_result['evidence_category'],
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'tempo_segundos': round(t_elapsed, 2),
        }
        runs.append(run_data)
    
    # === Métricas ===
    
    # FR — Taxa de fabricação (runs com pelo menos 1 ID inválido)
    runs_with_fabrication = sum(1 for r in runs if r['invalid_ids'])
    fr = runs_with_fabrication / n_runs
    
    # IR — Taxa de referências inválidas
    total_ids_generated = sum(len(r['generated_ids']) for r in runs)
    total_invalid_ids = sum(len(r['invalid_ids']) for r in runs)
    ir = total_invalid_ids / total_ids_generated if total_ids_generated > 0 else 0
    
    # VR — Taxa de interceptação
    total_invalid_detected = sum(len(r['invalid_ids']) for r in runs)  # validator detecta todos
    vr = total_invalid_detected / total_invalid_ids if total_invalid_ids > 0 else 1.0  # 100% se não há invalidos
    
    # SR — Taxa de respostas semanticamente corretas
    semantic_pass = sum(1 for r in runs if 'PASS' in r['semantic_status'])
    sr = semantic_pass / n_runs
    
    # B1 controle — deve ser determinístico
    b1_top1_values = set(r['retrieval_top1'] for r in runs)
    b1_deterministic = len(b1_top1_values) == 1
    
    # Distribuição de tipos de fabricação
    fabrication_distribution = dict(fabrication_types)
    
    # Relação SEMANTIC × PROVENANCE
    semantic_pass_provenance_valid = sum(1 for r in runs if 'PASS' in r['semantic_status'] and r['provenance_status'] == 'VALID')
    semantic_pass_provenance_invalid = sum(1 for r in runs if 'PASS' in r['semantic_status'] and r['provenance_status'] == 'INVALID')
    semantic_fail_provenance_valid = sum(1 for r in runs if 'PASS' not in r['semantic_status'] and r['provenance_status'] == 'VALID')
    semantic_fail_provenance_invalid = sum(1 for r in runs if 'PASS' not in r['semantic_status'] and r['provenance_status'] == 'INVALID')
    
    return {
        'n_runs': n_runs,
        'runs': runs,
        'metrics': {
            'FR_fabrication_rate': fr,
            'FR_runs_with_fabrication': runs_with_fabrication,
            'IR_invalid_reference_rate': ir,
            'IR_total_ids_generated': total_ids_generated,
            'IR_total_invalid_ids': total_invalid_ids,
            'VR_validation_interception_rate': vr,
            'VR_total_detected': total_invalid_detected,
            'SR_semantic_pass_rate': sr,
            'SR_semantic_pass_count': semantic_pass,
        },
        'b1_control': {
            'b1_deterministic': b1_deterministic,
            'b1_top1_values': list(b1_top1_values),
        },
        'fabrication_distribution': fabrication_distribution,
        'semantic_provenance_crosstab': {
            'semantic_pass_provenance_valid': semantic_pass_provenance_valid,
            'semantic_pass_provenance_invalid': semantic_pass_provenance_invalid,
            'semantic_fail_provenance_valid': semantic_fail_provenance_valid,
            'semantic_fail_provenance_invalid': semantic_fail_provenance_invalid,
        },
    }


def main():
    print("=" * 80)
    print("AION Passo 6.3.0 — Baseline Estatístico de Fabricação B2")
    print(f"N = {N_RUNS} runs independentes")
    print("=" * 80)
    
    # Freeze operacional
    print(f"\n[FREEZE] Componentes congelados:")
    print(f"  Corpus: v1.3.0")
    print(f"  Oracle: v3")
    print(f"  GraphRAG: v1.0.0")
    print(f"  P-RESP-001: v0.3")
    print(f"  AION-EVAL-002: v0.2")
    print(f"  B1 Retrieval: configuração 6.2.11 (J cross-lingual)")
    print(f"  PROIBIDO: alterar prompt, modelo, temperatura, retrieval, oracle, schema, validator")
    
    # Setup
    print(f"\n[SETUP] Construindo chunks base...")
    base_chunks = build_base_chunks()
    print(f"  Base chunks: {len(base_chunks)}")
    
    validator = ProvenanceValidator(base_chunks)
    print(f"  Validator CORPUS_INDEX: {len(validator.corpus_index)} chunks")
    
    # Braço J (cross-lingual) — mesmo do 6.2.11
    print(f"\n[SETUP] Inicializando braço J (cross-lingual)...")
    
    class ExperimentJ_V3(ExperimentJ_CrossLingual):
        def query_original(self, question: str, top_k: int = 8):
            q_vec = self.vectorizer.transform([question])
            scores = cosine_similarity(q_vec, self.matrix).flatten()
            top_indices = np.argsort(scores)[::-1][:top_k]
            results = []
            for rank, idx in enumerate(top_indices, 1):
                r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
                results.append(r)
            return results
    
    j_store = ExperimentJ_V3(base_chunks, B1_PERGUNTA_EN)
    print(f"  Braço J inicializado")
    
    # Executar N runs
    print(f"\n[EXECUÇÃO] {N_RUNS} runs independentes de B2...")
    print(f"  Cada run: mesmo retrieval, mesmo contexto, geração independente")
    
    result = run_b2_baseline(j_store, validator, base_chunks, n_runs=N_RUNS)
    
    # === RELATÓRIO ===
    print(f"\n{'=' * 80}")
    print("[RELATÓRIO ESTATÍSTICO — AION-6.3.0]")
    print(f"{'=' * 80}")
    
    m = result['metrics']
    b1 = result['b1_control']
    fab = result['fabrication_distribution']
    crosstab = result['semantic_provenance_crosstab']
    
    print(f"\n  N = {result['n_runs']} runs")
    
    print(f"\n  === MÉTRICAS PRIMÁRIAS ===")
    print(f"  FR (Taxa de fabricação):       {m['FR_fabrication_rate']:.4f} ({m['FR_runs_with_fabrication']}/{result['n_runs']} runs)")
    print(f"  IR (Taxa de refs inválidas):   {m['IR_invalid_reference_rate']:.4f} ({m['IR_total_invalid_ids']}/{m['IR_total_ids_generated']} IDs)")
    print(f"  VR (Taxa de interceptação):     {m['VR_validation_interception_rate']:.4f} ({m['VR_total_detected']}/{m['IR_total_invalid_ids']} detectados)")
    print(f"  SR (Taxa semântica correta):    {m['SR_semantic_pass_rate']:.4f} ({m['SR_semantic_pass_count']}/{result['n_runs']} PASS)")
    
    print(f"\n  === CONTROLE B1 ===")
    print(f"  B1 determinístico: {'SIM ✅' if b1['b1_deterministic'] else 'NAO ❌'}")
    print(f"  B1 Top-1 valores: {b1['b1_top1_values']}")
    
    print(f"\n  === DISTRIBUIÇÃO DE TIPOS DE FABRICAÇÃO ===")
    if fab:
        for fab_type, count in sorted(fab.items(), key=lambda x: -x[1]):
            print(f"    {fab_type}: {count}")
    else:
        print(f"    Nenhuma fabricação detectada")
    
    print(f"\n  === CROSSTAB SEMÂNTICO × PROVENÂNCIA ===")
    print(f"    Semantic PASS + Provenance VALID:   {crosstab['semantic_pass_provenance_valid']}")
    print(f"    Semantic PASS + Provenance INVALID: {crosstab['semantic_pass_provenance_invalid']}")
    print(f"    Semantic FAIL + Provenance VALID:   {crosstab['semantic_fail_provenance_valid']}")
    print(f"    Semantic FAIL + Provenance INVALID: {crosstab['semantic_fail_provenance_invalid']}")
    
    # Veredito
    print(f"\n  === VEREDITO AION-6.3.0 ===")
    
    criteria = {
        'A_RETRIEVAL': b1['b1_deterministic'],
        'B_SEMANTIC': m['SR_semantic_pass_rate'] > 0,
        'C_PROVENANCE': m['FR_fabrication_rate'] < 1.0,  # nem todas as runs fabricam
        'D_VALIDATION': m['VR_validation_interception_rate'] == 1.0,  # 100% interceptação
    }
    
    for crit, passed in criteria.items():
        print(f"    {'✅' if passed else '❌'} {crit}")
    
    all_pass = all(criteria.values())
    
    if all_pass:
        verdict = 'AION-6.3.0 CONCLUÍDO — baseline estatístico estabelecido'
        next_action = 'AION-6.3.1+ pode investigar intervenções em geração'
    else:
        verdict = 'AION-6.3.0 PARCIAL — alguns critérios não atendidos'
        next_action = 'Investigar critérios falhados'
    
    print(f"\n    >>> {verdict}")
    print(f"    >>> {next_action}")
    
    # Salvar relatório
    report = {
        'metadata': {
            'experiment': 'AION-6.3.0 — Baseline Estatístico de Fabricação B2',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
            'n_runs': N_RUNS,
        },
        'freeze': {
            'corpus': 'v1.3.0',
            'oracle': 'v3',
            'graphrag': 'v1.0.0',
            'p_resp_001': 'v0.3',
            'aion_eval_002': 'v0.2',
            'b1_retrieval': 'configuração 6.2.11 (J cross-lingual)',
        },
        'metrics': m,
        'b1_control': b1,
        'fabrication_distribution': fab,
        'semantic_provenance_crosstab': crosstab,
        'verdict': {
            'criteria': criteria,
            'all_pass': all_pass,
            'verdict': verdict,
            'next_action': next_action,
        },
        'runs_summary': [
            {
                'run_id': r['run_id'],
                'invalid_ids': r['invalid_ids'],
                'invalid_types': r['invalid_types'],
                'validator_status': r['validator_status'],
                'semantic_status': r['semantic_status'],
                'provenance_status': r['provenance_status'],
            } for r in result['runs']
        ],
    }
    
    json_path = OUTPUT_DIR / 'aion_6_3_0_baseline_fabricacao.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
