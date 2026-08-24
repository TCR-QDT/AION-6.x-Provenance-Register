#!/usr/bin/env python3
"""
AION Passo 6.3.1.1-2 — Auditoria causal das 15 fabricações F3

Analisa o contexto entregue ao LLM nas 15 runs com fabricação do baseline 6.3.0.
Classifica cada F3 como:
  F3-A — padrão incorreto presente no contexto (chunk_001 estava visível)
  F3-B — padrão incorreto NÃO presente no contexto
  F3-C — contexto contém múltiplos schemas (chunk_001 E p1_01 visíveis)
  F3-D — origem indeterminada

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 21 de agosto de 2026
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

OUTPUT_DIR = Path('/home/z/my-project/download/rag')


def audit_fabrication_contexts():
    """Audita o contexto das 15 runs com fabricação do baseline 6.3.0."""
    print("=" * 80)
    print("AION Passo 6.3.1.1 — Auditoria causal das fabricações F3")
    print("=" * 80)
    
    # Carrega baseline 6.3.0
    baseline_path = OUTPUT_DIR / 'aion_6_3_0_baseline_fabricacao.json'
    baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
    
    # Filtra runs com fabricação
    runs_with_fab = [r for r in baseline['runs_summary'] if r['invalid_ids']]
    
    print(f"\n  Total runs baseline: {baseline['metadata']['n_runs']}")
    print(f"  Runs com fabricação: {len(runs_with_fab)}")
    
    # O contexto entregue ao LLM é o mesmo em todas as runs (retrieval é determinístico)
    # Precisamos reconstruir o contexto que foi entregue ao LLM
    
    # Para B2, o retrieval retorna top-5 chunks
    # O contexto inclui os IDs dos chunks no formato [chunk_id | ...]
    
    # Reconstituir os chunks recuperados (são os mesmos em todas as runs)
    # Do baseline, não temos os textos completos, mas temos os IDs
    
    # Carregar dados do corpus para obter os textos dos chunks recuperados
    sys.path.insert(0, '/home/z/my-project/scripts')
    sys.path.insert(0, '/home/z/.venv/lib/python3.12/site-packages')
    
    from aion_rag_proxy import parse_extracted_markdown
    from aion_6_1_f_rebenchmark_lcr import CORPUS_V13_FILES
    from aion_6_2_6_top_k_efgh import build_base_chunks
    from aion_6_2_9_oracle_crosslingual import B1_PERGUNTA_EN, ExperimentJ_CrossLingual
    from aion_bench_001 import BENCH_TESTS
    
    base_chunks = build_base_chunks()
    
    class ExperimentJ_V3(ExperimentJ_CrossLingual):
        def query_original(self, question: str, top_k: int = 8):
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np
            q_vec = self.vectorizer.transform([question])
            scores = cosine_similarity(q_vec, self.matrix).flatten()
            top_indices = np.argsort(scores)[::-1][:top_k]
            from aion_rag_proxy import RetrievedChunk
            results = []
            for rank, idx in enumerate(top_indices, 1):
                r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
                results.append(r)
            return results
    
    j_store = ExperimentJ_V3(base_chunks, B1_PERGUNTA_EN)
    
    # Reconstruir retrieval de B2 (mesma pergunta, mesmo retrieval)
    test_b2 = BENCH_TESTS['B2']
    retrieved = j_store.query_original(test_b2['pergunta'], top_k=8)
    retrieved_top5 = retrieved[:5]
    
    print(f"\n  B2 retrieved top-5 (idêntico em todas as runs):")
    for r in retrieved_top5:
        print(f"    #{r.rank} {r.chunk.chunk_id} | {r.chunk.corpus_id}")
    
    # Reconstruir o contexto exato entregue ao LLM
    # O prompt inclui: [chunk_id | short_title | page | section | score=...]
    context_parts = []
    for r in retrieved_top5:
        context_parts.append(
            f"[{r.chunk.chunk_id} | {r.chunk.short_title} | {r.chunk.page} | {r.chunk.section} | score={r.score:.3f}]\n"
            f"{r.chunk.text}\n"
        )
    context_assembled = "\n---\n".join(context_parts)
    
    # IDs presentes no contexto
    context_ids = re.findall(r'CORPUS-\d{3}#\w+', context_assembled)
    unique_context_ids = list(set(context_ids))
    
    print(f"\n  IDs presentes no contexto entregue ao LLM:")
    for cid in unique_context_ids:
        print(f"    • {cid}")
    
    # Verificar quais formatos de chunk estão presentes
    context_chunk_formats = {}
    for cid in unique_context_ids:
        doc = cid.split('#')[0]
        chunk_suffix = cid.split('#')[1]
        if doc not in context_chunk_formats:
            context_chunk_formats[doc] = []
        context_chunk_formats[doc].append(chunk_suffix)
    
    print(f"\n  Formatos de chunk por documento no contexto:")
    for doc, suffixes in context_chunk_formats.items():
        print(f"    {doc}: {suffixes}")
    
    # Verificar se chunk_001 está presente no contexto
    chunk_001_present = any('chunk_001' in cid for cid in unique_context_ids)
    print(f"\n  'chunk_001' presente no contexto: {'SIM' if chunk_001_present else 'NAO'}")
    
    # Verificar se p1_01 está presente
    p1_01_present = any('p1_01' in cid for cid in unique_context_ids)
    print(f"  'p1_01' presente no contexto: {'SIM' if p1_01_present else 'NAO'}")
    
    # === CLASSIFICAR CADA F3 ===
    print(f"\n{'=' * 80}")
    print("[6.3.1.2] Classificação da origem do schema incorreto")
    print(f"{'=' * 80}")
    
    classifications = []
    
    for run in runs_with_fab:
        run_id = run['run_id']
        invalid_ids = run['invalid_ids']
        invalid_types = run['invalid_types']
        
        for inv_id, inv_type in zip(invalid_ids, invalid_types):
            if inv_type != 'F3_DOCUMENT_CORRECT_FORMAT_INCORRECT':
                # Pular não-F3 (apenas 1 caso F4)
                classifications.append({
                    'run_id': run_id,
                    'invalid_id': inv_id,
                    'type': inv_type,
                    'classification': 'NON_F3',
                    'description': 'Tipo não-F3 — não analisado nesta auditoria',
                })
                continue
            
            # F3: documento correto (CORPUS-002) + formato de chunk incorreto (chunk_001)
            # Verificar se chunk_001 estava no contexto
            if chunk_001_present:
                # Verificar se é do mesmo documento ou de outro
                chunk_001_from_corpus_002 = any(
                    cid == 'CORPUS-002#chunk_001' for cid in unique_context_ids
                )
                chunk_001_from_other = any(
                    'chunk_001' in cid and 'CORPUS-002' not in cid for cid in unique_context_ids
                )
                
                if chunk_001_from_corpus_002:
                    f3_class = 'F3-A_PATTERN_PRESENT_SAME_DOC'
                    f3_desc = 'Padrão chunk_001 presente no contexto para o MESMO documento (CORPUS-002)'
                elif chunk_001_from_other:
                    f3_class = 'F3-C_MULTIPLE_SCHEMAS'
                    f3_desc = 'Contexto contém múltiplos schemas: chunk_001 (de outro doc) E p1_01 (do CORPUS-002)'
                else:
                    f3_class = 'F3-D_INDETERMINATE'
                    f3_desc = 'Origem indeterminada'
            else:
                # chunk_001 NÃO está no contexto
                if p1_01_present:
                    f3_class = 'F3-B_PATTERN_NOT_PRESENT'
                    f3_desc = 'Padrão chunk_001 NÃO presente no contexto; p1_01 SIM presente — LLM construiu ID sintético'
                else:
                    f3_class = 'F3-D_INDETERMINATE'
                    f3_desc = 'Nem chunk_001 nem p1_01 presentes — origem indeterminada'
            
            classifications.append({
                'run_id': run_id,
                'invalid_id': inv_id,
                'type': inv_type,
                'classification': f3_class,
                'description': f3_desc,
            })
            
            print(f"\n  Run {run_id}: {inv_id}")
            print(f"    Tipo: {inv_type}")
            print(f"    Classificação: {f3_class}")
            print(f"    Descrição: {f3_desc}")
    
    # Resumo da classificação
    print(f"\n{'=' * 80}")
    print("RESUMO DA CLASSIFICAÇÃO F3:")
    print(f"{'=' * 80}")
    
    class_counts = Counter(c['classification'] for c in classifications)
    for cls, count in sorted(class_counts.items(), key=lambda x: -x[1]):
        print(f"  {cls}: {count}")
    
    # Análise causal
    print(f"\n{'=' * 80}")
    print("ANÁLISE CAUSAL:")
    print(f"{'=' * 80}")
    
    f3_c_count = class_counts.get('F3-C_MULTIPLE_SCHEMAS', 0)
    f3_b_count = class_counts.get('F3-B_PATTERN_NOT_PRESENT', 0)
    f3_a_count = class_counts.get('F3-A_PATTERN_PRESENT_SAME_DOC', 0)
    f3_d_count = class_counts.get('F3-D_INDETERMINATE', 0)
    non_f3_count = class_counts.get('NON_F3', 0)
    
    total_f3 = f3_c_count + f3_b_count + f3_a_count + f3_d_count
    
    print(f"\n  Total F3 analisados: {total_f3}")
    print(f"  F3-A (padrão presente, mesmo doc): {f3_a_count}")
    print(f"  F3-B (padrão NÃO presente): {f3_b_count}")
    print(f"  F3-C (múltiplos schemas no contexto): {f3_c_count}")
    print(f"  F3-D (indeterminado): {f3_d_count}")
    print(f"  Non-F3: {non_f3_count}")
    
    if f3_c_count > 0 and f3_c_count == total_f3:
        causal_hypothesis = (
            'H-F3 CONFIRMADA: A fabricação F3 resulta de competição entre diferentes '
            'esquemas de identificação de chunks presentes no contexto de geração. '
            f'100% dos casos F3 ({f3_c_count}/{total_f3}) têm múltiplos schemas visíveis.'
        )
    elif f3_b_count > 0 and f3_b_count == total_f3:
        causal_hypothesis = (
            'H-F3 REJEITADA: O padrão chunk_001 NÃO está presente no contexto em nenhum caso. '
            f'O LLM constrói IDs sintéticos ({f3_b_count}/{total_f3}). '
            'A fabricação não resulta de competição de schemas, mas de construção sintética.'
        )
    elif f3_c_count > 0:
        causal_hypothesis = (
            f'H-F3 PARCIALMENTE CONFIRMADA: {f3_c_count}/{total_f3} casos têm múltiplos schemas. '
            f'Mas {f3_b_count} casos não têm o padrão presente (construção sintética). '
            'Há dois mecanismos contribuintes.'
        )
    else:
        causal_hypothesis = 'H-F3 INCONCLUSIVA — necessária análise adicional'
    
    print(f"\n  >>> {causal_hypothesis}")
    
    # Salvar relatório
    report = {
        'metadata': {
            'experiment': 'AION-6.3.1.1-2 — Auditoria causal das fabricações F3',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'context_analysis': {
            'retrieved_top5': [r.chunk.chunk_id for r in retrieved_top5],
            'unique_context_ids': unique_context_ids,
            'chunk_formats_by_doc': context_chunk_formats,
            'chunk_001_present': chunk_001_present,
            'p1_01_present': p1_01_present,
        },
        'f3_classifications': classifications,
        'classification_summary': dict(class_counts),
        'causal_hypothesis': causal_hypothesis,
    }
    
    json_path = OUTPUT_DIR / 'aion_6_3_1_auditoria_f3.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    audit_fabrication_contexts()
