#!/usr/bin/env python3
"""
AION Corpus Extractor — Passo 3 (Normalização via Docling-substitute)

Extrai texto estruturado de PDFs do corpus AION-001, preservando:
- Estrutura de seções (h1/h2/h3)
- Equações (preservadas como Unicode quando possível)
- Tabelas (extraídas via pdfplumber)
- Metadados do PDF
- Referências de página

Saída: Markdown estruturado por documento + relatório de extração.

Autor: IA Curadora
Data: 16 de agosto de 2026
"""

import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime, timezone

import fitz  # PyMuPDF
import pdfplumber

UPLOAD_DIR = Path('/home/z/my-project/upload')
OUTPUT_DIR = Path('/home/z/my-project/download')
SCRIPTS_DIR = Path('/home/z/my-project/scripts')

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Mapeamento nome de arquivo -> ID CORPUS
CORPUS_MAP = {
    'AION-DOC-000.html': 'CORPUS-001',
    'Paper_A_v6.2_FINAL.pdf': 'CORPUS-002',
    'PARTE_IV_Formalizacao_Teorica_PT-BR.pdf': 'CORPUS-003',
    'Paper_B_QDT_JCP_v6.1_PT-BR.pdf': 'CORPUS-004',
    'Cover_Letter_Paper_A_PRE_PT-BR.md': 'CORPUS-005',
}

# Heurística para detectar possíveis equações perdidas
MATH_CHARS = re.compile(r'[∂∇∫∑∏√∞±≤≥≠∈∉∪∩⊂⊃∀∃¬≡≅≈∝αβγδεζηθικλμνξπρστυφχψωΔΘΛΞΠΣΦΨΩ]')


def extract_metadata_pdf(pdf_path: Path) -> dict:
    """Extrai metadados embutidos no PDF."""
    doc = fitz.open(pdf_path)
    meta = dict(doc.metadata)
    meta['_page_count'] = len(doc)
    meta['_file_size_bytes'] = pdf_path.stat().st_size
    doc.close()
    return meta


def extract_text_by_page(pdf_path: Path) -> list:
    """Extrai texto página por página, preservando blocos."""
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        # Texto com preservação de layout
        text = page.get_text('text')
        # Blocos para análise estrutural
        blocks = page.get_text('blocks')
        pages.append({
            'page_number': i + 1,
            'text': text,
            'blocks': blocks,
        })
    doc.close()
    return pages


def extract_tables_pdf(pdf_path: Path) -> list:
    """Extrai tabelas via pdfplumber."""
    tables_found = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for j, table in enumerate(tables):
                tables_found.append({
                    'page': i + 1,
                    'table_index': j + 1,
                    'rows': table,
                })
    return tables_found


def detect_math_issues(text: str) -> list:
    """Heurística: identifica possíveis locais onde equações podem ter sido perdidas."""
    issues = []
    # Procura por padrões suspeitos: linhas curtas com símbolos matemáticos
    for line in text.split('\n'):
        if not line.strip():
            continue
        math_count = len(MATH_CHARS.findall(line))
        # Linha com alta densidade matemática mas curta — possível equação fragmentada
        if math_count >= 2 and len(line.strip()) < 80:
            issues.append(line.strip())
        # Linha com caracteres de substituição típicos de extração falha
        if '�' in line or '\ufffd' in line:
            issues.append(f'[CARACTERE PERDIDO] {line.strip()}')
    return issues


def render_markdown_table(rows: list) -> str:
    """Renderiza uma lista de linhas como tabela Markdown."""
    if not rows:
        return ''
    # Limpa células None
    cleaned = [[(c or '').strip() for c in row] for row in rows]
    max_cols = max(len(r) for r in cleaned)
    # Normaliza número de colunas
    cleaned = [r + [''] * (max_cols - len(r)) for r in cleaned]
    if len(cleaned) < 2:
        # Tabela sem cabeçalho claro
        header = cleaned[0] if cleaned else []
        body = []
    else:
        header = cleaned[0]
        body = cleaned[1:]
    md = ['| ' + ' | '.join(header) + ' |',
          '| ' + ' | '.join(['---'] * max_cols) + ' |']
    for row in body:
        md.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(md)


def detect_section_headers(text: str) -> list:
    """Heurística: identifica possíveis cabeçalhos de seção."""
    headers = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            continue
        # Padrões típicos de cabeçalho em papers científicos
        if re.match(r'^(\d+\.?\d*\.?\d*)\s+[A-ZÀ-Ú]', s) and len(s) < 100:
            headers.append({'line': i + 1, 'text': s})
        elif re.match(r'^(Abstract|Introduction|Conclusion|References|Acknowledg|Discussion|Results|Methods|Background)\b', s, re.IGNORECASE) and len(s) < 80:
            headers.append({'line': i + 1, 'text': s})
        elif s.isupper() and len(s) < 80 and len(s) > 3:
            headers.append({'line': i + 1, 'text': s})
    return headers


def build_markdown(pdf_path: Path, corpus_id: str) -> tuple:
    """Constrói o Markdown estruturado para um PDF do corpus."""
    meta = extract_metadata_pdf(pdf_path)
    pages = extract_text_by_page(pdf_path)
    tables = extract_tables_pdf(pdf_path)

    md_lines = []
    md_lines.append(f'# {corpus_id} — Extração de Texto Estruturado')
    md_lines.append('')
    md_lines.append(f'**Arquivo de origem:** `{pdf_path.name}`')
    md_lines.append(f'**ID do Corpus:** {corpus_id}')
    md_lines.append(f'**Extração realizada em:** {datetime.now(timezone.utc).isoformat(timespec="seconds")}')
    md_lines.append(f'**Ferramenta:** PyMuPDF {fitz.__doc__.split(":")[1].strip() if fitz.__doc__ else "1.26.7"} + pdfplumber {pdfplumber.__version__}')
    md_lines.append('')
    md_lines.append('## Metadados do PDF')
    md_lines.append('')
    md_lines.append('| Campo | Valor |')
    md_lines.append('|---|---|')
    for k, v in meta.items():
        if not k.startswith('_'):
            md_lines.append(f'| {k} | {v} |')
    md_lines.append(f'| _page_count | {meta["_page_count"]} |')
    md_lines.append(f'| _file_size_bytes | {meta["_file_size_bytes"]} |')
    md_lines.append('')
    md_lines.append('---')
    md_lines.append('')
    md_lines.append('## Conteúdo Textual por Página')
    md_lines.append('')

    all_text = ''
    math_issues_all = []

    for page in pages:
        md_lines.append(f'### Página {page["page_number"]}')
        md_lines.append('')
        text = page['text']
        all_text += text + '\n'
        # Detecta cabeçalhos
        headers = detect_section_headers(text)
        # Detecta possíveis problemas de equação
        math_issues = detect_math_issues(text)
        math_issues_all.extend([(page['page_number'], m) for m in math_issues])

        if headers:
            md_lines.append('<details><summary>Cabeçalhos detectados nesta página</summary>')
            md_lines.append('')
            for h in headers:
                md_lines.append(f'- Linha {h["line"]}: `{h["text"]}`')
            md_lines.append('')
            md_lines.append('</details>')
            md_lines.append('')

        # Texto da página em bloco literal para preservar formatação
        md_lines.append('```text')
        md_lines.append(text.rstrip())
        md_lines.append('```')
        md_lines.append('')

    # Tabelas extraídas
    if tables:
        md_lines.append('---')
        md_lines.append('')
        md_lines.append('## Tabelas Extraídas')
        md_lines.append('')
        for t in tables:
            md_lines.append(f'### Tabela {t["table_index"]} (página {t["page"]})')
            md_lines.append('')
            md_lines.append(render_markdown_table(t['rows']))
            md_lines.append('')

    # Relatório de problemas potenciais
    if math_issues_all:
        md_lines.append('---')
        md_lines.append('')
        md_lines.append('## ⚠️ Possíveis Equações Problemáticas')
        md_lines.append('')
        md_lines.append('> Heurística: linhas curtas com alta densidade de caracteres matemáticos,')
        md_lines.append('> ou linhas com caracteres de substituição Unicode. **Verificar manualmente**.')
        md_lines.append('')
        for page_num, line in math_issues_all:
            md_lines.append(f'- P{page_num}: `{line}`')
        md_lines.append('')

    return '\n'.join(md_lines), {
        'corpus_id': corpus_id,
        'page_count': meta['_page_count'],
        'tables_found': len(tables),
        'math_issues_count': len(math_issues_all),
        'char_count': len(all_text),
    }


def main():
    if len(sys.argv) < 2:
        print('Uso: extract_aion_corpus.py <arquivo.pdf>')
        sys.exit(1)
    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f'ERRO: arquivo não encontrado: {pdf_path}')
        sys.exit(1)

    corpus_id = CORPUS_MAP.get(pdf_path.name)
    if not corpus_id:
        print(f'AVISO: arquivo não está no CORPUS_MAP. Usando nome como ID.')
        corpus_id = pdf_path.stem

    print(f'[AION] Extraindo: {pdf_path.name} -> {corpus_id}')
    md_content, stats = build_markdown(pdf_path, corpus_id)

    output_path = OUTPUT_DIR / f'{corpus_id}_extracted.md'
    output_path.write_text(md_content, encoding='utf-8')

    print(f'[AION] Markdown salvo em: {output_path}')
    print(f'[AION] Estatísticas: {json.dumps(stats, indent=2, ensure_ascii=False)}')
    return stats


if __name__ == '__main__':
    main()
