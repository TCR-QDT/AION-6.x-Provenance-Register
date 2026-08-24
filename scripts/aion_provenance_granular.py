#!/usr/bin/env python3
"""
AION Passo 5.6 — Proveniência Granular por Nó/Aresta

Implementa a estrutura de dados especificada pelo Projetista Master:
- Nós com: documentos_origem, versoes, secoes, chunks, classificacao_epistemica, data
- Arestas com: evidence_type, documento_origem, versao, secao, chunk_id, peso, confidence, status
- PGI (Provenance Granularity Index) calculado para arestas [E] canônicas
- Status: DECLARED (E) | CANDIDATE (E-cooc) | VALIDATED | CONTESTED | REVOKED

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import re
import sys
import hashlib
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, '/home/z/my-project/scripts')
sys.path.insert(0, '/home/z/.local/lib/python3.13/site-packages')

import networkx as nx
from aion_rag_proxy import CORPUS_FILES, CORPUS_DIR, parse_extracted_markdown
from aion_graphrag import (
    CONCEPTS, ONTOLOGY_EDGES_E, REVOKED_EDGES,
    CONCEPT_PATTERNS, detect_concepts_in_text, build_graph, enrich_with_cooccurrence
)

OUTPUT_DIR = Path('/home/z/my-project/download/rag')
CORPUS_DIR_PATH = CORPUS_DIR

# Versões canônicas declaradas no HTML v1.2.0
CORPUS_VERSIONS = {
    'CORPUS-001': '0.1.0',
    'CORPUS-002': 'v6.2',
    'CORPUS-003': '1.0',
    'CORPUS-004': 'v6.1',
    'CORPUS-005': 'NÃO DECLARADO [E]',
}

# Datas canônicas declaradas no HTML v1.2.0
CORPUS_DATES = {
    'CORPUS-001': 'NÃO DECLARADO',
    'CORPUS-002': '2026-08-12',
    'CORPUS-003': '2026-08-10',
    'CORPUS-004': '2026-08-12',
    'CORPUS-005': '2026-08-10',
}

# Mapeamento de localização exata para cada uma das 25 arestas [E]
# (auditoria manual da IA Curadora contra os textos extraídos)
EDGE_LOCATIONS = {
    # Cluster A — composições
    ('C', 'I'): {'doc': 'CORPUS-002', 'secao': 'Abstract, p.1', 'linha': 46, 'chunk_id': 'CORPUS-002#p1_01'},
    ('C', 'S'): {'doc': 'CORPUS-002', 'secao': 'Abstract, p.1', 'linha': 46, 'chunk_id': 'CORPUS-002#p1_01'},
    ('C', 'H'): {'doc': 'CORPUS-002', 'secao': 'Abstract, p.1', 'linha': 46, 'chunk_id': 'CORPUS-002#p1_01'},
    ('C', 'beta'): {'doc': 'CORPUS-002', 'secao': 'Sec. II, p.2', 'linha': 149, 'chunk_id': 'CORPUS-002#p2_01'},
    
    # Cluster B — formalização
    ('Phi_cat', 'Yoneda'): {'doc': 'CORPUS-003', 'secao': 'Sec. 2.1, p.4', 'linha': 196, 'chunk_id': 'CORPUS-003#p4_01'},
    ('Q_munu', 'Einstein_mod'): {'doc': 'CORPUS-003', 'secao': 'p.3, Eq. 2', 'linha': 163, 'chunk_id': 'CORPUS-003#p3_01'},
    ('Chanyal', 'Validation'): {'doc': 'CORPUS-003', 'secao': 'p.10', 'linha': 571, 'chunk_id': 'CORPUS-003#p10_01'},
    ('Sun', 'Validation'): {'doc': 'CORPUS-003', 'secao': 'p.10', 'linha': 571, 'chunk_id': 'CORPUS-003#p10_01'},
    ('Pradhan', 'Validation'): {'doc': 'CORPUS-003', 'secao': 'p.10', 'linha': 571, 'chunk_id': 'CORPUS-003#p10_01'},
    ('Chanyal', 'Q_munu'): {'doc': 'CORPUS-003', 'secao': 'p.10', 'linha': 588, 'chunk_id': 'CORPUS-003#p10_01'},
    ('Pradhan', 'Q_munu'): {'doc': 'CORPUS-003', 'secao': 'p.10-11', 'linha': 597, 'chunk_id': 'CORPUS-003#p11_01'},
    ('Sun', 'Q_munu'): {'doc': 'CORPUS-003', 'secao': 'p.10', 'linha': 586, 'chunk_id': 'CORPUS-003#p10_01'},
    
    # Cluster D — estrutura lakatosiana
    ('Lakatos', 'Nucleus_firm'): {'doc': 'CORPUS-003', 'secao': 'Sec. 5, p.11', 'linha': 664, 'chunk_id': 'CORPUS-003#p11_02'},
    ('Lakatos', 'Protective_belt'): {'doc': 'CORPUS-003', 'secao': 'Sec. 5, p.11', 'linha': 664, 'chunk_id': 'CORPUS-003#p11_02'},
    ('Phi_cat', 'Conjecture'): {'doc': 'CORPUS-003', 'secao': 'Tabela 2, p.11', 'linha': 620, 'chunk_id': 'CORPUS-003#p11_02'},
    ('Q_munu', 'Proposal'): {'doc': 'CORPUS-003', 'secao': 'Tabela 2, p.11', 'linha': 620, 'chunk_id': 'CORPUS-003#p11_02'},
    ('Chanyal', 'Validation'): {'doc': 'CORPUS-003', 'secao': 'Tabela 2, p.11', 'linha': 620, 'chunk_id': 'CORPUS-003#p11_02'},
    ('Phi_cat', 'Protective_belt'): {'doc': 'CORPUS-003', 'secao': 'Sec. 5, p.11', 'linha': 673, 'chunk_id': 'CORPUS-003#p11_02'},
    ('Q_munu', 'Protective_belt'): {'doc': 'CORPUS-003', 'secao': 'Sec. 5, p.11', 'linha': 673, 'chunk_id': 'CORPUS-003#p11_02'},
    ('Nucleus_firm', 'Protective_belt'): {'doc': 'CORPUS-003', 'secao': 'Sec. 5, p.11', 'linha': 668, 'chunk_id': 'CORPUS-003#p11_02'},
    ('Conjecture', 'Proposal'): {'doc': 'CORPUS-003', 'secao': 'Passo 16→17', 'linha': 192, 'chunk_id': 'CORPUS-003#p4_01'},
    ('Proposal', 'Validation'): {'doc': 'CORPUS-003', 'secao': 'Passo 17→18', 'linha': 468, 'chunk_id': 'CORPUS-003#p9_01'},
    
    # Cross-cluster — aplicação
    ('QDT', 'FMO'): {'doc': 'CORPUS-004', 'secao': 'p.1', 'linha': 67, 'chunk_id': 'CORPUS-004#p1_01'},
    ('FMO', 'Power_law_T2'): {'doc': 'CORPUS-004', 'secao': 'p.1-2, Eq. 2', 'linha': 51, 'chunk_id': 'CORPUS-004#p1_01'},
    ('Power_law_T2', 'eta_hyp'): {'doc': 'CORPUS-004', 'secao': 'p.2', 'linha': 111, 'chunk_id': 'CORPUS-004#p2_01'},
}


def build_enriched_node(concept: dict) -> dict:
    """Constrói nó enriquecido com proveniência completa."""
    return {
        'node_id': concept['id'],
        'label': concept['label'],
        'tipo': 'conceito',
        'cluster': concept['cluster'],
        'definition': concept['definition'],
        'documentos_origem': [concept['corpus']],
        'versoes': [CORPUS_VERSIONS.get(concept['corpus'], 'NÃO DECLARADO')],
        'datas': [CORPUS_DATES.get(concept['corpus'], 'NÃO DECLARADO')],
        'secoes': extract_sections_for_concept(concept),
        'chunks': extract_chunks_for_concept(concept),
        'classificacao_epistemica': '[E]',
        'evidence_type': '[E]',
        'data_registro': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }


def extract_sections_for_concept(concept: dict) -> list:
    """Extrai seções onde o conceito aparece, baseado nas arestas."""
    sections = set()
    for (src, dst), loc in EDGE_LOCATIONS.items():
        if concept['id'] in (src, dst):
            sections.add(f"{loc['doc']} {loc['secao']}")
    return sorted(sections)


def extract_chunks_for_concept(concept: dict) -> list:
    """Extrai chunk_ids onde o conceito aparece, baseado nas arestas."""
    chunks = set()
    for (src, dst), loc in EDGE_LOCATIONS.items():
        if concept['id'] in (src, dst):
            chunks.add(loc['chunk_id'])
    return sorted(chunks)


def build_enriched_edge(src: str, dst: str, attrs: dict, edge_id: str) -> dict:
    """Constrói aresta enriquecida com proveniência completa."""
    location = EDGE_LOCATIONS.get((src, dst), {})
    
    return {
        'edge_id': edge_id,
        'source': src,
        'target': dst,
        'relation': attrs.get('type', 'unknown'),
        'evidence_type': '[E]' if attrs.get('source') == 'ontology_v1.0.0_E' else '[E-cooc]',
        'documento_origem': location.get('doc', 'NÃO MAPEADO'),
        'versao': CORPUS_VERSIONS.get(location.get('doc', ''), 'NÃO DECLARADO'),
        'secao': location.get('secao', 'NÃO MAPEADO'),
        'linha': location.get('linha', None),
        'chunk_id': location.get('chunk_id', 'NÃO MAPEADO'),
        'peso': attrs.get('weight', 0.5),
        'confidence': 1.0 if attrs.get('source') == 'ontology_v1.0.0_E' else 0.5,
        'status': 'DECLARED' if attrs.get('source') == 'ontology_v1.0.0_E' else 'CANDIDATE',
        'evidence_text': attrs.get('evidence', ''),
    }


def compute_pgi(edges: list) -> dict:
    """
    PGI (Provenance Granularity Index):
    razão entre arestas [E] com proveniência completa e total de arestas [E] auditadas.
    """
    e_edges = [e for e in edges if e['evidence_type'] == '[E]']
    e_with_full_provenance = [
        e for e in e_edges
        if e['documento_origem'] != 'NÃO MAPEADO'
        and e['secao'] != 'NÃO MAPEADO'
        and e['chunk_id'] != 'NÃO MAPEADO'
    ]
    
    return {
        'total_e_edges': len(e_edges),
        'e_edges_with_full_provenance': len(e_with_full_provenance),
        'pgi': len(e_with_full_provenance) / len(e_edges) if e_edges else 0.0,
        'pgi_percentage': f"{(len(e_with_full_provenance) / len(e_edges) * 100) if e_edges else 0:.1f}%",
    }


def main():
    print("=" * 70)
    print("AION Passo 5.6 — Proveniência Granular")
    print("=" * 70)
    
    # Reconstrói chunks
    print("\n[5.6.1] Reconstruindo chunks...")
    all_chunks = []
    for filename, meta in CORPUS_FILES.items():
        path = CORPUS_DIR_PATH / filename
        if not path.exists():
            continue
        md_text = path.read_text(encoding='utf-8')
        chunks = parse_extracted_markdown(md_text, meta['id'])
        all_chunks.extend(chunks)
    print(f"  {len(all_chunks)} chunks disponíveis")
    
    # Constrói grafo base
    print("\n[5.6.2] Construindo grafo base...")
    G = build_graph()
    enrich_with_cooccurrence(G, all_chunks)
    print(f"  Grafo: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")
    
    # Enriquece nós
    print("\n[5.6.3] Enriquecendo nós com proveniência completa...")
    enriched_nodes = []
    for concept in CONCEPTS:
        enriched_node = build_enriched_node(concept)
        enriched_nodes.append(enriched_node)
    print(f"  {len(enriched_nodes)} nós enriquecidos")
    
    # Enriquece arestas
    print("\n[5.6.4] Enriquecendo arestas com proveniência completa...")
    enriched_edges = []
    edge_counter = 0
    
    # Arestas da ontologia [E]
    # Força o atributo source para que build_enriched_edge identifique como [E]
    for src, dst, attrs in ONTOLOGY_EDGES_E:
        edge_counter += 1
        edge_id = f"E_{edge_counter:03d}_{src}_to_{dst}"
        attrs_with_source = dict(attrs)
        attrs_with_source['source'] = 'ontology_v1.0.0_E'
        enriched_edge = build_enriched_edge(src, dst, attrs_with_source, edge_id)
        enriched_edges.append(enriched_edge)
    
    # Arestas de co-ocorrência [E-cooc] (apenas as que NÃO estão na ontologia)
    ontology_edge_keys = {(s, d) for s, d, _ in ONTOLOGY_EDGES_E}
    cooc_added = 0
    for u, v, attrs in G.edges(data=True):
        if attrs.get('source') != 'rag_cooccurrence_auto':
            continue
        if (u, v) in ontology_edge_keys:
            continue
        edge_counter += 1
        edge_id = f"EC_{edge_counter:03d}_{u}_to_{v}"
        # Para co-ocorrência, usa attrs do grafo
        enriched_edge = build_enriched_edge(u, v, attrs, edge_id)
        # Substitui proveniência com chunks onde co-ocorre
        sample_chunks = attrs.get('sample_chunks', [])
        if sample_chunks:
            first_chunk_id = sample_chunks[0]
            doc_match = re.match(r'(CORPUS-\d{3})', first_chunk_id)
            if doc_match:
                enriched_edge['documento_origem'] = doc_match.group(1)
                enriched_edge['versao'] = CORPUS_VERSIONS.get(doc_match.group(1), 'NÃO DECLARADO')
            enriched_edge['chunk_id'] = ', '.join(sample_chunks[:3])
            enriched_edge['secao'] = f"Co-ocorrência em {len(sample_chunks)} chunks"
        enriched_edges.append(enriched_edge)
        cooc_added += 1
    
    print(f"  {len(enriched_edges)} arestas enriquecidas ({len(ONTOLOGY_EDGES_E)} [E] + {cooc_added} [E-cooc])")
    
    # Calcula PGI
    print("\n[5.6.5] Calculando PGI (Provenance Granularity Index)...")
    pgi = compute_pgi(enriched_edges)
    print(f"  PGI = {pgi['pgi']:.4f} ({pgi['pgi_percentage']})")
    print(f"  Arestas [E] com proveniência completa: {pgi['e_edges_with_full_provenance']}/{pgi['total_e_edges']}")
    
    # Verificação cruzada: para cada uma das 25 arestas [E], validar que a localização existe
    print("\n[5.6.6] Verificação cruzada de localizações...")
    missing = []
    for src, dst, _ in ONTOLOGY_EDGES_E:
        if (src, dst) not in EDGE_LOCATIONS:
            missing.append((src, dst))
    if missing:
        print(f"  ⚠️ {len(missing)} arestas [E] sem localização mapeada: {missing}")
    else:
        print(f"  ✅ Todas as {len(ONTOLOGY_EDGES_E)} arestas [E] têm localização mapeada")
    
    # Arestas revogadas
    revoked = []
    for src, dst, attrs in REVOKED_EDGES:
        revoked.append({
            'source': src,
            'target': dst,
            'status': 'REVOKED',
            'reason': attrs['reason'],
            'evidence_original': attrs['evidence_original'],
            'evidence_revocation': attrs['evidence_revocation'],
        })
    
    # Estrutura final
    graph_v2 = {
        'metadata': {
            'version': '2.0.0',
            'generated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
            'protocol': 'AION-CORPUS-001 v1.2.0 + ONTOLOGY v1.0.0',
        },
        'nodes': enriched_nodes,
        'edges': enriched_edges,
        'revoked_edges': revoked,
        'pgi': pgi,
        'summary': {
            'nodes_total': len(enriched_nodes),
            'edges_total': len(enriched_edges),
            'edges_E': len(ONTOLOGY_EDGES_E),
            'edges_E_cooc': cooc_added,
            'revoked_edges': len(revoked),
        },
    }
    
    # Salva
    output_path = OUTPUT_DIR / 'graphrag_enriched_v2.0.json'
    output_path.write_text(json.dumps(graph_v2, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[5.6.7] Arquivo salvo: {output_path}")
    print(f"  Tamanho: {output_path.stat().st_size} bytes")
    
    # Resumo final
    print(f"\n{'=' * 70}")
    print("[RESUMO Passo 5.6 — Proveniência Granular]")
    print(f"{'=' * 70}")
    print(f"Nós: {len(enriched_nodes)} (cada um com: documentos_origem, versoes, datas, secoes, chunks, classificacao_epistemica)")
    print(f"Arestas: {len(enriched_edges)}")
    print(f"  - [E] DECLARED: {len(ONTOLOGY_EDGES_E)}")
    print(f"  - [E-cooc] CANDIDATE: {cooc_added}")
    print(f"  - REVOKED: {len(revoked)}")
    print(f"PGI: {pgi['pgi']:.4f} ({pgi['pgi_percentage']})")
    
    return graph_v2


if __name__ == '__main__':
    main()
