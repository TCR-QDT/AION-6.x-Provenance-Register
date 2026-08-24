#!/usr/bin/env python3
"""
AION Passo 5.8 — Reconciliação Histórica (AION-HIST-001)

Implementa bateria de 6 testes de reconstrução da evolução intelectual,
com estrutura de Memória Negativa explícita.

Autor da estrutura: Edson C. Nascimento (Projetista Master)
Implementação técnica: IA Curadora
Data: 17 de agosto de 2026
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

OUTPUT_DIR = Path('/home/z/my-project/download/rag')

# Carrega grafo temporal já construído
temporal_path = OUTPUT_DIR / 'aion_temporal_graph_v1.0.json'
TEMPORAL = json.loads(temporal_path.read_text(encoding='utf-8'))


# === Estrutura de Memória Negativa ===

NEGATIVE_MEMORY_TYPES = {
    'DESCONHECIDO': 'Informação que o sistema não possui e não pode determinar a partir do corpus atual.',
    'AUSENTE': 'Termo ou conceito não aparece textualmente em nenhum documento do corpus.',
    'CONTRADITO': 'Conceito introduzido mas posteriormente contradito por auditoria documental.',
    'REVOGADO': 'Afirmação ou conceito explicitamente abandonado pelo autor em versão posterior.',
    'INDETERMINADO': 'Estado cuja data não pode ser estabelecida a partir do corpus atual.',
}


def build_negative_memory(states: list) -> dict:
    """Constrói registro de Memória Negativa a partir dos estados temporais."""
    negative = {
        'DESCONHECIDO': [],
        'AUSENTE': [],
        'CONTRADITO': [],
        'REVOGADO': [],
        'INDETERMINADO': [],
    }
    
    for s in states:
        # INDETERMINADO: estados UNKNOWN
        if s['valid_at'] == 'UNKNOWN' or s['document_date'] == 'UNKNOWN':
            negative['INDETERMINADO'].append({
                'concept_id': s['concept_id'],
                'concept_label': s['concept_label'],
                'state': s['state'],
                'reason': f"Data não estabelecida (valid_at={s['valid_at']}, document_date={s['document_date']})",
                'document': s['document'],
            })
        
        # CONTRADICTED: conceitos cuja presença foi posteriormente negada
        if s['change_type'] == 'CONTRADICTED':
            negative['CONTRADITO'].append({
                'concept_id': s['concept_id'],
                'concept_label': s['concept_label'],
                'state': s['state'],
                'previous_state': s['previous_state'],
                'reason': f"Auditoria contradisse presença do conceito no programa.",
                'evidence': s['evidence_text'],
                'document': s['document'],
            })
        
        # REVOKED: retrações formais
        if s['change_type'] == 'REVOKED':
            negative['REVOGADO'].append({
                'concept_id': s['concept_id'],
                'concept_label': s['concept_label'],
                'state': s['state'],
                'previous_state': s['previous_state'],
                'reason': f"Autor retrata formalmente em {s['version']}.",
                'evidence': s['evidence_text'],
                'document': s['document'],
                'date': s['valid_at'],
            })
    
    # AUSENTE: termos procurados mas não encontrados no corpus
    # (caso paradigmático: "consciência" e "campo primordial" — embora INTRODUCED no Handoff,
    #  a auditoria T4 mostrou que não estão nos textos)
    absent_terms = [
        {
            'term': 'consciência',
            'searched_in': ['CORPUS-001', 'CORPUS-002', 'CORPUS-003', 'CORPUS-004', 'CORPUS-005'],
            'found': False,
            'note': 'Termo aparece apenas em inferência do Handoff original; auditoria T4 confirmou ausência textual.',
            'only_reference': 'Paper A cita Tononi (Φ-IIT) como referência externa, não como conceito do programa.',
        },
        {
            'term': 'campo primordial',
            'searched_in': ['CORPUS-001', 'CORPUS-002', 'CORPUS-003', 'CORPUS-004', 'CORPUS-005'],
            'found': False,
            'note': 'Atribuído ao CORPUS-003 no Handoff original; auditoria confirmou ausência no texto extraído.',
        },
        {
            'term': 'Paper C (versão final submetida à Foundations of Physics)',
            'searched_in': ['CORPUS-001', 'CORPUS-002', 'CORPUS-003', 'CORPUS-004', 'CORPUS-005'],
            'found': False,
            'note': 'Cover Letter PT-BR afirma submissão; CORPUS-003 (Parte IV) é rascunho PT-BR, não a versão final submetida.',
            'only_reference': 'Cover Letter afirma: "Paper C submetido à Foundations of Physics em 10 de agosto de 2026"',
        },
        {
            'term': 'Cover Letter oficial em inglês (Cover_Letter_Paper_A_PRE.md)',
            'searched_in': ['CORPUS-001', 'CORPUS-002', 'CORPUS-003', 'CORPUS-004', 'CORPUS-005'],
            'found': False,
            'note': 'T6 — lacuna documental. A versão PT-BR no corpus é rascunho v6.1 aspiracional.',
        },
        {
            'term': 'Partes I-III do Programa de Formalização Físico-Matemática',
            'searched_in': ['CORPUS-001', 'CORPUS-002', 'CORPUS-003', 'CORPUS-004', 'CORPUS-005'],
            'found': False,
            'note': 'T9 — lacuna estrutural. CORPUS-003 é "Parte IV, Passos 16-18" apenas.',
        },
        {
            'term': 'Versão v5.1 do Paper A (submetida ao Brazilian Journal of Physics)',
            'searched_in': ['CORPUS-001', 'CORPUS-002', 'CORPUS-003', 'CORPUS-004', 'CORPUS-005'],
            'found': False,
            'note': 'Existência inferida do Acknowledgments do Paper A v6.2; documento não está no corpus.',
        },
        {
            'term': 'Versão v6.0 do Paper A (com termo de recursão R^α)',
            'searched_in': ['CORPUS-001', 'CORPUS-002', 'CORPUS-003', 'CORPUS-004', 'CORPUS-005'],
            'found': False,
            'note': 'Existência declarada no Paper A v6.2: "Earlier versions of TCR included a recursion term R with exponent α = 1.3"; documento não está no corpus.',
        },
        {
            'term': 'Versão v6.0 do Paper B (com hipótese η e dímero 2 sítios)',
            'searched_in': ['CORPUS-001', 'CORPUS-002', 'CORPUS-003', 'CORPUS-004', 'CORPUS-005'],
            'found': False,
            'note': 'Existência declarada no Paper B v6.1; documento não está no corpus.',
        },
    ]
    negative['AUSENTE'] = absent_terms
    
    # DESCONHECIDO: perguntas que o sistema não pode responder
    unknown_answers = [
        {
            'question': 'Quando exatamente Edson abandonou o termo de recursão R^α?',
            'reason': 'Não há documento intermediário entre v5.1 (com R) e v6.2 (sem R). A transição ocorreu em algum momento entre as duas versões, mas não pode ser datada.',
            'would_resolve_with': 'Inclusão de versões v6.0 e v6.1 do Paper A no corpus.',
        },
        {
            'question': 'Quando Edson propôs formalmente a hipótese η pela primeira vez?',
            'reason': 'Hipótese η está descrita como existente em "nosso trabalho anterior (v6.0)" do Paper B v6.1. Documento v6.0 não está no corpus.',
            'would_resolve_with': 'Inclusão da versão v6.0 do Paper B no corpus.',
        },
        {
            'question': 'O Paper C foi efetivamente submetido à Foundations of Physics em 10/08/2026?',
            'reason': 'T10 — afirmado textualmente na Cover Letter PT-BR [E-textual], mas o evento no mundo não foi confirmado pelo autor [I-pending-author-confirmation].',
            'would_resolve_with': 'Confirmação direta do autor ou evidência externa (recibo de submissão).',
        },
        {
            'question': 'Qual é o conteúdo das Partes I, II e III do Programa de Formalização?',
            'reason': 'T9 — CORPUS-003 é "Parte IV, Passos 16-18" apenas. Partes I-III não estão no corpus.',
            'would_resolve_with': 'Inclusão das Partes I-III no corpus.',
        },
        {
            'question': 'Qual é o conteúdo da Cover Letter oficial enviada ao PRE?',
            'reason': 'T6 — versão PT-BR no corpus é rascunho v6.1 aspiracional; versão EN não está no corpus.',
            'would_resolve_with': 'Inclusão de Cover_Letter_Paper_A_PRE.md (EN) no corpus.',
        },
    ]
    negative['DESCONHECIDO'] = unknown_answers
    
    return negative


def run_hist_test(test_id: str, question: str, states: list, negative_memory: dict) -> dict:
    """Executa um teste do protocolo AION-HIST-001."""
    print(f"\n[{test_id}] {question}")
    print('-' * 70)
    
    if test_id == 'HIST-001':
        # Ideias abandonadas
        revoked = [s for s in states if s['change_type'] == 'REVOKED']
        contradicted = [s for s in states if s['change_type'] == 'CONTRADICTED']
        
        answer_lines = [f"## Resposta a HIST-001: Ideias abandonadas\n"]
        answer_lines.append(f"Total de retrações formais (REVOKED): {len(revoked)}")
        answer_lines.append(f"Total de contradições documentais (CONTRADICTED): {len(contradicted)}\n")
        
        answer_lines.append("### RETRAÇÕES FORMAIS PELO AUTOR:")
        for s in revoked:
            answer_lines.append(f"\n**{s['concept_label']}**")
            answer_lines.append(f"- Data da retração: {s['valid_at']}")
            answer_lines.append(f"- Documento: {s['document']} ({s['version']})")
            answer_lines.append(f"- Estado anterior: {s['previous_state']}")
            answer_lines.append(f"- Estado final: {s['state']}")
            answer_lines.append(f"- Evidência: \"{s['evidence_text']}\"")
            answer_lines.append(f"- Tipo: {s['evidence_type']}")
        
        answer_lines.append("\n### CONTRADIÇÕES DOCUMENTAIS (inferências descreditadas):")
        for s in contradicted:
            answer_lines.append(f"\n**{s['concept_label']}**")
            answer_lines.append(f"- Data da contradição: {s['valid_at']}")
            answer_lines.append(f"- Documento: {s['document']}")
            answer_lines.append(f"- Estado anterior (inferido): {s['previous_state']}")
            answer_lines.append(f"- Estado final (auditado): {s['state']}")
            answer_lines.append(f"- Evidência: \"{s['evidence_text']}\"")
            answer_lines.append(f"- Tipo: {s['evidence_type']}")
        
        answer = '\n'.join(answer_lines)
    
    elif test_id == 'HIST-002':
        # Ideias refinadas (não abandonadas)
        refined = [s for s in states if s['change_type'] == 'REFINED']
        
        answer_lines = [f"## Resposta a HIST-002: Ideias refinadas (não abandonadas)\n"]
        answer_lines.append(f"Total de refinamentos: {len(refined)}\n")
        
        for s in refined:
            answer_lines.append(f"**{s['concept_label']}** ({s['concept_id']})")
            answer_lines.append(f"- Data do refinamento: {s['valid_at']}")
            answer_lines.append(f"- Documento: {s['document']} ({s['version']})")
            answer_lines.append(f"- Estado anterior: {s['previous_state']}")
            answer_lines.append(f"- Estado refinado: {s['state']}")
            answer_lines.append(f"- Evidência: \"{s['evidence_text']}\"")
            answer_lines.append(f"- Tipo: {s['evidence_type']}")
            answer_lines.append(f"- Nota: {s.get('note', '')}\n")
        
        answer = '\n'.join(answer_lines)
    
    elif test_id == 'HIST-003':
        # Conceitos estáveis (Núcleo de Continuidade Intelectual)
        grouped = defaultdict(list)
        for s in states:
            grouped[s['concept_id']].append(s)
        
        stable_concepts = []
        for cid, cid_states in grouped.items():
            # Conceito é estável se: ou é STABLE, ou tem apenas INTRODUCED (sem REFINED/REVOKED/CONTRADICTED)
            change_types = {s['change_type'] for s in cid_states}
            if change_types == {'STABLE'} or change_types == {'INTRODUCED'}:
                stable_concepts.append({
                    'concept_id': cid,
                    'concept_label': cid_states[0]['concept_label'],
                    'states': cid_states,
                    'stable_since': cid_states[0]['valid_at'],
                    'kind': 'STABLE' if 'STABLE' in change_types else 'INTRODUCED-ONLY',
                })
        
        answer_lines = [f"## Resposta a HIST-003: Núcleo de Continuidade Intelectual\n"]
        answer_lines.append(f"Total de conceitos estáveis: {len(stable_concepts)}\n")
        answer_lines.append("### NÚCLEO DE CONTINUIDADE INTELECTUAL:\n")
        
        for sc in stable_concepts:
            answer_lines.append(f"**{sc['concept_label']}** ({sc['concept_id']})")
            answer_lines.append(f"- Estável desde: {sc['stable_since']}")
            answer_lines.append(f"- Tipo: {sc['kind']}")
            answer_lines.append(f"- Estado: {sc['states'][-1]['state']}\n")
        
        answer = '\n'.join(answer_lines)
    
    elif test_id == 'HIST-004':
        # Afirmações que apareceram mas foram contraditas
        contradicted = negative_memory['CONTRADITO']
        
        answer_lines = [f"## Resposta a HIST-004: Afirmações contraditas pela auditoria\n"]
        answer_lines.append(f"Total: {len(contradicted)}\n")
        
        for c in contradicted:
            answer_lines.append(f"**{c['concept_label']}**")
            answer_lines.append(f"- Estado anterior (inferido): {c['previous_state']}")
            answer_lines.append(f"- Estado final (auditado): {c['state']}")
            answer_lines.append(f"- Razão: {c['reason']}")
            answer_lines.append(f"- Evidência: \"{c['evidence']}\"")
            answer_lines.append(f"- Documento da auditoria: {c['document']}\n")
        
        answer = '\n'.join(answer_lines)
    
    elif test_id == 'HIST-005':
        # O que o AION não consegue determinar
        unknown = negative_memory['DESCONHECIDO']
        indeterminate = negative_memory['INDETERMINADO']
        
        answer_lines = [f"## Resposta a HIST-005: Lacunas de determinação\n"]
        answer_lines.append(f"Total de perguntas não respondíveis: {len(unknown)}")
        answer_lines.append(f"Total de estados com data indeterminada: {len(indeterminate)}\n")
        
        answer_lines.append("### PERGUNTAS NÃO RESPONDÍVEIS:")
        for u in unknown:
            answer_lines.append(f"\n**Pergunta:** {u['question']}")
            answer_lines.append(f"- Razão: {u['reason']}")
            answer_lines.append(f"- Resolveria com: {u['would_resolve_with']}")
        
        answer_lines.append(f"\n### ESTADOS COM DATA INDETERMINADA (UNKNOWN):")
        for i in indeterminate:
            answer_lines.append(f"\n**{i['concept_label']}**")
            answer_lines.append(f"- Estado: {i['state']}")
            answer_lines.append(f"- Razão: {i['reason']}")
        
        answer = '\n'.join(answer_lines)
    
    elif test_id == 'HIST-006':
        # Documentos necessários para reduzir lacunas
        unknown = negative_memory['DESCONHECIDO']
        absent = negative_memory['AUSENTE']
        
        # Agrega would_resolve_with das perguntas desconhecidas
        docs_needed = {}
        for u in unknown:
            doc = u['would_resolve_with']
            if doc not in docs_needed:
                docs_needed[doc] = {
                    'questions_resolved': [],
                    'lacunas_resolvidas': 0,
                }
            docs_needed[doc]['questions_resolved'].append(u['question'])
            docs_needed[doc]['lacunas_resolvidas'] += 1
        
        # Mapeia termos ausentes para documentos que os resolveriam
        absent_docs_map = {
            'Paper C (versão final submetida à Foundations of Physics)': 'Inclusão da versão final do Paper C (submetida) no corpus.',
            'Cover Letter oficial em inglês (Cover_Letter_Paper_A_PRE.md)': 'Inclusão de Cover_Letter_Paper_A_PRE.md (EN) no corpus.',
            'Partes I-III do Programa de Formalização Físico-Matemática': 'Inclusão das Partes I, II e III do programa de formalização no corpus.',
            'Versão v5.1 do Paper A (submetida ao Brazilian Journal of Physics)': 'Inclusão da versão v5.1 do Paper A no corpus.',
            'Versão v6.0 do Paper A (com termo de recursão R^α)': 'Inclusão da versão v6.0 do Paper A no corpus.',
            'Versão v6.0 do Paper B (com hipótese η e dímero 2 sítios)': 'Inclusão da versão v6.0 do Paper B no corpus.',
        }
        
        answer_lines = [f"## Resposta a HIST-006: Documentos necessários\n"]
        answer_lines.append(f"Documentos identificados como necessários: {len(absent_docs_map)}\n")
        answer_lines.append("### PRIORIZAÇÃO PARA AION-CORPUS-001 v1.3.0:\n")
        
        # Ordena por número de lacunas resolvidas
        priority = []
        for doc, info in docs_needed.items():
            priority.append({
                'document': doc,
                'questions_resolved': info['questions_resolved'],
                'count': info['lacunas_resolvidas'],
                'priority': 'ALTA' if info['lacunas_resolvidas'] >= 2 else 'MÉDIA',
            })
        # Adiciona os que só aparecem como AUSENTE
        for term, doc in absent_docs_map.items():
            if doc not in [p['document'] for p in priority]:
                priority.append({
                    'document': doc,
                    'questions_resolved': [],
                    'count': 0,
                    'priority': 'MÉDIA',
                    'related_absent_term': term,
                })
        
        priority.sort(key=lambda x: x['count'], reverse=True)
        
        for p in priority:
            answer_lines.append(f"**{p['document']}**")
            answer_lines.append(f"- Prioridade: {p['priority']}")
            answer_lines.append(f"- Lacunas resolvidas: {p['count']}")
            if p['questions_resolved']:
                for q in p['questions_resolved']:
                    answer_lines.append(f"  • {q}")
            if p.get('related_absent_term'):
                answer_lines.append(f"- Termo ausente relacionado: {p['related_absent_term']}")
            answer_lines.append("")
        
        answer = '\n'.join(answer_lines)
    
    else:
        answer = "Teste não reconhecido."
    
    print(answer[:3000] + ("..." if len(answer) > 3000 else ""))
    return {
        'test_id': test_id,
        'question': question,
        'answer': answer,
    }


def build_quem_e_edson_answer(states: list, negative_memory: dict) -> str:
    """Constrói resposta experimental a 'Quem é Edson Carvalho do Nascimento?'"""
    
    # Agrega dados
    grouped = defaultdict(list)
    for s in states:
        grouped[s['concept_id']].append(s)
    
    stable = []
    refined = []
    revoked = []
    contradicted = []
    
    for cid, cid_states in grouped.items():
        change_types = {s['change_type'] for s in cid_states}
        if change_types == {'STABLE'} or change_types == {'INTRODUCED'}:
            stable.append(cid_states[-1])
        if 'REFINED' in change_types:
            refined.append(cid_states[-1])
        if 'REVOKED' in change_types:
            revoked.append([s for s in cid_states if s['change_type'] == 'REVOKED'][0])
        if 'CONTRADICTED' in change_types:
            contradicted.append([s for s in cid_states if s['change_type'] == 'CONTRADICTED'][0])
    
    answer = f"""# Quem é Edson Carvalho do Nascimento?

## Resposta experimental — primeira reconstrução documental
### (Baseada no corpus AION-CORPUS-001 v1.2.0 + ontologia v1.0.0 + grafo temporal v1.0)

---

### Núcleo de Continuidade Intelectual ({len(stable)} conceitos estáveis)

Edson é um autor cujo núcleo teórico permaneceu estável desde sua primeira documentação no corpus:

"""
    for s in stable:
        answer += f"- **{s['concept_label']}** — {s['state']}\n"
    
    answer += f"""

### Capacidade de Refinamento ({len(refined)} conceitos refinados)

Edson refina suas ideias sem abandoná-las — incorpora calibração empírica e abandona componentes não-contributivos:

"""
    for s in refined:
        answer += f"- **{s['concept_label']}**: {s['previous_state']} → {s['state']}\n"
        answer += f"  - Motivo: {s.get('note', '')}\n"
    
    answer += f"""

### Capacidade de Autorretração ({len(revoked)} retrações formais)

Edson abandona formalmente hipóteses quando a evidência as contradiz — marca registrada de seu método:

"""
    for s in revoked:
        answer += f"- **{s['concept_label']}** (retraído em {s['valid_at']})\n"
        answer += f"  - Estado anterior: {s['previous_state']}\n"
        answer += f"  - Estado final: {s['state']}\n"
        answer += f"  - Evidência da retração: \"{s['evidence_text']}\"\n"
    
    answer += f"""

### Rigor Curatorial ({len(contradicted)} inferências descreditadas pela própria auditoria)

O programa de curadoria do AION (sobre o trabalho do autor) identificou conceitos que foram inferidos mas não textualmente presentes:

"""
    for s in contradicted:
        answer += f"- **{s['concept_label']}** — inferido em {s.get('previous_state', 'Handoff original')}\n"
        answer += f"  - Auditoria: {s['state']}\n"
    
    answer += f"""

### Lacunas Conhecidas ({len(negative_memory['DESCONHECIDO'])} perguntas não respondíveis)

O AION não pode determinar:

"""
    for u in negative_memory['DESCONHECIDO']:
        answer += f"- {u['question']}\n"
        answer += f"  - Resolveria com: {u['would_resolve_with']}\n"
    
    answer += f"""

### Documentos Necessários para Reduzir Lacunas

Para uma reconstrução mais completa da trajetória intelectual de Edson, seriam necessários:

"""
    docs_needed_set = set()
    for u in negative_memory['DESCONHECIDO']:
        docs_needed_set.add(u['would_resolve_with'])
    for term in negative_memory['AUSENTE']:
        if 'Cover Letter' in term['term'] or 'Paper C' in term['term'] or 'Partes I' in term['term'] or 'v5.1' in term['term'] or 'v6.0' in term['term']:
            docs_needed_set.add(f"Documento relacionado a: {term['term']}")
    
    for doc in docs_needed_set:
        answer += f"- {doc}\n"
    
    answer += f"""

---

## Síntese

Edson Carvalho do Nascimento, conforme reconstruído documentalmente pelo corpus AION-CORPUS-001 v1.2.0, é:

1. **Um autor com núcleo teórico estável** — formalização categórico-tensorial unificada (Φcat + Qµν + Einstein mod), estruturada lakatosianamente, em estado conjectural/propositivo.

2. **Um pesquisador que calibra empiricamente** — refina β via LOOCV quando a evidência o justifica; re-deriva power-laws quando a extrapolação se mostra injustificável.

3. **Um cientista que retrata formalmente** — abandona hipóteses (η, R^α) quando critérios quantitativos não são satisfeitos, mesmo quando isso enfraquece seu programa.

4. **Um curador intelectual epistemicamente rigoroso** — seu próprio sistema de curadoria (o AION em si) identificou e descreditou inferências que não tinham respaldo textual (consciência, campo primordial).

5. **Um autor com lacunas documentais conhecidas** — versões intermediárias (v5.1, v6.0) e documentos complementares (Cover Letter EN, Partes I-III, Paper C final) não estão no corpus. O AION sabe que não estão, e sabe que precisaria deles para responder certas perguntas.

Esta não é uma biografia. É uma **trajetória documentada de ideias, escolhas, revisões, erros, correções, permanências e lacunas**.

---

*Resposta gerada em {datetime.now(timezone.utc).isoformat(timespec='seconds')}*
*Protocolo: AION-HIST-001*
*Base: corpus AION-CORPUS-001 v1.2.0 + ontologia v1.0.0 + grafo temporal v1.0*
"""
    
    return answer


def main():
    print("=" * 70)
    print("AION Passo 5.8 — Reconciliação Histórica (AION-HIST-001)")
    print("=" * 70)
    
    states = TEMPORAL['states']
    print(f"\n[5.8.1] Estados temporais carregados: {len(states)}")
    
    # Constrói Memória Negativa
    print(f"\n[5.8.2] Construindo Memória Negativa...")
    negative_memory = build_negative_memory(states)
    for cat, items in negative_memory.items():
        print(f"  • {cat}: {len(items)}")
    
    # Executa testes HIST-001 a 006
    print(f"\n[5.8.3] Executando bateria HIST-001 a 006...")
    tests = [
        ('HIST-001', "Quais ideias Edson abandonou?"),
        ('HIST-002', "Quais ideias foram apenas refinadas?"),
        ('HIST-003', "Quais conceitos permanecem estáveis?"),
        ('HIST-004', "Quais afirmações aparecem no histórico mas foram posteriormente contraditas?"),
        ('HIST-005', "O que o AION não consegue determinar devido a lacunas documentais?"),
        ('HIST-006', "Quais documentos seriam necessários para reduzir essas lacunas?"),
    ]
    
    test_results = {}
    for test_id, question in tests:
        result = run_hist_test(test_id, question, states, negative_memory)
        test_results[test_id] = result
    
    # Constrói resposta experimental a "Quem é Edson?"
    print(f"\n[5.8.4] Construindo resposta experimental a 'Quem é Edson Carvalho do Nascimento?'...")
    quem_e_edson = build_quem_e_edson_answer(states, negative_memory)
    print(f"  Resposta gerada: {len(quem_e_edson)} caracteres")
    
    # Estrutura final
    report = {
        'metadata': {
            'version': '1.0.0',
            'generated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'author_structure': 'Edson C. Nascimento (Projetista Master)',
            'author_implementation': 'IA Curadora',
            'protocol': 'AION-HIST-001',
            'base': 'AION-CORPUS-001 v1.2.0 + ONTOLOGY v1.0.0 + aion_temporal_graph_v1.0',
        },
        'negative_memory': negative_memory,
        'negative_memory_summary': {
            cat: len(items) for cat, items in negative_memory.items()
        },
        'test_results': test_results,
        'quem_e_edson': quem_e_edson,
    }
    
    # Salvar JSON
    json_path = OUTPUT_DIR / 'aion_hist_001_reconciliacao.json'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n[5.8.5] JSON salvo: {json_path}")
    print(f"  Tamanho: {json_path.stat().st_size} bytes")
    
    # Salvar HTML
    html_path = OUTPUT_DIR / 'aion_hist_001_report.html'
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AION-HIST-001 — Reconciliação Histórica</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:1200px;margin:2rem auto;line-height:1.6;padding:0 1rem;background:#fafafa;color:#111}}
h1,h2,h3{{color:#1a252f}}
h2{{color:#2c3e50;border-left:4px solid #3498db;padding-left:.8rem;margin-top:2rem}}
.negative-memory{{background:#fff3cd;border-left:4px solid #f39c12;padding:1rem;margin:1rem 0}}
.positive-memory{{background:#d4edda;border-left:4px solid #28a745;padding:1rem;margin:1rem 0}}
.test-result{{background:#fff;padding:1rem;margin:1rem 0;border-left:4px solid #3498db}}
pre{{background:#f8f9fa;padding:1rem;overflow-x:auto;border-radius:4px}}
</style>
</head>
<body>
<header>
<h1>AION-HIST-001 — Reconciliação Histórica</h1>
<p><strong>Versão:</strong> 1.0.0</p>
<p><strong>Data:</strong> 17 de agosto de 2026</p>
<p><strong>Autor da estrutura:</strong> Edson C. Nascimento (Projetista Master)</p>
<p><strong>Implementação:</strong> IA Curadora</p>
</header>

<section>
<h2>Resumo Executivo</h2>
<div class="positive-memory">
<strong>Memória Positiva:</strong> {len(states)} estados conceituais documentados em {len(set(s['concept_id'] for s in states))} conceitos.
</div>
<div class="negative-memory">
<strong>Memória Negativa:</strong>
<ul>
<li>DESCONHECIDO: {len(negative_memory['DESCONHECIDO'])} perguntas não respondíveis</li>
<li>AUSENTE: {len(negative_memory['AUSENTE'])} termos/conceitos procurados e não encontrados</li>
<li>CONTRADITO: {len(negative_memory['CONTRADITO'])} inferências descreditadas pela auditoria</li>
<li>REVOGADO: {len(negative_memory['REVOGADO'])} retrações formais pelo autor</li>
<li>INDETERMINADO: {len(negative_memory['INDETERMINADO'])} estados com data desconhecida</li>
</ul>
</div>
</section>

<section>
<h2>Resultados dos Testes HIST-001 a 006</h2>
"""
    for test_id, result in test_results.items():
        html_content += f"""
<div class="test-result">
<h3>{test_id}: {result['question']}</h3>
<pre>{result['answer']}</pre>
</div>
"""
    
    html_content += f"""
</section>

<section>
<h2>Resposta Experimental: Quem é Edson Carvalho do Nascimento?</h2>
<pre>{quem_e_edson}</pre>
</section>

<footer>
<p><em>"Ausência de informação não é autorização para inferência. Estados UNKNOWN são dados, não lacunas a preencher."</em></p>
</footer>
</body>
</html>
"""
    html_path.write_text(html_content, encoding='utf-8')
    print(f"  HTML salvo: {html_path}")
    print(f"  Tamanho: {html_path.stat().st_size} bytes")
    
    # Resumo final
    print(f"\n{'=' * 70}")
    print("[RESUMO Passo 5.8 — Reconciliação Histórica]")
    print(f"{'=' * 70}")
    print(f"Testes executados: 6 (HIST-001 a HIST-006)")
    print(f"Memória Negativa:")
    for cat, items in negative_memory.items():
        print(f"  • {cat}: {len(items)}")
    print(f"Resposta experimental 'Quem é Edson?': {len(quem_e_edson)} caracteres")
    
    return report


if __name__ == '__main__':
    main()
