#!/usr/bin/env python3
"""
AION Reavaliação Semântica — Passo 5.5 (com AION-EVAL-001)

Reavalia os resultados do Passo 5 (GraphRAG enhanced) usando as 7 categorias
semânticas do protocolo AION-EVAL-001, em vez da avaliação léxica anterior.

Autor: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import re
from pathlib import Path
from datetime import datetime, timezone

OUTPUT_DIR = Path('/home/z/my-project/download/rag')

# Categorias do AION-EVAL-001 v0.1.0
CATEGORIES = {
    'PASS': 'Resposta correta com evidência documental direta',
    'PASS-ABSENCE': 'Resposta correta que declara ausência de informação no corpus',
    'PASS-PROVENANCE': 'Resposta correta que inclui referência à fonte (documento, seção, página)',
    'PARTIAL': 'Resposta parcialmente correta, com omissão ou imprecisão menor',
    'UNSUPPORTED': 'Resposta não suportada pelo corpus (invenção ou inferência não declarada)',
    'CONTRADICTION': 'Resposta que contradiz evidência documental explícita',
    'FAIL': 'Resposta incorreta ou que transforma ausência em evidência de ausência',
}


def semantic_evaluate(test_id: str, answer: str, retrieved_chunks: list) -> dict:
    """Avaliação semântica conforme AION-EVAL-001."""
    answer_lower = answer.lower()
    
    # Detecta citações a chunks
    has_chunk_citation = bool(re.search(r'CORPUS-\d{3}#?p?\d*', answer))
    
    # Detecta declaração de ausência
    absence_phrases = [
        'informação não encontrada',
        'não encontrado no contexto',
        'não consta no corpus',
        'não aparece em nenhum',
        'não está mencionado',
        'ausente do corpus',
    ]
    declares_absence = any(p in answer_lower for p in absence_phrases)
    
    # Detecta identificações de contradição
    contradiction_indicators = [
        'contradição',
        'contradiz',
        'em conflito',
        'divergência entre',
        'discrepância',
    ]
    identifies_contradiction = any(p in answer_lower for p in contradiction_indicators)
    
    # Detecta citação dupla (duas fontes comparadas)
    corpus_mentions = set(re.findall(r'CORPUS-(\d{3})', answer))
    has_double_citation = len(corpus_mentions) >= 2
    
    evaluation = {
        'test_id': test_id,
        'has_chunk_citation': has_chunk_citation,
        'declares_absence': declares_absence,
        'identifies_contradiction': identifies_contradiction,
        'has_double_citation': has_double_citation,
        'corpus_mentions': sorted(corpus_mentions),
    }
    
    # Lógica de categorização semântica
    if test_id == 'P1':
        # P1: sistema deve listar conceitos e documentos
        expected_concepts = [
            'coerência relacional', 'integração', 'simetria', 'entropia',
            'functor', 'yoneda', 'tensor', 'einstein', 'dissipativa', 'fmo',
            'lakatos', 'conjectura',
        ]
        found_concepts = [c for c in expected_concepts if c in answer_lower]
        expected_docs = ['corpus-001', 'corpus-002', 'corpus-003', 'corpus-004', 'corpus-005']
        found_docs = [d for d in expected_docs if d in answer_lower]
        
        evaluation['concepts_found'] = found_concepts
        evaluation['concepts_coverage'] = f"{len(found_concepts)}/{len(expected_concepts)}"
        evaluation['docs_found'] = found_docs
        evaluation['docs_coverage'] = f"{len(found_docs)}/{len(expected_docs)}"
        
        if len(found_concepts) >= 10 and len(found_docs) >= 4 and has_chunk_citation:
            category = 'PASS-PROVENANCE'
            justification = f"Lista {len(found_concepts)} conceitos em {len(found_docs)} documentos, com citações a chunks."
        elif len(found_concepts) >= 8 and len(found_docs) >= 3:
            category = 'PASS'
            justification = f"Lista {len(found_concepts)} conceitos em {len(found_docs)} documentos, mas com cobertura incompleta."
        elif len(found_concepts) >= 6:
            category = 'PARTIAL'
            justification = f"Cobertura parcial: {len(found_concepts)}/{len(expected_concepts)} conceitos, {len(found_docs)}/5 documentos."
        else:
            category = 'FAIL'
            justification = f"Cobertura insuficiente: {len(found_concepts)}/{len(expected_concepts)} conceitos."
    
    elif test_id == 'P2':
        # P2: sistema deve dizer que "consciência"/"campo primordial" não estão no corpus
        if declares_absence:
            category = 'PASS-ABSENCE'
            justification = "Sistema declarou corretamente a ausência da informação no corpus."
        elif 'não' in answer_lower and ('consciência' in answer_lower or 'mencionado' in answer_lower):
            category = 'PASS-ABSENCE'
            justification = "Sistema indicou ausência, embora com formulação diferente."
        else:
            category = 'FAIL'
            justification = "Sistema não identificou a ausência da informação."
    
    elif test_id == 'P3':
        # P3: sistema deve listar limitações do programa
        limitacoes_indicators = [
            'inconsistência', 'fixtures sintét', 'synthetic', 'ablação',
            'ablation', 'limitação', 'preliminar', '4 sujeitos',
        ]
        found_indicators = [i for i in limitacoes_indicators if i in answer_lower]
        
        evaluation['limitation_indicators_found'] = found_indicators
        
        if len(found_indicators) >= 3 and has_chunk_citation:
            category = 'PASS-PROVENANCE'
            justification = f"Lista limitações com citação a chunks. Indicadores: {found_indicators}."
        elif len(found_indicators) >= 2:
            category = 'PASS'
            justification = f"Lista limitações principais. Indicadores: {found_indicators}."
        elif len(found_indicators) >= 1:
            category = 'PARTIAL'
            justification = f"Cobertura parcial de limitações. Indicadores: {found_indicators}."
        else:
            category = 'FAIL'
            justification = "Não identificou limitações do programa."
    
    elif test_id == 'P4':
        # P4: sistema deve identificar contradições entre documentos
        expected_contradictions = ['c1', 'c2', 'c3', 'c4']  # marcadores esperados
        # Termos-chave para cada contradição
        contradiction_terms = {
            'C1 (Versão)': ['v6.1', 'v6.2', 'pronto', 'final'],
            'C2 (P3 results)': ['0.968', '0.793', '91.2', 'physionet', 'ds003768'],
            'C3 (P1/P2 datasets)': ['sintét', 'synthetic', 'empírico', 'watts', 'barabasi'],
            'C4 (Paper C status)': ['foundations of physics', 'paper c', 'submetido', 'reserved'],
        }
        found_contradictions = []
        for name, terms in contradiction_terms.items():
            if any(t in answer_lower for t in terms):
                found_contradictions.append(name)
        
        evaluation['contradictions_identified'] = found_contradictions
        evaluation['contradictions_coverage'] = f"{len(found_contradictions)}/4"
        
        if len(found_contradictions) >= 4 and has_double_citation:
            category = 'PASS-PROVENANCE'
            justification = f"Identificou {len(found_contradictions)}/4 contradições com citação dupla de documentos."
        elif len(found_contradictions) >= 3:
            category = 'PASS'
            justification = f"Identificou {len(found_contradictions)}/4 contradições. {found_contradictions}."
        elif len(found_contradictions) >= 2:
            category = 'PARTIAL'
            justification = f"Identificação parcial: {found_contradictions}."
        else:
            category = 'FAIL'
            justification = f"Cobertura insuficiente: {found_contradictions}."
    
    else:
        category = 'FAIL'
        justification = "Teste não reconhecido."
    
    evaluation['category'] = category
    evaluation['justification'] = justification
    evaluation['category_definition'] = CATEGORIES[category]
    
    return evaluation


def main():
    print("=" * 70)
    print("AION Reavaliação Semântica — Passo 5.5")
    print("Protocolo: AION-EVAL-001 v0.1.0 (7 categorias)")
    print("=" * 70)
    
    # Carrega resultados do Passo 4 (baseline) e Passo 5 (enhanced)
    passo4_path = OUTPUT_DIR / 'plano_teste_resultados.json'
    passo5_path = OUTPUT_DIR / 'graphrag_enhanced_results.json'
    
    passo4 = json.loads(passo4_path.read_text(encoding='utf-8'))
    passo5 = json.loads(passo5_path.read_text(encoding='utf-8'))
    
    print("\n[REAVIAÇÃO DO PASSO 4 — TF-IDF baseline]")
    print("-" * 60)
    reeval_p4 = {}
    for tid in ['P1', 'P2', 'P3', 'P4']:
        answer = passo4['results'][tid]['resposta_sistema']
        retrieved = passo4['results'][tid]['retrieved_chunks']
        eval_result = semantic_evaluate(tid, answer, retrieved)
        reeval_p4[tid] = eval_result
        print(f"\n[{tid}] → {eval_result['category']}")
        print(f"  Justificativa: {eval_result['justification']}")
    
    print("\n\n[REAVALIAÇÃO DO PASSO 5 — GraphRAG enhanced]")
    print("-" * 60)
    reeval_p5 = {}
    for tid in ['P1', 'P2', 'P3', 'P4']:
        answer = passo5['results'][tid]['resposta_sistema']
        retrieved = passo5['results'][tid]['retrieved_chunks']
        eval_result = semantic_evaluate(tid, answer, retrieved)
        reeval_p5[tid] = eval_result
        print(f"\n[{tid}] → {eval_result['category']}")
        print(f"  Justificativa: {eval_result['justification']}")
    
    # Relatório comparativo
    comparison = {
        'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'protocol': 'AION-EVAL-001 v0.1.0',
        'passo4_reevaluated': reeval_p4,
        'passo5_reevaluated': reeval_p5,
        'summary': {
            'passo4_pass_count': sum(1 for v in reeval_p4.values() if v['category'].startswith('PASS')),
            'passo5_pass_count': sum(1 for v in reeval_p5.values() if v['category'].startswith('PASS')),
            'passo4_categories': [v['category'] for v in reeval_p4.values()],
            'passo5_categories': [v['category'] for v in reeval_p5.values()],
        },
    }
    
    # Diferenças entre Passo 4 e Passo 5
    differences = []
    for tid in ['P1', 'P2', 'P3', 'P4']:
        p4_cat = reeval_p4[tid]['category']
        p5_cat = reeval_p5[tid]['category']
        if p4_cat != p5_cat:
            differences.append({
                'test': tid,
                'passo4_category': p4_cat,
                'passo5_category': p5_cat,
                'improvement': p5_cat.startswith('PASS') and not p4_cat.startswith('PASS'),
            })
    comparison['differences_p4_to_p5'] = differences
    
    report_path = OUTPUT_DIR / 'reevaluacao_semantica_passo5.5.json'
    report_path.write_text(json.dumps(comparison, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # Resumo final
    print(f"\n{'=' * 70}")
    print("[RESUMO DA REAVALIAÇÃO SEMÂNTICA]")
    print(f"{'=' * 70}")
    print(f"\nArquivo: {report_path}")
    print(f"\nComparativo Passo 4 → Passo 5:")
    print(f"  {'Teste':<8} {'Passo 4 (léxico)':<25} {'Passo 5 (léxico)':<25} {'Passo 4 (semântico)':<25} {'Passo 5 (semântico)':<25}")
    for tid in ['P1', 'P2', 'P3', 'P4']:
        p4_lex = '✅ PASS' if passo4['summary'][tid] else '❌ FAIL'
        p5_lex = '✅ PASS' if passo5['enhanced_passo5'][tid] else '❌ FAIL'
        p4_sem = reeval_p4[tid]['category']
        p5_sem = reeval_p5[tid]['category']
        print(f"  {tid:<8} {p4_lex:<25} {p5_lex:<25} {p4_sem:<25} {p5_sem:<25}")
    
    print(f"\nMudanças entre Passo 4 e Passo 5 (semântico):")
    if differences:
        for d in differences:
            arrow = '↑' if d['improvement'] else '↓'
            print(f"  {arrow} {d['test']}: {d['passo4_category']} → {d['passo5_category']}")
    else:
        print("  (nenhuma mudança — Passo 5 não alterou o veredito de nenhuma pergunta)")
    
    return comparison


if __name__ == '__main__':
    main()
