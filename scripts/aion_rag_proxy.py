#!/usr/bin/env python3
"""
AION RAG Proxy — Passo 4

Implementação mínima de RAG para validação do Plano de Teste do AION-MVP-001.
Substitui AnythingLLM (que requer Docker) por stack local:
- Chunking semântico por seção/página
- Embeddings TF-IDF (scikit-learn)
- Vector store em memória (numpy cosine similarity)
- Geração via z-ai-web-dev-sdk CLI

Autor: IA Curadora
Data: 17 de agosto de 2026
"""

import os
import re
import json
import subprocess
import hashlib
import math
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timezone

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# === Configurações ===

CORPUS_DIR = Path('/home/z/my-project/download')
OUTPUT_DIR = Path('/home/z/my-project/download/rag')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Mapeamento de arquivos extraídos -> metadados do corpus
CORPUS_FILES = {
    'CORPUS-001_extracted.md': {
        'id': 'CORPUS-001',
        'short_title': 'AION-DOC-000',
        'full_title': 'Especificação do Documento Canônico',
        'kind': 'normativo',
    },
    'CORPUS-002_extracted.md': {
        'id': 'CORPUS-002',
        'short_title': 'Paper A',
        'full_title': 'Relational Coherence in Biological Networks (TCR)',
        'kind': 'paper',
    },
    'CORPUS-003_extracted.md': {
        'id': 'CORPUS-003',
        'short_title': 'Parte IV',
        'full_title': 'Formalização Teórica — Functor Φcat, Tensor Qµν',
        'kind': 'paper',
    },
    'CORPUS-004_extracted.md': {
        'id': 'CORPUS-004',
        'short_title': 'Paper B',
        'full_title': 'Dinâmica Quântica Dissipativa (FMO 7-sítios)',
        'kind': 'paper',
    },
    'CORPUS-005_extracted.md': {
        'id': 'CORPUS-005',
        'short_title': 'Cover Letter',
        'full_title': 'Carta de Apresentação Paper A — PRE',
        'kind': 'carta',
    },
}

CHUNK_MAX_CHARS = 1500  # ~300-400 tokens
CHUNK_OVERLAP_CHARS = 200


# === Modelo de dados ===

@dataclass
class Chunk:
    chunk_id: str
    corpus_id: str
    short_title: str
    page: str  # ex: "p.4" ou "intro"
    section: str  # ex: "Sec. 2.1"
    text: str
    char_count: int
    chunk_hash: str  # hash do conteúdo para auditoria


@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float
    rank: int


# === Chunking ===

def parse_extracted_markdown(md_text: str, corpus_id: str) -> List[Chunk]:
    """
    Faz parse do Markdown estruturado gerado pelo extract_aion_corpus.py.
    Cada chunk é uma seção/página identificada.
    """
    chunks = []
    
    # Padrão: ### Página X
    page_pattern = re.compile(r'^### Página (\d+)', re.MULTILINE)
    page_matches = list(page_pattern.finditer(md_text))
    
    if not page_matches:
        # Documento sem páginas (Cover Letter, DOC-000)
        # Cria um único chunk para o conteúdo integral
        text = md_text.strip()
        if text:
            chunk_hash = hashlib.sha256(text.encode()).hexdigest()[:12]
            chunks.append(Chunk(
                chunk_id=f"{corpus_id}#chunk_001",
                corpus_id=corpus_id,
                short_title=CORPUS_FILES.get(f"{corpus_id}_extracted.md", {}).get('short_title', corpus_id),
                page="full",
                section="integral",
                text=text,
                char_count=len(text),
                chunk_hash=chunk_hash,
            ))
        return chunks
    
    for i, match in enumerate(page_matches):
        page_num = match.group(1)
        start = match.end()
        end = page_matches[i + 1].start() if i + 1 < len(page_matches) else len(md_text)
        page_content = md_text[start:end].strip()
        
        # Remove marcadores <details>...</details>
        page_content = re.sub(r'<details>.*?</details>', '', page_content, flags=re.DOTALL)
        # Remove blocos ```text ... ```
        page_content = re.sub(r'```(?:text)?\n(.*?)\n```', r'\1', page_content, flags=re.DOTALL)
        # Remove headers de Metadados
        page_content = re.sub(r'## Metadados.*?(?=##|$)', '', page_content, flags=re.DOTALL)
        
        page_content = page_content.strip()
        if not page_content:
            continue
        
        # Divide em sub-chunks se a página for muito longa
        sub_chunks = split_long_text(page_content, CHUNK_MAX_CHARS, CHUNK_OVERLAP_CHARS)
        
        for j, sub in enumerate(sub_chunks):
            if not sub.strip():
                continue
            
            # Detecta seção (cabeçalho mais próximo no início do sub)
            section = detect_section(sub)
            
            chunk_hash = hashlib.sha256(sub.encode()).hexdigest()[:12]
            chunks.append(Chunk(
                chunk_id=f"{corpus_id}#p{page_num}_{j+1:02d}",
                corpus_id=corpus_id,
                short_title=CORPUS_FILES.get(f"{corpus_id}_extracted.md", {}).get('short_title', corpus_id),
                page=f"p.{page_num}",
                section=section,
                text=sub,
                char_count=len(sub),
                chunk_hash=chunk_hash,
            ))
    
    return chunks


def split_long_text(text: str, max_chars: int, overlap: int) -> List[str]:
    """Divide texto longo em pedaços com sobreposição."""
    if len(text) <= max_chars:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        # Tenta cortar em quebra de linha próxima
        if end < len(text):
            last_newline = text.rfind('\n', start, end)
            if last_newline > start + max_chars // 2:
                end = last_newline
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
        if start >= len(text):
            break
    return chunks


def detect_section(text: str) -> str:
    """Tenta detectar a seção no início do chunk."""
    lines = text.strip().split('\n')
    for line in lines[:5]:
        s = line.strip()
        # Padrões como "2.1", "Sec. II", "Passo 16", etc.
        if re.match(r'^\d+\.?\d*\.?\d*\s+[A-ZÀ-Ú]', s):
            return s[:80]
        if re.match(r'^Passo\s+\d+', s, re.IGNORECASE):
            return s[:80]
        if re.match(r'^(Abstract|Introduction|Conclusion|References|Acknowledg)', s, re.IGNORECASE):
            return s[:80]
    return "—"


# === Vector Store ===

class TfidfVectorStore:
    def __init__(self):
        self.chunks: List[Chunk] = []
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.matrix: Optional[np.ndarray] = None
    
    def add_chunks(self, chunks: List[Chunk]):
        self.chunks.extend(chunks)
    
    def build_index(self):
        """Constrói índice TF-IDF após adicionar todos os chunks."""
        if not self.chunks:
            raise ValueError("Nenhum chunk para indexar")
        
        texts = [c.text for c in self.chunks]
        # n-gramas 1-2, max features 4096, remove stopwords inglês + portguês manual
        self.vectorizer = TfidfVectorizer(
            max_features=4096,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            token_pattern=r'(?u)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9_]+\b',
        )
        self.matrix = self.vectorizer.fit_transform(texts)
        print(f"  [Index] {len(self.chunks)} chunks indexados, matriz shape: {self.matrix.shape}")
    
    def query(self, question: str, top_k: int = 5) -> List[RetrievedChunk]:
        """Retorna os top_k chunks mais similares à pergunta."""
        if self.matrix is None:
            raise RuntimeError("Índice não construído")
        
        q_vec = self.vectorizer.transform([question])
        scores = cosine_similarity(q_vec, self.matrix).flatten()
        
        # Top-k
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for rank, idx in enumerate(top_indices, 1):
            results.append(RetrievedChunk(
                chunk=self.chunks[idx],
                score=float(scores[idx]),
                rank=rank,
            ))
        return results
    
    def save_state(self, path: Path):
        """Salva estado para auditoria."""
        state = {
            'chunk_count': len(self.chunks),
            'matrix_shape': list(self.matrix.shape) if self.matrix is not None else None,
            'vectorizer_vocab_size': len(self.vectorizer.vocabulary_) if self.vectorizer else 0,
            'chunks': [asdict(c) for c in self.chunks],
        }
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"  [Save] Estado salvo em {path}")


# === Geração (LLM) ===

def generate_answer(question: str, retrieved: List[RetrievedChunk]) -> Tuple[str, str]:
    """
    Gera resposta via z-ai CLI usando os chunks recuperados como contexto.
    Retorna (resposta, prompt_completo).
    """
    # Monta contexto com citação obrigatória
    context_parts = []
    for r in retrieved:
        context_parts.append(
            f"[{r.chunk.chunk_id} | {r.chunk.short_title} | {r.chunk.page} | {r.chunk.section} | score={r.score:.3f}]\n"
            f"{r.chunk.text}\n"
        )
    context = "\n---\n".join(context_parts)
    
    system_prompt = (
        "Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido. "
        "Para cada afirmação, cite o chunk_id de origem no formato [CORPUS-XXX#pY_ZZ]. "
        "Se a informação não estiver no contexto, diga 'INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO'. "
        "Não invente. Não use conhecimento externo. Responda em português."
    )
    
    user_prompt = f"""CONTEXTO RECUPERADO:

{context}

PERGUNTA: {question}

Responda usando apenas o contexto acima. Cada afirmação deve ter citação de chunk_id."""
    
    # Chama z-ai CLI
    try:
        result = subprocess.run(
            ['z-ai', 'chat',
             '--system', system_prompt,
             '--prompt', user_prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            return f"[ERRO z-ai: {result.stderr}]", user_prompt
        # Tenta parsear a resposta JSON
        try:
            data = json.loads(result.stdout)
            answer = data.get('content') or data.get('response') or result.stdout
        except json.JSONDecodeError:
            answer = result.stdout.strip()
        return answer, user_prompt
    except subprocess.TimeoutExpired:
        return "[ERRO z-ai: timeout]", user_prompt
    except Exception as e:
        return f"[ERRO z-ai: {e}]", user_prompt


# === Pipeline principal ===

def main():
    print("=" * 70)
    print("AION RAG PROXY — Passo 4")
    print("=" * 70)
    
    # Fase 2: Ingestão
    print("\n[FASE 2] Ingestão dos 5 documentos do corpus...")
    store = TfidfVectorStore()
    
    all_chunks = []
    for filename, meta in CORPUS_FILES.items():
        path = CORPUS_DIR / filename
        if not path.exists():
            print(f"  [SKIP] {filename} não encontrado")
            continue
        
        md_text = path.read_text(encoding='utf-8')
        chunks = parse_extracted_markdown(md_text, meta['id'])
        print(f"  [{meta['id']}] {filename} → {len(chunks)} chunks")
        all_chunks.extend(chunks)
        store.add_chunks(chunks)
    
    print(f"\n  TOTAL: {len(all_chunks)} chunks ingeridos")
    
    # Constrói índice
    print("\n[FASE 2] Construção do índice TF-IDF...")
    store.build_index()
    
    # Salva estado
    state_path = OUTPUT_DIR / 'rag_state.json'
    store.save_state(state_path)
    
    print(f"\n[OK] RAG pronto. {len(all_chunks)} chunks indexados.")
    print(f"     Estado salvo em: {state_path}")
    print(f"     Próximo passo: executar Plano de Teste (P1-P4)")
    
    return store


if __name__ == '__main__':
    main()
