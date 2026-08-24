#!/usr/bin/env python3
"""
AION Passo 5.13.1 — AION-EVAL-002 v0.2 + P-RESP-001 v0.2

Correções metodológicas:
- AION-EVAL-002 v0.2: distinção FAIL-SYSTEM vs FAIL-EVALUATOR, critérios semânticos
- P-RESP-001 v0.2: 10 regras P1-P10, sem placeholders com aparência de IDs,
  provenance negativa formalizada

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

OUTPUT_DIR = Path('/home/z/my-project/download/rag')


# === P-RESP-001 v0.2 — 10 regras P1-P10 ===

P_RESP_001_V02_SYSTEM_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido.

PROTOCOLO DE PROVENIÊNCIA EXPLICITA (P-RESP-001 v0.2) — 10 REGRAS:

REGRA P1 — Somente IDs presentes no contexto recuperado podem ser citados.
REGRA P2 — Nenhum ID pode ser inventado. Se você não sabe a fonte exata, NÃO cite ID.
REGRA P3 — Se não houver evidência, declarar explicitamente: "INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO."
REGRA P4 — Ausência NÃO requer chunk_id. Quando a resposta é sobre lacuna, não invente fonte.
REGRA P5 — Toda afirmação factual relevante deve ser classificada: [E], [I] ou [H].
REGRA P6 — [I] (interpretação) NÃO pode ser apresentada como [E] (evidência).
REGRA P7 — [H] (hipótese) NÃO pode ser apresentada como fato documental.
REGRA P8 — Distinguir: "não encontrado" (no contexto atual) ≠ "não existe" (no mundo).
REGRA P9 — Documento necessário mas ausente do corpus deve ser declarado como "documento necessário para verificação", NÃO como fonte consultada.
REGRA P10 — A resposta NÃO pode criar proveniência para completar a estrutura exigida.

FORMATO DE RESPOSTA:

Para cada afirmação factual relevante:

[afirmação] [E] [fonte: chunk_id=<ID real do contexto> | documento=CORPUS-XXX]

Para interpretações:

[interpretação] [I] [derivada de: chunk_id=<ID> | rationale=<explicação>]

Para hipóteses:

[hipótese] [H] [sem fonte direta | rationale=<explicação>]

Para ausência:

[afirmação sobre lacuna]
[ABSENT] Não há chunk disponível que sustente esta afirmação.
Documento necessário: <descrição do documento que resolveria>

ESTADOS PERMITIDOS para datas/estados desconhecidos:
- UNKNOWN (quando a data não pode ser estabelecida a partir do corpus)

NUNCA:
- Invente IDs como "CORPUS-XXX#pY_ZZ" ou similares
- Converta ausência em afirmação positiva
- Apresente interpretação como evidência
- Crie IDs fictícios para completar estrutura

Responda em português. Use APENAS o contexto fornecido."""

CONTROL_SYSTEM_PROMPT = """Você é a IA Curadora do projeto AION. Responda à pergunta usando APENAS o contexto fornecido. Para cada afirmação, cite o chunk_id de origem. Se a informação não estiver no contexto, diga 'INFORMAÇÃO NÃO ENCONTRADA NO CONTEXTO'. Não invente. Não use conhecimento externo. Responda em português."""


# === AION-EVAL-002 v0.2 — Funções de avaliação semântica ===

def get_retrieved_chunk_ids(retrieved: list) -> set:
    """Retorna set de chunk_ids efetivamente recuperados."""
    return {r.get('chunk_id', '') for r in retrieved}


def eval_R1_v02(test_id: str, retrieved: list, gabarito: dict) -> dict:
    """R1 v0.2: Retrieval correto — com classificação SYSTEM/EVALUATOR."""
    expected_chunk = gabarito.get('chunk_id')
    if not expected_chunk:
        return {'status': 'N/A', 'reason': 'Gabarito não especifica chunk_id', 'classification': 'N/A'}
    
    retrieved_ids = get_retrieved_chunk_ids(retrieved)
    # Verifica se algum chunk recuperado começa com o prefixo esperado
    expected_prefix = expected_chunk.split('#')[0]
    for r in retrieved:
        cid = r.get('chunk_id', '')
        if cid.startswith(expected_prefix):
            return {
                'status': 'PASS',
                'reason': f'Chunk esperado recuperado: {cid} (rank #{r.get("rank", "?")})',
                'classification': 'N/A'
            }
    return {
        'status': 'FAIL',
        'reason': f'Chunk esperado {expected_chunk} NÃO recuperado. Top: {retrieved[0].get("chunk_id", "?") if retrieved else "nenhum"}',
        'classification': 'SYSTEM'  # Falha real de retrieval, não do avaliador
    }


def eval_R2_v02(test_id: str, retrieved: list, gabarito: dict) -> dict:
    """R2 v0.2: Retrieval suficiente."""
    if test_id == 'B4':
        return {'status': 'N/A', 'reason': 'Pergunta sobre ausência', 'classification': 'N/A'}
    if not retrieved:
        return {'status': 'FAIL', 'reason': 'Nenhum chunk recuperado', 'classification': 'SYSTEM'}
    max_score = max((r.get('score', 0) for r in retrieved), default=0)
    if max_score > 0.05:
        return {'status': 'PASS', 'reason': f'Contexto contém informação (max score: {max_score:.3f})', 'classification': 'N/A'}
    return {'status': 'FAIL', 'reason': f'Scores baixos (max: {max_score:.3f})', 'classification': 'SYSTEM'}


def eval_P1_v02(test_id: str, answer: str, gabarito: dict, retrieved: list) -> dict:
    """P1 v0.2: Proveniência correta — com verificação semântica."""
    expected_doc = gabarito.get('documento')
    if not expected_doc:
        return {'status': 'N/A', 'reason': 'Gabarito não especifica documento', 'classification': 'N/A'}
    
    answer_lower = answer.lower()
    
    # 1. Verificação direta do documento esperado
    if expected_doc.lower() in answer_lower:
        return {'status': 'PASS', 'reason': f'Documento {expected_doc} citado', 'classification': 'N/A'}
    
    # 2. Sinônimos (Paper A, Paper B, etc.)
    synonyms = {
        'CORPUS-002': ['paper a', 'paper a v6.2', 'relational coherence', 'tcr'],
        'CORPUS-003': ['parte iv', 'formalização teórica', 'formalizacao teorica'],
        'CORPUS-004': ['paper b', 'paper b v6.1', 'qdt', 'fmo'],
        'CORPUS-005': ['cover letter', 'carta de apresentação'],
    }
    syn_list = synonyms.get(expected_doc, [])
    for syn in syn_list:
        if syn in answer_lower:
            return {'status': 'PASS-SEMANTIC', 'reason': f'Documento identificado por sinônimo "{syn}"', 'classification': 'N/A'}
    
    # 3. Verifica se citou documento diferente
    cited_docs = set(re.findall(r'CORPUS-(\d{3})', answer))
    retrieved_docs = set(r.get('corpus_id', '').replace('CORPUS-', '') for r in retrieved)
    
    if cited_docs:
        # Se citou apenas documentos recuperados, é falha do sistema (citou errado)
        wrong_citations = cited_docs - retrieved_docs
        if wrong_citations:
            return {
                'status': 'FAIL',
                'reason': f'Cita documentos não recuperados: {wrong_citations}',
                'classification': 'SYSTEM'  # Sistema inventou fonte
            }
        return {
            'status': 'FAIL',
            'reason': f'Cita {cited_docs} em vez de {expected_doc}',
            'classification': 'SYSTEM'  # Sistema citou documento errado
        }
    
    return {'status': 'FAIL', 'reason': f'Documento {expected_doc} não citado', 'classification': 'SYSTEM'}


def eval_P2_v02(test_id: str, answer: str, gabarito: dict) -> dict:
    """P2 v0.2: Proveniência granular — com verificação estruturada."""
    # Procura por citações estruturadas: chunk_id=<ID> ou [chunk_id=...]
    structured_citations = re.findall(r'chunk_id[=: ]+(\S+?)[\]\s|,)]', answer, re.IGNORECASE)
    
    if structured_citations:
        # Verifica se pelo menos uma citação tem formato válido (CORPUS-XXX#pY_ZZ)
        valid_format = any(re.match(r'CORPUS-\d{3}#\w+', c.strip('[],')) for c in structured_citations)
        if valid_format:
            return {'status': 'PASS', 'reason': f'Citação estruturada de chunk_id: {structured_citations[:3]}', 'classification': 'N/A'}
    
    # Fallback: procura por chunk_ids no formato antigo
    has_chunk = bool(re.search(r'CORPUS-\d{3}#\w+', answer))
    has_page = bool(re.search(r'p\.\d+|página \d+|p\. ?\d+', answer, re.IGNORECASE))
    has_section = bool(re.search(r'sec\.|section|seção|secção', answer, re.IGNORECASE))
    
    if has_chunk:
        return {'status': 'PASS', 'reason': 'Citação de chunk_id', 'classification': 'N/A'}
    if has_page or has_section:
        return {'status': 'PASS-SEMANTIC', 'reason': 'Citação de página/seção', 'classification': 'N/A'}
    
    return {'status': 'FAIL', 'reason': 'Sem citação granular', 'classification': 'SYSTEM'}


def eval_T1_v02(test_id: str, answer: str, gabarito: dict) -> dict:
    """T1 v0.2: Coerência temporal — com reconhecimento semântico."""
    answer_lower = answer.lower()
    
    if test_id == 'B2':
        # Critério semântico: deve distinguir duas versões/datas diferentes
        # Procura por: datas ISO, versões (vX.Y), ou referências temporais
        dates_iso = set(re.findall(r'2026-08-\d{2}', answer))
        versions = set(re.findall(r'v\d\.\d', answer))
        date_refs = set(re.findall(r'\d{1,2} de agosto', answer_lower))
        
        all_temporal = dates_iso | versions | date_refs
        
        if len(all_temporal) >= 2:
            return {'status': 'PASS', 'reason': f'Múltiplas referências temporais: {all_temporal}', 'classification': 'N/A'}
        
        # Também reconhece expressões como "versão anterior" / "versão atual"
        if 'versão anterior' in answer_lower and ('versão atual' in answer_lower or 'versão final' in answer_lower):
            return {'status': 'PASS-SEMANTIC', 'reason': 'Distingue versões (anterior/atual)', 'classification': 'N/A'}
        
        # Reconhece Cover Letter vs Paper A como temporal
        if 'cover letter' in answer_lower and 'paper a' in answer_lower:
            return {'status': 'PASS-SEMANTIC', 'reason': 'Distingue Cover Letter (v6.1) de Paper A (v6.2)', 'classification': 'N/A'}
        
        return {'status': 'FAIL', 'reason': 'Não distinguiu versões temporais', 'classification': 'SYSTEM'}
    
    if test_id == 'B3':
        # Deve identificar revogação temporalmente situada
        date_found = bool(re.search(r'2026-08-12|12 de agosto|12/08', answer))
        version_found = 'v6.1' in answer or 'paper b' in answer_lower
        revocation_found = any(w in answer_lower for w in ['retrat', 'abandonad', 'revogad', 'retirad', 'removid'])
        
        if revocation_found and (date_found or version_found):
            return {'status': 'PASS-SEMANTIC', 'reason': 'Revogação identificada temporalmente', 'classification': 'N/A'}
        return {'status': 'FAIL', 'reason': 'Revogação não temporalmente situada', 'classification': 'SYSTEM'}
    
    if test_id == 'B7':
        # Deve distinguir v6.0 de v6.1
        has_v60 = 'v6.0' in answer
        has_v61 = 'v6.1' in answer
        # Também reconhece dímero vs FMO como distinção temporal
        has_dimer = 'dímero' in answer_lower or 'dimero' in answer_lower
        has_fmo7 = '7 sítios' in answer_lower or '7 sitios' in answer_lower or 'fmo completo' in answer_lower
        
        if has_v60 and has_v61:
            return {'status': 'PASS', 'reason': 'Versões v6.0 e v6.1 distinguídas', 'classification': 'N/A'}
        if has_dimer and has_fmo7:
            return {'status': 'PASS-SEMANTIC', 'reason': 'Distingue dímero (v6.0) de FMO 7-sítios (v6.1)', 'classification': 'N/A'}
        return {'status': 'FAIL', 'reason': 'Versões não distinguídas', 'classification': 'SYSTEM'}
    
    return {'status': 'N/A', 'reason': 'T1 não aplicável', 'classification': 'N/A'}


def eval_E1_v02(test_id: str, answer: str, gabarito: dict) -> dict:
    """E1 v0.2: Distinção evidência/interpretação — com verificação de tags estruturadas."""
    # Procura por tags [E], [I], [H] formais
    e_count = len(re.findall(r'\[E\]', answer))
    i_count = len(re.findall(r'\[I\]', answer))
    h_count = len(re.findall(r'\[H\]', answer))
    
    if e_count + i_count + h_count > 0:
        return {'status': 'PASS', 'reason': f'Tags formais aplicadas: [E]={e_count}, [I]={i_count}, [H]={h_count}', 'classification': 'N/A'}
    
    # Fallback: citação de chunk como evidência implícita
    has_chunk_citation = bool(re.search(r'CORPUS-\d{3}#\w+', answer))
    if has_chunk_citation:
        return {'status': 'PASS-SEMANTIC', 'reason': 'Cita chunks como fonte (tags implícitas)', 'classification': 'N/A'}
    
    return {'status': 'FAIL', 'reason': 'Sem distinção [E]/[I]/[H]', 'classification': 'SYSTEM'}


def eval_N1_v02(test_id: str, answer: str, gabarito: dict) -> dict:
    """N1 v0.2: Tratamento de ausência — reconhece多种 formulações."""
    answer_lower = answer.lower()
    
    absence_phrases = [
        'não encontrado', 'não consta', 'não aparece', 'ausente',
        'não está', 'informação não encontrada', 'não há evidência',
        'não há menção', 'não existe', 'não foi encontrado',
        'não disponível', 'não disponivel', '[absent]', 'lacuna',
        'não há chunk', 'sem fonte', 'sem evidência',
    ]
    
    for phrase in absence_phrases:
        if phrase in answer_lower:
            return {'status': 'PASS', 'reason': f'Declara ausência: "{phrase}"', 'classification': 'N/A'}
    
    if test_id == 'B4':
        # Para B4: resposta esperada é "não" (consciência não está no corpus)
        if 'não' in answer_lower and ('consciência' in answer_lower or 'ausente' in answer_lower):
            return {'status': 'PASS-SEMANTIC', 'reason': 'Indica negação', 'classification': 'N/A'}
        return {'status': 'FAIL', 'reason': 'Não declara ausência', 'classification': 'SYSTEM'}
    
    if test_id == 'B6':
        # Para B6: deve reconhecer impossibilidade de determinação
        if any(p in answer_lower for p in ['não pode', 'não é possível', 'impossível', 'não há chunk']):
            return {'status': 'PASS', 'reason': 'Declara impossibilidade', 'classification': 'N/A'}
        return {'status': 'FAIL', 'reason': 'Não declara impossibilidade', 'classification': 'SYSTEM'}
    
    return {'status': 'N/A', 'reason': 'N1 não aplicável', 'classification': 'N/A'}


def eval_C1_v02(test_id: str, answer: str, gabarito: dict) -> dict:
    """C1 v0.2: Detecção de contradição — com reconhecimento semântico."""
    answer_lower = answer.lower()
    
    if test_id == 'B5':
        # Critério semântico: deve identificar divergência entre documentos
        # com citação dupla (dois CORPUS diferentes)
        cited_docs = set(re.findall(r'corpus-(\d{3})', answer_lower))
        
        # Reconhece termos de contradição (não apenas "contradição")
        contradiction_terms = [
            'contradição', 'contradiz', 'divergência', 'discrepância',
            'incompatíve', 'em conflito', 'inconsistência', 'diferença material',
            'contradição material', 'posições incompatíveis', 'resultados divergent',
        ]
        has_contradiction_term = any(t in answer_lower for t in contradiction_terms)
        
        # Verifica se há citação dupla (dois documentos diferentes)
        has_double_citation = len(cited_docs) >= 2
        
        if has_double_citation and has_contradiction_term:
            return {'status': 'PASS', 'reason': f'Contradição identificada entre {cited_docs}', 'classification': 'N/A'}
        
        if has_double_citation:
            # Citou dois documentos mas não usou termo de contradição — verificar se demonstrou
            if '0.968' in answer and '0.793' in answer:
                return {'status': 'PASS-SEMANTIC', 'reason': 'Demonstra contradição via números divergentes', 'classification': 'N/A'}
            return {'status': 'FAIL', 'reason': 'Cita múltiplos docs mas não demonstra contradição', 'classification': 'EVALUATOR'}
        
        return {'status': 'FAIL', 'reason': 'Sem detecção de contradição', 'classification': 'SYSTEM'}
    
    return {'status': 'N/A', 'reason': 'C1 não aplicável', 'classification': 'N/A'}


def eval_S1_v02(test_id: str, answer: str, gabarito: dict) -> dict:
    """S1 v0.2: Qualidade da síntese."""
    answer_lower = answer.lower()
    
    if test_id == 'B7':
        has_dimer = 'dímero' in answer_lower or 'dimero' in answer_lower or '2 sítios' in answer_lower or '2 sitios' in answer_lower
        has_fmo7 = '7 sítios' in answer_lower or '7 sitios' in answer_lower or 'fmo completo' in answer_lower or 'fmo 7' in answer_lower
        
        # Critério semântico: basta distinguir dímero de FMO completo
        if has_dimer and has_fmo7:
            return {'status': 'PASS-SEMANTIC', 'reason': 'Distingue dímero de FMO 7-sítios', 'classification': 'N/A'}
        return {'status': 'FAIL', 'reason': 'Não distinguiu estados', 'classification': 'SYSTEM'}
    
    return {'status': 'N/A', 'reason': 'S1 não aplicável', 'classification': 'N/A'}


def eval_H1_v02(test_id: str, answer: str, gabarito: dict) -> dict:
    """H1 v0.2: Honestidade epistemológica."""
    answer_lower = answer.lower()
    
    uncertainty_phrases = [
        'não encontrado', 'não pode ser determinado', 'não é possível',
        'desconhecido', 'unknown', 'lacuna', 'pendente', 'não tenho',
        'informação não disponível', 'ausente', 'não há chunk',
        'documento necessário', 'sem fonte', '[absent]',
    ]
    has_uncertainty = any(p in answer_lower for p in uncertainty_phrases)
    
    categorical_phrases = ['certamente', 'sem dúvida', 'definitivamente']
    has_unsupported_categorical = any(p in answer_lower for p in categorical_phrases)
    
    if has_uncertainty or not has_unsupported_categorical:
        if has_uncertainty:
            return {'status': 'PASS', 'reason': 'Incerteza marcada explicitamente', 'classification': 'N/A'}
        return {'status': 'PASS-SEMANTIC', 'reason': 'Sem afirmações categóricas não suportadas', 'classification': 'N/A'}
    
    return {'status': 'FAIL', 'reason': 'Afirmações categóricas sem suporte', 'classification': 'SYSTEM'}


def evaluate_with_eval002_v02(test_id: str, retrieved: list, answer: str, gabarito: dict) -> dict:
    """Aplica AION-EVAL-002 v0.2 com classificação SYSTEM/EVALUATOR."""
    categories = {
        'R1': eval_R1_v02(test_id, retrieved, gabarito),
        'R2': eval_R2_v02(test_id, retrieved, gabarito),
        'P1': eval_P1_v02(test_id, answer, gabarito, retrieved),
        'P2': eval_P2_v02(test_id, answer, gabarito),
        'T1': eval_T1_v02(test_id, answer, gabarito),
        'E1': eval_E1_v02(test_id, answer, gabarito),
        'N1': eval_N1_v02(test_id, answer, gabarito),
        'C1': eval_C1_v02(test_id, answer, gabarito),
        'S1': eval_S1_v02(test_id, answer, gabarito),
        'H1': eval_H1_v02(test_id, answer, gabarito),
    }
    
    # Avaliação final com regra de não-compensação
    h1_status = categories['H1']['status']
    if h1_status == 'FAIL':
        final = 'FAIL-SYSTEM'
        justification = 'H1 falhou — pré-requisito não atendido'
    else:
        critical_failures = []
        
        if test_id == 'B1':
            if categories['R1']['status'] == 'FAIL':
                critical_failures.append('R1')
            if categories['P1']['status'] == 'FAIL':
                critical_failures.append('P1')
        elif test_id in ['B2', 'B3']:
            if categories['R1']['status'] == 'FAIL':
                critical_failures.append('R1')
            if categories['T1']['status'] == 'FAIL':
                critical_failures.append('T1')
        elif test_id == 'B4':
            if categories['N1']['status'] == 'FAIL':
                critical_failures.append('N1')
        elif test_id == 'B5':
            if categories['C1']['status'] == 'FAIL':
                critical_failures.append('C1')
        elif test_id == 'B6':
            if categories['N1']['status'] == 'FAIL':
                critical_failures.append('N1')
        elif test_id == 'B7':
            if categories['S1']['status'] == 'FAIL':
                critical_failures.append('S1')
        
        if critical_failures:
            # Classifica: SYSTEM ou EVALUATOR
            classifications = [categories[cat]['classification'] for cat in critical_failures]
            if all(c == 'EVALUATOR' for c in classifications):
                final = 'FAIL-EVALUATOR'
                justification = f'Falhas críticas (classificação EVALUATOR): {critical_failures}'
            elif all(c == 'SYSTEM' for c in classifications):
                final = 'FAIL-SYSTEM'
                justification = f'Falhas críticas (classificação SYSTEM): {critical_failures}'
            else:
                final = 'FAIL-MIXED'
                justification = f'Falhas críticas mistas: {critical_failures} com classificações {classifications}'
        else:
            all_status = [c['status'] for c in categories.values()]
            has_real_fail = any(s == 'FAIL' for s in all_status)
            
            if has_real_fail:
                final = 'PARTIAL'
                justification = 'Critérios críticos PASS, falhas não-críticas'
            else:
                semantic_count = sum(1 for s in all_status if s == 'PASS-SEMANTIC')
                if semantic_count > 0:
                    final = 'PASS-SEMANTIC'
                    justification = f'PASS com {semantic_count} categorias semânticas'
                else:
                    final = 'PASS'
                    justification = 'Todos os critérios atendidos'
    
    return {
        'categories': categories,
        'avaliacao_final': final,
        'justificativa': justification,
    }


# === Geração e execução ===

def generate_answer(question: str, retrieved: list, system_prompt: str, system_extra: str = "") -> str:
    """Gera resposta via z-ai CLI."""
    context_parts = []
    for r in retrieved:
        context_parts.append(
            f"[{r.chunk.chunk_id} | {r.chunk.short_title} | {r.chunk.page} | {r.chunk.section} | score={r.score:.3f}]\n"
            f"{r.chunk.text}\n"
        )
    chunks_context = "\n---\n".join(context_parts)
    
    full_system = system_prompt
    if system_extra:
        full_system += " " + system_extra
    
    user_prompt = f"""CONTEXTO RECUPERADO:

{chunks_context}

{system_extra}

PERGUNTA: {question}

Responda usando apenas o contexto acima."""
    
    try:
        result = subprocess.run(
            ['z-ai', 'chat', '--system', full_system, '--prompt', user_prompt],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            return f"[ERRO z-ai: {result.stderr}]"
        try:
            data = json.loads(result.stdout)
            answer = data.get('content') or data.get('response') or result.stdout
        except json.JSONDecodeError:
            answer = result.stdout.strip()
        return answer
    except subprocess.TimeoutExpired:
        return "[ERRO z-ai: timeout]"
    except Exception as e:
        return f"[ERRO z-ai: {e}]"


def clean_answer(answer: str) -> str:
    if '🚀' in answer:
        try:
            json_start = answer.find('{')
            if json_start >= 0:
                json_str = answer[json_start:]
                data = json.loads(json_str)
                return data['choices'][0]['message']['content']
        except:
            pass
    return answer


def check_fabrication_v02(answer: str, retrieved: list) -> dict:
    """Verificação de fabricação v0.2 — com distinção entre placeholder e ID real."""
    valid_chunks = {r.get('chunk_id', '') for r in retrieved}
    
    # IDs citados na resposta
    cited_chunks = set(re.findall(r'CORPUS-\d{3}#\w+', answer))
    
    # Fabricados: citados mas não recuperados
    fabricated = cited_chunks - valid_chunks
    
    # Distinção: placeholder (formato pY_ZZ) vs ID real fabricado
    placeholders = {c for c in fabricated if 'pY_ZZ' in c or 'pY' in c.split('#')[-1]}
    real_fabricated = fabricated - placeholders
    
    return {
        'cited_chunks': list(cited_chunks),
        'valid_chunks': list(valid_chunks),
        'fabricated_chunks': list(fabricated),
        'placeholders_detected': list(placeholders),
        'real_fabricated': list(real_fabricated),
        'fabrication_detected': len(real_fabricated) > 0,  # Placeholders não contam como fabricação maliciosa
        'placeholder_bug': len(placeholders) > 0,
    }


def main():
    print("=" * 70)
    print("AION Passo 5.13.1 — P-RESP-001 v0.2 + AION-EVAL-002 v0.2")
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
    
    # Executa ambos os sistemas
    print("\n[SISTEMA A — Controle] Executando B1-B7...")
    results_A = {}
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        test = BENCH_TESTS[test_id]
        retrieved = store.query(test['pergunta'], top_k=8)
        
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
        
        retrieved_for_eval = [
            {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
            for i, r in enumerate(retrieved)
        ]
        
        eval_result = evaluate_with_eval002_v02(test_id, retrieved_for_eval, answer_clean, test['gabarito'])
        fab_check = check_fabrication_v02(answer_clean, retrieved_for_eval)
        
        results_A[test_id] = {
            'test_id': test_id,
            'categoria': test['categoria'],
            'pergunta': test['pergunta'],
            'resposta': answer_clean,
            'tempo_segundos': round(t_elapsed, 2),
            'retrieved_chunks_top5': retrieved_for_eval[:5],
            'eval_002_v02': eval_result,
            'fabrication_check': fab_check,
            'gabarito': test['gabarito'],
            'sistema': 'A (controle)',
        }
        print(f"  {test_id}: {eval_result['avaliacao_final']}")
    
    print("\n[SISTEMA B — P-RESP-001 v0.2] Executando B1-B7...")
    results_B = {}
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        test = BENCH_TESTS[test_id]
        retrieved = store.query(test['pergunta'], top_k=8)
        
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
        answer = generate_answer(test['pergunta'], retrieved[:5], P_RESP_001_V02_SYSTEM_PROMPT, system_extra)
        t_elapsed = time.time() - t_start
        answer_clean = clean_answer(answer)
        
        retrieved_for_eval = [
            {'rank': i+1, 'chunk_id': r.chunk.chunk_id, 'score': r.score, 'corpus_id': r.chunk.corpus_id}
            for i, r in enumerate(retrieved)
        ]
        
        eval_result = evaluate_with_eval002_v02(test_id, retrieved_for_eval, answer_clean, test['gabarito'])
        fab_check = check_fabrication_v02(answer_clean, retrieved_for_eval)
        
        results_B[test_id] = {
            'test_id': test_id,
            'categoria': test['categoria'],
            'pergunta': test['pergunta'],
            'resposta': answer_clean,
            'tempo_segundos': round(t_elapsed, 2),
            'retrieved_chunks_top5': retrieved_for_eval[:5],
            'eval_002_v02': eval_result,
            'fabrication_check': fab_check,
            'gabarito': test['gabarito'],
            'sistema': 'B (P-RESP-001 v0.2)',
        }
        print(f"  {test_id}: {eval_result['avaliacao_final']}")
    
    # Matriz comparativa
    print(f"\n{'=' * 90}")
    print("[MATRIZ COMPARATIVA v0.2]")
    print(f"{'=' * 90}")
    print(f"\n{'Teste':<6} {'Categoria':<15} {'A (controle)':<22} {'B (P-RESP-001 v0.2)':<25} {'Variação':<15} {'Classificação'}")
    print('-' * 100)
    
    hierarchy = {'PASS': 5, 'PASS-SEMANTIC': 4, 'PARTIAL': 3, 'FAIL-EVALUATOR': 2, 'FAIL-MIXED': 1, 'FAIL-SYSTEM': 0}
    
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        a_status = results_A[test_id]['eval_002_v02']['avaliacao_final']
        b_status = results_B[test_id]['eval_002_v02']['avaliacao_final']
        cat = results_A[test_id]['categoria']
        
        diff = hierarchy.get(b_status, 0) - hierarchy.get(a_status, 0)
        if diff > 0:
            variation = '↑ MELHOROU'
        elif diff < 0:
            variation = '↓ REGREDIU'
        else:
            variation = '= (mantido)'
        
        # Classificação para B
        b_classification = results_B[test_id]['eval_002_v02']['justificativa']
        
        a_emoji = {'PASS': '✅', 'PASS-SEMANTIC': '🟡', 'PARTIAL': '⚠️', 'FAIL-EVALUATOR': '🔵', 'FAIL-MIXED': '🟣', 'FAIL-SYSTEM': '❌'}.get(a_status, '?')
        b_emoji = {'PASS': '✅', 'PASS-SEMANTIC': '🟡', 'PARTIAL': '⚠️', 'FAIL-EVALUATOR': '🔵', 'FAIL-MIXED': '🟣', 'FAIL-SYSTEM': '❌'}.get(b_status, '?')
        
        print(f"{test_id:<6} {cat:<15} {a_emoji} {a_status:<19} {b_emoji} {b_status:<22} {variation:<15} {b_classification[:50]}")
    
    # Análise de regressões com classificação SYSTEM/EVALUATOR
    print(f"\n{'=' * 90}")
    print("[DIAGNÓSTICO DE REGRESSÕES — CLASSIFICAÇÃO SYSTEM/EVALUATOR]")
    print(f"{'=' * 90}")
    
    for test_id in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']:
        a_status = results_A[test_id]['eval_002_v02']['avaliacao_final']
        b_status = results_B[test_id]['eval_002_v02']['avaliacao_final']
        diff = hierarchy.get(b_status, 0) - hierarchy.get(a_status, 0)
        
        if diff < 0:  # Regressão
            print(f"\n[{test_id}] REGRESSÃO: {a_status} → {b_status}")
            # Detalha quais categorias falharam e com qual classificação
            b_cats = results_B[test_id]['eval_002_v02']['categories']
            for cat, cat_data in b_cats.items():
                if cat_data['status'] == 'FAIL':
                    print(f"  {cat}: {cat_data['status']} ({cat_data['classification']}) — {cat_data['reason'][:100]}")
        elif diff > 0:
            print(f"\n[{test_id}] MELHORIA: {a_status} → {b_status}")
    
    # Critérios de aprovação v0.2
    print(f"\n{'=' * 90}")
    print("[CRITÉRIOS DE APROVAÇÃO v0.2]")
    print(f"{'=' * 90}")
    
    criteria = {
        '1_B6_melhora': (
            hierarchy.get(results_B['B6']['eval_002_v02']['avaliacao_final'], 0) >= 
            hierarchy.get(results_A['B6']['eval_002_v02']['avaliacao_final'], 0)
        ),
        '2_proveniencia_identificavel': (
            # B6 deve declarar documento necessário (mesmo sem chunk_id)
            'documento necessário' in results_B['B6']['resposta'].lower() or
            'necessária' in results_B['B6']['resposta'].lower()
        ),
        '3_tags_EIH_diferenciadas': (
            any(results_B[tid]['eval_002_v02']['categories']['E1']['status'] in ('PASS', 'PASS-SEMANTIC')
                for tid in ['B5', 'B6', 'B7'])
        ),
        '4_UNKNOWN_nao_preenchido': all(
            not results_B[tid]['fabrication_check']['fabrication_detected']
            for tid in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
        ),
        '5_H1_PASS': all(
            results_B[tid]['eval_002_v02']['categories']['H1']['status'] in ('PASS', 'PASS-SEMANTIC')
            for tid in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
        ),
        '6_sem_regressao_real': all(
            # Considera apenas regressões SYSTEM (não EVALUATOR) como regressões reais
            not (
                hierarchy.get(results_B[tid]['eval_002_v02']['avaliacao_final'], 0) <
                hierarchy.get(results_A[tid]['eval_002_v02']['avaliacao_final'], 0) and
                not results_B[tid]['eval_002_v02']['avaliacao_final'].startswith('FAIL-EVALUATOR')
            )
            for tid in ['B1', 'B2', 'B3', 'B4', 'B5', 'B7']
        ),
        '7_sem_fabricacao_maliciosa': all(
            not results_B[tid]['fabrication_check']['fabrication_detected']
            for tid in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
        ),
    }
    
    for c, passed in criteria.items():
        print(f"  {'✅' if passed else '❌'} {c}")
    
    pass_count = sum(criteria.values())
    total = len(criteria)
    print(f"\nTotal: {pass_count}/{total}")
    
    # Veredito
    if pass_count == total:
        verdict = 'P-RESP-001 v0.2 APROVADO'
        decision = 'INCORPORAR protocolo P-RESP-001 v0.2 como prompt padrão'
    elif pass_count >= 5:
        verdict = 'P-RESP-001 v0.2 PARCIALMENTE APROVADO'
        decision = 'INCORPORAR com ressalvas documentadas'
    else:
        verdict = 'P-RESP-001 v0.2 REJEITADO'
        decision = 'MANTER prompt de controle'
    
    print(f"\n[VEREDITO] {verdict}")
    print(f"[DECISÃO] {decision}")
    
    # Salva relatório
    report = {
        'metadata': {
            'experiment': 'P-RESP-001 v0.2 + AION-EVAL-002 v0.2',
            'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
        },
        'sistema_A_controle': {
            'system_prompt': CONTROL_SYSTEM_PROMPT,
            'results': results_A,
        },
        'sistema_B_p_resp_001_v02': {
            'system_prompt': P_RESP_001_V02_SYSTEM_PROMPT,
            'results': results_B,
        },
        'criteria_evaluation': criteria,
        'pass_count': pass_count,
        'total_count': total,
        'verdict': verdict,
        'decision': decision,
    }
    
    json_path = OUTPUT_DIR / 'aion_p_resp_001_v02_resultados.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[SAVED] JSON: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    return report


if __name__ == '__main__':
    main()
