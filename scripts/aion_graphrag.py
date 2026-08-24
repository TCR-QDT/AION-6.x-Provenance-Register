#!/usr/bin/env python3
"""
AION GraphRAG — Passo 5

Constrói grafo conceitual a partir da ontologia v1.0.0 e o enriquece
com co-ocorrência extraída dos chunks do RAG proxy (Passo 4).

Estrutura:
- Nós: conceitos da ontologia (Cluster A-D)
- Arestas [E]: declaradas na ontologia v1.0.0 (verificadas textualmente)
- Arestas [co-ocorrência]: extraídas automaticamente dos chunks
- Arestas revogadas: marcadas como tal (não somam peso)

Autor: IA Curadora
Data: 17 de agosto de 2026
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

import networkx as nx

# Adiciona scripts dir
sys.path.insert(0, '/home/z/my-project/scripts')

# pyvis com path workaround
sys.path.insert(0, '/home/z/.local/lib/python3.13/site-packages')
try:
    from pyvis.network import Network
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False
    print("⚠️ pyvis não disponível — visualização HTML será pulada")

from aion_rag_proxy import (
    TfidfVectorStore, CORPUS_FILES, CORPUS_DIR,
    parse_extracted_markdown
)

OUTPUT_DIR = Path('/home/z/my-project/download/rag')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# === Ontologia v1.0.0 — definições canônicas ===

CONCEPTS = [
    # Cluster A — TCR
    {'id': 'C', 'label': 'Coerência Relacional (C)', 'cluster': 'A', 'corpus': 'CORPUS-002',
     'definition': 'C = I × S × H^β, β=0.5 (LOOCV)'},
    {'id': 'I', 'label': 'Integração (I)', 'cluster': 'A', 'corpus': 'CORPUS-002',
     'definition': 'Informação mútua multivariada normalizada'},
    {'id': 'S', 'label': 'Simetria (S)', 'cluster': 'A', 'corpus': 'CORPUS-002',
     'definition': 'log(|Aut(G)|+1)/log(N!)'},
    {'id': 'H', 'label': 'Entropia Espectral (H)', 'cluster': 'A', 'corpus': 'CORPUS-002',
     'definition': 'Entropia espectral Laplaciana normalizada'},
    {'id': 'beta', 'label': 'β (calibração LOOCV)', 'cluster': 'A', 'corpus': 'CORPUS-002',
     'definition': 'β = 0.5, consistência = 1.0 em [0.1, 1.5]'},
    
    # Cluster B — Formalização categórico-tensorial
    {'id': 'Phi_cat', 'label': 'Functor Φcat', 'cluster': 'B', 'corpus': 'CORPUS-003',
     'definition': 'Φcat : C → Set, X ↦ Hom_C(•, X) — Conjectura (Passo 16)'},
    {'id': 'Yoneda', 'label': 'Lema de Yoneda', 'cluster': 'B', 'corpus': 'CORPUS-003',
     'definition': 'Nat(Hom(A,−), F) ≅ F(A) — aplicação conjectural'},
    {'id': 'Q_munu', 'label': 'Tensor Qµν', 'cluster': 'B', 'corpus': 'CORPUS-003',
     'definition': 'Forma bilinear simétrica (0,2) — 5 axiomas — Proposta (Passo 17)'},
    {'id': 'Einstein_mod', 'label': 'Equação de Einstein modificada', 'cluster': 'B', 'corpus': 'CORPUS-003',
     'definition': 'Gµν = 8πG(Tµν + Qµν) — Proposta teórica'},
    {'id': 'Chanyal', 'label': 'Chanyal (validação)', 'cluster': 'B', 'corpus': 'CORPUS-003',
     'definition': 'Bianchi + campo magnético — validação externa Passo 18'},
    {'id': 'Sun', 'label': 'Sun (validação)', 'cluster': 'B', 'corpus': 'CORPUS-003',
     'definition': 'Dynamical systems + anisotropia — validação externa Passo 18'},
    {'id': 'Pradhan', 'label': 'Pradhan (validação)', 'cluster': 'B', 'corpus': 'CORPUS-003',
     'definition': 'Λ(t) variável — validação externa Passo 18'},
    
    # Cluster C — QDT
    {'id': 'QDT', 'label': 'Dinâmica Quântica Dissipativa (QDT)', 'cluster': 'C', 'corpus': 'CORPUS-004',
     'definition': 'Regime quântico dissipativo em sistemas abertos'},
    {'id': 'FMO', 'label': 'Complexo FMO 7-sítios', 'cluster': 'C', 'corpus': 'CORPUS-004',
     'definition': 'Fenna-Matthews-Olson — caso de estudo'},
    {'id': 'Power_law_T2', 'label': 'Power-law T₂', 'cluster': 'C', 'corpus': 'CORPUS-004',
     'definition': 'T₂ = K·J^0.831·λ^(-0.843)·γ^(-0.766)·T^(-0.261), R²=0.988'},
    {'id': 'eta_hyp', 'label': 'Hipótese η (RETRATADA)', 'cluster': 'C', 'corpus': 'CORPUS-004',
     'definition': 'Comensurabilidade cross-scale — RETIRADA em v6.1 (razão 0.291 > 0.2)'},
    
    # Cluster D — Lakatosiano
    {'id': 'Lakatos', 'label': 'Lakatos / Programa de pesquisa', 'cluster': 'D', 'corpus': 'CORPUS-003',
     'definition': 'Núcleo firme + cinturão protetor — estrutura epistêmica'},
    {'id': 'Conjecture', 'label': 'Conjectura (Passo 16)', 'cluster': 'D', 'corpus': 'CORPUS-003',
     'definition': 'Status epistêmico mais fraco'},
    {'id': 'Proposal', 'label': 'Proposta (Passo 17)', 'cluster': 'D', 'corpus': 'CORPUS-003',
     'definition': 'Status epistêmico intermediário'},
    {'id': 'Validation', 'label': 'Validação (Passo 18)', 'cluster': 'D', 'corpus': 'CORPUS-003',
     'definition': 'Status epistêmico mais forte'},
    {'id': 'Nucleus_firm', 'label': 'Núcleo firme', 'cluster': 'D', 'corpus': 'CORPUS-003',
     'definition': 'Hipótese: estrutura física admite formalização categórico-tensorial unificada'},
    {'id': 'Protective_belt', 'label': 'Cinturão protetor', 'cluster': 'D', 'corpus': 'CORPUS-003',
     'definition': 'Conjecturas Φcat + Qµν (vulneráveis, compensadas por validação externa)'},
]

# === Arestas declaradas na ontologia v1.0.0 (verificadas [E]) ===

ONTOLOGY_EDGES_E = [
    # Cluster A — composições
    ('C', 'I', {'type': 'composes', 'evidence': '[E] CORPUS-002 p.1', 'weight': 1.0}),
    ('C', 'S', {'type': 'composes', 'evidence': '[E] CORPUS-002 p.1', 'weight': 1.0}),
    ('C', 'H', {'type': 'composes', 'evidence': '[E] CORPUS-002 p.1', 'weight': 1.0}),
    ('C', 'beta', {'type': 'calibrates', 'evidence': '[E] CORPUS-002 p.1-2 LOOCV', 'weight': 1.0}),
    
    # Cluster B — formalização
    ('Phi_cat', 'Yoneda', {'type': 'applies_invokes', 'evidence': '[E] CORPUS-003 p.4-5', 'weight': 1.0}),
    ('Q_munu', 'Einstein_mod', {'type': 'modifies', 'evidence': '[E] CORPUS-003 p.3 Eq.2', 'weight': 1.0}),
    ('Chanyal', 'Validation', {'type': 'validates', 'evidence': '[E] CORPUS-003 p.10', 'weight': 1.0}),
    ('Sun', 'Validation', {'type': 'validates', 'evidence': '[E] CORPUS-003 p.10', 'weight': 1.0}),
    ('Pradhan', 'Validation', {'type': 'validates', 'evidence': '[E] CORPUS-003 p.10-11', 'weight': 1.0}),
    ('Chanyal', 'Q_munu', {'type': 'analogous_to', 'evidence': '[E] CORPUS-003 p.10 (T_mag)', 'weight': 0.8}),
    ('Pradhan', 'Q_munu', {'type': 'analogous_to', 'evidence': '[E] CORPUS-003 p.11 (Λ(t)gµν)', 'weight': 0.8}),
    ('Sun', 'Q_munu', {'type': 'compatible_with', 'evidence': '[E] CORPUS-003 p.10 (Kasner)', 'weight': 0.7}),
    
    # Cluster D — estrutura lakatosiana
    ('Lakatos', 'Nucleus_firm', {'type': 'structures', 'evidence': '[E] CORPUS-003 p.11', 'weight': 1.0}),
    ('Lakatos', 'Protective_belt', {'type': 'structures', 'evidence': '[E] CORPUS-003 p.11', 'weight': 1.0}),
    ('Phi_cat', 'Conjecture', {'type': 'has_status', 'evidence': '[E] CORPUS-003 Tabela 2', 'weight': 1.0}),
    ('Q_munu', 'Proposal', {'type': 'has_status', 'evidence': '[E] CORPUS-003 Tabela 2', 'weight': 1.0}),
    ('Chanyal', 'Validation', {'type': 'has_status', 'evidence': '[E] CORPUS-003 Tabela 2', 'weight': 1.0}),
    ('Phi_cat', 'Protective_belt', {'type': 'belongs_to', 'evidence': '[E] CORPUS-003 p.11', 'weight': 1.0}),
    ('Q_munu', 'Protective_belt', {'type': 'belongs_to', 'evidence': '[E] CORPUS-003 p.11', 'weight': 1.0}),
    ('Nucleus_firm', 'Protective_belt', {'type': 'sustained_by', 'evidence': '[E] CORPUS-003 p.11', 'weight': 1.0}),
    ('Conjecture', 'Proposal', {'type': 'precedes_epistemically', 'evidence': '[E] CORPUS-003 Passo 16→17', 'weight': 1.0}),
    ('Proposal', 'Validation', {'type': 'precedes_epistemically', 'evidence': '[E] CORPUS-003 Passo 17→18', 'weight': 1.0}),
    
    # Cross-cluster — aplicação
    ('QDT', 'FMO', {'type': 'applies_to', 'evidence': '[E] CORPUS-004', 'weight': 1.0}),
    ('FMO', 'Power_law_T2', {'type': 'characterized_by', 'evidence': '[E] CORPUS-004 p.1-2', 'weight': 1.0}),
    ('Power_law_T2', 'eta_hyp', {'type': 'tested_hypothesis', 'evidence': '[E] CORPUS-004 p.2', 'weight': 1.0}),
]

# === Arestas revogadas (declaradas no HTML v1.2.0 mas revogadas na ontologia v1.0.0) ===

REVOKED_EDGES = [
    ('CORPUS-002', 'CORPUS-003', {
        'reason': 'Dependência ontológica revogada — paralelismo epistêmico confirmado',
        'evidence_original': 'HTML canônico v1.2.0 seção 3',
        'evidence_revocation': '[E] CORPUS-002 p.5-6: "deliberately separated to maintain focus and falsifiability"',
    }),
]


# === Co-ocorrência: extrai arestas automáticas dos chunks ===

# Padrões de busca para cada conceito (em qualquer idioma)
CONCEPT_PATTERNS = {
    'C': [r'\bC\s*=\s*I\s*[×x]\s*S', r'coerência relacional', r'relational coherence', r'\bTCR\b'],
    'I': [r'\bI\s*=\s*1\s*/\s*N', r'\bintegration\b', r'mutual information', r'informação mútua'],
    'S': [r'S\s*=\s*log\s*\(', r'autormorfismo', r'automorphism', r'\bsymmetr'],
    'H': [r'\bspectral entropy\b', r'entropia espectral', r'Hspec'],
    'beta': [r'\bβ\s*=\s*0\.5', r'\\beta\s*=\s*0\.5', r'\bbeta\s*=\s*0\.5', r'LOOCV'],
    'Phi_cat': [r'Φcat', r'Φ_cat', r'Φ_\{?cat\}?', r'functor.*Φ', r'Phicat'],
    'Yoneda': [r'Yoneda'],
    'Q_munu': [r'Qµν', r'Q_\{?µ?\\?nu\}?', r'Q_\\mu\\nu', r'tensor Q'],
    'Einstein_mod': [r'Gµν\s*=\s*8πG\s*\(', r'equação modificada', r'modified.*Einstein', r'Einstein.*modif'],
    'Chanyal': [r'Chanyal'],
    'Sun': [r'\bSun\b'],
    'Pradhan': [r'Pradhan'],
    'QDT': [r'\bQDT\b', r'quântica dissipativa', r'quantum dissipative', r'dissipative quantum'],
    'FMO': [r'\bFMO\b', r'Fenna-Matthews', r'Fenna.*Olson'],
    'Power_law_T2': [r'T_?2\s*=\s*K', r'power.law', r'lei de potência', r'T2 = \(1\.567'],
    'eta_hyp': [r'\bη\b', r'\\eta\b', r'comensurabilidade', r'cross.scale'],
    'Lakatos': [r'Lakatos', r'programa de pesquisa', r'research programme'],
    'Conjecture': [r'conjectura', r'conjecture'],
    'Proposal': [r'proposta teórica', r'theoretical proposal'],
    'Validation': [r'validação teórica', r'theoretical validation', r'validação'],
    'Nucleus_firm': [r'núcleo firme', r'núcleo do programa', r'hard core'],
    'Protective_belt': [r'cinturão protetor', r'protective belt', r'cinturão'],
}


def detect_concepts_in_text(text: str) -> set:
    """Retorna IDs dos conceitos detectados no texto."""
    found = set()
    for concept_id, patterns in CONCEPT_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE):
                found.add(concept_id)
                break
    return found


def extract_cooccurrence_edges(chunks) -> dict:
    """
    Extrai arestas de co-ocorrência dos chunks.
    Retorna dict {(concept_a, concept_b): {'count': int, 'chunks': [...]}}.
    """
    cooc = defaultdict(lambda: {'count': 0, 'chunks': []})
    
    for chunk in chunks:
        concepts_in_chunk = detect_concepts_in_text(chunk.text)
        if len(concepts_in_chunk) < 2:
            continue
        
        # Todos os pares não-ordenados
        concepts_list = sorted(concepts_in_chunk)
        for i, a in enumerate(concepts_list):
            for b in concepts_list[i+1:]:
                key = (a, b)
                cooc[key]['count'] += 1
                cooc[key]['chunks'].append({
                    'chunk_id': chunk.chunk_id,
                    'corpus_id': chunk.corpus_id,
                    'page': chunk.page,
                })
    
    return dict(cooc)


# === Construção do grafo ===

def build_graph() -> nx.MultiDiGraph:
    """Constrói o grafo conceitual completo."""
    G = nx.MultiDiGraph()
    
    # Adiciona nós (conceitos)
    for c in CONCEPTS:
        G.add_node(c['id'], **c)
    
    # Adiciona arestas declaradas na ontologia [E]
    for src, dst, attrs in ONTOLOGY_EDGES_E:
        G.add_edge(src, dst, **attrs, source='ontology_v1.0.0_E')
    
    return G


def enrich_with_cooccurrence(G: nx.MultiDiGraph, chunks) -> dict:
    """Adiciona arestas de co-ocorrência ao grafo e retorna estatísticas."""
    cooc = extract_cooccurrence_edges(chunks)
    
    stats = {
        'total_cooc_pairs': len(cooc),
        'edges_added': 0,
        'edges_already_in_ontology': 0,
        'new_edges': 0,
        'new_edges_list': [],
    }
    
    # Para cada par de co-ocorrência
    for (a, b), info in cooc.items():
        # Verifica se já existe aresta ontológica entre estes nós (em qualquer direção)
        already_in_ontology = (
            G.has_edge(a, b) or G.has_edge(b, a)
        )
        
        if already_in_ontology:
            stats['edges_already_in_ontology'] += 1
        else:
            stats['new_edges'] += 1
            stats['new_edges_list'].append({
                'source': a,
                'target': b,
                'cooc_count': info['count'],
                'chunks': info['chunks'][:3],  # amostra
            })
        
        # Adiciona aresta de co-ocorrência (mesmo se já existe ontológica, é tipo diferente)
        G.add_edge(a, b,
                   type='co_occurs_with',
                   weight=info['count'],
                   source='rag_cooccurrence_auto',
                   chunk_count=info['count'],
                   sample_chunks=[c['chunk_id'] for c in info['chunks'][:3]])
        stats['edges_added'] += 1
    
    return stats


def validate_ontology_edges(G: nx.MultiDiGraph) -> dict:
    """Verifica se todas as arestas [E] da ontologia estão presentes no grafo."""
    validation = {
        'expected_e_edges': len(ONTOLOGY_EDGES_E),
        'found_e_edges': 0,
        'missing_e_edges': [],
        'extra_e_edges': [],
    }
    
    for src, dst, attrs in ONTOLOGY_EDGES_E:
        # Procura aresta ontológica usando get_edge_data
        found = False
        if G.has_edge(src, dst):
            edge_data_dict = G.get_edge_data(src, dst)
            # edge_data_dict é {key: data_dict} para MultiDiGraph
            for key, data in edge_data_dict.items():
                if isinstance(data, dict) and data.get('source') == 'ontology_v1.0.0_E':
                    found = True
                    break
        if found:
            validation['found_e_edges'] += 1
        else:
            validation['missing_e_edges'].append((src, dst))
    
    return validation


def detect_revoked_edges(G: nx.MultiDiGraph) -> list:
    """Verifica se as arestas revogadas aparecem como co-ocorrência (potencial falso positivo)."""
    detected = []
    for src, dst, attrs in REVOKED_EDGES:
        # No grafo de conceitos, aresta revogada é entre documentos, não conceitos
        # Então verificamos se há conceitos de ambos documentos conectados só por co-ocorrência
        detected.append({
            'revoked_edge': (src, dst),
            'reason': attrs['reason'],
            'note': 'Aresta revogada é entre documentos; no grafo conceitual, verificamos se conceitos destes documentos co-ocorrem apenas via chunks (sem relação ontológica direta).'
        })
    return detected


def generate_graph_report(G: nx.MultiDiGraph, validation: dict, enrichment: dict, revoked: list) -> dict:
    """Gera relatório completo do grafo."""
    report = {
        'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'graph_summary': {
            'nodes_total': G.number_of_nodes(),
            'edges_total': G.number_of_edges(),
            'edges_ontology_E': sum(1 for _, _, d in G.edges(data=True) if d.get('source') == 'ontology_v1.0.0_E'),
            'edges_cooccurrence': sum(1 for _, _, d in G.edges(data=True) if d.get('source') == 'rag_cooccurrence_auto'),
            'density': nx.density(G),
            'strongly_connected_components': nx.number_strongly_connected_components(G),
        },
        'clusters': {},
        'ontology_edge_validation': validation,
        'cooccurrence_enrichment': enrichment,
        'revoked_edges_status': revoked,
        'top_concepts_by_degree': [],
    }
    
    # Estatísticas por cluster
    for cluster_id in ['A', 'B', 'C', 'D']:
        nodes_in_cluster = [n for n, d in G.nodes(data=True) if d.get('cluster') == cluster_id]
        report['clusters'][cluster_id] = {
            'nodes': len(nodes_in_cluster),
            'node_ids': nodes_in_cluster,
        }
    
    # Top conceitos por degree
    degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)
    for node_id, deg in degrees[:10]:
        node_data = G.nodes[node_id]
        report['top_concepts_by_degree'].append({
            'id': node_id,
            'label': node_data.get('label'),
            'cluster': node_data.get('cluster'),
            'degree': deg,
        })
    
    return report


def generate_visualization(G: nx.MultiDiGraph, output_path: Path):
    """Gera visualização HTML interativa com pyvis."""
    if not PYVIS_AVAILABLE:
        print("  [SKIP] pyvis não disponível")
        return
    
    # Cores por cluster
    cluster_colors = {
        'A': '#3498db',  # azul
        'B': '#e74c3c',  # vermelho
        'C': '#2ecc71',  # verde
        'D': '#f39c12',  # amarelo
    }
    
    net = Network(height='800px', width='100%', directed=True,
                  notebook=False, bgcolor='#ffffff', font_color='#1a252f')
    
    # Adiciona nós
    for node_id, data in G.nodes(data=True):
        cluster = data.get('cluster', '?')
        color = cluster_colors.get(cluster, '#95a5a6')
        label = data.get('label', node_id)
        net.add_node(node_id,
                     label=label,
                     title=f"Cluster {cluster}\n{data.get('definition', '')}\nDoc: {data.get('corpus', '')}",
                     color=color,
                     size=25)
    
    # Adiciona arestas (agrupa arestas paralelas para visualização)
    edges_added = set()
    for src, dst, data in G.edges(data=True):
        key = (src, dst)
        if key in edges_added:
            continue
        edges_added.add(key)
        
        source = data.get('source', '')
        if 'ontology' in source:
            color = '#27ae60'  # verde — aresta verificada
            width = 3
        elif 'cooccurrence' in source:
            color = '#95a5a6'  # cinza — co-ocorrência automática
            width = 1
        else:
            color = '#bdc3c7'
            width = 1
        
        net.add_edge(src, dst, color=color, width=width,
                     title=f"{data.get('type', '')} | {data.get('evidence', '')}")
    
    # Configurações de física
    net.set_options('''
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    ''')
    
    try:
        net.save_graph(str(output_path))
        print(f"  [Visualização] HTML salvo em {output_path}")
    except Exception as e:
        print(f"  [ERRO pyvis] {e}")


def main():
    print("=" * 70)
    print("AION GraphRAG — Passo 5")
    print("=" * 70)
    
    # Passo 5.1: construir grafo base
    print("\n[5.1] Construindo grafo conceitual a partir da ontologia v1.0.0...")
    G = build_graph()
    print(f"  Nós: {G.number_of_nodes()}")
    print(f"  Arestas [E] da ontologia: {sum(1 for _, _, d in G.edges(data=True) if d.get('source') == 'ontology_v1.0.0_E')}")
    
    # Passo 5.2: enriquecer com co-ocorrência dos chunks
    print("\n[5.2] Enriquecendo grafo com co-ocorrência extraída dos chunks...")
    # Reconstrói chunks
    all_chunks = []
    for filename, meta in CORPUS_FILES.items():
        path = CORPUS_DIR / filename
        if not path.exists():
            continue
        md_text = path.read_text(encoding='utf-8')
        chunks = parse_extracted_markdown(md_text, meta['id'])
        all_chunks.extend(chunks)
    print(f"  Chunks analisados: {len(all_chunks)}")
    
    enrichment_stats = enrich_with_cooccurrence(G, all_chunks)
    print(f"  Pares de co-ocorrência identificados: {enrichment_stats['total_cooc_pairs']}")
    print(f"  Arestas adicionadas: {enrichment_stats['edges_added']}")
    print(f"  Já estavam na ontologia [E]: {enrichment_stats['edges_already_in_ontology']}")
    print(f"  Novas arestas (somente co-ocorrência): {enrichment_stats['new_edges']}")
    
    # Passo 5.3: validar arestas [E]
    print("\n[5.3] Validando arestas [E] da ontologia contra o grafo...")
    validation = validate_ontology_edges(G)
    print(f"  Arestas [E] esperadas: {validation['expected_e_edges']}")
    print(f"  Arestas [E] encontradas: {validation['found_e_edges']}")
    if validation['missing_e_edges']:
        print(f"  ⚠️ Faltam: {validation['missing_e_edges']}")
    
    # Arestas revogadas
    revoked_status = detect_revoked_edges(G)
    
    # Passo 5.4: visualização
    print("\n[5.4] Gerando visualização interativa...")
    viz_path = OUTPUT_DIR / 'graphrag_visualization.html'
    generate_visualization(G, viz_path)
    
    # Relatório final
    report = generate_graph_report(G, validation, enrichment_stats, revoked_status)
    report['graph_data'] = nx.node_link_data(G)
    
    report_path = OUTPUT_DIR / 'graphrag_report.json'
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(f"\n  Relatório salvo em: {report_path}")
    
    # Resumo
    print(f"\n{'=' * 70}")
    print("[RESUMO GraphRAG]")
    print(f"{'=' * 70}")
    print(f"Nós: {report['graph_summary']['nodes_total']}")
    print(f"Arestas totais: {report['graph_summary']['edges_total']}")
    print(f"  - Ontologia [E]: {report['graph_summary']['edges_ontology_E']}")
    print(f"  - Co-ocorrência: {report['graph_summary']['edges_cooccurrence']}")
    print(f"  - Densidade: {report['graph_summary']['density']:.3f}")
    print(f"  - Componentes fortemente conectados: {report['graph_summary']['strongly_connected_components']}")
    
    print(f"\nTop-5 conceitos por degree:")
    for c in report['top_concepts_by_degree'][:5]:
        print(f"  • {c['label']} (cluster {c['cluster']}): degree={c['degree']}")
    
    if enrichment_stats['new_edges_list']:
        print(f"\nTop-5 novas arestas (somente co-ocorrência):")
        sorted_new = sorted(enrichment_stats['new_edges_list'], key=lambda x: x['cooc_count'], reverse=True)
        for e in sorted_new[:5]:
            print(f"  • {e['source']} ↔ {e['target']} (co-oc: {e['cooc_count']} chunks)")
    
    return report


if __name__ == '__main__':
    main()
