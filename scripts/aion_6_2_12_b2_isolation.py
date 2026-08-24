#!/usr/bin/env python3
"""
AION Passo 6.2.12 — B2 Provenance Failure Isolation

Isola a origem do ID inválido detectado em B2 (Task ID 40):
- Reproduz B2 em 3 runs
- Verifica determinismo da falha
- Localiza origem: retrieval, prompt, mapping, ou generation
- Classifica o tipo do ID inválido
- Não altera validator, retrieval, oracle, ou qualquer componente congelado

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

from aion_rag_proxy import TfidfVectorStore, parse_extracted_markdown, RetrievedChunk
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


def reproduce_b2_n_times(j_store, validator, n_runs=3) -> dict:
    """Reproduz B2 N vezes para verificar determinismo da falha de proveniência."""
    test = BENCH_TESTS['B2']
    
    print(f"\n  Pergunta B2: {test['pergunta'][:100]}...")
    
    runs = []
    
    for run_idx in range(1, n_runs + 1):
        print(f"\n  --- Run {run_idx}/{n_runs} ---")
        
        # Retrieval (J cross-lingual — mas para B2 usamos pergunta original PT-BR)
        # B2 pergunta é sobre temporalidade — pode ser PT-BR ou EN
        # Para consistência com o teste de não-regressão do Task ID 40,
        # usamos pergunta original (PT-BR) para B2
        retrieved = j_store.query_original(test['pergunta'], top_k=8)
        
        # IDs efetivamente recuperados
        retrieved_ids = [r.chunk.chunk_id for r in retrieved[:5]]
        retrieved_ids_full = [r.chunk.chunk_id for r in retrieved]
        
        # IDs apresentados ao LLM (top-5)
        ids_presented_to_llm = retrieved_ids[:5]
        
        # System extra (igual ao Task ID 40)
        system_extra = ""
        temporal_data = json.loads((OUTPUT_DIR / 'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
        temporal_context = json.dumps(temporal_data['states'][:5], ensure_ascii=False, indent=2)[:2000]
        system_extra = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{temporal_context}"
        
        # Geração
        t_start = time.time()
        answer_raw = generate_answer(
            test['pergunta'], retrieved[:5], P_RESP_001_V02_SYSTEM_PROMPT, system_extra
        )
        t_elapsed = time.time() - t_start
        answer_clean = clean_answer(answer_raw)
        
        # IDs citados pelo LLM na resposta
        cited_ids = list(set(re.findall(r'CORPUS-\d{3}#\w+', answer_clean)))
        
        # IDs aceitos pelo validator
        retrieved_for_eval = [
            {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
            for i, r in enumerate(retrieved)
        ]
        
        validation_result = validator.validate_response(answer_clean, retrieved_for_eval)
        answer_final = validation_result['answer_cleaned']
        
        # IDs aceitos (válidos) e rejeitados (inválidos)
        valid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if v['is_valid']]
        invalid_ids = [v['chunk_id'] for v in validation_result['validation_log'] if not v['is_valid']]
        
        # Avaliação
        eval_result = evaluate_with_eval002_v02('B2', retrieved_for_eval, answer_final, test['gabarito'])
        
        run_data = {
            'run_idx': run_idx,
            'tempo_segundos': round(t_elapsed, 2),
            'retrieved_ids_top5': retrieved_ids,
            'retrieved_ids_all': retrieved_ids_full,
            'ids_presented_to_llm': ids_presented_to_llm,
            'ids_cited_by_llm': cited_ids,
            'ids_valid': valid_ids,
            'ids_invalid': invalid_ids,
            'invalid_count': len(invalid_ids),
            'valid_count': len(valid_ids),
            'evidence_status': validation_result['evidence_category'],
            'eval_status': eval_result['avaliacao_final'],
            'answer_excerpt': answer_clean[:500],
        }
        runs.append(run_data)
        
        print(f"    Retrieved top-5: {retrieved_ids}")
        print(f"    Citados pelo LLM: {cited_ids}")
        print(f"    Válidos: {valid_ids}")
        print(f"    Inválidos: {invalid_ids}")
        print(f"    Evidence status: {validation_result['evidence_category']}")
        print(f"    Eval status: {eval_result['avaliacao_final']}")
    
    # Verificar determinismo da falha
    invalid_ids_per_run = [tuple(run['ids_invalid']) for run in runs]
    deterministic_failure = all(s == invalid_ids_per_run[0] for s in invalid_ids_per_run)
    
    # Todos IDs inválidos únicos encontrados
    all_invalid_ids = list(set(id for run in runs for id in run['ids_invalid']))
    
    return {
        'runs': runs,
        'n_runs': n_runs,
        'deterministic_failure': deterministic_failure,
        'invalid_ids_per_run': [list(s) for s in invalid_ids_per_run],
        'all_unique_invalid_ids': all_invalid_ids,
    }


def classify_invalid_id(invalid_id: str, all_chunks: list) -> dict:
    """Classifica o tipo do ID inválido."""
    # Verifica se corresponde a documento existente
    doc_match = re.match(r'CORPUS-(\d{3})', invalid_id)
    doc_id = f'CORPUS-{doc_match.group(1)}' if doc_match else 'UNKNOWN'
    
    # Verifica se o documento existe no corpus
    doc_exists = any(c.corpus_id == doc_id for c in all_chunks)
    
    # Verifica se o chunk existe no corpus (CORPUS_INDEX)
    chunk_exists = any(c.chunk_id == invalid_id for c in all_chunks)
    
    # Verifica se corresponde a chunk de versão histórica
    is_historical = doc_id in ['CORPUS-002-HIST', 'CORPUS-004', 'CORPUS-006', 'CORPUS-007']
    
    # Verifica se houve transformação/truncamento
    # Procura por IDs similares no corpus
    similar_ids = []
    if '#' in invalid_id:
        prefix = invalid_id.split('#')[0]
        suffix = invalid_id.split('#')[1]
        for c in all_chunks:
            if c.corpus_id == prefix and c.chunk_id.split('#')[1].startswith(suffix[:3]):
                similar_ids.append(c.chunk_id)
    
    # Classificação
    if chunk_exists:
        classification = 'CHUNK_EXISTS_BUT_NOT_RETRIEVED'
        description = 'ID existe no corpus mas não estava nos chunks recuperados para esta consulta'
    elif doc_exists:
        classification = 'DOC_EXISTS_BUT_CHUNK_DOES_NOT'
        description = f'Documento {doc_id} existe, mas chunk {invalid_id} não existe no documento'
    elif is_historical:
        classification = 'HISTORICAL_VERSION'
        description = f'ID corresponde a versão histórica ({doc_id})'
    else:
        classification = 'FABRICATED_ID'
        description = f'ID não corresponde a nenhum documento ou chunk existente'
    
    return {
        'invalid_id': invalid_id,
        'document_id': doc_id,
        'document_exists': doc_exists,
        'chunk_exists': chunk_exists,
        'is_historical': is_historical,
        'similar_ids_in_corpus': similar_ids[:5],
        'classification': classification,
        'description': description,
    }


def localize_origin(retrieved_ids: list, cited_ids: list, invalid_ids: list, answer: str) -> dict:
    """Localiza a origem do ID inválido."""
    print(f"\n  Localização da origem do ID inválido:")
    
    for invalid_id in invalid_ids:
        print(f"\n    ID inválido: {invalid_id}")
        
        # 1. Está nos retrieved?
        in_retrieved = invalid_id in retrieved_ids
        print(f"      Está nos retrieved? {'SIM' if in_retrieved else 'NAO'}")
        
        # 2. Está nos IDs apresentados ao LLM?
        in_presented = invalid_id in retrieved_ids[:5]
        print(f"      Está nos apresentados ao LLM? {'SIM' if in_presented else 'NAO'}")
        
        # 3. Está nos citados pelo LLM?
        in_cited = invalid_id in cited_ids
        print(f"      Está nos citados pelo LLM? {'SIM' if in_cited else 'NAO'}")
        
        # 4. Origem provável
        if in_retrieved:
            origin = 'RETRIEVAL — ID estava nos chunks recuperados mas não deveria estar aceito'
        elif in_cited and not in_retrieved:
            origin = 'GENERATION — LLM fabricou o ID (não estava nos recuperados)'
        else:
            origin = 'UNKNOWN — origem não determinada'
        
        print(f"      Origem: {origin}")
        
        # 5. Verificar se o ID é uma transformação de um ID real
        # Procura por IDs que poderiam ter sido transformados
        if '#' in invalid_id:
            prefix = invalid_id.split('#')[0]
            invalid_suffix = invalid_id.split('#')[1]
            print(f"      Prefix: {prefix}, Suffix: {invalid_suffix}")
            
            # Procura por IDs no mesmo documento com sufixo similar
            similar = [rid for rid in retrieved_ids if rid.startswith(prefix + '#')]
            if similar:
                print(f"      IDs similares recuperados: {similar}")
                
                # Verifica se o LLM pode ter confundido/transformado
                for sim in similar:
                    sim_suffix = sim.split('#')[1]
                    if sim_suffix[:2] == invalid_suffix[:2]:
                        print(f"        >>> Possível transformação: {sim} → {invalid_id}")
    
    return {
        'invalid_ids_analyzed': invalid_ids,
        'origins': [],
    }


def main():
    print("=" * 80)
    print("AION Passo 6.2.12 — B2 Provenance Failure Isolation")
    print("=" * 80)
    
    # Setup
    print("\n[SETUP] Construindo chunks base do corpus v1.3.0...")
    base_chunks = build_base_chunks()
    print(f"  Base chunks: {len(base_chunks)}")
    
    validator = ProvenanceValidator(base_chunks)
    print(f"  Validator CORPUS_INDEX: {len(validator.corpus_index)} chunks")
    
    # Usar braço J (cross-lingual) — mesmo do Task ID 40
    print("\n[SETUP] Inicializando braço J (cross-lingual)...")
    
    class ExperimentJ_V3(ExperimentJ_CrossLingual):
        def query_original(self, question: str, top_k: int = 8):
            from sklearn.metrics.pairwise import cosine_similarity
            q_vec = self.vectorizer.transform([question])
            scores = cosine_similarity(q_vec, self.matrix).flatten()
            import numpy as np
            top_indices = np.argsort(scores)[::-1][:top_k]
            results = []
            for rank, idx in enumerate(top_indices, 1):
                r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
                results.append(r)
            return results
    
    j_store = ExperimentJ_V3(base_chunks, B1_PERGUNTA_EN)
    
    # ETAPA 1: Reproduzir B2 (3 runs)
    print(f"\n{'=' * 80}")
    print("[ETAPA 1] Reproduzir B2 (3 runs) — verificar determinismo da falha")
    print(f"{'=' * 80}")
    
    reproduction = reproduce_b2_n_times(j_store, validator, n_runs=3)
    
    print(f"\n  Determinismo da falha: {reproduction['deterministic_failure']}")
    print(f"  IDs inválidos por run:")
    for i, ids in enumerate(reproduction['invalid_ids_per_run']):
        print(f"    Run {i+1}: {ids}")
    print(f"  Todos IDs inválidos únicos: {reproduction['all_unique_invalid_ids']}")
    
    # ETAPA 2: Classificar tipo do ID inválido
    print(f"\n{'=' * 80}")
    print("[ETAPA 2] Classificar tipo do ID inválido")
    print(f"{'=' * 80}")
    
    all_invalid = reproduction['all_unique_invalid_ids']
    classifications = []
    
    for invalid_id in all_invalid:
        classification = classify_invalid_id(invalid_id, base_chunks)
        classifications.append(classification)
        
        print(f"\n  ID: {invalid_id}")
        print(f"    Documento: {classification['document_id']}")
        print(f"    Documento existe? {'SIM' if classification['document_exists'] else 'NAO'}")
        print(f"    Chunk existe? {'SIM' if classification['chunk_exists'] else 'NAO'}")
        print(f"    É versão histórica? {'SIM' if classification['is_historical'] else 'NAO'}")
        print(f"    IDs similares no corpus: {classification['similar_ids_in_corpus']}")
        print(f"    Classificação: {classification['classification']}")
        print(f"    Descrição: {classification['description']}")
    
    # ETAPA 3: Localizar origem
    print(f"\n{'=' * 80}")
    print("[ETAPA 3] Localizar origem do ID inválido")
    print(f"{'=' * 80}")
    
    if reproduction['runs']:
        first_run = reproduction['runs'][0]
        origin_analysis = localize_origin(
            first_run['retrieved_ids_top5'],
            first_run['ids_cited_by_llm'],
            first_run['ids_invalid'],
            first_run['answer_excerpt'],
        )
    
    # ETAPA 4: Veredito
    print(f"\n{'=' * 80}")
    print("[ETAPA 4] VEREDITO AION-6.2.12")
    print(f"{'=' * 80}")
    
    print(f"\n  Resumo da investigação:")
    print(f"    Falha reproduzida em 3/3 runs: {reproduction['deterministic_failure']}")
    print(f"    IDs inválidos únicos: {all_invalid}")
    print(f"    Classificação: {classifications[0]['classification'] if classifications else 'N/A'}")
    print(f"    Descrição: {classifications[0]['description'] if classifications else 'N/A'}")
    
    # Determinar causa
    if classifications:
        cls = classifications[0]
        
        if cls['classification'] == 'CHUNK_EXISTS_BUT_NOT_RETRIEVED':
            cause = 'RETRIEVAL — chunk existe no corpus mas não foi recuperado para B2'
            correctable = True
            correction = 'Aceitar chunk existente no corpus como válido para proveniência (estender validação V2 do validator)'
        elif cls['classification'] == 'DOC_EXISTS_BUT_CHUNK_DOES_NOT':
            cause = 'GENERATION — LLM fabricou ID usando documento existente mas chunk inexistente'
            correctable = False
            correction = 'Não corrigível sem alterar geração do LLM; validator já intercepta corretamente'
        elif cls['classification'] == 'FABRICATED_ID':
            cause = 'GENERATION — LLM fabricou ID completamente'
            correctable = False
            correction = 'Não corrigível sem alterar geração do LLM; validator já intercepta corretamente'
        else:
            cause = 'UNKNOWN'
            correctable = False
            correction = 'Investigação adicional necessária'
    else:
        cause = 'NO_INVALID_IDS — falha não reproduzida'
        correctable = False
        correction = 'N/A'
    
    print(f"\n    Causa: {cause}")
    print(f"    Corrigível? {'SIM' if correctable else 'NAO'}")
    print(f"    Correção: {correction}")
    
    # Veredito final
    if reproduction['deterministic_failure'] and classifications:
        cls = classifications[0]
        
        if cls['classification'] == 'CHUNK_EXISTS_BUT_NOT_RETRIEVED':
            verdict = 'CAUSA LOCALIZADA — chunk existe mas não foi recuperado para B2'
            action = 'Estender validação V2 do validator para aceitar chunks existentes no corpus (mesmo se não recuperados)'
        elif cls['classification'] in ('DOC_EXISTS_BUT_CHUNK_DOES_NOT', 'FABRICATED_ID'):
            verdict = 'CAUSA LOCALIZADA — geração do LLM (não corrigível sem alterar prompt)'
            action = 'Validator já intercepta corretamente; B2 provenance failure é LIMITAÇÃO DE GERAÇÃO aceita'
        else:
            verdict = 'CAUSA INDETERMINADA'
            action = 'Investigação adicional'
    else:
        verdict = 'FALHA NÃO REPRODUZIDA — erro não determinístico'
        action = 'Reproduzir com mais runs'
    
    print(f"\n    >>> VEREDITO: {verdict}")
    print(f"    >>> AÇÃO: {action}")
    
    # Salvar relatório
    report = {
        'metadata': {
            'experiment': 'AION-6.2.12 — B2 Provenance Failure Isolation',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'etapa_1_reproducao': reproduction,
        'etapa_2_classificacao': classifications,
        'etapa_3_origem': origin_analysis if 'origin_analysis' in dir() else {},
        'etapa_4_veredito': {
            'cause': cause,
            'correctable': correctable,
            'correction': correction,
            'verdict': verdict,
            'action': action,
        },
    }
    
    json_path = OUTPUT_DIR / 'aion_6_2_12_b2_provenance_isolation.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
