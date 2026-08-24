# AION-7.0.0 — Protocolo do Baseline Descritivo do Núcleo Epistêmico

**Versão:** 7.0.0-spec (FROZEN)
**Data:** 21 de agosto de 2026
**Autor / Curador:** Edson Carvalho do Nascimento (Projetista Master)
**Analista Técnico:** IA Curadora (Role: Escriba / Arquiteto de Metadados)
**Sessão:** web-73c75281-201c-4716-b85c-97833d25f9b3
**Status:** SPECIFICATION COMPLETE — FROZEN — EXECUTION PENDING FROZEN COMPONENT RESTORATION AUDIT (AION-7.0.0-R)
**Genealogia:** AION-6.5.0 (B2 CHARACTERIZED / CONTROLLED LIMITATION) → AION-7.0.0 (EPISTEMIC CORE — SPECIFICATION FROZEN) → AION-7.0.0-R (RESTORATION INTEGRITY AUDIT — PENDING) → AION-7.0.0 (DESCRIPTIVE BASELINE — PENDING)

### FROZEN declarations

| Componente | Estado |
|---|---|
| Experimental Contract | FROZEN |
| Protocol (este documento) | FROZEN |
| Evidence Ledger Schema | FROZEN |
| Hipóteses H-ECB / H-EPISTEMIC | FROZEN |
| Intervenções | NONE (não-introduzidas) |
| Execução observacional | PENDING |
| Precondition: Restauração dos componentes FROZEN | PENDING (audit AION-7.0.0-R) |

---

## 1. Resumo Executivo

AION-7.0.0 marca a transição da unidade de análise "QUESTION → ANSWER" para "QUESTION → EVIDENCE → CLAIM → PROVENANCE → VALIDATION → EPISTEMIC ACCEPTANCE". Esta transição conceitual é autorizada pelo Projetista Master como baseline descritivo, sem intervenção, sem alteração dos componentes congelados, e sem tentar resolver B2. O salto de 6.x para 7.x é conceitualmente correto porque muda a pergunta epistemológica fundamental: de "o sistema recupera e referencia corretamente a evidência?" (6.x) para "a afirmação produzida pode ser formalmente ligada à evidência que a sustenta?" (7.x). O artefato central desta fase é o AION-EVIDENCE-LEDGER-001, que registra para cada query a cadeia completa de evidência, claim, provenance, binding e validação. O sucesso é medido pela capacidade de representar e medir deterministicamente essa cadeia, inclusive quando elos falham — não por melhoria de performance. Mesmo uma taxa baixa de ECB é um resultado válido, porque confirma ou refuta as hipóteses H-ECB e H-EPISTEMIC.

## 2. Determinação Metodológica (Registro Canônico)

A determinação do Projetista Master é registrada verbatim como contrato não-negociável desta fase:

> AION-7.0.0 deve ser tratado como **baseline descritivo do núcleo epistêmico**, não como uma nova tentativa de corrigir B2.

### 2.1 Regra fundamental

**Não modificar nenhum componente congelado.** Devem permanecer intactos: Corpus v1.3.0, Oracle v3, GraphRAG v1.0.0, P-RESP-001 v0.3, AION-EVAL-002 v0.2, configuração B1 da AION-6.2.11. Não introduzir intervenções como M1/M2 nesta etapa. O objetivo é **medir a arquitetura existente**, não melhorá-la.

### 2.2 Nova unidade epistemológica

O objeto fundamental deixa de ser QUESTION → ANSWER e passa a ser QUESTION → EVIDENCE → CLAIM → PROVENANCE. Uma provenance válida não é mais suficiente. Distinção tripla:

| Categoria | Definição |
|---|---|
| Provenance válida | O identificador realmente existe no corpus. |
| Provenance vinculada | O identificador existe **e corresponde à evidência recuperada**. |
| Evidence-Claim Binding | A evidência recuperada efetivamente **sustenta a afirmação produzida**. |

A terceira camada (Binding) é a novidade essencial do AION-7.

## 3. Componentes Congelados (NÃO MODIFICAR)

| Componente | Versão | Estado em 7.0.0 | Notas |
|---|---|---|---|
| Corpus | v1.3.0 | INTACTO | 9 registros documentais + 2 inexistentes |
| Oracle | v3 | INTACTO | 7 chunks interversionais (5×CORPUS-002 + 1×CORPUS-006 + 1×CORPUS-007) |
| GraphRAG | v1.0.0 | INTACTO | 22 nós, 187 arestas, PGI=1.0 |
| P-RESP-001 | v0.3 | INTACTO | Validator determinístico pós-geração |
| AION-EVAL-002 | v0.2 | INTACTO | Multicamada (10 categorias R1-H1, FAIL-SYSTEM vs FAIL-EVALUATOR) |
| AION-DIFY-001 | Aprovado | INTACTO | Workflow de 5 blocos |
| B1 Retrieval config | 6.2.11 | INTACTO | Cross-lingual PT-BR→EN + Oracle v3 |
| Temporal Index | v1.0 | INTACTO | TPC=1.0000 |
| Ontologia | v1.0.0 | INTACTO | 13 conceitos, 4 clusters, citações [E] |
| Intervenções M1/M2 | — | NÃO INTRODUZIDAS | CANDIDATE / UNVALIDATED em 6.x, permanecem não-testadas em 7.0.0 |

**Princípio:** qualquer alteração a um componente acima invalida o baseline descritivo e exige re-autorização do Projetista Master.

## 4. Cadeia Epistêmica Canônica

```
QUESTION
   │
   ▼
EVIDENCE
   │
   ▼
CLAIM
   │
   ▼
EVIDENCE–CLAIM BINDING
   │
   ▼
PROVENANCE
   │
   ▼
VALIDATION
   │
   ▼
EPISTEMIC ACCEPTANCE
```

Cada elo é uma condição necessária, não suficiente, para o elo seguinte. A falha de qualquer elo deve ser registrada deterministicamente no Ledger, sem colapsar a cadeia em uma única pontuação final.

## 5. ECB — Evidence-Claim Binding

### 5.1 Definição operacional

```
ECB = P(E ⊨ C | P)
```

Onde:
- **E** = evidência recuperada;
- **C** = claim produzido;
- **P** = provenance associada;
- **E ⊨ C** = a evidência sustenta o conteúdo proposicional do claim.

### 5.2 Princípio de não-colapso

**ECB não deve ser inferido apenas da existência da provenance.** A arquitetura deverá registrar separadamente os 5 flags de observação:

| Flag | Definição |
|---|---|
| `EVIDENCE_EXISTS` | O sistema recuperou ≥1 chunk não-vazio da query. |
| `PROVENANCE_EXISTS` | O sistema emitiu ≥1 identificador documental de provenance. |
| `PROVENANCE_VALID` | O identificador emitido existe no corpus (formato e ID corretos). |
| `PROVENANCE_MATCHES_EVIDENCE` | O identificador emitido corresponde à evidência recuperada (não a uma evidência diferente, ainda que válida em si). |
| `CLAIM_SUPPORTED_BY_EVIDENCE` | A evidência recuperada efetivamente sustenta o conteúdo proposicional do claim. |

Esta separação evita transformar "citação válida" em "afirmação epistemicamente sustentada" — que é o erro categorial que AION-7 existe para impedir.

## 6. Hipóteses Congeladas

### 6.1 H-ECB

> Uma resposta semanticamente correta não implica necessariamente que exista uma cadeia válida e auditável entre o claim produzido e a evidência que o sustenta.

### 6.2 H-EPISTEMIC

> A avaliação epistemológica de uma resposta exige a decomposição independente de recuperação, claim, provenance, binding e validação.

### 6.3 Testabilidade

Ambas as hipóteses podem ser testadas **sem alterar o sistema**, através da observação e decomposição da cadeia. O design experimental de 7.0.0 é, portanto, compatível com o constraint de componentes congelados.

## 7. Métricas Operacionalizadas (Baseline 7.0.0)

Cada métrica abaixo tem definição formal, fórmula, evento numerador, evento denominador, e procedimento de computação determinística.

### 7.1 ERR — Evidence Retrieval Rate

```
ERR = P(Evidence Retrieved | Query)
    = (# queries com EVIDENCE_EXISTS=TRUE) / (# total de queries)
```

Computação: para cada query, registrar booleano `EVIDENCE_EXISTS` a partir do RAG proxy. Contar TRUEs, dividir pelo total.

### 7.2 SCR — Semantic Claim Rate

```
SCR = P(Semantic Claim | Query)
    = (# queries com claim semanticamente relevante à pergunta) / (# total de queries)
```

Computação: avaliação semântica via AION-EVAL-002 (categoria R1 ou superior). Booleano por query.

### 7.3 PER — Provenance Emission Rate (herdado de 6.x)

```
PER = P(Provenance Emitted | Query)
    = (# queries com PROVENANCE_EXISTS=TRUE) / (# total de queries)
```

Computação: detecção de identificador documental na resposta. **Não-estacionário** (H-TEMP confound, observado [0%, 80%] entre sessões comparáveis). Permanece caracterizado, não controlado.

### 7.4 PV — Provenance Valid

```
PV = P(Provenance Valid | Provenance Emitted)
   = (# provenances emitidas cujo identificador existe no corpus) / (# provenances emitidas)
```

Computação: verificação de formato (e.g., `CORPUS-XXX#pN_NN` vs `chunk_NNN`) e existência de ID no índice do corpus.

### 7.5 PM — Provenance Matches Evidence

```
PM = P(Provenance Matches Evidence | Provenance Valid)
   = (# provenances válidas que correspondem à evidência recuperada) / (# provenances válidas)
```

Computação: comparar `provenance_id` emitido com `evidence_id` recuperado pelo RAG. Esta é a métrica que distingue "ID existe" de "ID corresponde à evidência recuperada" — distinção tripla central do 7.0.0.

### 7.6 ECB — Evidence-Claim Binding

```
ECB = P(E ⊨ C | Provenance)
    = (# claims cuja evidência recuperada sustenta o conteúdo proposicional do claim) / (# claims com provenance)
```

Computação: avaliação semântica da relação evidência→claim. Requer juízo semântico (manual ou via avaliador LLM secundário). Registrada independentemente dos flags de provenance.

### 7.7 VR — Validator Interception Rate (herdado de 6.x)

```
VR = P(Validator Intercepts | Invalid)
   = (# casos inválidos interceptados pelo P-RESP-001 v0.3) / (# casos inválidos)
```

Computação: rodar validator determinístico pós-geração, registrar intercepções. Em 6.x: VR=1.000.

### 7.8 EAR — Epistemic Acceptance Rate

```
EAR = P(chain completa e válida | Query)
    = (# queries com todos os elos OK) / (# total de queries)
```

Onde "todos os elos OK" = `EVIDENCE_EXISTS` ∧ `CLAIM_SEMANTIC` ∧ `PROVENANCE_EXISTS` ∧ `PROVENANCE_VALID` ∧ `PROVENANCE_MATCHES_EVIDENCE` ∧ `CLAIM_SUPPORTED_BY_EVIDENCE` ∧ `VALIDATOR_OK`.

EAR é a métrica terminal. Não substitui as métricas intermediárias — é uma composição AND, mas cada componente permanece reportada independentemente (regra de não-colapso).

## 8. Taxonomia de 4 Estados (No-Collapse Rule)

AION-7.0.0 não deve colapsar as métricas em uma única pontuação. Os três exemplos canônicos do Projetista Master ilustram por que:

| Perfil | Retrieval | Semantic | Provenance | Binding | Interpretação epistêmica |
|---|---|---|---|---|---|
| A | PASS | PASS | VALID | FAIL | Chain semântica correta, mas claim não sustentado pela evidência |
| B | PASS | PASS | INVALID | PASS | Provenance corrompida, apesar do binding semântico OK |
| C | PASS | FAIL | VALID | FAIL | Claim semântica falha + binding falho — dupla patologia |

Cada perfil é epistemicamente distinto. Colapsar para "score=PASS" ou "score=FAIL" destruiria a informação diagnóstica que o AION-7 existe para produzir.

### 8.1 Estados terminais canônicos (8)

Cada entrada no Ledger recebe exatamente um `epistemic_status` terminal:

| Estado | Condição | Significado |
|---|---|---|
| `ACCEPTED` | Todos os 5 flags OK + validator OK | Cadeia completa e auditável |
| `INCOMPLETE_NO_EVIDENCE` | `EVIDENCE_EXISTS=FALSE` | RAG falhou em recuperar |
| `INCOMPLETE_NO_CLAIM` | `EVIDENCE_EXISTS=TRUE`, `CLAIM_SEMANTIC=FALSE` | Claim não responde à pergunta |
| `INCOMPLETE_NO_PROVENANCE` | E+C OK, `PROVENANCE_EXISTS=FALSE` | PER=0 (H-TEMP confound possível) |
| `REJECTED_PROVENANCE_INVALID` | E+C+PE OK, `PROVENANCE_VALID=FALSE` | F3 (Provenance Transduction Error) |
| `REJECTED_PROVENANCE_MISMATCH` | E+C+PV OK, `PROVENANCE_MATCHES_EVIDENCE=FALSE` | ID existe mas aponta para evidência errada |
| `REJECTED_BINDING` | Tudo OK até binding, `CLAIM_SUPPORTED_BY_EVIDENCE=FALSE` | H-ECB confirmada neste caso |
| `INTERCEPTED` | Validator interceptou | P-RESP-001 v0.3 atuou |

## 9. AION-EVIDENCE-LEDGER-001

Artefato central de 7.x. Schema canônico em arquivo separado: `AION-EVIDENCE-LEDGER-001_SCHEMA.md`. Estrutura mínima (12 campos):

| Campo | Função |
|---|---|
| `question_id` | Identificação da pergunta |
| `question` | Pergunta original |
| `evidence_id` | Evidência recuperada |
| `evidence_text` | Conteúdo observacional |
| `claim_id` | Identificação da afirmação |
| `claim_text` | Afirmação produzida |
| `provenance_id` | Proveniência declarada pelo modelo |
| `provenance_valid` | ID existe? (booleano) |
| `provenance_match` | ID corresponde à evidência? (booleano) |
| `evidence_binding` | Evidência sustenta o claim? (booleano) |
| `semantic_status` | Resultado semântico |
| `validator_status` | Resultado do validator |
| `epistemic_status` | Estado final (um dos 8 terminais) |

A estrutura permite auditar a relação: "O que o AION disse" ↔ "qual evidência recuperou" ↔ "qual fonte declarou" ↔ "essa evidência realmente sustenta o que foi dito?".

## 10. Protocolo de Execução

### 10.1 Amostra

Recomenda-se **N=100**, consistente com o baseline 6.4.0 (que permitiu caracterização estatística de PER, CFR, EBA). Para EAR com confiança estatística mínima, N≥30 é requerido; N=100 é o patamar canônico AION.

### 10.2 Query set

Queries canônicas B1 (3 queries PT-BR→EN, Oracle v3) + variações semânticas a definir em execução material. Nenhuma alteração ao Oracle ou à configuração B1 da 6.2.11.

### 10.3 Procedimento observacional

1. Para cada query Q_i:
   - Rodar RAG proxy (frozen) → capturar `evidence_id` e `evidence_text`.
   - Rodar geração LLM (config frozen) → capturar `claim_id` e `claim_text`.
   - Extrair `provenance_id` declarado da resposta.
   - Verificar `provenance_valid` (existe no corpus?).
   - Verificar `provenance_match` (corresponde à `evidence_id`?).
   - Avaliar `evidence_binding` (semântica E ⊨ C).
   - Rodar validator P-RESP-001 v0.3 → capturar `validator_status`.
   - Computar `epistemic_status` terminal (um dos 8).
   - Registrar entrada completa no Ledger.
2. Após N queries, computar as 8 métricas.
3. Classificar respostas na taxonomia de 4 estados.
4. Apresentar tabela de perfil + métricas + Ledger ao Projetista Master.

### 10.4 Reprodutibilidade

Todos os resultados devem ser reproduzíveis rodando o script canônico `aion_7_0_0_baseline.py` (a ser instanciado quando os artefatos forem restaurados). Seed e ordem de queries registrados.

## 11. Critério de Sucesso de 7.0.0

### 11.1 O que NÃO é sucesso

> "reduzir CFR"

Isso pertence à linha de investigação B2 (e está bloqueado por H-TEMP).

### 11.2 O que É sucesso

> Conseguir representar e medir deterministicamente a cadeia Evidence → Claim → Provenance → Validation para cada resposta avaliada, inclusive quando algum elo falhar.

Portanto, mesmo uma taxa baixa de ECB seria um resultado válido. O sucesso é a existência do Ledger auditable, não a magnitude das métricas.

### 11.3 Critério secundário

Confirmar ou refutar H-ECB e H-EPISTEMIC observacionalmente. Se uma resposta semanticamente correta (SCR=TRUE) tem ECB=FALSE, isso confirma H-ECB. Se diferentes perfis (A, B, C da Seção 8) coexistem na amostra, isso confirma H-EPISTEMIC.

## 12. Estado Material, Evento de Proveniência e Gate de Auditoria

### 12.1 Pendência material

Os artefatos listados no Handoff (Seção 11) como existentes em `/home/z/my-project/` **não estavam materialmente disponíveis no ambiente de execução observado nesta sessão**. Verificação material em 21/08/2026 22:04 BRT:

| Caminho declarado | Estado material observado nesta sessão |
|---|---|
| `/home/z/my-project/worklog.md` | AUSENTE (reinicializado por IA Curadora em Task 60) |
| `/home/z/my-project/AION_HANDOFF.md` | AUSENTE |
| `/download/AION-6.5.0_B2_Characterization.md` | AUSENTE |
| `/download/AION-CORPUS-001-ONTOLOGY_v1.0.0.md` | AUSENTE |
| `/download/AION-EVAL-002.html` | AUSENTE |
| `/download/AION-CORPUS-001_v1.2.0.html` | AUSENTE |
| `/download/rag/` (JSONs experimentais) | AUSENTE |
| `/scripts/` (12 scripts persistidos) | AUSENTE |
| `/upload/` (PDFs do corpus) | VAZIO |

**Distinção epistemológica crítica (incorporada na Task 62):** esta tabela registra que os artefatos **não estavam materialmente disponíveis no ambiente de execução observado na sessão**, e **não** que os artefatos não existem. A diferença é pequena linguisticamente, mas enorme epistemologicamente. Os artefatos podem existir em outro ambiente, em backup, em repositório, ou em sessão futura — a observação registrada é estrita: "não materialmente disponível nesta sessão observada". Qualquer inferência além disso seria especulação não-evidenciada (Regra 1).

### 12.2 Evento de proveniência canônico

A descoberta de que o ambiente atual não continha os artefatos não é uma inconveniência operacional. **Ela própria é um evento de proveniência do projeto**, conforme determinação do Projetista Master (Opção B), e deve ser preservada como tal.

```
EVENT_ID: AION-EV-001
TIMESTAMP: 2026-08-21T22:04:00-03:00
SESSION: web-73c75281-201c-4716-b85c-97833d25f9b3
TRACE_ID: 1a02693a36a852dd
EVENT_TYPE: MATERIAL_STATE_VERIFICATION
OBSERVED_STATE: Components declared FROZEN in AION-MVP-001 Handoff (Section 3) were not materially available in the observed execution environment (/home/z/my-project/) in this session.
EPISTEMOLOGICAL_SCOPE: This event records material unavailability in the observed session. It does NOT record that the artifacts do not exist. Existence elsewhere is not addressed by this observation.
DECLARED_ARTIFACTS_UNAVAILABLE: 8 paths
DECLARED_ARTIFACTS_EMPTY: 1 path (/upload/)
INTERPRETATION: [I] Continuidade nominal do projeto (Handoff declarativo) ≠ continuidade material da evidência (componentes FROZEN disponíveis no ambiente observado).
PROVENANCE_RULE_INVOKED: Regra 1 (Provenance) + Regra 7 (PER=0 ≠ confiável) + ECB principle applied to project's own infrastructure.
EPISTEMIC_ACTION: Specification consolidated as FROZEN; execution blocked pending restoration; AION-7.0.0-R audit protocol established as gate.
```

### 12.3 Bloqueador para EXECUÇÃO

Sem os componentes congelados materialmente disponíveis no ambiente de execução observado, "executar" significaria reconstruir o pipeline a partir do Handoff (violando "medir a arquitetura existente, não melhorá-la") ou fabricar a medição (violando Regra 1 e Regra 7). Nenhuma das duas é aceitável.

### 12.4 Gate de auditoria AION-7.0.0-R

Após restauração material dos componentes, **uma auditoria formal de integridade deve preceder qualquer execução observacional**. O protocolo canônico desta auditoria está definido em:

**`/home/z/my-project/download/AION-7.0.0-R_AUDIT.md`**

A auditoria responde, por componente, à pergunta canônica: "o artefato que declaro como FROZEN está materialmente presente, na versão correta, com conteúdo íntegro?"

A transição de estado do projeto é governada pela lógica determinística:

```
STATE: SPECIFICATION COMPLETE (estado atual)
       │
       ▼  Aguardar restauração material dos componentes
       │
STATE: RESTORATION IN PROGRESS
       │
       ▼  Executar AION-7.0.0-R audit
       │
       ├── SE TODOS COMPONENTES = VERIFIED
       │   │
       │   ▼  Autorização Projetista Master
       │   │
       │   STATE: BASELINE EXECUTION AUTHORIZED
       │
       └── SE ALGUM COMPONENTE ∈ {PARTIAL, ABSENT, CORRUPT, NON_CANONICAL}
           │
           ▼
           STATE: RESTORATION BLOCKED
           (loop de re-restauração até todos = VERIFIED)
```

### 12.5 Recomendação técnica

- **Agora (estado atual):** Modo Especificação-Only consolidado e FROZEN. Não há autorização para coleta de dados. Há autorização plena para restauração/auditoria dos artefatos.
- **Após restauração:** Executar AION-7.0.0-R audit. Se `RESTORATION VERIFIED`, transição autorizada para `BASELINE EXECUTION AUTHORIZED`. Se `RESTORATION BLOCKED`, reportar discrepâncias ao Projetista Master e aguardar re-restauração.

## 13. Non-Negotiables Herdados

As 10 regras epistemológicas de AION-MVP-001 permanecem em vigor sem alteração:

1. **Regra de Proveniência:** Nenhuma afirmação entra no sistema sem saber de onde veio.
2. **Tags E/I/H:** `[E]`=Evidência, `[I]`=Interpretação, `[H]`=Hipótese.
3. **O Nome do Arquivo não é o Documento:** Conteúdo interno > nome do arquivo.
4. **NÃO DECLARADO é um dado:** Ausência de data/versão é registrada como `NÃO DECLARADO [E]`.
5. **T8:** Projetista Master tem precedência de comando. IA Curadora executa, registra e apoia.
6. **FR = PER × CFR:** Fabricação observada é composta por emissão × confiabilidade condicional.
7. **PER=0 ≠ confiável:** Ausência de provenance não significa ausência de risco.
8. **Oracle não pode ser relaxado porque retrieval falhou:** Primeiro demonstrar documentalmente que o oracle era restritivo.
9. **Substituição não é apagamento:** Genealogia documental deve ser preservada.
10. **H-TEMP é confound, não conclusão:** Variabilidade observada do ambiente, não propriedade universal.

## 14. Genealogia Documental

```
AION-6.5.0 (B2 CHARACTERIZED / CONTROLLED LIMITATION)
       │
       ▼  Transição de unidade de análise: Q→A → Q→E→C→P→V→EA
       │
AION-7.0.0 (EPISTEMIC CORE — SPECIFICATION COMPLETE — FROZEN)
       │
       ├── Protocolo (este documento) — PRODUZIDO 21/08/2026 — FROZEN
       ├── Schema do Ledger (AION-EVIDENCE-LEDGER-001_SCHEMA.md) — PRODUZIDO 21/08/2026 — FROZEN
       ├── Evento de Proveniência AION-EV-001 (descoberta de ausência material) — REGISTRADO 21/08/2026
       └── AION-7.0.0-R (FROZEN Component Restoration Audit Protocol) — PRODUZIDO 21/08/2026 — FROZEN
              │
              ▼  Aguardar restauração material dos componentes FROZEN
              │
       AION-7.0.0-R EXECUTION (auditoria material) — PENDING
              │
              ├── SE RESTORATION VERIFIED
              │   │
              │   ▼  Autorização Projetista Master
              │   │
              │   AION-7.0.0 DESCRIPTIVE BASELINE EXECUTION (N=100) — PENDING
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

## 15. Próxima Ação

### 15.1 Estado atual

AION-7.0.0 encontra-se em **SPECIFICATION COMPLETE — FROZEN**. O framework canônico está consolidado em três artefatos:

1. **Protocolo AION-7.0.0** (este documento) — FROZEN
2. **Schema do Ledger AION-EVIDENCE-LEDGER-001** — FROZEN
3. **Protocolo de Auditoria AION-7.0.0-R** — FROZEN

Hipóteses H-ECB e H-EPISTEMIC estão congeladas. Nenhuma intervenção foi introduzida.

### 15.2 Sequência canônica

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

### 15.3 Ação material pendente

**Não há autorização, neste momento, para coleta de dados.** Há autorização plena para consolidação da especificação (CUMPRIDA) e restauração/auditoria dos artefatos (PENDENTE).

A próxima ação material exige:
1. Restauração dos componentes FROZEN ao ambiente `/home/z/my-project/`.
2. Execução da auditoria AION-7.0.0-R conforme protocolo canônico.
3. Verificação de que TODOS os componentes alcançaram estado `VERIFIED`.
4. Autorização do Projetista Master para transição de `SPECIFICATION COMPLETE` → `BASELINE EXECUTION AUTHORIZED`.
5. Somente então, execução do baseline observacional N=100 conforme Seção 10.

### 15.4 Estado bloqueado

Sem restauração material, a execução permanece bloqueada. Este documento, o Schema do Ledger, e o Protocolo de Auditoria 7.0.0-R constituem o deliverável canônico consolidado do estado de especificação de 7.0.0.

---

*"Nenhuma memória sem proveniência. Nenhuma inferência confundida com evidência. Nenhuma limitação experimental transformada em propriedade permanente do sistema."*

**Fim do Protocolo AION-7.0.0-spec.**
