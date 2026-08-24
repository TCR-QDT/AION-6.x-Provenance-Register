#!/usr/bin/env python3
"""
AION Passo 6.2.8 — Auditoria do Gabarito B1 + Análise lexical PT-BR ↔ EN

Etapa 1: AUDITORIA DO GABARITO B1
  - Encontrar todas as ocorrências de "C = I × S × H^β" no corpus v1.3.0
  - Para cada ocorrência: chunk, contexto, primariedade da evidência
  - Determinar se CORPUS-002#p1_01 é o único gabarito válido ou se há conjunto equivalente

Etapa 2: ANÁLISE LEXICAL PT-BR ↔ EN
  - Comparar termos da pergunta B1 vs textos-alvo
  - Mapear correspondências semânticas que TF-IDF não captura

NÃO altera: corpus, GraphRAG, P-RESP-001, AION-EVAL-002, gabarito
NÃO combina experimentos ainda

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')

from aion_rag_proxy import parse_extracted_markdown
from aion_6_1_f_rebenchmark_lcr import CORPUS_V13_FILES

OUTPUT_DIR = Path('/home/z/my-project/download/rag')

B1_PERGUNTA = "Qual é a fonte exata da afirmação de que a métrica TCR é C = I × S × H^β?"

# Padrões para detectar a fórmula da métrica TCR
FORMULA_PATTERNS = [
    r'C\s*=\s*I\s*[×x]\s*S\s*[×x]\s*H\s*β',  # C = I × S × Hβ (Unicode)
    r'C\s*=\s*I\s*\*\s*S\s*\*\s*H\s*β',  # C = I * S * Hβ (ASCII)
    r'C\s*=\s*I\s*[×x]\s*S\s*[×x]\s*H\^?\s*β',  # C = I × S × H^β
    r'\\mathcal\{C\}\s*=\s*I\s*\\times\s*S\s*\\times\s*H',  # LaTeX
    r'Relational Coherence Theory.*metric',  # descrição textual
    r'metric.*C.*=.*I.*S.*H',  # variação
    r'TCR.*metric',  # referência textual
]


def build_all_chunks():
    """Constrói lista de todos os chunks do corpus v1.3.0."""
    all_chunks = []
    for filename, meta in CORPUS_V13_FILES.items():
        path = meta['path']
        if not path.exists():
            continue
        md_text = path.read_text(encoding='utf-8')
        chunks = parse_extracted_markdown(md_text, meta['id'])
        all_chunks.extend(chunks)
    return all_chunks


def find_formula_occurrences(chunks: list) -> list:
    """Encontra todas as ocorrências de variações da fórmula TCR em todos os chunks."""
    occurrences = []
    
    for chunk in chunks:
        text = chunk.text
        
        # Procura por cada padrão
        for pattern_idx, pattern in enumerate(FORMULA_PATTERNS):
            matches = list(re.finditer(pattern, text, re.IGNORECASE | re.DOTALL))
            for match in matches:
                # Extrai contexto: 200 chars antes e depois
                start = max(0, match.start() - 200)
                end = min(len(text), match.end() + 200)
                context = text[start:end]
                
                occurrences.append({
                    'chunk_id': chunk.chunk_id,
                    'corpus_id': chunk.corpus_id,
                    'page': chunk.page,
                    'section': chunk.section,
                    'pattern_matched': pattern_idx,
                    'pattern': pattern[:50] + '...' if len(pattern) > 50 else pattern,
                    'matched_text': match.group(0),
                    'match_start': match.start(),
                    'context': context,
                    'char_count': chunk.char_count,
                })
    
    return occurrences


def classify_occurrence_primarity(occurrence: dict) -> dict:
    """Classifica se a ocorrência é evidência primária ou secundária."""
    context_lower = occurrence['context'].lower()
    
    # Evidência primária: contém definição da fórmula
    primary_indicators = [
        ('we introduce', 'we introduce'),
        ('we define', 'we define'),
        ('the metric is', 'the metric is'),
        ('definimos', 'definimos'),
        ('introduzimos', 'introduzimos'),
        ('a métrica é', 'a métrica é'),
        ('metric c as', 'metric c as'),
        ('é definida', 'é definida'),
        ('is defined', 'is defined'),
        ('propondo uma', 'propondo uma'),
        ('uma estrutura quantitativa', 'uma estrutura quantitativa'),
    ]
    
    # Evidência derivada: cita a fórmula mas não define
    secondary_indicators = [
        ('we adopt', 'we adopt'),
        ('the exponent β', 'the exponent β'),
        ('β = 0.5', 'β = 0.5'),
        ('calibrated via', 'calibrated via'),
        ('calibrado', 'calibrado'),
        ('canônico', 'canônico'),
        ('canonical', 'canonical'),
    ]
    
    # Evidência contextual: fórmula mencionada em discussão/comparação
    contextual_indicators = [
        ('the composite c', 'the composite c'),
        ('does not outperform', 'does not outperform'),
        ('adding no discriminative', 'adding no discriminative'),
        ('structural signature', 'structural signature'),
        ('interpretive', 'interpretive'),
        ('interpretativa', 'interpretativa'),
    ]
    
    primary_score = sum(1 for indicator, _ in primary_indicators if indicator in context_lower)
    secondary_score = sum(1 for indicator, _ in secondary_indicators if indicator in context_lower)
    contextual_score = sum(1 for indicator, _ in contextual_indicators if indicator in context_lower)
    
    if primary_score > 0:
        primarity = 'PRIMARY'
        classification = 'EVIDÊNCIA PRIMÁRIA — contém definição ou introdução da fórmula'
    elif secondary_score > 0:
        primarity = 'DERIVED'
        classification = 'EVIDÊNCIA DERIVADA — cita parâmetros mas não define a fórmula'
    elif contextual_score > 0:
        primarity = 'CONTEXTUAL'
        classification = 'EVIDÊNCIA CONTEXTUAL — fórmula mencionada em discussão'
    else:
        primarity = 'MENTION'
        classification = 'MENÇÃO — fórmula citada sem contexto definicional'
    
    return {
        'primarity': primarity,
        'classification': classification,
        'primary_indicators_found': [ind for ind, _ in primary_indicators if ind in context_lower],
        'secondary_indicators_found': [ind for ind, _ in secondary_indicators if ind in context_lower],
        'contextual_indicators_found': [ind for ind, _ in contextual_indicators if ind in context_lower],
    }


def audit_gabarito_b1(chunks: list) -> dict:
    """Etapa 1: Auditoria completa do gabarito B1."""
    print("\n[ETAPA 1] AUDITORIA DO GABARITO B1")
    print("=" * 70)
    print(f"\nGabarito atual: chunk_id = CORPUS-002#p1_01 (Paper A v6.2, Abstract, p.1)")
    print(f"Pergunta B1: {B1_PERGUNTA}")
    
    # Encontra todas as ocorrências da fórmula
    print(f"\nProcurando ocorrências de variações de 'C = I × S × H^β' no corpus v1.3.0...")
    occurrences = find_formula_occurrences(chunks)
    print(f"Total de ocorrências encontradas: {len(occurrences)}")
    
    # Classifica cada ocorrência
    print(f"\nClassificando cada ocorrência por primariedade...")
    classified_occurrences = []
    for occ in occurrences:
        classification = classify_occurrence_primarity(occ)
        occ.update(classification)
        classified_occurrences.append(occ)
    
    # Agrupa por chunk_id
    by_chunk = defaultdict(list)
    for occ in classified_occurrences:
        by_chunk[occ['chunk_id']].append(occ)
    
    # Agrupa por corpus_id
    by_corpus = defaultdict(list)
    for occ in classified_occurrences:
        by_corpus[occ['corpus_id']].append(occ)
    
    # Resumo por documento
    print(f"\n{'=' * 80}")
    print("OCORRÊNCIAS POR DOCUMENTO:")
    print(f"{'=' * 80}")
    for corpus_id, occs in sorted(by_corpus.items()):
        primary_count = sum(1 for o in occs if o['primarity'] == 'PRIMARY')
        derived_count = sum(1 for o in occs if o['primarity'] == 'DERIVED')
        contextual_count = sum(1 for o in occs if o['primarity'] == 'CONTEXTUAL')
        mention_count = sum(1 for o in occs if o['primarity'] == 'MENTION')
        unique_chunks = len(set(o['chunk_id'] for o in occs))
        print(f"\n  {corpus_id}:")
        print(f"    Total ocorrências: {len(occs)}")
        print(f"    Chunks únicos: {unique_chunks}")
        print(f"    PRIMARY: {primary_count} | DERIVED: {derived_count} | CONTEXTUAL: {contextual_count} | MENTION: {mention_count}")
    
    # Detalhe por chunk (apenas chunks com ocorrências PRIMARY)
    print(f"\n{'=' * 80}")
    print("CHUNKS COM EVIDÊNCIA PRIMÁRIA (definição/introdução da fórmula):")
    print(f"{'=' * 80}")
    primary_chunks = []
    for chunk_id, occs in by_chunk.items():
        primary_occs = [o for o in occs if o['primarity'] == 'PRIMARY']
        if primary_occs:
            primary_chunks.append({
                'chunk_id': chunk_id,
                'corpus_id': primary_occs[0]['corpus_id'],
                'page': primary_occs[0]['page'],
                'section': primary_occs[0]['section'],
                'primary_count': len(primary_occs),
                'primary_indicators': primary_occs[0]['primary_indicators_found'],
                'matched_text': primary_occs[0]['matched_text'],
                'context_excerpt': primary_occs[0]['context'][:300],
            })
    
    for pc in primary_chunks:
        print(f"\n  ✅ {pc['chunk_id']} ({pc['corpus_id']}, {pc['page']}, {pc['section']})")
        print(f"     Matched: '{pc['matched_text']}'")
        print(f"     Primary indicators: {pc['primary_indicators']}")
        print(f"     Context (300 chars): {pc['context_excerpt'][:200]}...")
    
    # Análise da validade do gabarito
    print(f"\n{'=' * 80}")
    print("ANÁLISE DA VALIDADE DO GABARITO B1:")
    print(f"{'=' * 80}")
    
    gabarito_chunk = 'CORPUS-002#p1_01'
    
    # Verificar se gabarito está na lista de PRIMARY
    gabarito_in_primary = any(pc['chunk_id'] == gabarito_chunk for pc in primary_chunks)
    
    # Verificar se há outros chunks PRIMARY em CORPUS-002
    corpus_002_primary = [pc for pc in primary_chunks if pc['corpus_id'] == 'CORPUS-002']
    
    # Verificar chunks PRIMARY em outros documentos
    other_corpus_primary = [pc for pc in primary_chunks if pc['corpus_id'] != 'CORPUS-002']
    
    print(f"\nGabarito atual: {gabarito_chunk}")
    print(f"Gabarito é evidência PRIMARY? {'SIM' if gabarito_in_primary else 'NAO'}")
    print(f"\nChunks PRIMARY em CORPUS-002 (Paper A):")
    for pc in corpus_002_primary:
        marker = 'GABARITO' if pc['chunk_id'] == gabarito_chunk else 'ALTERNATIVA'
        print(f"  [{marker}] {pc['chunk_id']} ({pc['page']}, {pc['section']})")
        print(f"           Indicators: {pc['primary_indicators']}")
    
    print(f"\nChunks PRIMARY em outros documentos:")
    for pc in other_corpus_primary:
        print(f"  {pc['chunk_id']} ({pc['corpus_id']}, {pc['page']}, {pc['section']})")
        print(f"           Indicators: {pc['primary_indicators']}")
    
    # Análise da especificação do gabarito
    print(f"\n{'=' * 80}")
    print("DECISÃO SOBRE ESPECIFICAÇÃO DO GABARITO:")
    print(f"{'=' * 80}")
    
    if not gabarito_in_primary:
        print(f"\n  ⚠️ GABARITO NÃO É EVIDÊNCIA PRIMÁRIA!")
        print(f"     {gabarito_chunk} não foi classificado como PRIMARY")
        print(f"     Verificar se gabarito precisa ser corrigido")
    
    if len(corpus_002_primary) > 1:
        print(f"\n  ⚠️ MÚLTIPLOS CHUNKS PRIMARY EM CORPUS-002:")
        print(f"     {len(corpus_002_primary)} chunks contêm definição primária")
        print(f"     Gabarito pode estar excessivamente estreito")
        alternative_chunks = [pc['chunk_id'] for pc in corpus_002_primary if pc['chunk_id'] != gabarito_chunk]
        print(f"     Chunks alternativos: {alternative_chunks}")
    
    # Verificar especialmente CORPUS-002#p1_03 e CORPUS-002#p2_01
    # que sabíamos conter a fórmula
    specific_chunks = ['CORPUS-002#p1_01', 'CORPUS-002#p1_03', 'CORPUS-002#p2_01', 'CORPUS-002#p2_02']
    print(f"\n  Detalhe dos chunks específicos:")
    for chunk_id_target in specific_chunks:
        if chunk_id_target in by_chunk:
            occs = by_chunk[chunk_id_target]
            primary_occs = [o for o in occs if o['primarity'] == 'PRIMARY']
            derived_occs = [o for o in occs if o['primarity'] == 'DERIVED']
            print(f"    {chunk_id_target}: {len(occs)} ocorrências (PRIMARY={len(primary_occs)}, DERIVED={len(derived_occs)})")
            if primary_occs:
                print(f"      Primary indicators: {primary_occs[0]['primary_indicators_found']}")
        else:
            print(f"    {chunk_id_target}: Nenhuma ocorrência encontrada")
    
    return {
        'total_occurrences': len(occurrences),
        'classified_occurrences': classified_occurrences,
        'by_chunk': dict(by_chunk),
        'by_corpus': dict(by_corpus),
        'primary_chunks': primary_chunks,
        'gabarito_analysis': {
            'gabarito_chunk': gabarito_chunk,
            'gabarito_in_primary': gabarito_in_primary,
            'corpus_002_primary_count': len(corpus_002_primary),
            'corpus_002_primary_chunks': [pc['chunk_id'] for pc in corpus_002_primary],
            'other_corpus_primary': [pc['chunk_id'] for pc in other_corpus_primary],
            'gabarito_is_unique_primary': len(corpus_002_primary) == 1 and gabarito_in_primary,
        },
    }


def lexical_analysis_ptbr_en(chunks: list) -> dict:
    """Etapa 2: Análise lexical PT-BR ↔ EN da pergunta B1 vs textos-alvo."""
    print(f"\n{'=' * 80}")
    print("[ETAPA 2] ANÁLISE LEXICAL PT-BR ↔ EN")
    print(f"{'=' * 80}")
    
    print(f"\nPergunta B1 (PT-BR): '{B1_PERGUNTA}'")
    
    # Tokenizar pergunta
    question_tokens = re.findall(r'\w+', B1_PERGUNTA.lower())
    question_math_symbols = re.findall(r'[=×βΦαµν∂∇∑∏HIS]', B1_PERGUNTA)
    
    print(f"\nTokens da pergunta (PT-BR): {question_tokens}")
    print(f"Símbolos matemáticos: {question_math_symbols}")
    
    # Mapeamento PT-BR ↔ EN
    pt_en_mapping = {
        'qual': 'what/which',
        'fonte': 'source',
        'exata': 'exact',
        'afirmação': 'statement/claim',
        'métrica': 'metric',
        'tcr': 'TCR (acronym — same in EN)',
        'coerência': 'coherence',
        'relacional': 'relational',
    }
    
    print(f"\nMapeamento PT-BR ↔ EN dos termos da pergunta:")
    for pt_term, en_translation in pt_en_mapping.items():
        if pt_term in [t.lower() for t in question_tokens]:
            print(f"  '{pt_term}' → '{en_translation}'")
    
    # Análise dos chunks-alvo
    target_chunks = ['CORPUS-002#p1_01', 'CORPUS-002#p1_03', 'CORPUS-002#p2_01']
    
    print(f"\nAnálise lexical dos chunks-alvo (Paper A v6.2, EN):")
    chunk_analyses = []
    
    for target_chunk_id in target_chunks:
        target_chunks_list = [c for c in chunks if c.chunk_id == target_chunk_id]
        if not target_chunks_list:
            print(f"\n  {target_chunk_id}: NÃO ENCONTRADO")
            continue
        
        chunk = target_chunks_list[0]
        text = chunk.text
        
        # Idioma detectado
        en_indicators = ['we introduce', 'we define', 'the metric', 'where I is', 'where S is', 'where H is', 'we adopt', 'calibrated via', 'we test']
        pt_indicators = ['introduzimos', 'definimos', 'a métrica', 'onde I é', 'calibrado', 'testamos']
        
        en_count = sum(1 for ind in en_indicators if ind in text.lower())
        pt_count = sum(1 for ind in pt_indicators if ind in text.lower())
        
        if en_count > pt_count:
            detected_language = 'EN (English)'
        elif pt_count > en_count:
            detected_language = 'PT-BR (Português)'
        else:
            detected_language = 'MIXED/AMBIGUOUS'
        
        # Tokens do chunk
        chunk_tokens = re.findall(r'\w+', text.lower())
        
        # Tokens compartilhados com pergunta
        shared_tokens = set(question_tokens) & set(chunk_tokens)
        
        # Correspondências semânticas PT-BR ↔ EN que TF-IDF não captura
        semantic_matches = []
        for pt_term, en_term in [
            ('fonte', 'source'),
            ('exata', 'exact'),
            ('afirmação', 'statement/claim/definition'),
            ('métrica', 'metric'),
            ('coerência', 'coherence'),
            ('relacional', 'relational'),
        ]:
            # Procura o termo EN no chunk
            en_term_variants = en_term.split('/')
            for variant in en_term_variants:
                if variant.lower() in chunk_tokens:
                    semantic_matches.append({
                        'pt_term': pt_term,
                        'en_equivalent': variant,
                        'present_in_chunk': True,
                        'tfidf_captures': pt_term in chunk_tokens,  # TF-IDF só captura se PT aparecer
                    })
                    break
        
        # Tokens matemáticos no chunk
        chunk_math = re.findall(r'[=×βΦαµν∂∇∑∏HIS]', text)
        
        chunk_analysis = {
            'chunk_id': chunk.chunk_id,
            'corpus_id': chunk.corpus_id,
            'page': chunk.page,
            'section': chunk.section,
            'detected_language': detected_language,
            'en_indicator_count': en_count,
            'pt_indicator_count': pt_count,
            'chunk_tokens_count': len(chunk_tokens),
            'shared_tokens_with_question': list(shared_tokens),
            'shared_tokens_count': len(shared_tokens),
            'semantic_matches_pt_en': semantic_matches,
            'chunk_math_symbols': chunk_math,
            'first_300_chars': text[:300],
        }
        chunk_analyses.append(chunk_analysis)
        
        print(f"\n  {chunk.chunk_id} ({chunk.corpus_id}, {chunk.page}, {chunk.section})")
        print(f"    Idioma detectado: {detected_language}")
        print(f"    EN indicators: {en_count}, PT indicators: {pt_count}")
        print(f"    Tokens total: {len(chunk_tokens)}")
        print(f"    Tokens compartilhados com pergunta: {len(shared_tokens)}")
        print(f"      {shared_tokens}")
        print(f"    Símbolos matemáticos: {chunk_math}")
        print(f"    Correspondências semânticas PT→EN (TF-IDF NÃO captura):")
        for sm in semantic_matches:
            tfidf_status = '✅ CAPTURA' if sm['tfidf_captures'] else '❌ NÃO CAPTURA'
            print(f"      '{sm['pt_term']}' (PT-BR) ↔ '{sm['en_equivalent']}' (EN) — {tfidf_status}")
    
    # Análise de assimetria PT-BR ↔ EN
    print(f"\n{'=' * 80}")
    print("ANÁLISE DE ASSIMETRIA PT-BR ↔ EN:")
    print(f"{'=' * 80}")
    
    total_semantic_matches = sum(len(ca['semantic_matches_pt_en']) for ca in chunk_analyses)
    tfidf_captures = sum(1 for ca in chunk_analyses for sm in ca['semantic_matches_pt_en'] if sm['tfidf_captures'])
    tfidf_misses = total_semantic_matches - tfidf_captures
    
    print(f"\nTotal de correspondências semânticas PT→EN: {total_semantic_matches}")
    print(f"TF-IDF captura: {tfidf_captures}")
    print(f"TF-IDF NÃO captura: {tfidf_misses}")
    print(f"Taxa de perda lexical: {tfidf_misses/total_semantic_matches*100:.1f}%" if total_semantic_matches > 0 else "N/A")
    
    asymmetry_assessment = {
        'total_semantic_matches': total_semantic_matches,
        'tfidf_captures': tfidf_captures,
        'tfidf_misses': tfidf_misses,
        'loss_rate': tfidf_misses/total_semantic_matches if total_semantic_matches > 0 else 0,
        'assessment': 'FORTE ASSIMETRIA PT-BR ↔ EN' if tfidf_misses > tfidf_captures else 'ASSIMETRIA MODERADA',
    }
    
    print(f"\nAvaliação: {asymmetry_assessment['assessment']}")
    print(f"TF-IDF perde {tfidf_misses} correspondências semânticas devido à diferença de idioma")
    
    return {
        'question_analysis': {
            'tokens': question_tokens,
            'math_symbols': question_math_symbols,
            'pt_en_mapping': pt_en_mapping,
        },
        'chunk_analyses': chunk_analyses,
        'asymmetry_assessment': asymmetry_assessment,
    }


def classify_cause(audit_result: dict, lexical_result: dict) -> dict:
    """Etapa 3: Classificação da causa/causas (A/B/C/D)."""
    print(f"\n{'=' * 80}")
    print("[ETAPA 3] CLASSIFICAÇÃO DA CAUSA/CAUSAS")
    print(f"{'=' * 80}")
    
    gabarito_analysis = audit_result['gabarito_analysis']
    asymmetry = lexical_result['asymmetry_assessment']
    
    # Critérios para cada classificação
    gabarito_narrow = not gabarito_analysis['gabarito_is_unique_primary']
    lexical_asymmetry = asymmetry['tfidf_misses'] > asymmetry['tfidf_captures']
    
    print(f"\nGabarito excessivamente estreito? {gabarito_narrow}")
    print(f"  - Gabarito é único PRIMARY? {gabarito_analysis['gabarito_is_unique_primary']}")
    print(f"  - Chunks PRIMARY em CORPUS-002: {gabarito_analysis['corpus_002_primary_count']}")
    print(f"  - Chunks PRIMARY: {gabarito_analysis['corpus_002_primary_chunks']}")
    
    print(f"\nAssimetria lexical PT-BR ↔ EN? {lexical_asymmetry}")
    print(f"  - TF-IDF captura: {asymmetry['tfidf_captures']}")
    print(f"  - TF-IDF perde: {asymmetry['tfidf_misses']}")
    print(f"  - Taxa de perda: {asymmetry['loss_rate']*100:.1f}%")
    
    # Classificação A/B/C/D
    if lexical_asymmetry and not gabarito_narrow:
        classification = 'A'
        description = 'Gabarito correto + problema lexical (cross-lingual retrieval necessário)'
    elif gabarito_narrow and not lexical_asymmetry:
        classification = 'B'
        description = 'Gabarito excessivamente estreito (múltiplas evidências equivalentes)'
    elif not lexical_asymmetry and not gabarito_narrow:
        classification = 'C'
        description = 'Gabarito correto + problema de representação'
    else:  # ambos
        classification = 'D'
        description = 'Ambos: PT-BR ↔ EN + evidência distribuída em múltiplos chunks + representação'
    
    print(f"\n{'=' * 80}")
    print(f"CLASSIFICAÇÃO: {classification} — {description}")
    print(f"{'=' * 80}")
    
    return {
        'classification': classification,
        'description': description,
        'gabarito_narrow': gabarito_narrow,
        'lexical_asymmetry': lexical_asymmetry,
        'gabarito_analysis': gabarito_analysis,
        'asymmetry_assessment': asymmetry,
    }


def main():
    print("=" * 70)
    print("AION Passo 6.2.8 — Auditoria do Gabarito B1 + Análise lexical PT-BR ↔ EN")
    print("=" * 70)
    
    # Constrói todos os chunks
    print("\n[SETUP] Construindo chunks do corpus v1.3.0...")
    chunks = build_all_chunks()
    print(f"  Total chunks: {len(chunks)}")
    
    # ETAPA 1: Auditoria do gabarito
    audit_result = audit_gabarito_b1(chunks)
    
    # ETAPA 2: Análise lexical PT-BR ↔ EN
    lexical_result = lexical_analysis_ptbr_en(chunks)
    
    # ETAPA 3: Classificação da causa
    classification_result = classify_cause(audit_result, lexical_result)
    
    # Salvar relatório
    report = {
        'metadata': {
            'experiment': 'AION-6.2.8 — Auditoria do Gabarito B1 + Análise lexical',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'etapa_1_audit_gabarito': audit_result,
        'etapa_2_lexical_analysis': lexical_result,
        'etapa_3_classification': classification_result,
        'next_steps': [
            'Aguardar determinação do Projetista Master sobre:',
            '1. Decisão sobre o oracle (manter estreito ou ampliar formalmente)',
            '2. Se necessário, novos experimentos baseados na classificação A/B/C/D',
        ],
    }
    
    json_path = OUTPUT_DIR / 'aion_6_2_8_audit_gabarito.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
