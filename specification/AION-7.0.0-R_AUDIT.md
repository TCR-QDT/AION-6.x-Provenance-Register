# AION-7.0.0-R — FROZEN Component Restoration Audit

**Versão:** 7.0.0-R-spec
**Data:** 21 de agosto de 2026
**Autor / Curador:** Edson Carvalho do Nascimento (Projetista Master)
**Analista Técnico:** IA Curadora (Role: Escriba / Arquiteto de Metadados)
**Sessão:** web-73c75281-201c-4716-b85c-97833d25f9b3
**Status:** AUDIT PROTOCOL FROZEN — Auditoria material PENDENTE de restauração
**Genealogia:** Derivado do Protocolo AION-7.0.0-spec (Seção 12 — Estado Material e Pendências), após determinação do Projetista Master de Opção B (Specification-Only)

---

## 1. Resumo Executivo

AION-7.0.0-R é o protocolo canônico de auditoria de restauração dos componentes FROZEN do projeto AION. Sua função é verificar materialmente, antes de qualquer execução observacional do baseline 7.0.0, que cada componente declarado FROZEN no Handoff AION-MVP-001 (Seção 3) foi restaurado ao ambiente `/home/z/my-project/` em sua versão correta, íntegra e autenticável. Sem esta auditoria, nenhuma transição do estado `SPECIFICATION COMPLETE` para `BASELINE EXECUTION AUTHORIZED` é permitida. A auditoria responde, por componente, à pergunta canônica: "o artefato que declaro como FROZEN está materialmente presente, na versão correta, com conteúdo íntegro?" — porque o AION não confunde continuidade nominal do projeto com continuidade material da evidência.

### 1.1 Regra adicional de integridade (incorporada na Task 62)

O próprio `AION-7.0.0-R_AUDIT.md` **não deve ser considerado evidência suficiente para autenticar os componentes que ele pretende auditar.** O protocolo é o **instrumento de auditoria**, não a prova da existência ou identidade dos artefatos auditados. A prova da existência, versão, integridade e canonicidade de cada componente vem exclusivamente da execução material das quatro verificações (V1, V2, V3, V4 — Seção 4) sobre o componente restaurado. O protocolo define o método; o método não se substitui à execução do método.

## 2. Propósito e Princípio Epistemológico

### 2.1 Propósito

A auditoria 7.0.0-R existe para impedir a seguinte falha categorial: executar AION-7.0.0 sobre componentes que não são os declarados FROZEN. Se isso ocorresse, qualquer resultado do baseline seria atribuído à arquitetura 6.x, mas materialmente teria sido produzido sobre uma reconstrução — violando a Regra 1 (Provenance), a Regra 3 (O Nome do Arquivo não é o Documento), e o princípio operacional de 7.0.0 de "medir a arquitetura existente, não melhorá-la".

### 2.2 Princípio

A descoberta de que o ambiente atual não contém os artefatos não é uma inconveniência operacional. É, ela própria, um evento de proveniência do projeto que deve ser preservado. O AION não pode ser autorizado a dizer:

> "AION-7.0.0 executou sobre a arquitetura 6.x congelada"

quando materialmente não conseguimos demonstrar isso.

O estado correto, e que esta auditoria existe para destravar, é:

> "AION-7.0.0 foi especificado e congelado; sua execução permanece pendente da restauração verificável dos componentes experimentais congelados."

### 2.3 Auto-aplicação

AION-7.0.0-R é uma oportunidade para o AION aplicar pela primeira vez a própria regra que está tentando medir: **não confundir continuidade nominal do projeto com continuidade material da evidência.** A auditoria é a materialização operacional do princípio ECB aplicado à própria infraestrutura do projeto — exigindo que a "provenance" declarada (o componente FROZEN) seja verificada quanto à sua existência material (restauração) e correspondência (versão/hash corretos), antes de qualquer inferência ("execução bem-sucedida") ser aceita.

## 3. Componentes a Auditar

Para cada componente abaixo, a auditoria deve preencher a tabela canônica:

| Componente | Versão Esperada | Versão Encontrada | Hash/Checksum | Integridade | Ação |
|---|---|---|---|---|---|
| Corpus | v1.3.0 | — | — | PENDING | restaurar |
| Oracle | v3 | — | — | PENDING | restaurar |
| GraphRAG | v1.0.0 | — | — | PENDING | restaurar |
| P-RESP-001 | v0.3 | — | — | PENDING | restaurar |
| AION-EVAL-002 | v0.2 | — | — | PENDING | restaurar |
| B1 Retrieval config | 6.2.11 | — | — | PENDING | restaurar |

### 3.1 Sub-componentes do Corpus

Como o Corpus é um agregado de 9 registros documentais (CORPUS-001 a CORPUS-007, CORPUS-011, mais 2 declarados inexistentes), a auditoria do Corpus deve também verificar cada sub-registro:

| Sub-registro | Documento | Estado Esperado |
|---|---|---|
| CORPUS-001 | AION-DOC-000.html | CURRENT |
| CORPUS-002-HIST | Paper A v6.2 anterior (134KB) | SUPERSEDED |
| CORPUS-002 | Paper A v6.2 (137KB) | CURRENT/AUTHORITATIVE |
| CORPUS-003 | PARTE IV Formalização Teórica | CURRENT |
| CORPUS-004 | Paper B anterior (3 págs) | HISTORICAL |
| CORPUS-005 | Cover Letter PT-BR | CURRENT |
| CORPUS-006 | Paper A v6.1 oficial (138KB) | HISTORICAL |
| CORPUS-007 | Paper A v6.1 revisão (326KB) | HISTORICAL/SCIENTIFIC_REVISION |
| CORPUS-011 | Paper B v6.1 PT novo (5 págs) | CURRENT |
| Paper A v6.0 | — | DOES NOT EXIST (verificar ausência) |
| Paper B v6.0 | — | DOES NOT EXIST (verificar ausência) |

### 3.2 Sub-componentes do Oracle v3

O Oracle v3 é composto por 7 chunks interversionais. A auditoria deve verificar a presença e integridade de cada um:

| Chunk | Origem |
|---|---|
| Chunk 1 | CORPUS-002#p1_01 |
| Chunk 2 | CORPUS-002#p1_02 |
| Chunk 3 | CORPUS-002#p2_01 |
| Chunk 4 | CORPUS-002#p5_01 |
| Chunk 5 | CORPUS-002#p5_02 |
| Chunk 6 | CORPUS-006#p1_01 |
| Chunk 7 | CORPUS-007#p1_01 |

### 3.3 Sub-componentes dos scripts

Os 12 scripts persistidos devem ser verificados individualmente:

| Script | Função |
|---|---|
| `scripts/extract_aion_corpus.py` | Extração de PDF |
| `scripts/aion_rag_proxy.py` | RAG proxy (TF-IDF + chunking) |
| `scripts/aion_graphrag.py` | GraphRAG (NetworkX) |
| `scripts/aion_provenance_granular.py` | Proveniência granular (PGI=1.0) |
| `scripts/aion_temporal_graph.py` | Grafo temporal (TPC=1.0) |
| `scripts/aion_historical_reconciliation.py` | Reconciliação histórica |
| `scripts/aion_bench_001.py` | Benchmark B1-B7 |
| `scripts/aion_p_resp_001_v03.py` | P-RESP-001 v0.3 |
| `scripts/aion_dify_001.py` | Workflow DIFY |
| `scripts/aion_6_3_0_baseline.py` | Baseline N=100 |
| `scripts/aion_6_4_0_conditional.py` | Confiabilidade condicional |
| `scripts/aion_6_4_2_minimal.py` | Ancoragem minimal (M0/M1/M2) |

### 3.4 Artefatos canônicos (documentos)

| Artefato | Conteúdo |
|---|---|
| `/download/AION-CORPUS-001_v1.2.0.html` | Registro do corpus (v1.2.0 histórico) |
| `/download/AION-CORPUS-001-ONTOLOGY_v1.0.0.md` | Ontologia verificada (13 conceitos, 4 clusters) |
| `/download/AION-EVAL-002.html` | Protocolo de avaliação multicamada |
| `/download/AION-6.5.0_B2_Characterization.md` | Caracterização canônica de B2 |

### 3.5 Dados experimentais (JSONs em `/download/rag/`)

| Arquivo | Conteúdo |
|---|---|
| `aion_6_4_0_conditional_reliability.json` | Baseline N=100 (PER, CFR, EBA) |
| `aion_6_2_11_oracle_v3_rebenchmark.json` | B1 resolvido (Top-1=3/3) |
| `aion_6_5_0_*` | Caracterização B2 |
| `graphrag_enriched_v2.0.json` | Grafo enriquecido (PGI=1.0) |
| `aion_temporal_graph_v1.0.json` | Grafo temporal (TPC=1.0) |

## 4. Procedimento de Verificação por Componente

Para cada componente, a auditoria executa quatro verificações em sequência. A falha em qualquer uma marca o componente como `INTEGRITY: FAIL` e bloqueia a transição para `BASELINE EXECUTION AUTHORIZED`.

### 4.1 Verificação de Existência (V1)

**Pergunta:** O arquivo declarado está materialmente presente no caminho declarado?

**Procedimento:**
- Verificar presença física do arquivo em `/home/z/my-project/` ou subdiretório declarado.
- Para diretórios (`/scripts/`, `/download/rag/`, `/upload/`), verificar que contém o conjunto esperado de arquivos.

**Saída:** `EXISTENCE: PRESENT` ou `EXISTENCE: ABSENT`.

### 4.2 Verificação de Versão (V2)

**Pergunta:** A versão do arquivo corresponde à versão esperada declarada no Handoff?

**Procedimento:**
- Inspecionar metadados internos do arquivo (cabeçalho de versão, comment de versão).
- Para scripts Python: procurar por string de versão no cabeçalho (e.g., `# AION-RAG-PROXY v1.0.0`).
- Para JSONs: procurar campo `version` ou `pipeline_version` no JSON.
- Para PDFs: comparar tamanho declarado no Handoff (e.g., CORPUS-002 = 137KB) com tamanho real.

**Saída:** `VERSION: MATCH` ou `VERSION: MISMATCH` (com versão encontrada declarada).

### 4.3 Verificação de Integridade (V3)

**Pergunta:** O conteúdo do arquivo é íntegro (não corrompido, não modificado)?

**Procedimento:**
- Computar hash SHA-256 do arquivo restaurado.
- Comparar com hash de referência (se houver; caso contrário, registrar hash como baseline para futuras verificações).
- Para scripts Python: executar `python -c "import <module>"` para verificar que carregam sem erro de sintaxe.
- Para JSONs: executar `jq '.' <file> > /dev/null` para verificar validade sintática.
- Para PDFs: executar `pdfinfo <file>` para verificar que PDF é parseable.

**Saída:** `INTEGRITY: VERIFIED` (com hash registrado), `INTEGRITY: CORRUPT`, ou `INTEGRITY: HASH_BASELINE_REGISTERED` (primeira verificação).

### 4.4 Verificação de Conteúdo Canônico (V4)

**Pergunta:** O conteúdo do arquivo corresponde ao esperado pela especificação canônica?

**Procedimento:**
- Para o Corpus: verificar número de registros (esperado: 9 existentes + 2 declarados inexistentes = 11 entradas no catálogo, com 9 PDFs presentes em `/upload/`).
- Para o Oracle v3: verificar número de chunks (esperado: 7), e que cada chunk tem origem CORPUS-002/006/007 conforme Seção 3.2.
- Para GraphRAG: verificar número de nós (esperado: 22) e arestas (esperado: 187), PGI=1.0.
- Para P-RESP-001 v0.3: verificar presença do validator determinístico, e que validator intercepta 100% (VR=1.000) em testes de regressão.
- Para AION-EVAL-002 v0.2: verificar as 10 categorias R1-H1, e classificação FAIL-SYSTEM vs FAIL-EVALUATOR.
- Para B1 config: verificar 3 queries canônicas PT-BR→EN, e que Top-1=3/3 é reproduzível.
- Para Temporal Index v1.0: verificar TPC=1.0000.

**Saída:** `CONTENT: CANONICAL`, `CONTENT: DEVIANT` (com descrição da desvio), ou `CONTENT: HASH_BASELINE_REGISTERED`.

## 5. Critérios de Integridade

Para cada componente, o campo `Integridade` da tabela canônica (Seção 3) recebe um dos seguintes estados:

| Estado | Condição |
|---|---|
| `PENDING` | Auditoria ainda não executada (estado inicial desta especificação). |
| `VERIFIED` | V1 ∧ V2 ∧ V3 ∧ V4 = todos PASS. |
| `PARTIAL` | V1=PRESENT, mas algum de V2/V3/V4 falhou. Componente presente mas possivelmente corrompido ou em versão errada. |
| `ABSENT` | V1=ABSENT. Componente não materialmente presente. |
| `CORRUPT` | V1=PRESENT mas V3=CORRUPT. Componente presente mas com conteúdo corrompido. |
| `NON_CANONICAL` | V1=PRESENT ∧ V3=VERIFIED, mas V4=DEVIANT. Componente presente e íntegro, mas conteúdo não corresponde ao esperado pela especificação. |

Apenas `VERIFIED` autoriza a transição para `BASELINE EXECUTION AUTHORIZED`.

## 6. Authorization Gate Logic

### 6.1 Fórmula canônica (conjuntiva, não-compensatória)

O critério de autorização é **estritamente conjuntivo**. Nenhum componente correto pode compensar um componente não-autenticado. Formalmente:

$$\text{AUTH}_{7.0} = \bigwedge_{i=1}^{6} (E_i \land V_i \land H_i \land C_i)$$

Onde, para cada componente $i \in \{\text{Corpus}, \text{Oracle}, \text{GraphRAG}, \text{P-RESP-001}, \text{EVAL-002}, \text{B1}\}$:

| Símbolo | Verificação | Definição |
|---|---|---|
| $E_i$ | Existência | V1 — artefato materialmente presente no caminho declarado |
| $V_i$ | Versão | V2 — versão encontrada = versão esperada no Handoff |
| $H_i$ | Hash/Integridade | V3 — SHA-256 verificado (ou registrado como baseline) |
| $C_i$ | Conteúdo Canônico | V4 — conteúdo corresponde à especificação canônica |

**Regra operacional:** um componente `ABSENT`, `CORRUPT`, `PARTIAL` ou `NON_CANONICAL` bloqueia a execução inteira. Não há compensação parcial.

### 6.2 Transições de estado do projeto

A transição entre estados do projeto AION-7.0.0 é governada pela seguinte lógica determinística:

```
STATE: SPECIFICATION COMPLETE
       │
       ▼  Aguardar restauração material dos componentes
       │
STATE: RESTORATION IN PROGRESS
       │
       ▼  Executar AION-7.0.0-R audit (V1 ∧ V2 ∧ V3 ∧ V4 por componente)
       │
       ├── SE AUTH_{7.0} = TRUE (todos os 6 componentes = VERIFIED)
       │   │
       │   ▼
       │   STATE: RESTORATION VERIFIED
       │   │
       │   ▼  Autorização do Projetista Master
       │   │
       │   STATE: BASELINE EXECUTION AUTHORIZED
       │   │
       │   ▼  Executar N=100 queries
       │   │
       │   STATE: BASELINE EXECUTION COMPLETE
       │
       └── SE AUTH_{7.0} = FALSE (algum componente ∈ {PARTIAL, ABSENT, CORRUPT, NON_CANONICAL})
           │
           ▼
           STATE: RESTORATION BLOCKED
           │
           ▼  Reportar ao Projetista Master com tabela de discrepâncias
           │
           STATE: AGUARDAR RE-RESTAURAÇÃO
           │
           ▼  Re-executar AION-7.0.0-R
           │
           (loop até AUTH_{7.0} = TRUE)
```

### 6.3 Regra de não-delegação

Nenhum componente pode ser marcado como `VERIFIED` sem as quatro verificações (V1, V2, V3, V4) terem sido executadas e terem passado. **Marcação por convenção ("sabemos que está ok porque foi restaurado") é proibida.** A verificação é sempre material.

### 6.4 Regra de não-substituição

Se um componente restaurado tem versão diferente da esperada, ele não pode ser aceito como "aproximação" ou "equivalente". Deve ser marcado `PARTIAL` (se presente) e o estado permanece `RESTORATION BLOCKED`. Substituir por versão aproximada violaria Regra 9 (Substituição não é apagamento — genealogia documental deve ser preservada) e Regra 8 (Oracle não pode ser relaxado porque retrieval falhou — primeiro demonstrar documentalmente que o oracle era restritivo).

## 7. Formato de Saída da Auditoria

A auditoria 7.0.0-R produz dois artefatos ao concluir:

### 7.1 Tabela canônica (canônica, legível por humano)

Caminho: `/home/z/my-project/download/AION-7.0.0-R_AUDIT_REPORT.md`

Conteúdo:
- Tabela principal de componentes (Seção 3, preenchida).
- Tabelas auxiliares de sub-componentes (Seções 3.1, 3.2, 3.3, 3.4, 3.5, preenchidas).
- Estado final da auditoria: `RESTORATION VERIFIED` ou `RESTORATION BLOCKED`.
- Lista de discrepâncias (se houver).
- Hashes de referência registrados (V3 e V4).

### 7.2 Relatório estruturado (machine-readable)

Caminho: `/home/z/my-project/download/rag/aion_7_0_0_r_audit_report.json`

Schema:
```json
{
  "audit_version": "7.0.0-R-1",
  "audit_timestamp": "ISO-8601",
  "auditor": "IA Curadora",
  "components": [
    {
      "component": "Corpus",
      "expected_version": "v1.3.0",
      "found_version": "v1.3.0",
      "hash_sha256": "abc123...",
      "existence": "PRESENT",
      "version_match": "MATCH",
      "integrity": "VERIFIED",
      "content_canonical": "CANONICAL",
      "final_state": "VERIFIED",
      "subcomponents_audited": 11,
      "subcomponents_verified": 11
    },
    {
      "component": "Oracle",
      "expected_version": "v3",
      "found_version": "v3",
      "hash_sha256": "def456...",
      "existence": "PRESENT",
      "version_match": "MATCH",
      "integrity": "VERIFIED",
      "content_canonical": "CANONICAL",
      "final_state": "VERIFIED",
      "subcomponents_audited": 7,
      "subcomponents_verified": 7
    }
    // ... e assim por diante
  ],
  "audit_result": "RESTORATION_VERIFIED" | "RESTORATION_BLOCKED",
  "discrepancies": [],
  "authorization_transition": "AUTHORIZED" | "BLOCKED"
}
```

## 8. Estados Possíveis Pós-Auditoria

| Estado | Condição | Ação subsequente |
|---|---|---|
| `RESTORATION VERIFIED` | Todos os componentes (incluindo sub-componentes) = `VERIFIED` | Transição autorizada para `BASELINE EXECUTION AUTHORIZED` mediante assinatura do Projetista Master. |
| `RESTORATION BLOCKED — PARTIAL` | Um ou mais componentes = `PARTIAL` (presentes mas versão/hash errados) | Re-restaurar componentes faltantes, re-executar auditoria. |
| `RESTORATION BLOCKED — ABSENT` | Um ou mais componentes = `ABSENT` | Aguardar re-anexação material dos artefatos ausentes. |
| `RESTORATION BLOCKED — CORRUPT` | Um ou mais componentes = `CORRUPT` | Re-restaurar versões íntegras. Investigar causa de corrompimento. |
| `RESTORATION BLOCKED — NON_CANONICAL` | Um ou mais componentes = `NON_CANONICAL` (íntegros mas conteúdo desviante) | Determinação do Projetista Master sobre aceitar ou rejeitar o desvio. |

## 9. Ação em Caso de Falha de Restauração

Se a auditoria retorna qualquer estado que não `RESTORATION VERIFIED`:

1. **Não executar o baseline.** Sem exceções.
2. **Reportar discrepâncias ao Projetista Master** com tabela completa e descrição específica de cada falha.
3. **Aguardar determinação** do Projetista Master sobre re-restauração ou ajuste metodológico.
4. **Preservar a falha como evento de proveniência**, com timestamp, sessão, e descrição — porque a ausência de material para execução é, ela própria, um dado sobre o estado do projeto (Regra 4: NÃO DECLARADO é um dado).

### 9.1 Não-intromissão metodológica

A auditoria 7.0.0-R **não tem autoridade** para:
- Decidir aceitar um componente em versão diferente.
- Substituir um componente por versão aproximada.
- Reconstruir um componente faltante a partir do Handoff.
- Relaxar qualquer verificação.

Essas decisões pertencem exclusivamente ao Projetista Master (Regra 5: T8).

## 10. Registro de Evento de Proveniência

A determinação do Projetista Master de que a ausência material dos artefatos deve ser preservada como evento de proveniência (não como falha experimental) é materializada da seguinte forma:

### 10.1 Evento canônico

```
EVENT_ID: AION-EV-001
TIMESTAMP: 2026-08-21T22:04:00-03:00
SESSION: web-73c75281-201c-4716-b85c-97833d25f9b3
TRACE_ID: 1a02693a36a852dd
EVENT_TYPE: MATERIAL_STATE_VERIFICATION
OBSERVED_STATE: Components declared FROZEN in AION-MVP-001 Handoff (Section 3) were not materially available in the observed execution environment (/home/z/my-project/) in this session.
EPISTEMOLOGICAL_SCOPE: This event records material unavailability in the observed session. It does NOT record that the artifacts do not exist. Existence elsewhere is not addressed by this observation.
DECLARED_ARTIFACTS_UNAVAILABLE: 8 paths (worklog.md, AION_HANDOFF.md, B2_Characterization.md, ONTOLOGY_v1.0.0.md, EVAL-002.html, CORPUS-001_v1.2.0.html, /download/rag/, /scripts/)
DECLARED_ARTIFACTS_EMPTY: 1 path (/upload/)
INTERPRETATION: [I] Continuidade nominal do projeto (Handoff declarativo) ≠ continuidade material da evidência (componentes FROZEN disponíveis no ambiente observado).
PROVENANCE_RULE_INVOKED: Regra 1 (Provenance) + Regra 7 (PER=0 ≠ confiável) + ECB principle applied to project's own infrastructure.
EPISTEMIC_ACTION: Specification consolidated as FROZEN; execution blocked pending restoration; AION-7.0.0-R audit protocol established as gate.
```

### 10.1.1 Correção epistemológica (Task 62)

O evento AION-EV-001 é classificado como **evento de estado material** — registra indisponibilidade material no ambiente de execução observado nesta sessão. **Não** é evidência de que os arquivos foram destruídos ou nunca existiram.

A formulação correta é:

> **"Os artefatos não estavam materialmente disponíveis no ambiente de execução observado na sessão."**

A formulação proibida é:

> ~~"Os artefatos não existem."~~

Esta distinção é pequena linguisticamente, mas enorme epistemologicamente. Negar existência sem observação da não-existência (que é logicamente distinta de observação de ausência) seria violar a Regra 1 (Provenance) — fazer uma afirmação não-evidenciada.

### 10.2 Local de registro

Este evento é referenciado em:
- Protocolo AION-7.0.0-spec, Seção 12 (Estado Material e Pendências).
- Este documento, Seção 10.
- `worklog.md`, Task 60 (descoberta) e Task 61 (consolidação).
- AION-EVIDENCE-LEDGER-001 (quando instanciado, como metadado de proveniência do baseline — registrando que o baseline foi produzido SOBRE componentes verificados pela auditoria 7.0.0-R).

### 10.3 Princípio

Este registro materializa o princípio auto-aplicativo do AION: o sistema deve ser capaz de demonstrar a própria regra que está tentando medir. Se o AION exige `EVIDENCE_EXISTS` e `PROVENANCE_VALID` em suas métricas, então a execução do próprio AION exige que seus componentes FROZEN tenham `EXISTENCE=PRESENT` e `INTEGRITY=VERIFIED` antes de produzir qualquer medição. Caso contrário, o AION estaria cometendo exatamente o erro categorial que ele existe para impedir.

## 11. Genealogia Documental

```
AION-6.5.0 (B2 CHARACTERIZED / CONTROLLED LIMITATION)
       │
       ▼
AION-7.0.0-spec (Protocolo + Schema do Ledger) — PRODUZIDO 21/08/2026
       │
       ▼  Determinação Projetista Master: Opção B (Specification-Only)
       │
AION-7.0.0-R (este documento — FROZEN Component Restoration Audit Protocol) — PRODUZIDO 21/08/2026
       │
       ▼  Aguardar restauração material dos componentes
       │
AION-7.0.0-R EXECUTION (auditoria material) — PENDING
       │
       ├── SE RESTORATION VERIFIED
       │   │
       │   ▼  Autorização Projetista Master
       │   │
       │   AION-7.0.0 BASELINE EXECUTION (N=100) — PENDING
       │   │
       │   ▼
       │   AION-EVIDENCE-LEDGER-001 POPULATED — PENDING
       │
       └── SE RESTORATION BLOCKED
           │
           ▼  Loop de re-restauração + re-auditoria
           │
           (volta para AION-7.0.0-R EXECUTION)
```

## 12. Status Final

| Componente | Estado |
|---|---|
| AION-7.0.0 Protocol | SPECIFICATION COMPLETE — FROZEN |
| AION-EVIDENCE-LEDGER-001 Schema | SPECIFICATION COMPLETE — FROZEN |
| AION-7.0.0-R Audit Protocol (este documento) | SPECIFICATION COMPLETE — FROZEN |
| H-ECB / H-EPISTEMIC | FROZEN |
| Intervenções | NONE (não-introduzidas, conforme determinação) |
| Execução observacional N=100 | PENDING |
| Componentes experimentais FROZEN | ABSENT DO AMBIENTE |
| Auditoria 7.0.0-R | PENDING DE RESTAURAÇÃO PRÉVIA |

**Sequência canônica:**

```
6.5.0
  ↓
7.0.0 — PROTOCOL / LEDGER (FROZEN)
  ↓
7.0.0-R — RESTORATION INTEGRITY AUDIT (PENDING)
  ↓
7.0.0 — DESCRIPTIVE BASELINE (PENDING)
  ↓
Evidence → Claim → Provenance
  ↓
Binding / ECB
  ↓
Epistemic Acceptance
```

---

*"O AION não pode ser autorizado a declarar continuidade que materialmente não consegue demonstrar. A auditoria 7.0.0-R é a materialização operacional do princípio de que nenhuma inferência — nem mesmo a inferência de que o sistema está pronto para executar — pode ser aceita sem verificação material da evidência que a sustenta."*

**Fim do Protocolo AION-7.0.0-R-spec.**
