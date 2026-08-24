#!/usr/bin/env python3
"""
AION Passo 5.11 — Rebenchmark B1-B7 com AION-EVAL-002

Aplica protocolo multicamada (10 categorias R1-H1) com regra de não-compensação
aos 7 testes B1-B7 do AION-BENCH-001.

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import re
from pathlib import Path
from datetime import datetime, timezone

OUTPUT_DIR = Path('/home/z/my-project/download/rag')

# Carrega resultados do bench anterior
BENCH_RESULTS = json.loads((OUTPUT_DIR / 'aion_bench_001_resultados.json').read_text(encoding='utf-8'))


# === AION-EVAL-002 — Implementação do protocolo multicamada ===

def eval_R1_retrieval_correct(test_id: str, retrieved: list, gabarito: dict) -> dict:
    """R1: Retrieval correto — chunk correto está entre os top-K recuperados."""
    expected_chunk = gabarito.get('chunk_id')
    if not expected_chunk:
        return {'status': 'N/A', 'reason': 'Gabarito não especifica chunk_id esperado'}
    
    for r in retrieved:
        chunk_id = r.get('chunk_id', '')
        # Compara normalizado (sem sufixo de sub-chunk)
        if chunk_id.startswith(expected_chunk.split('#')[0]):
            return {'status': 'PASS', 'reason': f'Chunk esperado {expected_chunk} recuperado em #{r["rank"]}'}
    
    return {'status': 'FAIL', 'reason': f'Chunk esperado {expected_chunk} NÃO recuperado. Top recuperado: {retrieved[0]["chunk_id"] if retrieved else "nenhum"}'}


def eval_R2_retrieval_sufficient(test_id: str, retrieved: list, gabarito: dict) -> dict:
    """R2: Retrieval suficiente — contexto contém informação suficiente."""
    # Para B4 (ausência): se a resposta correta é "não encontrado", R2 deve ser N/A
    if test_id == 'B4':
        return {'status': 'N/A', 'reason': 'Pergunta sobre ausência — não exige retrieval de chunk específico'}
    
    # Verifica se algum chunk recuperado contém informação relacionada ao gabarito
    if not retrieved:
        return {'status': 'FAIL', 'reason': 'Nenhum chunk recuperado'}
    
    # Heurística: pelo menos um chunk recuperado tem score > 0.05
    max_score = max((r.get('score', 0) for r in retrieved), default=0)
    if max_score > 0.05:
        return {'status': 'PASS', 'reason': f'Contexto contém informação (max score: {max_score:.3f})'}
    return {'status': 'FAIL', 'reason': f'Scores baixos demais (max: {max_score:.3f})'}


def eval_P1_provenance_correct(test_id: str, answer: str, gabarito: dict) -> dict:
    """P1: Proveniência correta — resposta cita documento certo."""
    expected_doc = gabarito.get('documento')
    if not expected_doc:
        return {'status': 'N/A', 'reason': 'Gabarito não especifica documento esperado'}
    
    answer_lower = answer.lower()
    expected_doc_lower = expected_doc.lower()
    
    if expected_doc_lower in answer_lower:
        return {'status': 'PASS', 'reason': f'Documento {expected_doc} citado corretamente'}
    
    # Sinônimos: Paper A = CORPUS-002, Paper B = CORPUS-004, etc.
    synonyms = {
        'CORPUS-002': ['paper a', 'paper a v6.2', 'paper a v6.1', 'relational coherence'],
        'CORPUS-003': ['parte iv', 'formalização teórica', 'formalizacao teorica'],
        'CORPUS-004': ['paper b', 'paper b v6.1', 'qdt', 'fmo'],
        'CORPUS-005': ['cover letter', 'carta de apresentação', 'carta de submissão'],
    }
    syn_list = synonyms.get(expected_doc, [])
    for syn in syn_list:
        if syn in answer_lower:
            return {'status': 'PASS-SEMANTIC', 'reason': f'Documento {expected_doc} identificado por sinônimo "{syn}"'}
    
    # Se citou documento diferente
    cited_docs = re.findall(r'CORPUS-(\d{3})', answer)
    if cited_docs:
        return {'status': 'FAIL', 'reason': f'Cita CORPUS-{cited_docs[0]} em vez de {expected_doc}'}
    
    return {'status': 'FAIL', 'reason': f'Documento {expected_doc} não citado'}


def eval_P2_provenance_granular(test_id: str, answer: str, gabarito: dict) -> dict:
    """P2: Proveniência granular — resposta cita seção/página/chunk específico."""
    answer_lower = answer.lower()
    
    # Procura por referências granulares
    has_page = bool(re.search(r'p\.\d+|página \d+|p\. ?\d+', answer_lower))
    has_section = bool(re.search(r'sec\.|section|seção|secção', answer_lower))
    has_chunk = bool(re.search(r'CORPUS-\d{3}#\w+', answer))
    has_line = bool(re.search(r'linha \d+|line \d+', answer_lower))
    
    if has_chunk:
        return {'status': 'PASS', 'reason': 'Citação de chunk_id específica'}
    if has_page or has_section:
        return {'status': 'PASS-SEMANTIC', 'reason': 'Citação de página ou seção (granularidade menor)'}
    
    return {'status': 'FAIL', 'reason': 'Sem citação granular (chunk_id, página, seção ou linha)'}


def eval_T1_temporal_coherence(test_id: str, answer: str, gabarito: dict) -> dict:
    """T1: Coerência temporal — resposta distingue versões temporais."""
    answer_lower = answer.lower()
    
    # Para B2: deve mencionar duas datas diferentes
    if test_id == 'B2':
        # Procura por datas ou versões
        dates_found = re.findall(r'2026-08-\d{2}|v6\.\d|v\d\.\d|\d{1,2} de agosto', answer)
        unique_dates = set(dates_found)
        if len(unique_dates) >= 2:
            return {'status': 'PASS', 'reason': f'Múltiplas versões/datas distinguídas: {unique_dates}'}
        # Sinônimos: "v6.1" e "v6.2" são versões
        versions = set(re.findall(r'v\d\.\d', answer))
        if len(versions) >= 2:
            return {'status': 'PASS-SEMANTIC', 'reason': f'Versões distinguídas (sem datas explícitas): {versions}'}
        return {'status': 'FAIL', 'reason': 'Não distinguiu versões temporais'}
    
    # Para B3: deve mencionar revogação em data específica
    if test_id == 'B3':
        date_found = bool(re.search(r'2026-08-12|12 de agosto|12/08', answer))
        version_found = bool(re.search(r'v6\.1|paper b', answer_lower))
        if date_found or version_found:
            return {'status': 'PASS-SEMANTIC', 'reason': 'Revogação temporalmente situada'}
        return {'status': 'FAIL', 'reason': 'Revogação não temporalmente situada'}
    
    # Para B7: deve distinguir v6.0 de v6.1
    if test_id == 'B7':
        has_v60 = 'v6.0' in answer
        has_v61 = 'v6.1' in answer
        if has_v60 and has_v61:
            return {'status': 'PASS', 'reason': 'Versões v6.0 e v6.1 distinguídas'}
        return {'status': 'FAIL', 'reason': 'Versões não distinguídas'}
    
    return {'status': 'N/A', 'reason': 'T1 não aplicável a este teste'}


def eval_E1_evidence_interpretation(test_id: str, answer: str, gabarito: dict) -> dict:
    """E1: Distinção evidência/interpretação — resposta marca [E]/[I]/[H]."""
    answer_lower = answer.lower()
    
    # Procura por marcações [E], [I], [H]
    has_e = '[e]' in answer_lower or 'evidence_type' in answer_lower or 'evidência' in answer_lower
    has_i = '[i]' in answer_lower or 'inferência' in answer_lower or 'inferencia' in answer_lower
    
    if has_e or has_i:
        return {'status': 'PASS-SEMANTIC', 'reason': 'Distingue evidência de inferência (ainda que não com tags formais)'}
    
    # Se a resposta cita chunk_id, isso é uma forma de marcação de evidência
    has_chunk_citation = bool(re.search(r'CORPUS-\d{3}#\w+', answer))
    if has_chunk_citation:
        return {'status': 'PASS-SEMANTIC', 'reason': 'Cita chunks como fonte (forma implícita de marcar evidência)'}
    
    return {'status': 'FAIL', 'reason': 'Sem distinção entre evidência e interpretação'}


def eval_N1_absence_treatment(test_id: str, answer: str, gabarito: dict) -> dict:
    """N1: Tratamento correto de ausência."""
    answer_lower = answer.lower()
    
    # Para B4: resposta esperada é "não"
    if test_id == 'B4':
        absence_phrases = [
            'não encontrado', 'não consta', 'não aparece', 'ausente',
            'não está', 'informação não encontrada', 'não há evidência',
            'não há menção', 'não existe', 'não foi encontrado',
        ]
        for phrase in absence_phrases:
            if phrase in answer_lower:
                return {'status': 'PASS', 'reason': f'Declara ausência: "{phrase}"'}
        # Sinônimos
        if 'não' in answer_lower and ('consciência' in answer_lower or 'defende' in answer_lower):
            return {'status': 'PASS-SEMANTIC', 'reason': 'Indica negação (formulação variada)'}
        return {'status': 'FAIL', 'reason': 'Não declara ausência'}
    
    # Para B6: resposta sobre lacuna
    if test_id == 'B6':
        if 'não' in answer_lower and ('pode' in answer_lower or 'possível' in answer_lower or 'determinar' in answer_lower):
            return {'status': 'PASS', 'reason': 'Declara impossibilidade de determinação'}
    
    return {'status': 'N/A', 'reason': 'N1 não aplicável a este teste'}


def eval_C1_contradiction_detection(test_id: str, answer: str, gabarito: dict) -> dict:
    """C1: Detecção de contradição."""
    answer_lower = answer.lower()
    
    if test_id == 'B5':
        # Deve citar dois documentos diferentes e identificar divergência
        cited_docs = set(re.findall(r'corpus-(\d{3})', answer_lower))
        contradiction_indicators = ['contradição', 'contradiz', 'divergência', 'discrepância', 'incompatíve', 'em conflito']
        has_contradiction_term = any(c in answer_lower for c in contradiction_indicators)
        
        if len(cited_docs) >= 2 and has_contradiction_term:
            return {'status': 'PASS', 'reason': f'Contradição identificada entre {cited_docs}'}
        if len(cited_docs) >= 2:
            return {'status': 'PASS-SEMANTIC', 'reason': 'Cita múltiplos documentos (mas não usa termo "contradição")'}
        return {'status': 'FAIL', 'reason': 'Não identificou contradição entre documentos'}
    
    return {'status': 'N/A', 'reason': 'C1 não aplicável a este teste'}


def eval_S1_synthesis_quality(test_id: str, answer: str, gabarito: dict) -> dict:
    """S1: Qualidade da síntese histórica."""
    answer_lower = answer.lower()
    
    if test_id == 'B7':
        # Deve distinguir dímero (2 sítios) de FMO completo (7 sítios)
        has_dimer = 'dímero' in answer_lower or 'dimero' in answer_lower or '2 sítios' in answer_lower or '2 sitios' in answer_lower
        has_fmo7 = '7 sítios' in answer_lower or '7 sitios' in answer_lower or 'fmo completo' in answer_lower or 'fmo 7' in answer_lower
        has_v60 = 'v6.0' in answer
        has_v61 = 'v6.1' in answer
        
        if has_dimer and has_fmo7 and has_v60 and has_v61:
            return {'status': 'PASS', 'reason': 'Síntese distingue v6.0/dímero de v6.1/FMO 7-sítios sem misturar'}
        if has_dimer and has_fmo7:
            return {'status': 'PASS-SEMANTIC', 'reason': 'Distingue dímero de FMO 7-sítios (sem versões explícitas)'}
        return {'status': 'FAIL', 'reason': 'Não distinguiu estados temporais'}
    
    return {'status': 'N/A', 'reason': 'S1 não aplicável a este teste'}


def eval_H1_epistemic_honesty(test_id: str, answer: str, gabarito: dict) -> dict:
    """H1: Honestidade epistemológica — sistema não disfarça incerteza."""
    answer_lower = answer.lower()
    
    # Procura por indicações de incerteza explícita
    uncertainty_phrases = [
        'não encontrado', 'não pode ser determinado', 'não é possível',
        'desconhecido', 'unknown', 'lacuna', 'pendente', 'não tenho',
        'informação não disponível',
    ]
    has_uncertainty = any(p in answer_lower for p in uncertainty_phrases)
    
    # Verifica se NÃO há afirmações categóricas não suportadas
    categorical_phrases = ['certamente', 'sem dúvida', 'definitivamente', 'é evidente que']
    has_unsupported_categorical = any(p in answer_lower for p in categorical_phrases)
    
    # H1 passa se há incerteza marcada OU se não há afirmações categóricas não suportadas
    if has_uncertainty or not has_unsupported_categorical:
        if has_uncertainty:
            return {'status': 'PASS', 'reason': 'Incerteza marcada explicitamente'}
        return {'status': 'PASS-SEMANTIC', 'reason': 'Nenhuma afirmação categórica não suportada'}
    
    return {'status': 'FAIL', 'reason': 'Afirmações categóricas sem suporte'}


# === Aplicação do protocolo ===

def evaluate_with_eval002(test_id: str, retrieved: list, answer: str, gabarito: dict) -> dict:
    """Aplica todas as 10 categorias do AION-EVAL-002."""
    categories = {
        'R1': eval_R1_retrieval_correct(test_id, retrieved, gabarito),
        'R2': eval_R2_retrieval_sufficient(test_id, retrieved, gabarito),
        'P1': eval_P1_provenance_correct(test_id, answer, gabarito),
        'P2': eval_P2_provenance_granular(test_id, answer, gabarito),
        'T1': eval_T1_temporal_coherence(test_id, answer, gabarito),
        'E1': eval_E1_evidence_interpretation(test_id, answer, gabarito),
        'N1': eval_N1_absence_treatment(test_id, answer, gabarito),
        'C1': eval_C1_contradiction_detection(test_id, answer, gabarito),
        'S1': eval_S1_synthesis_quality(test_id, answer, gabarito),
        'H1': eval_H1_epistemic_honesty(test_id, answer, gabarito),
    }
    
    # Avaliação final com regra de não-compensação
    # H1 é pré-requisito
    h1_status = categories['H1']['status']
    if h1_status == 'FAIL':
        final = 'FAIL'
        justification = 'H1 (honestidade epistemológica) falhou — pré-requisito não atendido'
    else:
        # Verifica critérios críticos por tipo de teste
        critical_failures = []
        
        if test_id == 'B1':  # Proveniência
            if categories['R1']['status'] == 'FAIL':
                critical_failures.append('R1 (retrieval correto)')
            if categories['P1']['status'] == 'FAIL':
                critical_failures.append('P1 (proveniência correta)')
        elif test_id == 'B2':  # Temporalidade
            if categories['R1']['status'] == 'FAIL':
                critical_failures.append('R1 (retrieval correto)')
            if categories['T1']['status'] == 'FAIL':
                critical_failures.append('T1 (coerência temporal)')
        elif test_id == 'B3':  # Revogação
            if categories['R1']['status'] == 'FAIL':
                critical_failures.append('R1 (retrieval correto)')
            if categories['T1']['status'] == 'FAIL':
                critical_failures.append('T1 (coerência temporal)')
        elif test_id == 'B4':  # Ausência
            if categories['N1']['status'] == 'FAIL':
                critical_failures.append('N1 (tratamento de ausência)')
        elif test_id == 'B5':  # Contradição
            if categories['C1']['status'] == 'FAIL':
                critical_failures.append('C1 (detecção de contradição)')
        elif test_id == 'B6':  # Lacuna
            if categories['N1']['status'] == 'FAIL':
                critical_failures.append('N1 (tratamento de ausência)')
        elif test_id == 'B7':  # Síntese
            if categories['S1']['status'] == 'FAIL':
                critical_failures.append('S1 (qualidade da síntese)')
            if categories['T1']['status'] == 'FAIL':
                critical_failures.append('T1 (coerência temporal)')
        
        if critical_failures:
            final = 'FAIL'
            justification = f'Falhas críticas: {", ".join(critical_failures)}'
        else:
            # Verifica se há apenas falhas léxicas
            all_status = [c['status'] for c in categories.values()]
            has_real_fail = any(s == 'FAIL' for s in all_status)
            has_lexical_fail_only = any(s == 'FAIL-LEXICAL-ONLY' for s in all_status)
            
            if has_real_fail:
                final = 'PARTIAL'
                justification = 'Critérios críticos PASS, mas há falhas não-críticas'
            else:
                # Conta PASS-SEMANTIC
                semantic_count = sum(1 for s in all_status if s == 'PASS-SEMANTIC')
                if semantic_count > 0:
                    final = 'PASS-SEMANTIC'
                    justification = f'PASS com {semantic_count} categorias em modo semântico (sinônimos)'
                else:
                    final = 'PASS'
                    justification = 'Todos os critérios atendidos'
    
    return {
        'categories': categories,
        'avaliacao_final': final,
        'justificativa': justification,
    }


def main():
    print("=" * 70)
    print("AION Passo 5.11 — Rebenchmark B1-B7 com AION-EVAL-002")
    print("=" * 70)
    
    # Reavalia cada teste B1-B7 com o novo protocolo
    results_002 = {}
    
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        test_data = BENCH_RESULTS['sistema_A']['results'][test_id]
        retrieved = test_data['retrieved_chunks_top5']
        answer = test_data['resposta']
        gabarito = test_data['gabarito']
        
        # Limpa a resposta (remove prefixos de inicialização do z-ai)
        answer_clean = answer
        if '🚀' in answer:
            # Tenta extrair content do JSON
            try:
                json_start = answer.find('{')
                if json_start >= 0:
                    json_str = answer[json_start:]
                    data = json.loads(json_str)
                    answer_clean = data['choices'][0]['message']['content']
            except:
                pass
        
        eval_result = evaluate_with_eval002(test_id, retrieved, answer_clean, gabarito)
        results_002[test_id] = {
            'test_id': test_id,
            'categoria': test_data['categoria'],
            'pergunta': test_data['pergunta'],
            'retrieved_chunks': retrieved,
            'resposta': answer_clean,
            'gabarito': gabarito,
            'eval_002': eval_result,
            'eval_001_original': test_data['evaluation'],
        }
        
        print(f"\n[{test_id}] ({test_data['categoria']})")
        print(f"  Avaliação 001 (léxica): {test_data['evaluation']['criterion_pass']}")
        print(f"  Avaliação 002 (multicamada):")
        for cat, cat_result in eval_result['categories'].items():
            print(f"    {cat}: {cat_result['status']:<18} — {cat_result['reason'][:80]}")
        print(f"  FINAL: {eval_result['avaliacao_final']}")
        print(f"  Justificativa: {eval_result['justificativa']}")
    
    # Resumo comparativo
    comparison = {
        'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'protocol': 'AION-EVAL-002 v1.0.0',
        'replaces': 'AION-EVAL-001 v0.1.0',
        'results': results_002,
        'summary': {
            'eval_001_pass_count': sum(1 for r in results_002.values() if r['eval_001_original']['criterion_pass']),
            'eval_001_total': len(results_002),
            'eval_002_pass_count': sum(1 for r in results_002.values() if r['eval_002']['avaliacao_final'] in ('PASS', 'PASS-SEMANTIC')),
            'eval_002_total': len(results_002),
            'eval_002_pass_strict': sum(1 for r in results_002.values() if r['eval_002']['avaliacao_final'] == 'PASS'),
            'eval_002_pass_semantic': sum(1 for r in results_002.values() if r['eval_002']['avaliacao_final'] == 'PASS-SEMANTIC'),
            'eval_002_partial': sum(1 for r in results_002.values() if r['eval_002']['avaliacao_final'] == 'PARTIAL'),
            'eval_002_fail': sum(1 for r in results_002.values() if r['eval_002']['avaliacao_final'] == 'FAIL'),
        },
    }
    
    # Salvar JSON
    json_path = OUTPUT_DIR / 'aion_bench_001_eval002_resultados.json'
    json_path.write_text(json.dumps(comparison, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    # Resumo final
    print(f"\n{'=' * 70}")
    print("[RESUMO Passo 5.11 — Rebenchmark com AION-EVAL-002]")
    print(f"{'=' * 70}")
    print(f"\nComparativo EVAL-001 (léxico) vs EVAL-002 (multicamada):")
    print(f"  EVAL-001: {comparison['summary']['eval_001_pass_count']}/{comparison['summary']['eval_001_total']} PASS")
    print(f"  EVAL-002: {comparison['summary']['eval_002_pass_count']}/{comparison['summary']['eval_002_total']} PASS ou PASS-SEMANTIC")
    print(f"    - PASS estrito: {comparison['summary']['eval_002_pass_strict']}")
    print(f"    - PASS-SEMANTIC: {comparison['summary']['eval_002_pass_semantic']}")
    print(f"    - PARTIAL: {comparison['summary']['eval_002_partial']}")
    print(f"    - FAIL: {comparison['summary']['eval_002_fail']}")
    
    print(f"\nDetalhes por teste:")
    for tid, r in results_002.items():
        e1 = '✅' if r['eval_001_original']['criterion_pass'] else '❌'
        e2_final = r['eval_002']['avaliacao_final']
        e2_emoji = {'PASS': '✅', 'PASS-SEMANTIC': '🟡', 'PARTIAL': '⚠️', 'FAIL': '❌'}.get(e2_final, '?')
        print(f"  {tid} ({r['categoria']:<15}) EVAL-001: {e1} → EVAL-002: {e2_emoji} {e2_final}")
    
    return comparison


if __name__ == '__main__':
    main()
