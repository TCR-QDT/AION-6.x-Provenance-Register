#!/usr/bin/env python3
"""
AION Passo 6.2 Etapas 6.2.3-6.2.5 — Experimentos B, C, D isolados

Cada experimento altera UM ÚNICO mecanismo entre EVIDÊNCIA e RETRIEVAL:
- B: Normalização matemática (β→beta, ×→*, etc.) — altera apenas representação experimental
- C: Chunking matemático — altera apenas boundaries de chunk
- D: Tokenização matemática — altera apenas token_pattern do TF-IDF

Regras:
- Documento-fonte preservado exatamente (evidência inalterada)
- Apenas representação intermediária é alterada
- Corpus v1.3.0, GraphRAG, P-REP-001 v0.3, AION-EVAL-002 v0.2: FROZEN
- Cada experimento testado isoladamente
- invalid_count > 0 invalida provenance

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

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from aion_rag_proxy import parse_extracted_markdown, Chunk, RetrievedChunk
from aion_bench_001 import BENCH_TESTS
from aion_p_resp_001_v03 import ProvenanceValidator
from aion_6_1_f_rebenchmark_lcr import CORPUS_V13_FILES

OUTPUT_DIR = Path('/home/z/my-project/download/rag')


# === Mapeamentos de normalização matemática ===

MATH_NORMALIZATION = {
    'β': 'beta',
    'α': 'alpha',
    'µ': 'mu',
    'μ': 'mu',  # variant
    'ν': 'nu',
    '×': '*',
    '·': '*',
    '∂': 'partial',
    '∇': 'nabla',
    '∑': 'sum',
    '∏': 'prod',
    '∫': 'int',
    'Φ': 'Phi',
    'Φcat': 'Phi_cat',
    'Φ_cat': 'Phi_cat',
    'λ': 'lambda',
    'η': 'eta',
    'γ': 'gamma',
    'δ': 'delta',
    'θ': 'theta',
    'π': 'pi',
    'ρ': 'rho',
    'σ': 'sigma',
    'τ': 'tau',
    'Λ': 'Lambda',
    'Ω': 'Omega',
    'Δ': 'Delta',
    'Θ': 'Theta',
    'Σ': 'Sigma',
    '≤': '<=',
    '≥': '>=',
    '≠': '!=',
    '≈': 'approx',
    '∞': 'infinity',
    '√': 'sqrt',
    '±': '+-',
    '∈': 'in',
    '∉': 'notin',
    '∀': 'forall',
    '∃': 'exists',
    '≅': 'cong',
    '≡': 'equiv',
    '∝': 'prop',
}


def normalize_math(text: str) -> str:
    """Normaliza símbolos matemáticos para ASCII."""
    normalized = text
    for unicode_char, ascii_replacement in MATH_NORMALIZATION.items():
        normalized = normalized.replace(unicode_char, ascii_replacement)
    return normalized


# === Store base reutilizável ===

def build_base_chunks() -> list:
    """Constrói lista de chunks do corpus v1.3.0 (mesma função do 6.1-F)."""
    all_chunks = []
    for filename, meta in CORPUS_V13_FILES.items():
        path = meta['path']
        if not path.exists():
            continue
        md_text = path.read_text(encoding='utf-8')
        chunks = parse_extracted_markdown(md_text, meta['id'])
        all_chunks.extend(chunks)
    return all_chunks


# === Experimento B — Normalização matemática ===

class ExperimentB_Store:
    """Store com normalização matemática aplicada apenas à representação."""
    
    def __init__(self, chunks: list):
        self.chunks = chunks
        # Aplica normalização APENAS à representação (texto para TF-IDF)
        # Documento-fonte (chunk.text original) permanece inalterado
        self.normalized_texts = [normalize_math(c.text) for c in self.chunks]
        
        self.vectorizer = TfidfVectorizer(
            max_features=4096,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            token_pattern=r'(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9_]+\b',  # mesmo token_pattern do controle
        )
        self.matrix = self.vectorizer.fit_transform(self.normalized_texts)
        print(f"  [Exp B] Vocabulário: {len(self.vectorizer.vocabulary_)} termos")
        print(f"  [Exp B] 'beta' no vocabulário: {'beta' in self.vectorizer.vocabulary_}")
        print(f"  [Exp B] 'mu' no vocabulário: {'mu' in self.vectorizer.vocabulary_}")
    
    def query(self, question: str, top_k: int = 8):
        # Normaliza também a pergunta
        normalized_question = normalize_math(question)
        q_vec = self.vectorizer.transform([normalized_question])
        scores = cosine_similarity(q_vec, self.matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for rank, idx in enumerate(top_indices, 1):
            r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
            results.append(r)
        return results


# === Experimento C — Chunking matemático ===

class ExperimentC_Store:
    """Store com chunking matemático — preserva fórmulas como unidades."""

    def __init__(self, chunks: list):
        # Re-chunca preservando fórmulas matemáticas como unidades semânticas
        # Detecta fórmulas no padrão X = Y × Z^β (com símbolos matemáticos)
        # e as mantém intactas dentro de chunks
        self.chunks = self.rechunk_preserving_math(chunks)

        self.vectorizer = TfidfVectorizer(
            max_features=4096,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            token_pattern=r'(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9_]+\b',  # mesmo token_pattern do controle
        )
        texts = [c.text for c in self.chunks]
        self.matrix = self.vectorizer.fit_transform(texts)
        print(f"  [Exp C] Chunks após re-chunking: {len(self.chunks)}")
        print(f"  [Exp C] Vocabulário: {len(self.vectorizer.vocabulary_)} termos")

    def rechunk_preserving_math(self, original_chunks: list) -> list:
        """Re-chunca preservando fórmulas matemáticas como unidades."""
        new_chunks = []

        # Padrões de fórmulas matemáticas (preservar como unidades)
        math_formula_pattern = re.compile(
            r'('
            r'[A-Za-zΦαβγδεζηθικλμνξπρστυφχψωΛΞΠΣΦΨΩΔΘ]\s*=\s*[^=\n]{1,80}'  # X = ...
            r'|C\s*=\s*I\s*[×x]\s*S\s*[×x]\s*'  # C = I × S ×
            r'|β\s*=\s*[\d.]+'  # β = 0.5
            r'|T_?2\s*=\s*'  # T2 = ...
            r'|Gµν\s*='  # Gµν =
            r'|Qµν\s*='  # Qµν =
            r')',
            re.IGNORECASE
        )

        for chunk in original_chunks:
            text = chunk.text

            # Encontra todas as fórmulas no chunk
            formulas = list(math_formula_pattern.finditer(text))

            if not formulas:
                # Sem fórmulas detectadas — manter chunk original
                new_chunks.append(chunk)
                continue

            # Se há fórmulas, criar chunk separado para cada fórmula + contexto
            # Estratégia: dividir o chunk em torno das fórmulas
            # Mantém 100 chars antes e depois de cada fórmula
            last_end = 0
            for i, match in enumerate(formulas):
                formula_start = match.start()
                formula_end = match.end()

                # Contexto: 100 chars antes da fórmula
                context_start = max(last_end, formula_start - 100)
                # Contexto: 100 chars depois da fórmula
                context_end = min(len(text), formula_end + 100)

                # Extrair sub-chunk com fórmula + contexto
                sub_text = text[context_start:context_end].strip()
                if sub_text:
                    import hashlib as hl
                    sub_hash = hl.sha256(sub_text.encode()).hexdigest()[:12]
                    new_chunk = Chunk(
                        chunk_id=f"{chunk.chunk_id}#math_{i+1:02d}",
                        corpus_id=chunk.corpus_id,
                        short_title=chunk.short_title,
                        page=chunk.page,
                        section=chunk.section,
                        text=sub_text,
                        char_count=len(sub_text),
                        chunk_hash=sub_hash,
                    )
                    new_chunks.append(new_chunk)

                last_end = context_end

            # Adicionar resto do texto (após última fórmula)
            if last_end < len(text):
                remaining = text[last_end:].strip()
                if remaining and len(remaining) > 50:
                    new_chunks.append(chunk)

        # Deduplicar chunks (alguns podem ter sido adicionados duas vezes)
        seen_hashes = set()
        unique_chunks = []
        for c in new_chunks:
            if c.chunk_hash not in seen_hashes:
                seen_hashes.add(c.chunk_hash)
                unique_chunks.append(c)

        return unique_chunks

    def query(self, question: str, top_k: int = 8):
        q_vec = self.vectorizer.transform([question])
        scores = cosine_similarity(q_vec, self.matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for rank, idx in enumerate(top_indices, 1):
            r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
            results.append(r)
        return results


# === Experimento D — Tokenização matemática ===

class ExperimentD_Store:
    """Store com token_pattern estendido para capturar símbolos matemáticos."""

    def __init__(self, chunks: list):
        self.chunks = chunks

        # Token pattern estendido para incluir símbolos matemáticos
        # Permite: letras (incluindo acentuadas), dígitos, _, e símbolos matemáticos
        math_symbols_class = 'βγδαεζηθικλμνξπρστυφχψωΛΞΠΣΦΨΩΔΘ=×·*Φcat_'
        extended_token_pattern = rf'(?u)\b[a-zA-ZÀ-ÿ{math_symbols_class}][a-zA-ZÀ-ÿ0-9_{math_symbols_class}]+\b'

        self.vectorizer = TfidfVectorizer(
            max_features=4096,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            token_pattern=extended_token_pattern,
        )
        texts = [c.text for c in self.chunks]
        self.matrix = self.vectorizer.fit_transform(texts)
        print(f"  [Exp D] Vocabulário: {len(self.vectorizer.vocabulary_)} termos")
        print(f"  [Exp D] 'β' no vocabulário: {'β' in self.vectorizer.vocabulary_}")
        print(f"  [Exp D] 'Hβ' no vocabulário: {'Hβ' in self.vectorizer.vocabulary_}")
        print(f"  [Exp D] 'C' no vocabulário: {'C' in self.vectorizer.vocabulary_}")
        print(f"  [Exp D] 'TCR' no vocabulário: {'TCR' in self.vectorizer.vocabulary_}")

    def query(self, question: str, top_k: int = 8):
        q_vec = self.vectorizer.transform([question])
        scores = cosine_similarity(q_vec, self.matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for rank, idx in enumerate(top_indices, 1):
            r = RetrievedChunk(chunk=self.chunks[idx], score=float(scores[idx]), rank=rank)
            results.append(r)
        return results


# === Avaliação de B1 para cada experimento ===

def evaluate_b1_for_experiment(store, experiment_name: str, n_runs: int = 3) -> dict:
    """Avalia B1 para um experimento (3 runs para verificar determinismo)."""
    print(f"\n  Avaliando B1 com {experiment_name} ({n_runs} runs)...")
    
    test = BENCH_TESTS['B1']
    expected_prefix = 'CORPUS-002#p1'
    
    runs = []
    for run_idx in range(1, n_runs + 1):
        retrieved = store.query(test['pergunta'], top_k=8)
        
        # Top-3 chunks
        top3 = [
            {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
            for i, r in enumerate(retrieved[:3])
        ]
        
        # Verificar hit
        hit_top3 = any(r['chunk_id'].startswith(expected_prefix) for r in top3)
        hit_top5 = any(retrieved[i].chunk.chunk_id.startswith(expected_prefix) for i in range(min(5, len(retrieved))))
        
        # Rank do chunk esperado (se recuperado)
        expected_rank = None
        for r in retrieved:
            if r.chunk.chunk_id.startswith(expected_prefix):
                expected_rank = r.rank
                break
        
        run_result = {
            'run_idx': run_idx,
            'top3_chunks': top3,
            'hit_top3': hit_top3,
            'hit_top5': hit_top5,
            'expected_rank': expected_rank,
        }
        runs.append(run_result)
        
        if run_idx == 1:
            print(f"    Top-3 recuperado:")
            for r in top3:
                marker = '✅' if r['chunk_id'].startswith(expected_prefix) else '  '
                print(f"      {marker} #{r['rank']} score={r['score']:.4f} | {r['chunk_id']:<30} | {r['corpus_id']}")
            print(f"    Hit top-3: {hit_top3}")
            if expected_rank:
                print(f"    Expected rank: #{expected_rank}")
    
    # Estatísticas
    hits_top3 = sum(1 for r in runs if r['hit_top3'])
    hits_top5 = sum(1 for r in runs if r['hit_top5'])
    
    # Verificar determinismo (top-3 idêntico em todos os runs)
    top3_sets = [tuple(r['chunk_id'] for r in run['top3_chunks']) for run in runs]
    deterministic = all(s == top3_sets[0] for s in top3_sets)
    
    return {
        'experiment': experiment_name,
        'runs': runs,
        'n_runs': n_runs,
        'hits_top3': hits_top3,
        'hits_top5': hits_top5,
        'retrieval_hit_rate': hits_top3 / n_runs,
        'deterministic': deterministic,
        'B1_status': 'PASS' if hits_top3 == n_runs else ('PARTIAL' if hits_top3 > 0 else 'FAIL-SYSTEM'),
    }


# === Main ===

def main():
    print("=" * 70)
    print("AION Passo 6.2 Etapas 6.2.3-6.2.5 — Experimentos B, C, D isolados")
    print("=" * 70)
    
    # Constrói chunks base
    print("\n[SETUP] Construindo chunks base do corpus v1.3.0...")
    base_chunks = build_base_chunks()
    print(f"  Base chunks: {len(base_chunks)}")
    
    # === EXPERIMENTO B — Normalização matemática ===
    print(f"\n{'=' * 70}")
    print("[6.2.3] EXPERIMENTO B — Normalização matemática")
    print(f"{'=' * 70}")
    print("\n  Documento-fonte: PRESERVADO (evidência inalterada)")
    print("  Representação experimental: normalizada (β→beta, ×→*, etc.)")
    
    exp_b_store = ExperimentB_Store(base_chunks)
    exp_b_result = evaluate_b1_for_experiment(exp_b_store, 'B (Normalização)', n_runs=3)
    
    print(f"\n  Resultado Experimento B:")
    print(f"    Hits top-3: {exp_b_result['hits_top3']}/3")
    print(f"    Retrieval hit rate: {exp_b_result['retrieval_hit_rate']:.2%}")
    print(f"    B1 status: {exp_b_result['B1_status']}")
    print(f"    Deterministic: {exp_b_result['deterministic']}")
    
    # === EXPERIMENTO C — Chunking matemático ===
    print(f"\n{'=' * 70}")
    print("[6.2.4] EXPERIMENTO C — Chunking matemático")
    print(f"{'=' * 70}")
    print("\n  Documento-fonte: PRESERVADO (evidência inalterada)")
    print("  Chunking: re-estruturado para preservar fórmulas como unidades")
    
    exp_c_store = ExperimentC_Store(base_chunks)
    exp_c_result = evaluate_b1_for_experiment(exp_c_store, 'C (Chunking)', n_runs=3)
    
    print(f"\n  Resultado Experimento C:")
    print(f"    Hits top-3: {exp_c_result['hits_top3']}/3")
    print(f"    Retrieval hit rate: {exp_c_result['retrieval_hit_rate']:.2%}")
    print(f"    B1 status: {exp_c_result['B1_status']}")
    print(f"    Deterministic: {exp_c_result['deterministic']}")
    
    # === EXPERIMENTO D — Tokenização matemática ===
    print(f"\n{'=' * 70}")
    print("[6.2.5] EXPERIMENTO D — Tokenização matemática")
    print(f"{'=' * 70}")
    print("\n  Documento-fonte: PRESERVADO (evidência inalterada)")
    print("  Tokenização: token_pattern estendido para símbolos matemáticos")
    
    exp_d_store = ExperimentD_Store(base_chunks)
    exp_d_result = evaluate_b1_for_experiment(exp_d_store, 'D (Tokenização)', n_runs=3)
    
    print(f"\n  Resultado Experimento D:")
    print(f"    Hits top-3: {exp_d_result['hits_top3']}/3")
    print(f"    Retrieval hit rate: {exp_d_result['retrieval_hit_rate']:.2%}")
    print(f"    B1 status: {exp_d_result['B1_status']}")
    print(f"    Deterministic: {exp_d_result['deterministic']}")
    
    # === COMPARAÇÃO ===
    print(f"\n{'=' * 70}")
    print("[6.2.6] COMPARAÇÃO B/C/D × Controle")
    print(f"{'=' * 70}")
    
    # Carrega baseline (Experimento A — Controle)
    baseline_path = OUTPUT_DIR / 'aion_6_2_baseline_diagnosis.json'
    baseline_data = json.loads(baseline_path.read_text(encoding='utf-8'))
    baseline_b1 = baseline_data['stage_6_2_1_b1_reproduction']
    
    comparison = {
        'A (Controle)': {
            'intervention': 'NENHUMA (TF-IDF atual)',
            'hits_top3': baseline_b1['hits'],
            'retrieval_hit_rate': baseline_b1['baseline_retrieval_hit_rate'],
            'B1_status': baseline_b1['baseline_B1'],
            'deterministic': baseline_b1['deterministic'],
        },
        'B (Normalização)': {
            'intervention': 'Normalização matemática (β→beta, ×→*)',
            'hits_top3': exp_b_result['hits_top3'],
            'retrieval_hit_rate': exp_b_result['retrieval_hit_rate'],
            'B1_status': exp_b_result['B1_status'],
            'deterministic': exp_b_result['deterministic'],
        },
        'C (Chunking)': {
            'intervention': 'Chunking matemático (preservar fórmulas)',
            'hits_top3': exp_c_result['hits_top3'],
            'retrieval_hit_rate': exp_c_result['retrieval_hit_rate'],
            'B1_status': exp_c_result['B1_status'],
            'deterministic': exp_c_result['deterministic'],
        },
        'D (Tokenização)': {
            'intervention': 'Token_pattern estendido (símbolos matemáticos)',
            'hits_top3': exp_d_result['hits_top3'],
            'retrieval_hit_rate': exp_d_result['retrieval_hit_rate'],
            'B1_status': exp_d_result['B1_status'],
            'deterministic': exp_d_result['deterministic'],
        },
    }
    
    print(f"\n{'Braço':<25} {'Intervention':<45} {'Hits':<8} {'Hit Rate':<10} {'B1':<15} {'Det'}")
    print('-' * 115)
    for arm, data in comparison.items():
        print(f"{arm:<25} {data['intervention'][:43]:<45} {data['hits_top3']}/3      {data['retrieval_hit_rate']:.0%}      {data['B1_status']:<15} {'✅' if data['deterministic'] else '❌'}")
    
    # Identificar melhor braço
    best_arm = max(comparison.items(), key=lambda x: x[1]['retrieval_hit_rate'])
    
    print(f"\n  Melhor braço: {best_arm[0]}")
    print(f"    Retrieval hit rate: {best_arm[1]['retrieval_hit_rate']:.2%}")
    print(f"    B1 status: {best_arm[1]['B1_status']}")
    
    # Salvar relatório
    report = {
        'metadata': {
            'experiment': 'AION-6.2 Etapas 6.2.3-6.2.5 — Experimentos B, C, D',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'experiment_B_normalization': {
            'description': 'Normalização matemática (β→beta, ×→*, etc.)',
            'document_preservation': 'Documento-fonte PRESERVADO; apenas representação experimental normalizada',
            'result': exp_b_result,
        },
        'experiment_C_chunking': {
            'description': 'Chunking matemático (preservar fórmulas como unidades)',
            'document_preservation': 'Documento-fonte PRESERVADO; apenas boundaries de chunk alterados',
            'result': exp_c_result,
        },
        'experiment_D_tokenization': {
            'description': 'Token_pattern estendido para símbolos matemáticos',
            'document_preservation': 'Documento-fonte PRESERVADO; apenas token_pattern alterado',
            'result': exp_d_result,
        },
        'comparison': comparison,
        'best_arm': {
            'name': best_arm[0],
            'data': best_arm[1],
        },
        'next_step': '6.2.7 — Rebenchmark B1-B7 da melhor intervenção',
        'rules_preserved': [
            'Corpus v1.3.0: FROZEN',
            'GraphRAG: FROZEN',
            'P-RESP-001 v0.3: FROZEN',
            'AION-EVAL-002 v0.2: FROZEN',
            'Documento-fonte: PRESERVADO em todos os braços',
        ],
    }
    
    json_path = OUTPUT_DIR / 'aion_6_2_experiments_bcd.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
