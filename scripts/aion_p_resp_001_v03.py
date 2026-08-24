#!/usr/bin/env python3
"""
AION Passo 5.13.2 — P-RESP-001 v0.3 com Validator Determinístico

Validator pós-geração que elimina fabricação de chunk_id:
- REGRA V1: ID deve existir no corpus (CORPUS_INDEX)
- REGRA V2: ID deve estar entre chunks recuperados (RETRIEVED_CHUNKS)
- REGRA V3: Interseção obrigatória (V1 AND V2)

3 categorias de evidência:
- [EVIDENCE_VALID] — existe evidência, chunk é recuperado
- [EVIDENCE_ABSENT] — não existe evidência disponível
- [PROVENANCE_INVALID] — sistema tentou atribuir fonte, mas fonte não pode ser validada

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import sys
import re
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

from aion_rag_proxy import TfidfVectorStore, CORPUS_FILES, CORPUS_DIR, parse_extracted_markdown
from aion_bench_001 import BENCH_TESTS
from aion_p_resp_001_v02 import (
    P_RESP_001_V02_SYSTEM_PROMPT, CONTROL_SYSTEM_PROMPT,
    evaluate_with_eval002_v02, generate_answer, clean_answer,
)

OUTPUT_DIR = Path('/home/z/my-project/download/rag')


# === Validator P-RESP v0.3 — Determinístico ===

class ProvenanceValidator:
    """Validator determinístico que elimina fabricação de chunk_id."""
    
    def __init__(self, all_chunks: list):
        # Constrói índice de chunks existentes no corpus (CORPUS_INDEX)
        self.corpus_index = {c.chunk_id for c in all_chunks}
        # Mapeia prefixo de documento (CORPUS-XXX) -> lista de chunk_ids
        self.doc_to_chunks = {}
        for c in all_chunks:
            doc_match = re.match(r'(CORPUS-\d{3})', c.chunk_id)
            if doc_match:
                doc = doc_match.group(1)
                if doc not in self.doc_to_chunks:
                    self.doc_to_chunks[doc] = []
                self.doc_to_chunks[doc].append(c.chunk_id)
    
    def validate_response(self, answer: str, retrieved_chunks: list) -> dict:
        """
        Valida todos os chunk_ids citados na resposta.
        Retorna:
        - answer_cleaned: resposta com IDs inválidos marcados como [PROVENANCE_INVALID]
        - validation_log: log de cada ID citado e seu status
        - invalid_count: número de IDs inválidos
        - valid_count: número de IDs válidos
        - has_invalid_provenance: True se houve qualquer ID inválido
        """
        retrieved_set = {r.get('chunk_id', '') for r in retrieved_chunks}
        
        # Encontra todos os chunk_ids citados na resposta
        cited_ids = re.findall(r'CORPUS-\d{3}#\w+', answer)
        unique_cited = list(set(cited_ids))
        
        validation_log = []
        answer_cleaned = answer
        invalid_count = 0
        valid_count = 0
        
        for cid in unique_cited:
            exists_in_corpus = cid in self.corpus_index
            was_retrieved = cid in retrieved_set
            
            # REGRA V3: interseção obrigatória
            is_valid = exists_in_corpus and was_retrieved
            
            validation_log.append({
                'chunk_id': cid,
                'exists_in_corpus': exists_in_corpus,
                'was_retrieved': was_retrieved,
                'is_valid': is_valid,
                'action': 'PRESERVAR' if is_valid else 'REJEITAR',
            })
            
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                # Substitui o ID inválido por [PROVENANCE_INVALID]
                answer_cleaned = answer_cleaned.replace(cid, '[PROVENANCE_INVALID]')
        
        return {
            'answer_cleaned': answer_cleaned,
            'validation_log': validation_log,
            'invalid_count': invalid_count,
            'valid_count': valid_count,
            'has_invalid_provenance': invalid_count > 0,
            'evidence_category': self.classify_evidence(answer_cleaned, valid_count, invalid_count),
        }
    
    def classify_evidence(self, answer: str, valid_count: int, invalid_count: int) -> str:
        """
        Classifica a resposta em uma das 3 categorias:
        - EVIDENCE_VALID: existe evidência, chunk é recuperado (valid_count > 0)
        - EVIDENCE_ABSENT: não existe evidência disponível (nem valid nem invalid)
        - PROVENANCE_INVALID: sistema tentou atribuir fonte, mas fonte não pode ser validada
        """
        if invalid_count > 0:
            return 'PROVENANCE_INVALID'
        if valid_count > 0:
            return 'EVIDENCE_VALID'
        # Nem valid nem invalid — verificar se declarou ausência
        answer_lower = answer.lower()
        absence_indicators = [
            'informação não encontrada', 'não encontrado', '[absent]',
            'ausente', 'não há chunk', 'sem fonte', 'lacuna',
        ]
        if any(p in answer_lower for p in absence_indicators):
            return 'EVIDENCE_ABSENT'
        # Sem citações e sem declaração de ausência — ambíguo
        return 'EVIDENCE_ABSENT'  # default conservador


# === Sistema B v0.3: LLM + Validator ===

def run_test_with_validator(test_id: str, store, validator, system_prompt: str, system_name: str) -> dict:
    """Executa teste com validator pós-geração."""
    test = BENCH_TESTS[test_id]
    
    # Retrieval
    retrieved = store.query(test['pergunta'], top_k=8)
    retrieved_for_eval = [
        {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
        for i, r in enumerate(retrieved)
    ]
    
    # System extra (igual ao v0.2)
    system_extra = ""
    if test_id == 'B2':
        temporal_data = json.loads((OUTPUT_DIR / 'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
        temporal_context = json.dumps(temporal_data['states'][:5], ensure_ascii=False, indent=2)[:2000]
        system_extra = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{temporal_context}"
    elif test_id == 'B6':
        hist_data = json.loads((OUTPUT_DIR / 'aion_hist_001_reconciliacao.json').read_text(encoding='utf-8'))
        negative_context = json.dumps(hist_data['negative_memory']['DESCONHECIDO'], ensure_ascii=False, indent=2)[:2000]
        system_extra = f"\n\nMEMÓRIA NEGATIVA:\n{negative_context}"
    
    # Geração LLM
    t_start = time.time()
    answer_raw = generate_answer(test['pergunta'], retrieved[:5], system_prompt, system_extra)
    t_elapsed = time.time() - t_start
    answer_clean = clean_answer(answer_raw)
    
    # VALIDATOR PÓS-GERAÇÃO (v0.3 — novo)
    validation_result = validator.validate_response(answer_clean, retrieved_for_eval)
    answer_final = validation_result['answer_cleaned']
    
    # Avaliação com AION-EVAL-002 v0.2 (igual ao v0.2, mas sobre resposta validada)
    eval_result = evaluate_with_eval002_v02(test_id, retrieved_for_eval, answer_final, test['gabarito'])
    
    return {
        'test_id': test_id,
        'categoria': test['categoria'],
        'pergunta': test['pergunta'],
        'resposta_raw': answer_clean,
        'resposta_final_apos_validacao': answer_final,
        'tempo_segundos': round(t_elapsed, 2),
        'retrieved_chunks_top5': retrieved_for_eval[:5],
        'validation_log': validation_result['validation_log'],
        'invalid_count': validation_result['invalid_count'],
        'valid_count': validation_result['valid_count'],
        'has_invalid_provenance': validation_result['has_invalid_provenance'],
        'evidence_category': validation_result['evidence_category'],
        'eval_002_v02': eval_result,
        'gabarito': test['gabarito'],
        'sistema': system_name,
    }


def main():
    print("=" * 70)
    print("AION Passo 5.13.2 — P-RESP-001 v0.3 com Validator Determinístico")
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
    
    # Inicializa validator
    print("\n[SETUP] Inicializando ProvenanceValidator v0.3...")
    validator = ProvenanceValidator(all_chunks)
    print(f"  CORPUS_INDEX: {len(validator.corpus_index)} chunks")
    print(f"  Documentos mapeados: {list(validator.doc_to_chunks.keys())}")
    
    # Executa Controle (Sistema A — sem validator, prompt de controle)
    print("\n[SISTEMA A — Controle (sem validator)] Executando B1-B7...")
    results_A = {}
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        # Para controle: usa prompt de controle + sem validator
        test = BENCH_TESTS[test_id]
        retrieved = store.query(test['pergunta'], top_k=8)
        retrieved_for_eval = [
            {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
            for i, r in enumerate(retrieved)
        ]
        system_extra = ""
        if test_id == 'B2':
            temporal_data = json.loads((OUTPUT_DIR / 'aion_temporal_graph_v1.0.json').read_text(encoding='utf-8'))
            temporal_context = json.dumps(temporal_data['states'][:5], ensure_ascii=False, indent=2)[:2000]
            system_extra = f"\n\nCONTEXTO TEMPORAL ADICIONAL:\n{temporal_context}"
        elif test_id == 'B6':
            hist_data = json.loads((OUTPUT_DIR / 'aion_hist_001_reconciliacao.json').read_text(encoding='utf-8'))
            negative_context = json.dumps(hist_data['negative_memory']['DESCONHECIDO'], ensure_ascii=False, indent=2)[:2000]
            system_extra = f"\n\nMEMÓRIA NEGATIVA:\n{negative_context}"
        
        t_start = time.time()
        answer = generate_answer(test['pergunta'], retrieved[:5], CONTROL_SYSTEM_PROMPT, system_extra)
        t_elapsed = time.time() - t_start
        answer_clean = clean_answer(answer)
        
        # Para controle: SEM validator
        eval_result = evaluate_with_eval002_v02(test_id, retrieved_for_eval, answer_clean, test['gabarito'])
        
        results_A[test_id] = {
            'test_id': test_id,
            'categoria': test['categoria'],
            'pergunta': test['pergunta'],
            'resposta': answer_clean,
            'tempo_segundos': round(t_elapsed, 2),
            'retrieved_chunks_top5': retrieved_for_eval[:5],
            'eval_002_v02': eval_result,
            'gabarito': test['gabarito'],
            'sistema': 'A (controle, sem validator)',
            'validator_aplicado': False,
        }
        print(f"  {test_id}: {eval_result['avaliacao_final']}")
    
    # Executa P-RESP-001 v0.3 (Sistema B — prompt v0.2 + validator)
    print("\n[SISTEMA B — P-RESP-001 v0.3 (prompt v0.2 + validator)] Executando B1-B7...")
    results_B = {}
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        result = run_test_with_validator(
            test_id, store, validator,
            P_RESP_001_V02_SYSTEM_PROMPT,
            'B (P-RESP-001 v0.3: prompt v0.2 + validator)'
        )
        results_B[test_id] = result
        print(f"  {test_id}: {result['eval_002_v02']['avaliacao_final']} | evidence={result['evidence_category']} | invalid={result['invalid_count']} valid={result['valid_count']}")
    
    # === MATRIZ COMPARATIVA v0.3 ===
    print(f"\n{'=' * 120}")
    print("[MATRIZ COMPARATIVA v0.3 — Controle × P-RESP-001 v0.3]")
    print(f"{'=' * 120}")
    print(f"\n{'Teste':<6} {'Categoria':<15} {'A (controle)':<22} {'B (v0.3)':<22} {'Variação':<15} {'Evidence Cat':<18} {'Invalid IDs'}")
    print('-' * 120)
    
    hierarchy = {'PASS': 5, 'PASS-SEMANTIC': 4, 'PARTIAL': 3, 'FAIL-EVALUATOR': 2, 'FAIL-MIXED': 1, 'FAIL-SYSTEM': 0}
    
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        a_status = results_A[test_id]['eval_002_v02']['avaliacao_final']
        b_status = results_B[test_id]['eval_002_v02']['avaliacao_final']
        cat = results_A[test_id]['categoria']
        b_evidence = results_B[test_id].get('evidence_category', 'N/A')
        b_invalid = results_B[test_id].get('invalid_count', 0)
        
        diff = hierarchy.get(b_status, 0) - hierarchy.get(a_status, 0)
        if diff > 0:
            variation = '↑ MELHOROU'
        elif diff < 0:
            variation = '↓ REGREDIU'
        else:
            variation = '= (mantido)'
        
        a_emoji = {'PASS': '✅', 'PASS-SEMANTIC': '🟡', 'PARTIAL': '⚠️', 'FAIL-EVALUATOR': '🔵', 'FAIL-MIXED': '🟣', 'FAIL-SYSTEM': '❌'}.get(a_status, '?')
        b_emoji = {'PASS': '✅', 'PASS-SEMANTIC': '🟡', 'PARTIAL': '⚠️', 'FAIL-EVALUATOR': '🔵', 'FAIL-MIXED': '🟣', 'FAIL-SYSTEM': '❌'}.get(b_status, '?')
        
        print(f"{test_id:<6} {cat:<15} {a_emoji} {a_status:<19} {b_emoji} {b_status:<19} {variation:<15} {b_evidence:<18} {b_invalid}")
    
    # === LOG DE PROVENANCE PRODUZIDA/VALIDADA/REJEITADA ===
    print(f"\n{'=' * 120}")
    print("[LOG DE PROVENANCE — Sistema B v0.3]")
    print(f"{'=' * 120}")
    
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        result = results_B[test_id]
        log = result.get('validation_log', [])
        if log:
            print(f"\n[{test_id}] — {result['categoria']}")
            for entry in log:
                status = '✅ VÁLIDO' if entry['is_valid'] else '❌ INVÁLIDO'
                reasons = []
                if not entry['exists_in_corpus']:
                    reasons.append('não existe no corpus')
                if not entry['was_retrieved']:
                    reasons.append('não estava nos retrieved chunks')
                reason_str = ', '.join(reasons) if reasons else 'OK'
                print(f"  {entry['chunk_id']:<35} {status:<10} | {reason_str}")
        else:
            print(f"\n[{test_id}] — Nenhum chunk_id citado")
    
    # === B5 — DETALHE COMPLETO (foco do experimento) ===
    print(f"\n{'=' * 120}")
    print("[DETALHE B5 — Foco do experimento]")
    print(f"{'=' * 120}")
    
    b5 = results_B['B5']
    print(f"\nID(s) produzido(s) pelo LLM:")
    for entry in b5.get('validation_log', []):
        print(f"  - {entry['chunk_id']}")
        print(f"    Existe no corpus?      {'SIM' if entry['exists_in_corpus'] else 'NÃO'}")
        print(f"    Estava retrieved?      {'SIM' if entry['was_retrieved'] else 'NÃO'}")
        print(f"    Proveniência válida?   {'SIM' if entry['is_valid'] else 'NÃO'}")
        print(f"    Ação do validator:     {entry['action']}")
    
    print(f"\nResposta APÓS validação (primeiros 1000 chars):")
    print(b5['resposta_final_apos_validacao'][:1000])
    
    # === CRITÉRIOS DE APROVAÇÃO v0.3 ===
    print(f"\n{'=' * 120}")
    print("[CRITÉRIOS DE APROVAÇÃO v0.3]")
    print(f"{'=' * 120}")
    
    criteria = {
        '1_zero_provenance_inventada': all(
            results_B[tid].get('invalid_count', 0) == 0
            for tid in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
        ),
        '2_B5_sem_id_inexistente': results_B['B5'].get('invalid_count', 0) == 0,
        '3_nenhum_id_real_nao_recuperado': all(
            not any(
                (entry['exists_in_corpus'] and not entry['was_retrieved'])
                for entry in results_B[tid].get('validation_log', [])
            )
            for tid in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
        ),
        '4_B6_respeita_ausencia': (
            results_B['B6'].get('evidence_category') == 'EVIDENCE_ABSENT' or
            results_B['B6'].get('evidence_category') == 'EVIDENCE_VALID'
        ),
        '5_H1_PASS_em_todos': all(
            results_B[tid]['eval_002_v02']['categories']['H1']['status'] in ('PASS', 'PASS-SEMANTIC')
            for tid in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
        ),
        '6_B2_B4_nao_regrediram': (
            hierarchy.get(results_B['B2']['eval_002_v02']['avaliacao_final'], 0) >= 
            hierarchy.get(results_A['B2']['eval_002_v02']['avaliacao_final'], 0)
        ) and (
            hierarchy.get(results_B['B4']['eval_002_v02']['avaliacao_final'], 0) >= 
            hierarchy.get(results_A['B4']['eval_002_v02']['avaliacao_final'], 0)
        ),
        '7_B1_B3_FAIL_SYSTEM_nao_mascarado': (
            results_B['B1']['eval_002_v02']['avaliacao_final'] == 'FAIL-SYSTEM' and
            results_B['B3']['eval_002_v02']['avaliacao_final'] == 'FAIL-SYSTEM'
        ),
    }
    
    for c, passed in criteria.items():
        print(f"  {'✅' if passed else '❌'} {c}")
    
    pass_count = sum(criteria.values())
    total = len(criteria)
    print(f"\nTotal: {pass_count}/{total}")
    
    # Veredito
    if pass_count == total:
        verdict = 'P-RESP-001 v0.3 APROVADO'
        decision = 'MVP ESTABILIZADO — Passo 6 (Dify) liberado'
    elif pass_count >= 5:
        verdict = 'P-RESP-001 v0.3 PARCIALMENTE APROVADO'
        decision = 'Incorporar com ressalvas — Passo 6 ainda bloqueado'
    else:
        verdict = 'P-RESP-001 v0.3 REJEITADO'
        decision = 'MVP NÃO estabilizado — investigar falha específica'
    
    print(f"\n[VEREDITO] {verdict}")
    print(f"[DECISÃO] {decision}")
    
    # Salva relatório completo
    report = {
        'metadata': {
            'experiment': 'P-RESP-001 v0.3 com Validator Determinístico',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'validator_rules': {
            'V1_existence': 'Todo chunk_id citado deve existir no corpus (CORPUS_INDEX)',
            'V2_retrieval': 'Todo chunk_id citado deve estar entre retrieved chunks',
            'V3_intersection': 'Válido = V1 AND V2',
            'no_silent_substitution': 'IDs inválidos são substituídos por [PROVENANCE_INVALID], não por IDs alternativos',
        },
        'evidence_categories': {
            'EVIDENCE_VALID': 'Existe evidência e chunk é recuperado',
            'EVIDENCE_ABSENT': 'Não existe evidência disponível no contexto',
            'PROVENANCE_INVALID': 'Sistema tentou atribuir fonte, mas fonte não pode ser validada',
        },
        'sistema_A_controle': {
            'description': 'Prompt controle, sem validator',
            'results': results_A,
        },
        'sistema_B_v03': {
            'description': 'Prompt v0.2 + Validator determinístico pós-geração',
            'results': results_B,
            'provenance_log': {tid: results_B[tid].get('validation_log', []) for tid in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']},
        },
        'criteria_evaluation': criteria,
        'pass_count': pass_count,
        'total_count': total,
        'verdict': verdict,
        'decision': decision,
    }
    
    json_path = OUTPUT_DIR / 'aion_p_resp_001_v03_resultados.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
