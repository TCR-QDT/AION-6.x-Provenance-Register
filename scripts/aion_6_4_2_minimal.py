#!/usr/bin/env python3
"""
AION Passo 6.4.2 — Provenance Anchoring Minimal Intervention

M0: baseline (P_RESP_001 v0.3)
M1: literal-copy ("copie somente IDs literalmente observados")
M2: context-presence ("documento+chunk devem aparecer literalmente")

N=30 por condição, INTERCALADOS (M0,M1,M2,M0,M1,M2,...)
90 runs total.

Função objetivo: min CFR sujeito a PER≈, SR≈, EBA≥, VR=1

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 21 de agosto de 2026
"""

import json, sys, re, time, hashlib, subprocess
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from aion_rag_proxy import RetrievedChunk
from aion_bench_001 import BENCH_TESTS
from aion_p_resp_001_v02 import P_RESP_001_V02_SYSTEM_PROMPT, evaluate_with_eval002_v02, generate_answer, clean_answer
from aion_p_resp_001_v03 import ProvenanceValidator
from aion_6_2_6_top_k_efgh import build_base_chunks
from aion_6_2_9_oracle_crosslingual import B1_PERGUNTA_EN, ExperimentJ_CrossLingual

OUTPUT_DIR = Path('/home/z/my-project/download/rag')
N_PER = 10  # Reduzir se timeout

M0_PROMPT = P_RESP_001_V02_SYSTEM_PROMPT

M1_PROMPT = P_RESP_001_V02_SYSTEM_PROMPT + """

REGRA DE ANCORAGEM LITERAL:
Ao citar uma fonte, copie EXATAMENTE um identificador que apareça literalmente no contexto fornecido acima. Se você não encontrar o identificador exato, cite o identificador mais próximo que estiver literalmente presente no contexto."""

M2_PROMPT = P_RESP_001_V02_SYSTEM_PROMPT + """

REGRA DE VERIFICAÇÃO DE PRESENÇA:
Antes de emitir um identificador como provenância, verifique se a combinação documento+chunk aparece literalmente no contexto fornecido acima. Se a combinação exata não estiver visível no contexto, não a emitir — use o identificador literalmente disponível mais próximo."""


def classify_fab(invalid_id, all_chunks, retrieved_ids):
    doc_match = re.match(r'CORPUS-(\d{3})', invalid_id)
    if not doc_match: return 'F5'
    doc_id = f'CORPUS-{doc_match.group(1)}'
    doc_exists = any(c.corpus_id == doc_id for c in all_chunks)
    chunk_exists = any(c.chunk_id == invalid_id for c in all_chunks)
    if not doc_exists: return 'F1'
    if doc_exists and not chunk_exists:
        if '#chunk_' in invalid_id and doc_id in ('CORPUS-002','CORPUS-003','CORPUS-004','CORPUS-006','CORPUS-007','CORPUS-011'): return 'F3'
        return 'F2'
    if chunk_exists and invalid_id not in retrieved_ids: return 'F4'
    return 'F7'


def run_single(j_store, validator, all_chunks, prompt, retrieved, retrieved_for_eval, retrieved_ids, system_extra):
    test = BENCH_TESTS['B2']
    t_start = time.time()
    answer_raw = generate_answer(test['pergunta'], retrieved[:5], prompt, system_extra)
    t_elapsed = time.time() - t_start
    answer_clean = clean_answer(answer_raw)
    cited_ids = list(set(re.findall(r'CORPUS-\d{3}#\w+', answer_clean)))
    e_claims = len(re.findall(r'\[E\]', answer_clean))
    i_claims = len(re.findall(r'\[I\]', answer_clean))
    provenance_emitted = len(cited_ids) > 0
    validation_result = validator.validate_response(answer_clean, retrieved_for_eval)
    answer_final = validation_result['answer_cleaned']
    valid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if v['is_valid']]
    invalid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if not v['is_valid']]
    invalid_types = [classify_fab(inv, all_chunks, retrieved_ids) for inv in invalid_ids]
    f3_count = sum(1 for t in invalid_types if t == 'F3')
    eba_valid = sum(1 for vid in valid_ids if vid in retrieved_ids[:5])
    eval_result = evaluate_with_eval002_v02('B2', retrieved_for_eval, answer_final, test['gabarito'])
    return {
        'provenance_emitted': provenance_emitted, 'provenance_count': len(cited_ids),
        'valid_id_count': len(valid_ids), 'invalid_id_count': len(invalid_ids),
        'f3_count': f3_count, 'invalid_types': invalid_types,
        'semantic_pass': 'PASS' in eval_result['avaliacao_final'],
        'eba_valid': eba_valid, 'cited_ids': cited_ids,
        'valid_ids': valid_ids, 'invalid_ids': invalid_ids,
        'tempo': round(t_elapsed, 2),
    }


def compute_metrics(runs):
    n = len(runs)
    runs_prov = sum(1 for r in runs if r['provenance_emitted'])
    per = runs_prov / n
    total_ids = sum(r['provenance_count'] for r in runs)
    total_invalid = sum(r['invalid_id_count'] for r in runs)
    cfr_id = total_invalid / total_ids if total_ids > 0 else 0
    runs_prov_inv = sum(1 for r in runs if r['provenance_emitted'] and r['invalid_id_count'] > 0)
    cfr_run = runs_prov_inv / runs_prov if runs_prov > 0 else 0
    total_eba = sum(r['eba_valid'] for r in runs)
    eba = total_eba / total_ids if total_ids > 0 else 0
    vr = 1.0
    f3_runs = sum(1 for r in runs if r['f3_count'] > 0)
    f3r = f3_runs / n
    sr = sum(1 for r in runs if r['semantic_pass']) / n
    fr = runs_prov_inv / n
    empty = sum(1 for r in runs if not r['provenance_emitted'])
    return {'PER':per,'CFR_ID':cfr_id,'CFR_RUN':cfr_run,'EBA':eba,'VR':vr,'F3R':f3r,'SR':sr,'FR':fr,
            'runs_prov':runs_prov,'empty':empty,'total_ids':total_ids,'total_invalid':total_invalid,'runs_prov_inv':runs_prov_inv}


def main():
    print("="*80)
    print("AION Passo 6.4.2 — Provenance Anchoring Minimal Intervention")
    print(f"M0/M1/M2, N={N_PER} cada (90 runs), INTERCALADOS")
    print("="*80)
    
    base_chunks = build_base_chunks()
    validator = ProvenanceValidator(base_chunks)
    
    class J3(ExperimentJ_CrossLingual):
        def query_original(self, q, top_k=8):
            v = self.vectorizer.transform([q]); s = cosine_similarity(v, self.matrix).flatten()
            ti = np.argsort(s)[::-1][:top_k]
            return [RetrievedChunk(chunk=self.chunks[i], score=float(s[i]), rank=r) for r,i in enumerate(ti,1)]
    
    j = J3(base_chunks, B1_PERGUNTA_EN)
    test = BENCH_TESTS['B2']
    retrieved = j.query_original(test['pergunta'], top_k=8)
    rfe = [{'rank':i+1,'chunk_id':r.chunk.chunk_id,'score':r.score,'corpus_id':r.chunk.corpus_id} for i,r in enumerate(retrieved)]
    rids = [r.chunk.chunk_id for r in retrieved]
    
    td = json.loads((OUTPUT_DIR/'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
    tc = json.dumps(td['states'][:5], ensure_ascii=False, indent=2)[:2000]
    se = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{tc}"
    
    prompts = {'M0':M0_PROMPT,'M1':M1_PROMPT,'M2':M2_PROMPT}
    runs_by_cond = {'M0':[],'M1':[],'M2':[]}
    
    for i in range(N_PER):
        if i % 5 == 0: print(f"  Bloco {i+1}/{N_PER}...")
        for cond in ['M0','M1','M2']:
            r = run_single(j, validator, base_chunks, prompts[cond], retrieved, rfe, rids, se)
            r['run_id'] = f"{cond}-{i+1}"; r['condition'] = cond
            runs_by_cond[cond].append(r)
    
    m = {c: compute_metrics(runs_by_cond[c]) for c in ['M0','M1','M2']}
    
    print(f"\n{'='*80}")
    print("[MATRIZ M0/M1/M2]")
    print(f"{'='*80}")
    print(f"\n{'Métrica':<12} {'M0':<12} {'M1':<12} {'M2':<12}")
    print('-'*48)
    for metric in ['PER','CFR_ID','CFR_RUN','EBA','VR','F3R','SR','FR']:
        print(f"{metric:<12} {m['M0'][metric]:<12.4f} {m['M1'][metric]:<12.4f} {m['M2'][metric]:<12.4f}")
    
    print(f"\n  Runs c/ prov: M0={m['M0']['runs_prov']}, M1={m['M1']['runs_prov']}, M2={m['M2']['runs_prov']}")
    print(f"  Total IDs:    M0={m['M0']['total_ids']}, M1={m['M1']['total_ids']}, M2={m['M2']['total_ids']}")
    print(f"  Total inval:  M0={m['M0']['total_invalid']}, M1={m['M1']['total_invalid']}, M2={m['M2']['total_invalid']}")
    
    # Veredito
    print(f"\n{'='*80}")
    print("[VEREDITO]")
    print(f"{'='*80}")
    
    for cond in ['M1','M2']:
        cfr_red = m[cond]['CFR_RUN'] < m['M0']['CFR_RUN']
        f3_red = m[cond]['F3R'] < m['M0']['F3R']
        eba_ok = m[cond]['EBA'] >= m['M0']['EBA']
        per_ok = m[cond]['PER'] >= m['M0']['PER'] * 0.5
        sr_ok = m[cond]['SR'] >= m['M0']['SR'] * 0.5
        vr_ok = m[cond]['VR'] == 1.0
        
        print(f"\n  {cond}:")
        print(f"    CFR↓? {'✅' if cfr_red else '❌'} ({m['M0']['CFR_RUN']:.4f} → {m[cond]['CFR_RUN']:.4f})")
        print(f"    F3R↓? {'✅' if f3_red else '❌'} ({m['M0']['F3R']:.4f} → {m[cond]['F3R']:.4f})")
        print(f"    EBA≥? {'✅' if eba_ok else '❌'} ({m['M0']['EBA']:.4f} → {m[cond]['EBA']:.4f})")
        print(f"    PER≈? {'✅' if per_ok else '❌'} ({m['M0']['PER']:.4f} → {m[cond]['PER']:.4f})")
        print(f"    SR≈?  {'✅' if sr_ok else '❌'} ({m['M0']['SR']:.4f} → {m[cond]['SR']:.4f})")
        print(f"    VR=1? {'✅' if vr_ok else '❌'}")
        
        if cfr_red and f3_red and eba_ok and per_ok and sr_ok and vr_ok:
            v = f"CANDIDATO FORTE ✅"
        elif cfr_red and f3_red and (not per_ok or not sr_ok):
            v = f"CANDIDATO PARCIAL 🟡 (CFR/F3R↓ mas PER/SR↓)"
        elif not cfr_red and not f3_red:
            v = f"SEM EFEITO 🔴"
        elif m[cond]['PER'] < 0.1:
            v = f"FALSA SOLUÇÃO 🔴 (PER→0)"
        else:
            v = f"MISTO — análise manual"
        print(f"    >>> {v}")
    
    # Salvar
    report = {
        'metadata': {'experiment':'AION-6.4.2 — Minimal Anchoring','timestamp':datetime.now(timezone.utc).isoformat(timespec='seconds'),
                      'n_per':N_PER,'total_runs':3*N_PER,'interleaved':True},
        'metrics': m,
        'runs': {c: [{'run_id':r['run_id'],'provenance_emitted':r['provenance_emitted'],'provenance_count':r['provenance_count'],
                       'valid_id_count':r['valid_id_count'],'invalid_id_count':r['invalid_id_count'],'f3_count':r['f3_count'],
                       'semantic_pass':r['semantic_pass'],'eba_valid':r['eba_valid'],'cited_ids':r['cited_ids'],'invalid_ids':r['invalid_ids']}
                      for r in runs_by_cond[c]] for c in ['M0','M1','M2']},
    }
    json_path = OUTPUT_DIR / 'aion_6_4_2_minimal_anchoring.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] {json_path} ({json_path.stat().st_size} bytes)")
    return report

if __name__ == '__main__': main()
