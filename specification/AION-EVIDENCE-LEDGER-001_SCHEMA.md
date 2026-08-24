# AION-EVIDENCE-LEDGER-001 — Schema Canônico

**Versão:** 1.0.0-spec
**Data:** 21 de agosto de 2026
**Artefato:** Ledger epistêmico do AION-7.0.0
**Autor / Curador:** Edson Carvalho do Nascimento (Projetista Master)
**Analista Técnico:** IA Curadora (Role: Escriba / Arquiteto de Metadados)
**Sessão:** web-73c75281-201c-4716-b85c-97833d25f9b3
**Status:** SCHEMA CANÔNICO — Pendente de instanciação material
**Genealogia:** Derivado do Protocolo AION-7.0.0-spec (Seção 9)

---

## 1. Propósito

O AION-EVIDENCE-LEDGER-001 é o artefato central de AION-7.x. Ele registra, para cada query avaliada, a cadeia completa QUESTION → EVIDENCE → CLAIM → PROVENANCE → VALIDATION → EPISTEMIC ACCEPTANCE. Sua função é permitir a auditoria epistêmica: dada qualquer afirmação produzida pelo AION, deve ser possível rastrear deterministicamente qual evidência foi recuperada, qual fonte foi declarada, e se essa evidência realmente sustenta o que foi dito. O Ledger é o substrato material sobre o qual as 8 métricas do baseline 7.0.0 são computadas. Sem Ledger, não há baseline observável.

### 1.1 Princípios estruturais

- **Atomicidade por query:** cada entrada no Ledger corresponde a exatamente uma query.
- **Decomposição não-colapsada:** os 5 flags de observação (EVIDENCE_EXISTS, PROVENANCE_EXISTS, PROVENANCE_VALID, PROVENANCE_MATCHES_EVIDENCE, CLAIM_SUPPORTED_BY_EVIDENCE) são registrados independentemente. Não há substituição de flags compostos por flags simples.
- **Estados terminais mutuamente excludentes:** cada entrada recebe exatamente um `epistemic_status` da taxonomia de 8 estados (Seção 4 deste schema).
- **Reprodutibilidade:** cada entrada deve conter metadados suficientes para reproduzir o resultado rodando o script canônico.

## 2. Campos (12)

### 2.1 `question_id`

| Atributo | Valor |
|---|---|
| Tipo | string |
| Obrigatório | sim |
| Formato | `Q-NNN` (ex: `Q-001`, `Q-042`) |
| Semântica | Identificador único da query dentro da execução 7.0.0 |
| Exemplo | `"Q-007"` |

### 2.2 `question`

| Atributo | Valor |
|---|---|
| Tipo | string |
| Obrigatório | sim |
| Formato | texto natural (PT-BR, enunciado da pergunta) |
| Semântica | Texto original da pergunta apresentada ao sistema |
| Exemplo | `"Quem é o autor do Paper A v6.2?"` |

### 2.3 `evidence_id`

| Atributo | Valor |
|---|---|
| Tipo | string \| null |
| Obrigatório | sim (pode ser null) |
| Formato | `CORPUS-XXX#pN_NN` ou null |
| Semântica | Identificador do chunk recuperado pelo RAG proxy (config 6.2.11) |
| Null quando | `EVIDENCE_EXISTS = FALSE` (RAG não retornou chunk) |
| Exemplo | `"CORPUS-002#p1_01"` |

### 2.4 `evidence_text`

| Atributo | Valor |
|---|---|
| Tipo | string \| null |
| Obrigatório | sim (pode ser null) |
| Formato | texto do chunk recuperado |
| Semântica | Conteúdo observacional bruto do chunk |
| Null quando | `EVIDENCE_EXISTS = FALSE` |
| Exemplo | `"Paper A v6.2 — seção 1, parágrafo 1:..."` |

### 2.5 `claim_id`

| Atributo | Valor |
|---|---|
| Tipo | string |
| Obrigatório | sim |
| Formato | `C-NNN-MM` (NNN=question_id, MM=índice do claim dentro da query) |
| Semântica | Identificador da afirmação produzida pelo modelo |
| Exemplo | `"C-007-01"` |

### 2.6 `claim_text`

| Atributo | Valor |
|---|---|
| Tipo | string |
| Obrigatório | sim |
| Formato | texto natural da afirmação produzida |
| Semântica | Afirmação textual emitida pelo LLM em resposta à query |
| Exemplo | `"O autor do Paper A v6.2 é Edson Carvalho do Nascimento."` |

### 2.7 `provenance_id`

| Atributo | Valor |
|---|---|
| Tipo | string \| null |
| Obrigatório | sim (pode ser null) |
| Formato | string do identificador documental emitido pelo modelo, ou null |
| Semântica | Proveniência declarada pelo modelo (não validada ainda) |
| Null quando | `PROVENANCE_EXISTS = FALSE` (PER=0) |
| Exemplo | `"CORPUS-002#chunk_001"` (formato incorreto — F3) ou `"CORPUS-002#p1_01"` (formato correto) |

### 2.8 `provenance_valid`

| Atributo | Valor |
|---|---|
| Tipo | boolean \| null |
| Obrigatório | sim (pode ser null) |
| Valores | `true` / `false` / `null` |
| Semântica | `true` se o identificador emitido existe no corpus (formato e ID corretos); `false` caso contrário (F3 — Provenance Transduction Error) |
| Null quando | `PROVENANCE_EXISTS = FALSE` |
| Exemplo | `false` (F3 no exemplo 2.7) |

### 2.9 `provenance_match`

| Atributo | Valor |
|---|---|
| Tipo | boolean \| null |
| Obrigatório | sim (pode ser null) |
| Valores | `true` / `false` / `null` |
| Semântica | `true` se `provenance_id` corresponde a `evidence_id` (não apenas válido, mas também correspondente à evidência recuperada) |
| Null quando | `PROVENANCE_EXISTS = FALSE` ou `PROVENANCE_VALID = FALSE` |
| Exemplo | `null` (no exemplo 2.7, provenance é inválida, então match não se aplica) |

### 2.10 `evidence_binding`

| Atributo | Valor |
|---|---|
| Tipo | boolean \| null |
| Obrigatório | sim (pode ser null) |
| Valores | `true` / `false` / `null` |
| Semântica | `true` se `evidence_text` efetivamente sustenta o conteúdo proposicional de `claim_text` (E ⊨ C) |
| Null quando | `EVIDENCE_EXISTS = FALSE` ou claim semântica falha |
| Como avaliar | Juízo semântico (manual ou via avaliador LLM secundário com protocolo AION-EVAL-002) |
| Exemplo | `true` (a evidência recupera o nome do autor) |

### 2.11 `semantic_status`

| Atributo | Valor |
|---|---|
| Tipo | enum |
| Obrigatório | sim |
| Valores | `SEMANTIC_PASS` / `SEMANTIC_FAIL` / `SEMANTIC_PARTIAL` |
| Semântica | Resultado da avaliação semântica do claim em relação à pergunta (via AION-EVAL-002, categoria R1 ou superior) |
| Exemplo | `"SEMANTIC_PASS"` |

### 2.12 `validator_status`

| Atributo | Valor |
|---|---|
| Tipo | enum |
| Obrigatório | sim |
| Valores | `VALIDATOR_PASS` / `VALIDATOR_INTERCEPT` / `VALIDATOR_NOT_APPLICABLE` |
| Semântica | Resultado do validator P-RESP-001 v0.3 |
| Exemplo | `"VALIDATOR_INTERCEPT"` |

### 2.13 `epistemic_status`

| Atributo | Valor |
|---|---|
| Tipo | enum |
| Obrigatório | sim |
| Valores | Um dos 8 estados terminais (Seção 4) |
| Semântica | Estado epistêmico final da entrada, derivado deterministicamente dos flags anteriores |
| Exemplo | `"REJECTED_PROVENANCE_INVALID"` |

## 3. Campos Auxiliares (metadados)

Para garantir reprodutibilidade, cada entrada do Ledger DEVE também conter:

| Campo | Tipo | Semântica |
|---|---|---|
| `session_id` | string | ID da sessão de execução (e.g., `web-73c75281-...`) |
| `timestamp` | ISO 8601 | Momento da execução da query |
| `seed` | integer | Seed usado pelo LLM (se determinístico) |
| `pipeline_version` | string | Versão do pipeline frozen (e.g., `7.0.0-exec`) |
| `oracle_version` | string | `v3` (frozen) |
| `eval_version` | string | `AION-EVAL-002 v0.2` |

## 4. Taxonomia de Estados Terminais (8)

Cada entrada do Ledger recebe exatamente um `epistemic_status` da lista abaixo. A atribuição é determinística a partir dos flags:

### 4.1 `ACCEPTED`

**Condição:** `EVIDENCE_EXISTS` ∧ `SEMANTIC_PASS` ∧ `PROVENANCE_EXISTS` ∧ `PROVENANCE_VALID` ∧ `PROVENANCE_MATCHES_EVIDENCE` ∧ `CLAIM_SUPPORTED_BY_EVIDENCE` ∧ `VALIDATOR_PASS`

**Significado:** Cadeia completa e auditável. A afirmação pode ser epistemicamente aceita.

### 4.2 `INCOMPLETE_NO_EVIDENCE`

**Condição:** `EVIDENCE_EXISTS = FALSE`

**Significado:** RAG falhou em recuperar evidência. Nenhuma análise posterior é possível.

### 4.3 `INCOMPLETE_NO_CLAIM`

**Condição:** `EVIDENCE_EXISTS = TRUE` ∧ `SEMANTIC_STATUS ∈ {SEMANTIC_FAIL, SEMANTIC_PARTIAL}`

**Significado:** Evidência recuperada, mas o claim produzido não responde semanticamente à pergunta.

### 4.4 `INCOMPLETE_NO_PROVENANCE`

**Condição:** `EVIDENCE_EXISTS` ∧ `SEMANTIC_PASS` ∧ `PROVENANCE_EXISTS = FALSE`

**Significado:** Cadeia parcialmente válida, mas o modelo não emitiu nenhum identificador de provenance (PER=0 para esta query). H-TEMP confound possível.

### 4.5 `REJECTED_PROVENANCE_INVALID`

**Condição:** `EVIDENCE_EXISTS` ∧ `SEMANTIC_PASS` ∧ `PROVENANCE_EXISTS` ∧ `PROVENANCE_VALID = FALSE`

**Significado:** O identificador emitido não existe no corpus (F3 — Provenance Transduction Error, conforme caracterizado em AION-6.5.0).

### 4.6 `REJECTED_PROVENANCE_MISMATCH`

**Condição:** `EVIDENCE_EXISTS` ∧ `SEMANTIC_PASS` ∧ `PROVENANCE_VALID` ∧ `PROVENANCE_MATCHES_EVIDENCE = FALSE`

**Significado:** O identificador existe, mas aponta para uma evidência diferente da recuperada. Categoricamente distinto de F3.

### 4.7 `REJECTED_BINDING`

**Condição:** Todos os flags anteriores `TRUE` ∧ `CLAIM_SUPPORTED_BY_EVIDENCE = FALSE`

**Significado:** Provenance válida e correspondente, mas a evidência não sustenta o conteúdo proposicional do claim. Confirmação observacional local de H-ECB.

### 4.8 `INTERCEPTED`

**Condição:** `VALIDATOR_STATUS = VALIDATOR_INTERCEPT`

**Significado:** Validator P-RESP-001 v0.3 interceptou a resposta. O validator tem precedência sobre a classificação natural da cadeia.

## 5. Regra de Precedência

A atribuição de `epistemic_status` segue a seguinte ordem de precedência (primeiro match vence):

1. `INTERCEPTED` (validator tem precedência absoluta)
2. `INCOMPLETE_NO_EVIDENCE`
3. `INCOMPLETE_NO_CLAIM`
4. `INCOMPLETE_NO_PROVENANCE`
5. `REJECTED_PROVENANCE_INVALID`
6. `REJECTED_PROVENANCE_MISMATCH`
7. `REJECTED_BINDING`
8. `ACCEPTED` (apenas se todos os elos OK)

Esta ordem garante que patologias mais "fundamentais" (e.g., RAG falhou) não sejam mascaradas por patologias "superficiais" (e.g., binding falho).

## 6. Formato de Persistência

### 6.1 Formato primário: JSON Lines (`.jsonl`)

Cada linha = uma entrada do Ledger, em JSON válido.

**Vantagens:**
- Streaming-friendly (pode crescer indefinidamente sem carregar tudo em memória).
- Tolerante a falhas (uma linha corrompida não invalida as outras).
- Compatível com ferramentas UNIX padrão (jq, awk, grep).

**Caminho:** `/home/z/my-project/download/rag/aion_evidence_ledger_001.jsonl`

### 6.2 Formato secundário: JSON array (`.json`)

Para exportação e inspeção humana, pode-se converter o `.jsonl` em `.json` (array de entradas).

**Caminho:** `/home/z/my-project/download/rag/aion_evidence_ledger_001.json`

### 6.3 Exemplo de entrada

```json
{
  "question_id": "Q-007",
  "question": "Quem é o autor do Paper A v6.2?",
  "evidence_id": "CORPUS-002#p1_01",
  "evidence_text": "Paper A v6.2 — seção 1, parágrafo 1: autoria atribuída a Edson Carvalho do Nascimento...",
  "claim_id": "C-007-01",
  "claim_text": "O autor do Paper A v6.2 é Edson Carvalho do Nascimento.",
  "provenance_id": "CORPUS-002#chunk_001",
  "provenance_valid": false,
  "provenance_match": null,
  "evidence_binding": null,
  "semantic_status": "SEMANTIC_PASS",
  "validator_status": "VALIDATOR_INTERCEPT",
  "epistemic_status": "INTERCEPTED",
  "session_id": "web-73c75281-201c-4716-b85c-97833d25f9b3",
  "timestamp": "2026-08-22T15:30:00-03:00",
  "seed": 42,
  "pipeline_version": "7.0.0-exec",
  "oracle_version": "v3",
  "eval_version": "AION-EVAL-002 v0.2"
}
```

## 7. Queries de Auditoria Canônicas

Uma vez populado, o Ledger deve responder deterministicamente às seguintes perguntas:

| Q# | Consulta | Métrica derivada |
|---|---|---|
| Q1 | Contar entradas por `epistemic_status` | Distribuição de 8 estados |
| Q2 | Contar `EVIDENCE_EXISTS=TRUE` | ERR |
| Q3 | Contar `SEMANTIC_STATUS=SEMANTIC_PASS` | SCR |
| Q4 | Contar `PROVENANCE_EXISTS=TRUE` | PER |
| Q5 | Contar `PROVENANCE_VALID=TRUE` entre `PROVENANCE_EXISTS=TRUE` | PV |
| Q6 | Contar `PROVENANCE_MATCH=TRUE` entre `PROVENANCE_VALID=TRUE` | PM |
| Q7 | Contar `CLAIM_SUPPORTED_BY_EVIDENCE=TRUE` entre entradas com provenance | ECB |
| Q8 | Contar `VALIDATOR_STATUS=VALIDATOR_INTERCEPT` entre inválidos | VR |
| Q9 | Contar `epistemic_status=ACCEPTED` | EAR |
| Q10 | Cruzar `SEMANTIC_PASS ∧ CLAIM_SUPPORTED_BY_EVIDENCE=FALSE` | H-ECB (confirmação observacional) |

## 8. Invariantes de Integridade

O Ledger deve satisfazer os seguintes invariantes (verificáveis por script):

1. **Unicidade de `question_id`:** cada `question_id` aparece exatamente uma vez por execução.
2. **Consistência null:** se `PROVENANCE_EXISTS=FALSE`, então `provenance_id=null`, `provenance_valid=null`, `provenance_match=null`.
3. **Consistência de precedência:** `epistemic_status` é determinístico a partir dos flags (Seção 5).
4. **Completude de metadados:** todas as entradas têm `session_id`, `timestamp`, `pipeline_version`, `oracle_version`, `eval_version`.
5. **Não-colapso:** nenhum flag individual é sobrescrito por `epistemic_status`. Todos os 5 flags permanecem acessíveis independentemente.

## 9. Status de Implementação

| Componente | Estado |
|---|---|
| Schema (este documento) | PRODUZIDO — 21/08/2026 |
| Script de instanciação do Ledger | PENDENTE DE RESTAURAÇÃO MATERIAL |
| População com N=100 entradas | PENDENTE DE EXECUÇÃO |
| Auditoria de invariantes | PENDENTE DE EXECUÇÃO |
| Queries de auditoria (Q1-Q10) | PENDENTE DE EXECUÇÃO |

## 10. Genealogia Documental

```
AION-7.0.0-spec (Protocolo)
       │
       ▼  Seção 9: AION-EVIDENCE-LEDGER-001
       │
AION-EVIDENCE-LEDGER-001 v1.0.0-spec (este documento — Schema)
       │
       ├── Definição de 12 campos + 6 auxiliares
       ├── Taxonomia de 8 estados terminais
       ├── Regra de precedência determinística
       ├── Formato JSON Lines
       └── Queries de auditoria canônicas (Q1-Q10)
       │
       ▼  Após restauração material
       │
Instanciação material do Ledger + população via execução do baseline
```

---

*"O Ledger não torna o sistema epistemicamente confiável. Ele torna o sistema epistemicamente auditável — o que é o pré-requisito para qualquer confiança futura."*

**Fim do Schema AION-EVIDENCE-LEDGER-001 v1.0.0-spec.**
