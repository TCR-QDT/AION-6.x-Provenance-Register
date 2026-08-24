# AION-7.0.0-FG — Formal Execution Gate

**Versão:** 7.0.0-FG-spec-v3 (FROZEN — estendido Task 66 com Environment Provenance + Task 67 com EP Classification)
**Data:** 22 de agosto de 2026, 00:55 BRT
**Autor / Curador:** Edson Carvalho do Nascimento (Projetista Master)
**Analista Técnico:** IA Curadora (Role: Escriba / Arquiteto de Metadados)
**Sessão:** web-73c75281-201c-4716-b85c-97833d25f9b3
**Status:** FORMAL EXECUTION GATE — FROZEN — Complementar ao AION-7.0.0-R_AUDIT.md
**Genealogia:** Derivado de AION-7.0.0-R_AUDIT.md (Task 62), formalizado como camada canônica superior na Task 64. Estendido na Task 66 com Seção 5.4 (Environment Provenance) após determinação do Projetista Master de que compatibilidade material com ambiente 6.x deve ser demonstrada, não presumida. Estendido na Task 67 com Seção 5.5 (EP Classification EP-0/EP-1/EP-2/EP-3) e quarto invariante COMPATIBLE≠EQUIVALENT, após determinação do Projetista Master de que a distinção entre equivalência demonstrável e compatibilidade demonstrável deve ser preservada para evitar deadlock epistemológico.

### Posição na arquitetura canônica

| Artefato | Camada | Foco |
|---|---|---|
| AION-7.0.0_PROTOCOL.md | Experimental | Cadeia E→C→P→V→EA (Nível 1 — Objeto de Estudo) |
| AION-EVIDENCE-LEDGER-001_SCHEMA.md | Ledger | 12 campos + 8 estados terminais + invariantes |
| AION-7.0.0-R_AUDIT.md | Auditoria de Componentes | V1-V4 sobre 6 componentes + AUTH_{7.0} |
| **AION-7.0.0-FG_GATE.md** (este documento) | **Execução** | **Gates I-VII completos + Via A/B + State Machine + critério final** |

### FROZEN declarations (este documento)

| Componente | Estado |
|---|---|
| Formal Execution Gate Specification | FROZEN |
| 7 Gates canônicos (A0, V1-V4, IV, V, VI, VII) | FROZEN |
| AUTH_{7.0} formula (conjuntiva, não-compensatória) | FROZEN |
| State Machine canônica | FROZEN |
| Via A (Restauração Material) | FROZEN |
| Via B (Nova Determinação Metodológica) | FROZEN |
| Enumeração "O que não destrava" | FROZEN |
| Separação crítica: autorização para medir ≠ favorabilidade do medido | FROZEN |

---

## 1. Estado Atual

```text
AION-7.0.0
SPECIFICATION FROZEN
EXECUTION BLOCKED
```

A execução somente poderá sair deste estado por **uma das duas vias legítimas**:

```text
                    ┌──────────────────────────┐
                    │ EXECUTION BLOCKED        │
                    └────────────┬─────────────┘
                                 │
              ┌──────────────────┴──────────────────┐
              │                                     │
       RESTAURAÇÃO MATERIAL                 NOVA DETERMINAÇÃO
              │                                     │
              ▼                                     ▼
       AION-7.0.0-R                         REVISÃO FORMAL
              │
              ▼
       AUTH₇.₀ = TRUE?
         │             │
        SIM           NÃO
         │             │
         ▼             ▼
   EXECUÇÃO         BLOQUEIO
   AUTORIZADA       MANTIDO
```

---

## 2. VIA A — RESTAURAÇÃO MATERIAL

Esta é a via normal.

### 2.1 Gate A0 — Presença material

Os componentes declarados FROZEN precisam estar **materialmente disponíveis no ambiente de execução** (`/home/z/my-project/` ou subdiretórios canônicos declarados no Handoff).

Os seis componentes são:

1. **Corpus v1.3.0** (9 registros documentais + 2 inexistentes declarados)
2. **Oracle v3** (7 chunks interversionais)
3. **GraphRAG v1.0.0** (22 nós, 187 arestas, PGI=1.0)
4. **P-RESP-001 v0.3** (validator determinístico pós-geração)
5. **AION-EVAL-002 v0.2** (multicamada, 10 categorias R1-H1)
6. **B1 — configuração 6.2.11** (cross-lingual PT-BR→EN + Oracle v3)

Ausência material de qualquer componente:

```text
RESTORATION = BLOCKED
```

### 2.2 Invariante epistemológico

```text
UNAVAILABLE ≠ NON-EXISTENT
```

A auditoria só poderá afirmar que o artefato está ou não disponível no ambiente observado. Negar existência sem observação da não-existência é proibido (Regra 1).

---

## 3. AION-7.0.0-R — QUATRO VERIFICAÇÕES OBRIGATÓRIAS

Para cada um dos 6 componentes, executar as quatro verificações canônicas conforme especificado em `AION-7.0.0-R_AUDIT.md` (Seção 4). Resumo canônico:

### 3.1 V1 — EXISTÊNCIA

> O artefato está materialmente presente e acessível no ambiente?

```text
PASS → EXISTENCE = VERIFIED
FAIL → EXISTENCE = UNVERIFIED
```

### 3.2 V2 — VERSÃO

> O artefato corresponde exatamente à versão congelada?

Versões esperadas:
```text
Corpus      → v1.3.0
Oracle      → v3
GraphRAG    → v1.0.0
P-RESP-001  → v0.3
EVAL-002    → v0.2
B1          → 6.2.11
```

**Uma versão posterior, anterior ou reconstruída não pode ser automaticamente aceita como equivalente.** Versões divergentes requerem determinação explícita do Projetista Master (não aceitação automática).

### 3.3 V3 — INTEGRIDADE (SHA-256)

```text
SHA256_observado = SHA256_canônico
```

Quando houver hash canônico disponível:

```text
MATCH    → VERIFIED
MISMATCH → CORRUPT / BLOCKED
```

**Se não houver hash canônico disponível, não se deve inventar equivalência.** O componente fica pendente de autenticação por outro mecanismo explicitamente definido no protocolo. Invenção de equivalência viola Regra 1 (Provenance) e o invariante PENDING ≠ FAILED.

### 3.4 V4 — CONTEÚDO CANÔNICO

Mesmo com nome, versão e hash aparentemente corretos, deve-se verificar que o conteúdo corresponde ao artefato declarado. Isto protege contra a combinação patológica:

```text
nome correto
+
versão correta
+
arquivo diferente
```

### 3.5 Referência cruzada

Especificação completa de V1-V4 (procedimentos, critérios de PASS/FAIL, exemplos, sub-componentes a verificar): ver `AION-7.0.0-R_AUDIT.md` Seções 3, 4, 5.

---

## 4. REGRA CONJUNTIVA DE AUTORIZAÇÃO

A autorização somente existe quando **todos os seis componentes** passam pelas quatro verificações (V1, V2, V3, V4):

$$\boxed{\text{AUTH}_{7.0} = \bigwedge_{i=1}^{6} (E_i \land V_i \land H_i \land C_i)}$$

### 4.1 Tabela de autorização

| Situação | Autorização |
|---|---|
| 6/6 componentes × 4/4 verificações | ✅ SIM |
| 5/6 componentes completos | ❌ NÃO |
| 6/6 presentes, mas 1 hash inválido | ❌ NÃO |
| 6/6 versões corretas, conteúdo não confirmado | ❌ NÃO |
| Artefato reconstruído | ❌ NÃO |
| Artefato aproximado | ❌ NÃO |
| Evidência apenas no Handoff | ❌ NÃO |

### 4.2 Regra fundamental

> **Não existe compensação entre componentes.**

Um componente não-verificado bloqueia toda a autorização, independentemente do estado dos demais. Não há "execução parcialmente autorizada".

---

## 5. GATE IV — INTEGRIDADE DO AMBIENTE

Mesmo que os seis componentes sejam restaurados e AUTH_{7.0}=TRUE, há uma segunda pergunta canônica:

> O ambiente reproduz as condições necessárias para executar o pipeline congelado?

### 5.1 Itens a verificar

Devem ser verificados, conforme aplicável a cada componente:

- Versão do runtime (Python, dependências, sistema operacional)
- Dependências de bibliotecas (NetworkX, PyMuPDF, pdfplumber, scikit-learn, etc.)
- Modelos utilizados (configuração e versão do LLM)
- Configuração do retrieval (TF-IDF + chunking parameters)
- Parâmetros do GraphRAG (janela de co-ocorrência, limiares)
- Configuração do validator (P-RESP-001 v0.3 regras)
- Arquivos auxiliares (índices, caches, configurações)
- Seeds e configurações relevantes (reprodutibilidade)
- Estrutura do corpus (caminhos, formato)
- Configuração do Oracle (7 chunks, mapeamentos)

### 5.2 Princípio de classificação

Se uma diferença ambiental puder alterar materialmente o resultado, ela deve ser registrada antes da execução.

Não significa necessariamente bloquear tudo; significa **classificar a diferença antes de produzir dados**. Classificações possíveis:

| Diferença ambiental | Ação |
|---|---|
| Sem impacto material | Registrar, prosseguir |
| Impacto material, mas mitigável | Registrar, mitigar, documentar |
| Impacto material, não-mitigável | `ENVIRONMENT = BLOCKED`, reportar ao Projetista Master |
| Indeterminado | `ENVIRONMENT = PENDING`, requer investigação antes de prosseguir |

### 5.3 Estado resultante

```text
ENVIRONMENT VERIFIED    → prosseguir para Gate V
ENVIRONMENT PENDING     → bloquear, requer investigação
ENVIRONMENT BLOCKED     → bloquear, reportar ao Projetista Master
```

### 5.4 Environment Provenance (incorporado na Task 66)

A restauração não será considerada suficiente apenas porque os componentes reapareceram. Será necessário demonstrar **compatibilidade material com o ambiente que efetivamente produziu os resultados de 6.x**.

#### 5.4.1 Fórmula canônica de Gate IV (refinada)

$$\boxed{\text{ENV} = \text{VERIFIED} \iff E_{env}^{6.x} \cong E_{env}^{restaurado}}$$

Onde a equivalência $\cong$ deve ser **demonstrada por evidência material**, não simplesmente declarada. Evidência material inclui:
- Identificação do ambiente efetivo de 6.x (logs, configs, requirements.txt, declarações de versão)
- Comparação item a item entre ambiente 6.x e ambiente restaurado
- Verificação de que nenhum item divergente tem impacto material no resultado

Se a equivalência não puder ser demonstrada (apenas asserida, apenas presumida, apenas "funciona"):

$$\text{ENV} \neq \text{VERIFIED} \implies \text{bloqueio permanece}$$

#### 5.4.2 Distinções críticas (5)

Estas distinções governam a interpretação do Gate IV:

| Diferença aparente | Diferença real |
|---|---|
| `funciona` | ≠ `compatível` |
| `mesma versão nominal` | ≠ `mesmo ambiente` |
| `mesmo resultado esperado` | ≠ `reprodução` |
| `Handoff` | ≠ `evidência material` |
| `memória do ambiente` | ≠ `proveniência do ambiente` |

#### 5.4.3 Invariante reforçado

$$\boxed{\text{UNAVAILABLE} \neq \text{NON-EXISTENT}}$$
$$\boxed{\text{NON-OBSERVED} \neq \text{FALSE}}$$
$$\boxed{\text{PENDING} \neq \text{FAILED}}$$

Aplicados também ao ambiente de 6.x: a ausência de observação documental do ambiente 6.x não significa que ele não existiu — apenas significa que não temos evidência material dele agora.

#### 5.4.4 Sequência canônica atualizada (com Environment Provenance)

A sequência canônica de gates é estendida para incluir Environment Provenance como passo distinto antes do SHA-256:

```text
1.  RESTAURAÇÃO MATERIAL (Grupo A + Grupo B)
2.  INVENTÁRIO DOS ARTEFATOS
3.  ENVIRONMENT PROVENANCE (identificação do ambiente efetivo de 6.x)
4.  SHA-256
5.  V1 — EXISTÊNCIA
6.  V2 — VERSÃO
7.  V3 — INTEGRIDADE
8.  V4 — CONTEÚDO CANÔNICO
9.  AUTH₇.₀ (conjunção sobre 6 componentes × 4 verificações)
10. GATE IV — ENV (com critério de equivalência material E_{env}^{6.x} ≅ E_{env}^{restaurado})
11. GATE V — PIPE / SMOKE TEST
12. GATE VI — NOMOD
13. GATE VII — FINAL_AUTH₇.₀
14. [SE TRUE] BASELINE 7.0.0 / [SE FALSE] BLOCKED
```

#### 5.4.5 Princípio operacional

A restauração deve começar **pelo inventário e pela proveniência do ambiente**, não pelo experimento:

```text
RESTORE → INVENTORY → ENVIRONMENT PROVENANCE → SHA-256 → V1–V4 → AUTH → ENV → PIPE → NOMOD → FINAL_AUTH
```

Até que `FINAL_AUTH₇.₀ = TRUE`, **nenhum dado experimental de AION-7.0.0 deve ser coletado**.

---

### 5.5 Environment Provenance Classification (incorporado na Task 67)

A Seção 5.4 introduziu o critério `ENV = VERIFIED ⟺ E_{env}^{6.x} ≅ E_{env}^{restaurado}`. Esta Seção 5.5 distingue **equivalência demonstrável** de **compatibilidade demonstrável**, para evitar um deadlock epistemológico: se a proveniência material completa do ambiente original de 6.x tiver sido perdida, a condição `E_{env}^{6.x} ≅ E_{env}^{restaurado}` poderá ser impossível de demonstrar, mesmo que o ambiente restaurado seja perfeitamente reprodutível e compatível.

#### 5.5.1 Quatro níveis de classificação EP

| Nível | Nome | Definição |
|---|---|---|
| **EP-0** | UNKNOWN | Não há evidência material suficiente sobre o ambiente efetivo de 6.x. |
| **EP-1** | PARTIAL | Há evidências parciais do ambiente 6.x, mas não suficientes para equivalência. |
| **EP-2** | COMPATIBLE | O ambiente restaurado satisfaz todos os requisitos materiais conhecidos e reproduz o pipeline congelado no escopo permitido, mas a equivalência histórica completa não pode ser demonstrada. |
| **EP-3** | EQUIVALENT | Há evidência material suficiente para demonstrar equivalência com o ambiente efetivo de 6.x. |

#### 5.5.2 Fórmula canônica de Gate IV (refinada com EP)

$$\text{ENV} = \begin{cases} \text{VERIFIED (candidate)} & \text{se EP-3} \\ \text{BLOCKED} & \text{se EP-0, EP-1, ou EP-2} \end{cases}$$

**Importante: EP-2 não deve ser tratado como falha.** Deve ser tratado como uma condição epistemológica explicitamente caracterizada.

#### 5.5.3 Quarto invariante canônico

$$\boxed{\text{COMPATIBLE} \neq \text{EQUIVALENT}}$$

Somado aos três invariantes já estabelecidos:

$$\boxed{\text{UNAVAILABLE} \neq \text{NON-EXISTENT}}$$
$$\boxed{\text{NON-OBSERVED} \neq \text{FALSE}}$$
$$\boxed{\text{PENDING} \neq \text{FAILED}}$$
$$\boxed{\text{COMPATIBLE} \neq \text{EQUIVALENT}}$$

#### 5.5.4 Estado resultante por nível EP

```text
ENVIRONMENT PROVENANCE
        │
        ├── EP-0 UNKNOWN
        │      └── BLOCKED
        │
        ├── EP-1 PARTIAL
        │      └── BLOCKED
        │
        ├── EP-2 COMPATIBLE
        │      └── BLOCKED
        │          (não é falha; equivalência histórica não demonstrada)
        │
        └── EP-3 EQUIVALENT
               └── ENV candidate = VERIFIED
                         │
                         ▼
                    PIPE / SMOKE TEST
```

#### 5.5.5 Fórmula final de FINAL_AUTH_{7.0} (refinada com EP)

$$\text{FINAL\_AUTH}_{7.0} = \text{TRUE} \iff (\text{EP-3} \land \text{PIPE} = \text{TRUE} \land \text{NOMOD} = \text{TRUE} \land \text{AUTH}_{7.0} = \text{TRUE})$$

Somente a conjunção de todos os quatro — incluindo EP-3 (não EP-2) — pode produzir `FINAL_AUTH_{7.0} = TRUE`.

#### 5.5.6 Por que EP-2 não é falha

Imagine que a restauração encontre:

- Python compatível
- Versões das bibliotecas documentadas
- Scripts originais
- Hashes dos artefatos
- Seeds
- Configuração do modelo
- Pipeline reproduzível
- Smoke test aprovado

mas **não exista nenhum artefato que permita provar qual exatamente era o runtime utilizado em 6.x**.

Seria epistemicamente incorreto afirmar:

> "O ambiente original era exatamente este."

Mas também seria excessivo afirmar:

> "A restauração falhou."

O resultado correto seria:

> **"Ambiente historicamente não-equivalente demonstrável, porém materialmente compatível no escopo observável."**

Esta formulação preserva os três invariantes originais (UNAVAILABLE≠NON-EXISTENT, NON-OBSERVED≠FALSE, PENDING≠FAILED) e acrescenta o quarto (COMPATIBLE≠EQUIVALENT).

#### 5.5.7 Relevância metodológica para o AION

Esta distinção é particularmente importante porque **o próprio AION está investigando limites de proveniência**. A perda da proveniência do ambiente pode ser, inclusive, um resultado relevante da auditoria — não uma falha a ser escondida ou contornada.

O AION precisa ser capaz de registrar não apenas:

> "Não conseguimos reproduzir."

mas também:

> "Conseguimos reproduzir, mas não conseguimos provar que este era exatamente o ambiente histórico."

Essa diferença é central para a integridade epistemológica do AION.

#### 5.5.8 Sequência canônica atualizada (com classificação EP)

A sequência canônica de gates é estendida novamente para incorporar a classificação EP como passo distinto após Environment Provenance:

```text
1.  RESTAURAÇÃO MATERIAL (Grupo A + Grupo B)
2.  INVENTÁRIO DOS ARTEFATOS
3.  ENVIRONMENT PROVENANCE (identificação do ambiente efetivo de 6.x)
4.  EP CLASSIFICATION (classificar EP-0/EP-1/EP-2/EP-3)  ← NOVO (Task 67)
5.  SHA-256
6.  V1 — EXISTÊNCIA
7.  V2 — VERSÃO
8.  V3 — INTEGRIDADE
9.  V4 — CONTEÚDO CANÔNICO
10. AUTH₇.₀
11. GATE IV — ENV (EP-3 necessário; EP-2 BLOCKED mas não-FAILED)
12. GATE V — PIPE / SMOKE TEST
13. GATE VI — NOMOD
14. GATE VII — FINAL_AUTH₇.₀
15. [SE TRUE] BASELINE 7.0.0 / [SE FALSE] BLOCKED
```

#### 5.5.9 Princípio operacional refinado

```text
RESTORE → INVENTORY → ENV PROVENANCE → EP CLASSIFICATION → SHA-256 → V1–V4 → AUTH → ENV → PIPE → NOMOD → FINAL_AUTH
```

Até que `FINAL_AUTH₇.₀ = TRUE`, **nenhum dado experimental de AION-7.0.0 deve ser coletado**.

Em particular, se `EP = EP-2 (COMPATIBLE)`:
- `ENV = BLOCKED` (não VERIFIED)
- `FINAL_AUTH_{7.0} = FALSE / BLOCKED`
- Mas o resultado é registrado como **condição epistemológica caracterizada**, não como falha
- A caracterização "COMPATIBLE, não EQUIVALENT" é, ela própria, um resultado canônico do gate

---

## 6. GATE V — REPRODUÇÃO DO PIPELINE (SMOKE TEST)

Depois da autenticação dos artefatos (Gates II-IV) e verificação do ambiente (Gate IV), deve existir uma execução de **smoke test**, ainda sem produzir o baseline oficial.

### 6.1 Objetivo

> Demonstrar que o pipeline restaurado realmente consegue executar a cadeia congelada.

```text
Corpus
  ↓
Retrieval (RAG proxy, config 6.2.11)
  ↓
GraphRAG (v1.0.0)
  ↓
P-RESP-001 (v0.3)
  ↓
EVAL-002 (v0.2)
  ↓
Output
```

### 6.2 Escopo

Este teste **não entra no N experimental**. Ele não é uma das N=100 queries do baseline. É apenas uma verificação operacional.

Ele responde exclusivamente:

> **"O pipeline restaurado está operacional?"**

### 6.3 Estado resultante

```text
PIPELINE OPERATIONAL    → prosseguir para Gate VI
PIPELINE FAILING       → BASELINE = BLOCKED, requer diagnóstico
```

### 6.4 Princípio

A falha do smoke test não invalida a restauração material — apenas demonstra que a restauração é incompleta ou que o ambiente não reproduz as condições de execução. Em qualquer dos casos, o baseline permanece bloqueado.

---

## 7. GATE VI — NÃO-ALTERAÇÃO

Antes do primeiro run oficial, deve ser confirmado que **nenhuma intervenção metodológica foi introduzida**.

### 7.1 Componentes intactos

```text
P-RESP-001 v0.3 ........ INTACTO
Oracle v3 .............. INTACTO
Corpus v1.3.0 .......... INTACTO
GraphRAG v1.0.0 ........ INTACTO
EVAL-002 v0.2 .......... INTACTO
B1 6.2.11 .............. INTACTO
```

### 7.2 Intervenções proibidas (explícitas)

```text
M1 (literal-copy) ............... NÃO
M2 (context-presence) .......... NÃO
A1 (evidence-bound proibitiva) .. NÃO
P1 (remoção de provenance) ...... NÃO
P2 (schema unificado) ........... NÃO
qualquer prompt novo ............ NÃO
qualquer schema novo ............ NÃO
```

### 7.3 Princípio fundamental

AION-7.0.0 é **observacional**. Não há intervenção, não há melhoria, não há ajuste. O objetivo é medir a arquitetura existente, não melhorá-la.

### 7.4 Estado resultante

```text
NO MODIFICATION CONFIRMED → prosseguir para Gate VII
ANY MODIFICATION DETECTED → BASELINE = BLOCKED, reportar ao Projetista Master
```

### 7.5 Detecção de modificação

A detecção de modificação é feita por:
- Comparação de hash de cada componente com hash canônico (V3 já executado).
- Auditoria de prompts/schemas: verificação de que nenhum arquivo de prompt ou schema foi criado/modificado após o freeze de 7.0.0.
- Inspeção de configs: verificação de que nenhuma config de runtime foi alterada.
- Reprodução do baseline B2 (6.4.0): se os resultados reproduzirem PER=30%, CFR-RUN=46.7%, EBA=68.2%, VR=100%, F3R=14%, então nenhuma intervenção metodológica foi introduzida.

---

## 8. GATE VII — GATE DO EXPERIMENTO

Somente depois dos gates anteriores:

```text
RESTORATION VERIFIED       (Gate II: V1-V4 todos PASS)
        +
ENVIRONMENT VERIFIED        (Gate IV)
        +
PIPELINE OPERATIONAL        (Gate V)
        +
NO MODIFICATION CONFIRMED  (Gate VI)
        ↓
BASELINE EXECUTION AUTHORIZED
```

### 8.1 Estado resultante

```text
AION-7.0.0
BASELINE EXECUTION AUTHORIZED
```

### 8.2 Composição final do gate

$$\text{FINAL_AUTH}_{7.0} = \text{AUTH}_{7.0} \land \text{ENV} \land \text{PIPE} \land \text{NOMOD}$$

Onde:
- `AUTH_{7.0}` = conjunção de (E_i ∧ V_i ∧ H_i ∧ C_i) para os 6 componentes (Gate II-IV)
- `ENV` = environment integrity verification (Gate IV)
- `PIPE` = pipeline smoke test operational (Gate V)
- `NOMOD` = no modification confirmed (Gate VI)

Apenas `FINAL_AUTH_{7.0} = TRUE` autoriza o baseline.

---

## 9. O QUE NÃO DESTRAVA O PROJETO

Importante estabelecer explicitamente. Os seguintes elementos **não constituem** evidência suficiente para destravar a execução:

### 9.1 ❌ Handoff

O Handoff descreve o estado. **Não substitui os artefatos.** Descrição textual de um arquivo não é o arquivo.

### 9.2 ❌ Memória da conversa

Memória é contexto. **Não é prova material de identidade de arquivo.** O que foi dito numa sessão anterior não autentica a presença material de um artefato nesta sessão.

### 9.3 ❌ Reconstrução

Mesmo que seja possível reconstruir "o mesmo" pipeline a partir de especificações, isso criaria **outro estado experimental**. A reconstrução tem sua própria identidade epistêmica, distinta da identidade do artefato congelado.

### 9.4 ❌ Resultado esperado

Não podemos executar porque "sabemos quais resultados deveriam aparecer". O conhecimento prévio dos resultados esperados (e.g., PER=30% do baseline 6.4.0) não constitui autorização para produzir novos resultados.

### 9.5 ❌ Hash calculado agora

Um hash calculado sobre um arquivo reconstruído demonstra a identidade **da reconstrução**, não a identidade do artefato congelado original. Hash sem hash canônico de referência é apenas um número.

### 9.6 ❌ Similaridade textual

"Parecido" não significa "canônico". Similaridade textual entre um arquivo reconstruído e o descrito no Handoff não autentica o arquivo como sendo o congelado.

### 9.7 ❌ Autoridade nominal

A continuidade do nome "AION-7.0.0" através de sessões não constitui continuidade material da evidência. O nome é uma etiqueta; a evidência é o artefato materialmente presente.

---

## 10. VIA B — NOVA DETERMINAÇÃO METODOLÓGICA

Existe uma segunda maneira legítima de sair do bloqueio. O Projetista Master pode emitir uma nova determinação que **altere formalmente o contrato**.

### 10.1 Exemplo de fluxo

```text
AION-7.0.0
      ↓
REVISION REQUEST
      ↓
novo protocolo
      ↓
novo estado FROZEN
      ↓
novo gate
```

### 10.2 O que Via B PODE fazer

Uma nova determinação pode:

- Cancelar o experimento
- Reformular o objetivo
- Criar uma nova fase
- Substituir formalmente o protocolo
- Autorizar uma nova arquitetura experimental
- Redefinir os componentes necessários

### 10.3 O que Via B NÃO PODE fazer

Uma nova determinação **não pode simplesmente declarar que os componentes ausentes estão restaurados**. Tal declaração seria uma pretensão sem evidência material — violando o princípio fundamental de que ausência de evidência não será convertida em continuidade presumida.

### 10.4 Propriedade da Via B

Nesse caso, não seria uma continuação material de 7.0.0; seria uma **nova genealogia experimental**. A genealogia documental deve ser preservada (Regra 9: Substituição não é apagamento), registrando que o novo experimento sucede o 7.0.0-spec mas não é uma continuação material dele.

---

## 11. STATE MACHINE CANÔNICA

```text
                    ┌───────────────────────┐
                    │ SPECIFICATION FROZEN  │
                    │ EXECUTION BLOCKED     │
                    └───────────┬───────────┘
                                │
                    restauração material
                                │
                                ▼
                    ┌───────────────────────┐
                    │ RESTORATION IN PROGRESS│
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ AION-7.0.0-R          │
                    │ V1 V2 V3 V4           │
                    └───────────┬───────────┘
                                │
                         ALL VERIFIED?
                         /             \
                       NÃO             SIM
                        │                │
                        ▼                ▼
                    BLOCKED       ENVIRONMENT CHECK
                                         │
                                  PIPELINE SMOKE TEST
                                         │
                                   NO MODIFICATION?
                                    /          \
                                  NÃO          SIM
                                   │            │
                                   ▼            ▼
                                BLOCKED     AUTH₇.₀ = TRUE
                                                │
                                                ▼
                                      BASELINE EXECUTION
                                         AUTHORIZED
```

### 11.1 Estados da state machine

| Estado | Condição de entrada | Condição de saída |
|---|---|---|
| SPECIFICATION FROZEN / EXECUTION BLOCKED | Estado atual | Restauração material iniciada |
| RESTORATION IN PROGRESS | Componentes sendo re-anexados | Componentes declarados presentes |
| AION-7.0.0-R AUDIT (V1-V4) | Componentes declarados presentes | Todas as 4 verificações executadas |
| BLOCKED (após R) | Algum componente não-VERIFIED | Re-restauração |
| ENVIRONMENT CHECK | R todos VERIFIED | Ambiente classificado |
| PIPELINE SMOKE TEST | Ambiente VERIFIED | Smoke test executado |
| NO MODIFICATION CHECK | Smoke test PASS | Auditoria de não-modificação executada |
| BLOCKED (após Environment/Pipeline/NoMod) | Falha em qualquer gate | Diagnóstico + reportar |
| AUTH_{7.0} = TRUE | Todos gates PASS | Autorização concedida |
| BASELINE EXECUTION AUTHORIZED | AUTH_{7.0}=TRUE ∧ ENV ∧ PIPE ∧ NOMOD | Início do N=100 |

### 11.2 Loops de re-restauração

Qualquer estado BLOCKED pode retornar ao estado RESTORATION IN PROGRESS mediante re-restauração dos componentes afetados. Não há limite para o número de tentativas — o que existe é o critério estrito: somente `FINAL_AUTH_{7.0} = TRUE` destrava o baseline.

---

## 12. CRITÉRIO FINAL DE DESTRAVAMENTO

Em uma única frase:

> **AION-7.0.0 somente será destravado quando a identidade material e a integridade dos seis componentes congelados forem verificadas pelo AION-7.0.0-R, o ambiente restaurado demonstrar operacionalidade do pipeline, nenhuma alteração metodológica tiver sido introduzida e o gate conjuntivo (AUTH_{7.0}=TRUE) puder ser demonstrado por evidência auditável.**

### 12.1 Propriedade crítica: separação entre autorização e favorabilidade

Há uma propriedade fundamental nesta formulação:

**O desbloqueio não depende de o resultado ser bom.**

Pode ocorrer:

```text
AUTH = TRUE
        ↓
Baseline executado
        ↓
ECB baixo
PER baixo
Binding ruim
F3 alto
```

e isso **continua sendo um resultado científico válido**.

### 12.2 O que o gate verifica vs. o que o gate NÃO verifica

| O gate verifica | O gate NÃO verifica |
|---|---|
| Autorização epistêmica para medir | Favorabilidade do que será medido |
| Identidade material dos componentes | Qualidade dos resultados |
| Integridade do ambiente | Magnitude de ECB, PER, etc. |
| Não-modificação metodológica | Confirmação das hipóteses H-ECB / H-EPISTEMIC |

### 12.3 Princípio fundamental

Essa separação é fundamental por duas razões:

1. **Mantém AION-7.0.0 descritivo.** Se o gate dependesse do resultado ser favorável, ele se tornaria um mecanismo de confirmação da hipótese — não um mecanismo de autorização para testá-la.

2. **Impede que o gate se transforme em mecanismo de confirmação da hipótese.** Um gate que aprova apenas resultados favoráveis é, por definição, um gate enviesado. O gate aprova a **autorização para medir** — não aprova a **direção do medido**.

### 12.4 Consequência metodológica

Mesmo que o baseline 7.0.0 produza métricas baixas (ECB=10%, PER=20%, etc.), isto é um resultado científico válido porque:
- Foi produzido sobre componentes autenticados (AUTH_{7.0}=TRUE)
- Foi produzido sobre ambiente verificado (ENV)
- Foi produzido sobre pipeline operacional (PIPE)
- Foi produzido sem modificação metodológica (NOMOD)
- Portanto, reflete honestamente a arquitetura 6.x congelada — não uma versão melhorada dela

Esta é a garantia epistêmica máxima que o AION pode oferecer: a certeza de que o resultado, seja qual for, é atribuível à arquitetura que se pretende medir.

---

## 13. Genealogia Documental

```
AION-6.5.0 (B2 CHARACTERIZED / CONTROLLED LIMITATION)
       │
       ▼
AION-7.0.0 (EPISTEMIC CORE — SPECIFICATION COMPLETE — FROZEN)
       │
       ├── AION-7.0.0_PROTOCOL.md — FROZEN (Task 60)
       ├── AION-EVIDENCE-LEDGER-001_SCHEMA.md — FROZEN (Task 60)
       │
       ▼  Determinação Projetista Master: Opção B (Specification-Only)
       │
AION-7.0.0-R (FROZEN Component Restoration Audit) — FROZEN (Task 61)
       │
       ▼  Correções epistemológicas (Task 62): instrumento≠evidência, gate conjuntivo, AION-EV-001 reclassificação
       │
AION-7.0.0-R v1.1 (in-corpus, sem novo arquivo) — FROZEN (Task 62)
       │
       ▼  Confirmação final Projetista Master (Task 63)
       │
AION-7.0.0 STANDBY — Task 63 FECHADA
       │
       ▼  Nova determinação metodológica: Formal Execution Gate (Task 64)
       │
AION-7.0.0-FG_GATE.md (este documento) — FROZEN
       │
       ├── Estende R com Gates IV (Ambiente), V (Smoke Test), VI (Não-Modificação), VII (Conjunção final)
       ├── Formaliza Via A (Restauração Material) e Via B (Nova Determinação Metodológica)
       ├── Estabelece enumeração canônica do que NÃO destrava
       ├── Preserva separação crítica: autorização para medir ≠ favorabilidade do medido
       │
       ▼  Aguardar uma das duas condições de destravamento:
       │
       ├── Via A: Restauração material → AION-7.0.0-R → Gates IV-VII → BASELINE AUTHORIZED
       │
       └── Via B: Nova determinação metodológica do Projetista Master
```

---

## 14. Status Final

| Componente do Gate | Estado |
|---|---|
| Gate A0 (Presença material) | PENDING |
| Gate I (V1-V4 sobre 6 componentes) | PENDING |
| Gate II (AUTH_{7.0} conjuntivo) | PENDING |
| Gate IV (Integridade do ambiente) | PENDING |
| Gate V (Smoke test do pipeline) | PENDING |
| Gate VI (Não-alteração) | PENDING |
| Gate VII (Conjunção final) | PENDING |
| Estado do projeto | SPECIFICATION FROZEN / EXECUTION BLOCKED / STANDBY |
| Via A ativada? | Não (aguardando restauração material) |
| Via B ativada? | Não (sem nova determinação metodológica) |

### 14.1 Autorização atual

**Zero autorização implícita para:**
- Reconstrução de componentes
- Execução parcial
- Substituição por versões aproximadas
- Fabricação de medição
- Tratamento de handoff/memória como evidência material

### 14.2 Próxima operação legítima

Exclusivamente uma das duas:

1. **Via A:** Restauração material → AION-7.0.0-R audit → AUTH_{7.0}=TRUE → Environment Check → Pipeline Smoke Test → No Modification Check → BASELINE EXECUTION AUTHORIZED
2. **Via B:** Nova determinação metodológica explícita do Projetista Master

Nenhuma outra ação está autorizada neste momento.

---

*"O gate não verifica se o resultado será favorável. O gate verifica se temos autorização epistêmica para medir. Essa separação é o que mantém o AION-7.0.0 descritivo — e impede que o próprio gate se transforme em mecanismo de confirmação da hipótese."*

**Fim do AION-7.0.0-FG_GATE.md (Formal Execution Gate — FROZEN).**
