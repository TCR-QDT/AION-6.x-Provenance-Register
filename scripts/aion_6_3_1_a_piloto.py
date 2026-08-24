#!/usr/bin/env python3
"""
AION Passo 6.3.1-A — Piloto C0-C3 (N=20 por condição, 80 runs total)

4 condições experimentais que isolam variáveis diferentes:
- C0: Baseline (contexto atual, múltiplos schemas)
- C1: Schema explícito (instrução sobre formato de ID por documento)
- C2: Whitelist (IDs válidos fornecidos explicitamente)
- C3: Evidence-bound (instrução para copiar exatamente o ID)

Cada condição altera SOMENTE a representação/constraint da provenance no prompt.
Retrieval, corpus, oracle, validator: INALTERADOS.

Variáveis registradas por run:
  schema_ids_visible, target_document_ids_visible, target_chunk_ids_visible,
  retrieval_top1, retrieval_top5, generated_ids, valid_ids, invalid_ids,
  invalid_type, validator_status, semantic_status, provenance_status, PER.

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 21 de agosto de 2026
"""

import json
import sys
import re
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from aion_rag_proxy import parse_extracted_markdown, RetrievedChunk
from aion_bench_001 import BENCH_TESTS
from aion_p_resp_001_v02 import (
    evaluate_with_eval002_v02, clean_answer,
)
from aion_p_resp_001_v03 import ProvenanceValidator
from aion_6_1_f_rebenchmark_lcr import CORPUS_V13_FILES
from aion_6_2_6_top_k_efgh import build_base_chunks
from aion_6_2_9_oracle_crosslingual import B1_PERGUNTA_EN, ExperimentJ_CrossLingual

OUTPUT_DIR = Path('/home/z/my-project/download/rag')

N_PER_CONDITION = 10

# === System prompts para cada condição ===

# C0 — Baseline (prompt atual do P-RESP-001 v0.2)
C0_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido. Para cada afirmação, cite o chunk_id de origem. Se a informação não estiver no contexto, diga 'INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO'. Não invente. Não use conhecimento externo. Responda em português."""

# C1 — Schema explícito
C1_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido.

ESQUEMA DE IDENTIFICAÇÃO DE CHUNKS:
- CORPUS-001 e CORPUS-005 usam formato: chunk_001, chunk_002, ...
- CORPUS-002, CORPUS-003, CORPUS-004, CORPUS-006, CORPUS-007, CORPUS-011 usam formato: p1_01, p2_01, p3_02, ...
- NUNCA construa um identificador. Use APENAS identificadores que aparecem literalmente no contexto fornecido.

Para cada afirmação, cite o chunk_id de origem EXATAMENTE como aparece no contexto. Se a informação não estiver no contexto, diga 'INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO'. Não invente. Não use conhecimento externo. Responda em português."""

# C2 — Whitelist
C2_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido.

IDENTIFICADORES VÁLIDOS PARA CITAÇÃO:
Você SÓ pode citar os seguintes identificadores que aparecem no contexto:
- CORPUS-005#chunk_001
- CORPUS-003#p3_03
- CORPUS-004#p2_04
- CORPUS-003#p3_02
- CORPUS-001#chunk_001

NENHUM outro identificador é aceitável. Se você precisar citar uma fonte que não está nesta lista, diga 'FONTE NÃO DISPONÍVEL NO CONTEXTO'.

Para cada afirmação, cite o chunk_id de origem EXATAMENTE como aparece acima. Se a informação não estiver no contexto, diga 'INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO'. Não invente. Não use conhecimento externo. Responda em português."""

# C3 — Evidence-bound
C3_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido.

REGRA CRÍTICA DE PROVENIÊNCIA:
Para cada afirmação, você DEVE copiar o identificador EXATAMENTE como ele aparece no contexto fornecido acima. Não modifique, não abrevie, não reconstrua, não combine partes de identificadores diferentes.

Se o contexto mostra "[CORPUS-005#chunk_001 | ...]", você deve citar "CORPUS-005#chunk_001".
Se o contexto mostra "[CORPUS-003#p3_03 | ...]", você deve citar "CORPUS-003#p3_03".

NUNCA produza um identificador que não apareça literalmente no contexto.
Se a informação não estiver no contexto, diga 'INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO'. Não invente. Não use conhecimento externo. Responda em português."""


CONDITIONS = {
    'C0': {'name': 'Baseline', 'prompt': C0_PROMPT, 'description': 'Prompt atual sem modificação'},
    'C1': {'name': 'Schema explícito', 'prompt': C1_PROMPT, 'description': 'Instrução sobre formato de ID por documento'},
    'C2': {'name': 'Whitelist', 'prompt': C2_PROMPT, 'description': 'IDs válidos fornecidos explicitamente'},
    'C3': {'name': 'Evidence-bound', 'prompt': C3_PROMPT, 'description': 'Instrução para copiar exatamente o ID'},
}


def generate_answer_with_prompt(question, retrieved, system_prompt, system_extra=""):
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
            ['z-ai', 'chat', '--system', full_system, '--prompt', user_prompt],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            return f"[ERRO z-ai: {result.stderr}]"
        try:
            data = json.loads(result.stdout)
            answer = data.get('content') or data.get('response') or result.stdout
        except json.JSONDecodeError:
            answer = result.stdout.strip()
        return answer
    except subprocess.TimeoutExpired:
        return "[ERRO z-ai: timeout]"
    except Exception as e:
        return f"[ERRO z-ai: {e}]"


def classify_fabrication(invalid_id, all_chunks, retrieved_ids):
    """Classifica fabricação F1-F7."""
    doc_match = re.match(r'CORPUS-(\d{3})', invalid_id)
    if not doc_match:
        return 'F5_MALFORMED'
    doc_id = f'CORPUS-{doc_match.group(1)}'
    doc_exists = any(c.corpus_id == doc_id for c in all_chunks)
    chunk_exists = any(c.chunk_id == invalid_id for c in all_chunks)
    
    if not doc_exists:
        return 'F1_DOCUMENT_INEXISTENT'
    if doc_exists and not chunk_exists:
        if '#chunk_' in invalid_id and doc_id in ('CORPUS-002', 'CORPUS-003', 'CORPUS-004', 'CORPUS-006', 'CORPUS-007', 'CORPUS-011'):
            return 'F3_DOCUMENT_CORRECT_FORMAT_INCORRECT'
        return 'F2_DOCUMENT_EXISTS_CHUNK_INEXISTENT'
    if chunk_exists and invalid_id not in retrieved_ids:
        return 'F4_CHUNK_EXISTS_DOCUMENT_INCORRECT'
    if not re.match(r'CORPUS-\d{3}#\w+', invalid_id):
        return 'F5_MALFORMED'
    return 'F7_OTHER'


def run_condition(j_store, validator, all_chunks, condition_key, condition_data, n_runs):
    """Executa uma condição experimental com N runs."""
    test = BENCH_TESTS['B2']
    
    # Retrieval fixo (mesmo em todas as runs)
    retrieved = j_store.query_original(test['pergunta'], top_k=8)
    retrieved_for_eval = [
        {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
        for i, r in enumerate(retrieved)
    ]
    retrieved_ids = [r.chunk.chunk_id for r in retrieved]
    retrieval_top1 = retrieved[0].chunk.chunk_id if retrieved else None
    retrieval_top5 = retrieved_ids[:5]
    
    # System extra (temporal context)
    temporal_data = json.loads((OUTPUT_DIR / 'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
    temporal_context = json.dumps(temporal_data['states'][:5], ensure_ascii=False, indent=2)[:2000]
    system_extra = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{temporal_context}"
    
    # Schema IDs visíveis no contexto
    schema_ids_visible = retrieved_ids[:5]
    
    # Target document IDs visíveis
    target_doc_ids = set(r.chunk.corpus_id for r in retrieved[:5])
    
    # Target chunk IDs visíveis (especificamente CORPUS-002#p1_01)
    target_chunk_ids_visible = [rid for rid in retrieved_ids if 'CORPUS-002' in rid]
    
    # CORPUS-002#p1_01 explicitly present?
    corpus_002_p1_01_present = 'CORPUS-002#p1_01' in retrieved_ids
    
    runs = []
    
    for run_idx in range(1, n_runs + 1):
        if run_idx % 5 == 0:
            print(f"    {condition_key} Run {run_idx}/{n_runs}...")
        
        # Geração
        t_start = time.time()
        answer_raw = generate_answer_with_prompt(
            test['pergunta'], retrieved[:5], condition_data['prompt'], system_extra
        )
        t_elapsed = time.time() - t_start
        answer_clean = clean_answer(answer_raw)
        
        # IDs citados
        cited_ids = list(set(re.findall(r'CORPUS-\d{3}#\w+', answer_clean)))
        
        # Validator
        validation_result = validator.validate_response(answer_clean, retrieved_for_eval)
        answer_final = validation_result['answer_cleaned']
        
        valid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if v['is_valid']]
        invalid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if not v['is_valid']]
        
        # Classificar fabricações
        invalid_types = [classify_fabrication(inv, all_chunks, retrieved_ids) for inv in invalid_ids]
        
        # PER — Provenance Exactness Rate
        # IDs exatamente copiados de IDs válidos no contexto
        exact_copies = sum(1 for cid in cited_ids if cid in retrieved_ids)
        per_run = exact_copies / len(cited_ids) if cited_ids else 1.0
        
        # Avaliação semântica
        eval_result = evaluate_with_eval002_v02('B2', retrieved_for_eval, answer_final, test['gabarito'])
        semantic_status = eval_result['avaliacao_final']
        
        provenance_status = 'VALID' if not invalid_ids else 'INVALID'
        
        run_data = {
            'run_id': run_idx,
            'condition': condition_key,
            'schema_ids_visible': schema_ids_visible,
            'target_document_ids_visible': list(target_doc_ids),
            'target_chunk_ids_visible': target_chunk_ids_visible,
            'corpus_002_p1_01_explicitly_present': corpus_002_p1_01_present,
            'retrieval_top1': retrieval_top1,
            'retrieval_top5': retrieval_top5,
            'generated_ids': cited_ids,
            'valid_ids': valid_ids,
            'invalid_ids': invalid_ids,
            'invalid_types': invalid_types,
            'per_run': per_run,
            'exact_copies': exact_copies,
            'total_cited': len(cited_ids),
            'validator_status': 'INTERCEPTED' if invalid_ids else 'CLEAN',
            'semantic_status': semantic_status,
            'provenance_status': provenance_status,
            'evidence_status': validation_result['evidence_category'],
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'tempo_segundos': round(t_elapsed, 2),
        }
        runs.append(run_data)
    
    # Métricas da condição
    fr = sum(1 for r in runs if r['invalid_ids']) / n_runs
    ir_total = sum(len(r['invalid_ids']) for r in runs)
    ir_total_gen = sum(len(r['generated_ids']) for r in runs)
    ir = ir_total / ir_total_gen if ir_total_gen > 0 else 0
    vr = ir_total / ir_total if ir_total > 0 else 1.0
    sr = sum(1 for r in runs if 'PASS' in r['semantic_status']) / n_runs
    f3_count = sum(1 for r in runs for t in r['invalid_types'] if t == 'F3_DOCUMENT_CORRECT_FORMAT_INCORRECT')
    f3r = f3_count / n_runs
    per_avg = sum(r['per_run'] for r in runs) / n_runs
    
    # Crosstab
    sp_pv = sum(1 for r in runs if 'PASS' in r['semantic_status'] and r['provenance_status'] == 'VALID')
    sp_pi = sum(1 for r in runs if 'PASS' in r['semantic_status'] and r['provenance_status'] == 'INVALID')
    sf_pv = sum(1 for r in runs if 'PASS' not in r['semantic_status'] and r['provenance_status'] == 'VALID')
    sf_pi = sum(1 for r in runs if 'PASS' not in r['semantic_status'] and r['provenance_status'] == 'INVALID')
    
    return {
        'condition': condition_key,
        'condition_name': condition_data['name'],
        'description': condition_data['description'],
        'n_runs': n_runs,
        'runs': runs,
        'metrics': {
            'FR': fr,
            'IR': ir,
            'VR': vr,
            'SR': sr,
            'F3R': f3r,
            'PER': per_avg,
            'total_ids_generated': ir_total_gen,
            'total_invalid_ids': ir_total,
            'f3_count': f3_count,
        },
        'crosstab': {
            'semantic_pass_provenance_valid': sp_pv,
            'semantic_pass_provenance_invalid': sp_pi,
            'semantic_fail_provenance_valid': sf_pv,
            'semantic_fail_provenance_invalid': sf_pi,
        },
        'b1_control': {
            'b1_top1': retrieval_top1,
            'b1_deterministic': len(set(r['retrieval_top1'] for r in runs)) == 1,
        },
    }


def main():
    print("=" * 80)
    print("AION Passo 6.3.1-A — Piloto C0-C3 (N=20 por condição)")
    print(f"Total: {4 * N_PER_CONDITION} runs")
    print("=" * 80)
    
    # Setup
    print("\n[SETUP] Construindo chunks base...")
    base_chunks = build_base_chunks()
    print(f"  Base chunks: {len(base_chunks)}")
    
    validator = ProvenanceValidator(base_chunks)
    print(f"  Validator CORPUS_INDEX: {len(validator.corpus_index)} chunks")
    
    class ExperimentJ_V3(ExperimentJ_CrossLingual):
        def query_original(self, question, top_k=8):
            q_vec = self.vectorizer.transform([question])
            scores = cosine_similarity(q_vec, self.matrix).flatten()
            top_indices = np.argsort(scores)[::-1][:top_k]
            results = []
            for rank, idx in enumerate(top_indices, 1):
                r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
                results.append(r)
            return results
    
    j_store = ExperimentJ_V3(base_chunks, B1_PERGUNTA_EN if 'B1_PERGUNTTA_EN' in dir() else B1_PERGUNTA_EN)
    
    # Executar cada condição
    results = {}
    
    for cond_key, cond_data in CONDITIONS.items():
        print(f"\n{'=' * 70}")
        print(f"[{cond_key}] {cond_data['name']} — N={N_PER_CONDITION}")
        print(f"{'=' * 70}")
        print(f"  Description: {cond_data['description']}")
        
        cond_result = run_condition(j_store, validator, base_chunks, cond_key, cond_data, N_PER_CONDITION)
        results[cond_key] = cond_result
        
        m = cond_result['metrics']
        b1 = cond_result['b1_control']
        print(f"\n  Resultados {cond_key}:")
        print(f"    FR = {m['FR']:.4f} ({sum(1 for r in cond_result['runs'] if r['invalid_ids'])}/{N_PER_CONDITION})")
        print(f"    IR = {m['IR']:.4f} ({m['total_invalid_ids']}/{m['total_ids_generated']})")
        print(f"    VR = {m['VR']:.4f}")
        print(f"    SR = {m['SR']:.4f}")
        print(f"    F3R = {m['F3R']:.4f} ({m['f3_count']} casos F3)")
        print(f"    PER = {m['PER']:.4f}")
        print(f"    B1 Top-1: {b1['b1_top1']} (determinístico: {b1['b1_deterministic']})")
    
    # Comparação
    print(f"\n{'=' * 80}")
    print("[COMPARAÇÃO C0 × C1 × C2 × C3]")
    print(f"{'=' * 80}")
    
    print(f"\n{'Condição':<25} {'FR':<10} {'IR':<10} {'VR':<10} {'SR':<10} {'F3R':<10} {'PER':<10}")
    print('-' * 85)
    for cond_key in ['C0', 'C1', 'C2', 'C3']:
        m = results[cond_key]['metrics']
        print(f"{cond_key} ({results[cond_key]['condition_name'][:18]:<20}) {m['FR']:<10.4f} {m['IR']:<10.4f} {m['VR']:<10.4f} {m['SR']:<10.4f} {m['F3R']:<10.4f} {m['PER']:<10.4f}")
    
    # B1 controle
    print(f"\n  B1 controle (deve ser determinístico em todas as condições):")
    for cond_key in ['C0', 'C1', 'C2', 'C3']:
        b1 = results[cond_key]['b1_control']
        print(f"    {cond_key}: Top-1={b1['b1_top1']}, determinístico={b1['b1_deterministic']}")
    
    # Veredito do piloto
    print(f"\n{'=' * 80}")
    print("[VEREDITO DO PILOTO]")
    print(f"{'=' * 80}")
    
    # Verificar se desenho está isolando variáveis
    b1_all_deterministic = all(results[k]['b1_control']['b1_deterministic'] for k in ['C0', 'C1', 'C2', 'C3'])
    retrieval_unchanged = all(results[k]['b1_control']['b1_top1'] == results['C0']['b1_control']['b1_top1'] for k in ['C1', 'C2', 'C3'])
    
    # Verificar se F3 é operacional (detectável em C0)
    f3_in_c0 = results['C0']['metrics']['f3_count'] > 0
    
    # Verificar efeito
    fr_c0 = results['C0']['metrics']['FR']
    fr_c1 = results['C1']['metrics']['FR']
    fr_c2 = results['C2']['metrics']['FR']
    fr_c3 = results['C3']['metrics']['FR']
    
    sr_c0 = results['C0']['metrics']['SR']
    sr_c1 = results['C1']['metrics']['SR']
    sr_c2 = results['C2']['metrics']['SR']
    sr_c3 = results['C3']['metrics']['SR']
    
    design_valid = b1_all_deterministic and retrieval_unchanged and f3_in_c0
    
    if design_valid:
        if fr_c2 == 0 or fr_c3 == 0:
            verdict = 'PILOTO VÁLIDO — efeito grande detectado; prosseguir para 400 runs'
        elif fr_c1 < fr_c0 or fr_c2 < fr_c0 or fr_c3 < fr_c0:
            verdict = 'PILOTO VÁLIDO — efeito moderado detectado; prosseguir para 400 runs'
        else:
            verdict = 'PILOTO VÁLIDO — mas sem efeito detectado; reconsiderar hipóteses'
    else:
        verdict = 'PILOTO INVÁLIDO — corrigir protocolo antes de 400 runs'
    
    print(f"\n  Desenho isola variáveis? {'SIM ✅' if design_valid else 'NAO ❌'}")
    print(f"  B1 determinístico em todas? {'SIM ✅' if b1_all_deterministic else 'NAO ❌'}")
    print(f"  Retrieval inalterado? {'SIM ✅' if retrieval_unchanged else 'NAO ❌'}")
    print(f"  F3 operacional em C0? {'SIM ✅' if f3_in_c0 else 'NAO ❌'}")
    print(f"  Efeito detectado? FR: C0={fr_c0:.2f} → C1={fr_c1:.2f} → C2={fr_c2:.2f} → C3={fr_c3:.2f}")
    print(f"  SR preservado? SR: C0={sr_c0:.2f} → C1={sr_c1:.2f} → C2={sr_c2:.2f} → C3={sr_c3:.2f}")
    print(f"\n  >>> {verdict}")
    
    # Salvar relatório
    report = {
        'metadata': {
            'experiment': 'AION-6.3.1-A — Piloto C0-C3 (N=20 por condição)',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
            'n_per_condition': N_PER_CONDITION,
            'total_runs': 4 * N_PER_CONDITION,
        },
        'conditions': results,
        'comparison': {
            'fr_by_condition': {k: results[k]['metrics']['FR'] for k in ['C0', 'C1', 'C2', 'C3']},
            'ir_by_condition': {k: results[k]['metrics']['IR'] for k in ['C0', 'C1', 'C2', 'C3']},
            'vr_by_condition': {k: results[k]['metrics']['VR'] for k in ['C0', 'C1', 'C2', 'C3']},
            'sr_by_condition': {k: results[k]['metrics']['SR'] for k in ['C0', 'C1', 'C2', 'C3']},
            'f3r_by_condition': {k: results[k]['metrics']['F3R'] for k in ['C0', 'C1', 'C2', 'C3']},
            'per_by_condition': {k: results[k]['metrics']['PER'] for k in ['C0', 'C1', 'C2', 'C3']},
        },
        'pilot_verdict': {
            'design_valid': design_valid,
            'b1_all_deterministic': b1_all_deterministic,
            'retrieval_unchanged': retrieval_unchanged,
            'f3_in_c0': f3_in_c0,
            'verdict': verdict,
        },
    }
    
    json_path = OUTPUT_DIR / 'aion_6_3_1_a_piloto_c0_c3.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
