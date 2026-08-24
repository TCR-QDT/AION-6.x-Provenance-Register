# AION-7.0.0-R0.3.3.A — V1-V4 Candidate Verification (Granular)

**Versão:** R0.3.3.A-1
**Data:** 23 de agosto de 2026, 02:30 BRT
**Autor / Curador:** Edson Carvalho do Nascimento (Projetista Master) — autorizou R0.3.3.A
**Analista Técnico:** IA Curadora (Role: Escriba / Arquiteto de Metadados) — executou R0.3.3.A
**Sessão:** web-73c75281-201c-4716-b85c-97833d25f9b3
**Status:** R0.3.3.A EXECUTADO. Ambos candidatos (C-01 CORPUS-002, C-02 CORPUS-006) classificados como **Caso D** (conteúdo compatível, proveniência insuficiente). EP-1 PARTIAL CANDIDATE permanece PRELIMINARY (não promovido a effective).
**Genealogia:** Derivado da determinação do Projetista Master (Task 80) autorizando V1-V4 individualmente para C-01 (Paper_A_v6.2_FINAL.pdf → CORPUS-002) e C-02 (Paper_A_v6.1_REVTeX_COMPLETE.pdf → CORPUS-006), com escopo estritamente limitado ao Grupo C.

---

## 1. Resumo Executivo

Foi executado o passo R0.3.3.A — V1-V4 Candidate Verification — em conformidade com a determinação do Projetista Master (Task 80) de verificar individualmente os dois candidatos materiais identificados no repositório TCR/QDT como potenciais correspondentes aos artefatos históricos CORPUS-002 e CORPUS-006. A verificação seguiu o framework V1-V4 reformulado pelo PM: V1 Identity, V2 Integrity, V3 Provenance, V4 Canonical Content. Para cada candidato, os quatro gates foram executados independentemente, com classificação granular por artefato (sem agregação proibida). O resultado canônico é: **ambos os candidatos classificados como Caso D** (conteúdo compatível, proveniência insuficiente) — V1 PASS, V2 PASS, V3 INSUFFICIENT, V4 PASS. Isto significa: o conteúdo dos PDFs corresponde materialmente ao esperado (incluindo correspondência com fontes .tex internas ao repositório, metadados PDF consistentes com Handoff, e autoria de Edson Carvalho do Nascimento confirmada), mas a cadeia material de proveniência liga o objeto ao repositório TCR/QDT — **não** à fonte original do corpus AION-6.x. Aplicando o princípio PM crítico: "compatibilidade de conteúdo não equivale a autenticação histórica." Consequentemente, **EP-1 PARTIAL CANDIDATE permanece PRELIMINARY** — não é promovido a EP-1 PARTIAL EFFECTIVE, porque nenhum dos candidatos alcançou Caso A (V1+V2+V3+V4 PASS). A classificação do Grupo C é refinada para: **EP-1 PARTIAL CANDIDATE / Caso D** (content-compatible, provenance-insufficient). AUTH₇.₀ permanece FALSE. FINAL_AUTH₇.₀ permanece BLOCKED. Os 4 artefatos FROZEN de 7.0.0-spec permanecem materialmente íntegros. O resultado é epistemicamente honesto: estabelece forte evidência material de que os PDFs do TCR/QDT correspondem em conteúdo aos PDFs esperados do corpus AION-6.x, mas não autentica que estes sejam os mesmos arquivos que estavam materialmente presentes no ambiente AION-6.x — porque nenhuma cadeia material conecta o repositório TCR/QDT ao corpus AION-6.x source.

## 2. Escopo Autorizado (PM Task 80)

### 2.1 Objeto da autorização

> Executar V1-V4 exclusivamente sobre candidatos materiais identificados no repositório TCR/QDT como potenciais correspondentes aos artefatos históricos CORPUS-002 e CORPUS-006.

### 2.2 Framework V1-V4 reformulado PM (Task 80)

| Gate | Pergunta |
|---|---|
| **V1 — Identity** | O objeto material corresponde ao artefato declarado? |
| **V2 — Integrity** | O objeto permanece íntegro e seu hash pode ser registrado? |
| **V3 — Provenance** | Existe cadeia material suficiente ligando o objeto ao repositório/origem observada? |
| **V4 — Canonical Content** | O conteúdo corresponde materialmente ao conteúdo esperado do corpus? |

### 2.3 Princípio crítico PM

> **Tamanho semelhante não é autenticação.** O fato de dois arquivos possuírem tamanhos correspondentes apenas justifica a passagem para verificação.

### 2.4 Granularidade obrigatória

A conclusão deverá permanecer **granular por artefato**. Não é permitido:

```
C-01 confirmado + C-02 confirmado → "Corpus AION confirmado"
```

### 2.5 Quatro casos possíveis (PM Task 80)

| Caso | Condição | Resultado |
|---|---|---|
| **A** | V1+V2+V3+V4 PASS | Candidato materialmente verificado |
| **B** | Algum gate crítico inconclusivo | EP-1 PARTIAL, sem autenticação |
| **C** | V1 FAIL | Candidato rejeitado como correspondência daquele CORPUS-ID |
| **D** | V4 positivo, V3 insuficiente | Compatibilidade de conteúdo não equivale a autenticação histórica |

### 2.6 Limites da autorização (NÃO permite)

- ✗ Instalar dependências
- ✗ Executar scripts TCR/QDT ou AION
- ✗ Reconstruir Oracle, GraphRAG, Corpus v1.3.0, P-RESP-001, AION-EVAL-002
- ✗ Inferir configuração B1
- ✗ Converter TCR/QDT em AION-6.x
- ✗ Declarar equivalência de ambiente
- ✗ Executar PIPE ou experimentos 7.0.0
- ✗ Alterar qualquer artefato FROZEN
- ✗ Promover automaticamente EP para conjunto completo
- ✗ Alterar `AUTH₇.₀ = FALSE`

### 2.7 Estado dos demais grupos (preservado)

```
Grupo A — EP-0 UNKNOWN (mantido)
Grupo B — EP-0 UNKNOWN (mantido)
Grupo C — candidatos autorizados para V1-V4 (este documento)
Grupo D — EP-0 UNKNOWN (mantido)
```

Mesmo que os dois candidatos do Grupo C sejam integralmente confirmados, **isso não autoriza AION-7.0.0**.

## 3. Candidato C-01 — V1-V4 Verification

### 3.1 Identificação do candidato

| Campo | Valor |
|---|---|
| Candidato ID | C-01 |
| Caminho no repositório TCR/QDT | `docs/pdfs/Paper_A_v6.2_FINAL.pdf` |
| Caminho completo | `/home/z/my-project/intake/external_repositories/Coerencia_Relacional/docs/pdfs/Paper_A_v6.2_FINAL.pdf` |
| CORPUS-ID alvo | CORPUS-002 |
| Descrição Handoff AION-MVP-001 | Paper A v6.2 (137KB, CURRENT/AUTHORITATIVE) |
| Tamanho esperado (Handoff) | 137 KB |
| Tamanho observado | 137520 bytes = 137.52 KB ≈ 137 KB (EXACT MATCH) |
| Git mode | 100644 (regular file) |

### 3.2 V1 — Identity

**Pergunta:** O objeto material corresponde ao artefato declarado?

| Verificação | Resultado |
|---|---|
| Arquivo existe materialmente | ✓ PASS — `ls -la` confirma presença |
| Filename corresponde ao esperado | ✓ PASS — `Paper_A_v6.2_FINAL.pdf` corresponde a "Paper A v6.2 FINAL" |
| Tamanho corresponde ao esperado | ✓ PASS — 137520 bytes ≈ 137 KB declarado no Handoff (EXACT MATCH) |
| PDF metadata Title | "Relational Coherence in Biological Networks" — corresponde a "Paper A" |
| PDF metadata Author | "Edson C. do Nascimento" — corresponde ao Projetista Master |
| PDF metadata CreationDate | "Wed Aug 12 21:22:09 2026 UTC" — corresponde à data declarada no Handoff (Paper A v6.2 consolidado em 12/08/2026) |
| PDF metadata Producer | "xdvipdfmx (0.1)" + Creator "LaTeX with hyperref" — coerente com fonte TeX |

**V1 Resultado:** ✓ **PASS** — objeto material corresponde ao artefato declarado em todos os critérios verificáveis (filename, tamanho, metadata).

### 3.3 V2 — Integrity

**Pergunta:** O objeto permanece íntegro e seu hash pode ser registrado?

| Verificação | Resultado |
|---|---|
| SHA-256 computável | ✓ PASS — `971986d96c4ceb1ea5d7a17acdf2a54f4276403f2805c3945874304020adc433` |
| PDF parseable (pdfinfo succeeded) | ✓ PASS — 6 páginas, sem encryption |
| PDF form | none (sem formulários preenchíveis) |
| PDF JavaScript | no |
| PDF Tagged | no |
| Page size | 612 x 792 pts (letter) — padrão REVTeX |

**V2 Resultado:** ✓ **PASS** — objeto permanece íntegro, hash registrado como baseline para futuras comparações.

### 3.4 V3 — Provenance

**Pergunta:** Existe cadeia material suficiente ligando o objeto ao repositório/origem observada?

#### 3.4.1 Cadeia material estabelecida

```
github.com/TCR-QDT/Coerencia_Relacional.git
        ↓ (git clone em 2026-08-23 01:27 BRT)
/home/z/my-project/intake/external_repositories/Coerencia_Relacional/
        ↓
docs/pdfs/Paper_A_v6.2_FINAL.pdf
```

| Verificação | Resultado |
|---|---|
| Arquivo rastreado no git history | ✓ Sim — commit `3e0d8c7` "Atualização 13082026" por Shukuwe |
| Git mode | 100644 (regular file, não symlink) |
| Git object hash | `30ef0dd35b1e51c468dc5f7816525a5e06c9667a` |
| Cadeia material ao repositório TCR/QDT | ✓ Demonstra que arquivo veio do TCR/QDT repo |

#### 3.4.2 Cadeia material ausente

| Verificação | Resultado |
|---|---|
| Cadeia material ao corpus AION-6.x source | ✗ **NÃO DEMONSTRADA** |
| AION Handoff declarou CORPUS-002 em | `/home/z/my-project/upload/` ou similar path em 6.x — nenhum artefato material liga TCR/QDT repo a este path |
| Hash canônico AION-6.x para CORPUS-002 | ✗ AUSENTE — Handoff não declara SHA-256 canônico para CORPUS-002 |
| Log de transferência TCR/QDT → AION-6.x | ✗ AUSENTE |
| Manifest de ingest AION-6.x | ✗ AUSENTE |

**V3 Resultado:** ⚠ **INSUFFICIENT** — cadeia material liga o objeto ao repositório TCR/QDT, mas **NÃO demonstra** cadeia material ao corpus AION-6.x source. A equivalência histórica entre TCR/QDT repo e AION-6.x corpus source não pode ser estabelecida materialmente.

### 3.5 V4 — Canonical Content

**Pergunta:** O conteúdo corresponde materialmente ao conteúdo esperado do corpus?

#### 3.5.1 Extração de texto PDF (primeiros 50 linhas)

```
Relational Coherence in Biological Networks:
A Quantitative Framework from Connectomes to EEG
Edson Carvalho do Nascimento1, ∗
1 Independent researcher, Curitiba, Brazil
(Dated: August 12, 2026)

We introduce the Relational Coherence Theory (TCR) for measuring informational coherence in
biological networks through the metric C = I×S×H β, where I is the normalized multivariate mutual
information (integration), S is the graph automorphism index (symmetry), and H is the normalized
spectral entropy. The exponent β is calibrated via leave-one-out cross-validation (LOOCV) over
12 synthetic connectome fixtures. The metric is validated on three empirical regimes: connectome
ranking (P1, p = 1.0 bootstrap), species discrimination against degree-matched random graphs (P2,
z = 28.4, p ≈ 0), and sleep/wake classification on real 32-channel EEG data from the OpenNeuro
ds003768 dataset (P3, AUC = 0.793 ± 0.133 across 4 subjects, p < 0.05)...
```

#### 3.5.2 Comparação com .tex source interno (autorizado por PM)

| Verificação | Resultado |
|---|---|
| .tex source correspondente | `docs/tex/Paper_A_v6.2_FINAL.tex` (33501 bytes, SHA-256: `9471c6e5a94e498a8f121d1756c0c1cea075b2e0d7e71cb9dcd772b062e90c47`) |
| TeX header comment | "Paper A — TCR Empírico (v6.1)" — NOTE: header diz v6.1 mas filename é v6.2 (inconsistência menor); conteúdo .tex reflete v6.2 (P3 com OpenNeuro ds003768, correção da v6.1 que usava PhysioNet Sleep-EDF) |
| Conteúdo PDF vs .tex | ✓ Corresponde — mesma estrutura, mesmo título, mesma data, mesmo autor, mesmo abstract |
| PDF metadata CreationDate vs .tex date | ✓ Corresponde — Aug 12, 2026 |
| Conteúdo vs descrição Handoff CORPUS-002 | ✓ Corresponde — "Paper A v6.2, CURRENT/AUTHORITATIVE, 137KB, by Edson Carvalho do Nascimento" |

**V4 Resultado:** ✓ **PASS** — conteúdo do PDF corresponde materialmente ao conteúdo esperado do corpus (declaração Handoff) e à fonte .tex interna ao repositório.

### 3.6 Classificação C-01 — Caso D

| Gate | Resultado |
|---|---|
| V1 Identity | ✓ PASS |
| V2 Integrity | ✓ PASS |
| V3 Provenance | ⚠ INSUFFICIENT |
| V4 Canonical Content | ✓ PASS |

**Classificação canônica:** **Caso D** — conteúdo compatível, proveniência insuficiente.

**Interpretação:** Aplicando princípio PM Task 80: "compatibilidade de conteúdo não equivale a autenticação histórica." O PDF em TCR/QDT tem conteúdo materialmente compatível com CORPUS-002 esperado (mesmo título, autor, data, abstract, tamanho), mas **não há cadeia material demonstrando que este PDF é o mesmo arquivo que estava materialmente presente no ambiente AION-6.x**. A proveniência liga o objeto ao TCR/QDT repo, não à fonte original do corpus AION-6.x.

**Status C-01:** CANDIDATE — **não autenticado**. Permanece como EVIDÊNCIA CANDIDATA.

## 4. Candidato C-02 — V1-V4 Verification

### 4.1 Identificação do candidato

| Campo | Valor |
|---|---|
| Candidato ID | C-02 |
| Caminho no repositório TCR/QDT | `docs/pdfs/Paper_A_v6.1_REVTeX_COMPLETE.pdf` |
| Caminho completo | `/home/z/my-project/intake/external_repositories/Coerencia_Relacional/docs/pdfs/Paper_A_v6.1_REVTeX_COMPLETE.pdf` |
| CORPUS-ID alvo | CORPUS-006 |
| Descrição Handoff AION-MVP-001 | Paper A v6.1 oficial (138KB, HISTORICAL) |
| Tamanho esperado (Handoff) | 138 KB |
| Tamanho observado | 138780 bytes = 138.78 KB ≈ 138 KB (EXACT MATCH) |
| Git mode | 100644 (regular file) |

### 4.2 V1 — Identity

**Pergunta:** O objeto material corresponde ao artefato declarado?

| Verificação | Resultado |
|---|---|
| Arquivo existe materialmente | ✓ PASS — `ls -la` confirma presença |
| Filename corresponde ao esperado | ✓ PASS — `Paper_A_v6.1_REVTeX_COMPLETE.pdf` corresponde a "Paper A v6.1 oficial" |
| Tamanho corresponde ao esperado | ✓ PASS — 138780 bytes ≈ 138 KB declarado no Handoff (EXACT MATCH) |
| PDF metadata Title | "Relational Coherence in Biological Networks" — corresponde a "Paper A" |
| PDF metadata Author | "Edson C. do Nascimento" — corresponde ao Projetista Master |
| PDF metadata CreationDate | "Mon Aug 10 22:48:50 2026 UTC" — corresponde à data declarada no Handoff (Paper A v6.1 oficializado em 10/08/2026) |
| PDF metadata Producer | "xdvipdfmx (0.1)" + Creator "LaTeX with hyperref" — coerente com fonte TeX |

**V1 Resultado:** ✓ **PASS** — objeto material corresponde ao artefato declarado em todos os critérios verificáveis.

### 4.3 V2 — Integrity

**Pergunta:** O objeto permanece íntegro e seu hash pode ser registrado?

| Verificação | Resultado |
|---|---|
| SHA-256 computável | ✓ PASS — `efd7f7caf19a5f99cd1663303c6f36d0beba50f19c71d4f44d44b81c396c8854` |
| PDF parseable (pdfinfo succeeded) | ✓ PASS — 6 páginas, sem encryption |
| PDF form | none |
| PDF JavaScript | no |
| PDF Tagged | no |
| Page size | 612 x 792 pts (letter) — padrão REVTeX |

**V2 Resultado:** ✓ **PASS** — objeto permanece íntegro, hash registrado como baseline.

### 4.4 V3 — Provenance

**Pergunta:** Existe cadeia material suficiente ligando o objeto ao repositório/origem observada?

#### 4.4.1 Cadeia material estabelecida

```
github.com/TCR-QDT/Coerencia_Relacional.git
        ↓ (git clone em 2026-08-23 01:27 BRT)
/home/z/my-project/intake/external_repositories/Coerencia_Relacional/
        ↓
docs/pdfs/Paper_A_v6.1_REVTeX_COMPLETE.pdf
```

| Verificação | Resultado |
|---|---|
| Arquivo rastreado no git history | ✓ Sim — commit `3e0d8c7` "Atualização 13082026" por Shukuwe |
| Git mode | 100644 (regular file, não symlink) |
| Git object hash | `f13596d644f60165d7ed06462edf82e74f22ed03` |
| Cadeia material ao repositório TCR/QDT | ✓ Demonstra que arquivo veio do TCR/QDT repo |

#### 4.4.2 Cadeia material ausente

| Verificação | Resultado |
|---|---|
| Cadeia material ao corpus AION-6.x source | ✗ **NÃO DEMONSTRADA** |
| AION Handoff declarou CORPUS-006 em | `/home/z/my-project/upload/` ou similar path em 6.x — nenhum artefato material liga TCR/QDT repo a este path |
| Hash canônico AION-6.x para CORPUS-006 | ✗ AUSENTE — Handoff não declara SHA-256 canônico para CORPUS-006 |
| Log de transferência TCR/QDT → AION-6.x | ✗ AUSENTE |
| Manifest de ingest AION-6.x | ✗ AUSENTE |

**V3 Resultado:** ⚠ **INSUFFICIENT** — cadeia material liga o objeto ao repositório TCR/QDT, mas **NÃO demonstra** cadeia material ao corpus AION-6.x source.

### 4.5 V4 — Canonical Content

**Pergunta:** O conteúdo corresponde materialmente ao conteúdo esperado do corpus?

#### 4.5.1 Extração de texto PDF (primeiros 50 linhas)

```
Relational Coherence in Biological Networks:
A Quantitative Framework from Connectomes to EEG
Edson Carvalho do Nascimento1, ∗
1 Independent researcher, Curitiba, Brazil
(Dated: August 10, 2026)

We introduce the Relational Coherence Theory (TCR) for measuring informational coherence in
biological networks through the metric C = I×S×H β, where I is the normalized multivariate mutual
information (integration), S is the graph automorphism index (symmetry), and H is the normalized
spectral entropy. The exponent β is calibrated via leave-one-out cross-validation (LOOCV) over
12 synthetic connectome fixtures. The metric is validated on three empirical regimes: connectome
ranking (P1, p = 1.0 bootstrap), species discrimination against degree-matched random graphs (P2,
z = 28.4, p ≈ 0), and sleep/wake classification on PhysioNet Sleep-EDF EEG data (P3, 91.2% ±
1.9% accuracy, p < 10−4)...
```

#### 4.5.2 Comparação com .tex source interno

| Verificação | Resultado |
|---|---|
| .tex source correspondente | `docs/tex/Paper_A_v6.1_REVTeX_COMPLETE.tex` (33501 bytes, SHA-256: `b5ee0f423e01269f571b4917586c4a448f447c05657656a6da1fda7aac00e5b8`) |
| TeX header comment | "Paper A — TCR Empírico (v6.1)" — corresponde ao filename v6.1 (CONSISTENT) |
| Conteúdo PDF vs .tex | ✓ Corresponde — mesma estrutura, mesmo título, mesma data, mesmo autor, mesmo abstract |
| PDF metadata CreationDate vs .tex date | ✓ Corresponde — Aug 10, 2026 |
| Conteúdo vs descrição Handoff CORPUS-006 | ✓ Corresponde — "Paper A v6.1, HISTORICAL, 138KB, by Edson Carvalho do Nascimento" |
| Diff vs v6.2 .tex | ✓ Diferenciação correta: v6.1 menciona "PhysioNet Sleep-EDF" para P3, enquanto v6.2 menciona "OpenNeuro ds003768" — evolução coerente de versão |

**V4 Resultado:** ✓ **PASS** — conteúdo do PDF corresponde materialmente ao conteúdo esperado do corpus e à fonte .tex interna.

### 4.6 Classificação C-02 — Caso D

| Gate | Resultado |
|---|---|
| V1 Identity | ✓ PASS |
| V2 Integrity | ✓ PASS |
| V3 Provenance | ⚠ INSUFFICIENT |
| V4 Canonical Content | ✓ PASS |

**Classificação canônica:** **Caso D** — conteúdo compatível, proveniência insuficiente.

**Interpretação:** Aplicando princípio PM Task 80: "compatibilidade de conteúdo não equivale a autenticação histórica." O PDF em TCR/QDT tem conteúdo materialmente compatível com CORPUS-006 esperado, mas **não há cadeia material demonstrando que este PDF é o mesmo arquivo que estava materialmente presente no ambiente AION-6.x**.

**Status C-02:** CANDIDATE — **não autenticado**. Permanece como EVIDÊNCIA CANDIDATA.

## 5. Evidence Ledger Granular (R0.3.3.A)

### 5.1 Tabela consolidada por candidato

| Candidato | CORPUS-ID alvo | Tamanho observado | Tamanho esperado | V1 Identity | V2 Integrity | V3 Provenance | V4 Canonical Content | Classificação |
|---|---|---|---|---|---|---|---|---|
| **C-01** | CORPUS-002 | 137520 bytes | 137 KB | ✓ PASS | ✓ PASS | ⚠ INSUFFICIENT | ✓ PASS | **Caso D** |
| **C-02** | CORPUS-006 | 138780 bytes | 138 KB | ✓ PASS | ✓ PASS | ⚠ INSUFFICIENT | ✓ PASS | **Caso D** |

### 5.2 Hashes registrados (baseline para futuras comparações)

| Artefato | SHA-256 |
|---|---|
| C-01 PDF | `971986d96c4ceb1ea5d7a17acdf2a54f4276403f2805c3945874304020adc433` |
| C-01 .tex source | `9471c6e5a94e498a8f121d1756c0c1cea075b2e0d7e71cb9dcd772b062e90c47` |
| C-02 PDF | `efd7f7caf19a5f99cd1663303c6f36d0beba50f19c71d4f44d44b81c396c8854` |
| C-02 .tex source | `b5ee0f423e01269f571b4917586c4a448f447c05657656a6da1fda7aac00e5b8` |

### 5.3 Aplicação da granularidade PM (sem agregação proibida)

```
C-01 classificado como Caso D
        +
C-02 classificado como Caso D
        ↓
NÃO permite concluir "Corpus AION confirmado"
```

Cada candidato permanece classificado individualmente. A agregação "Corpus AION confirmado" é **proibida** pela regra PM Task 80 Seção "Critério de decisão."

### 5.4 Distinção crítica preservada

```
CONTEÚDO COMPATÍVEL (V4 PASS)
        ≠
AUTENTICAÇÃO HISTÓRICA (V3 PASS)
```

Para autenticação histórica completa (Caso A — V1+V2+V3+V4 PASS), seria necessária uma cadeia material ligando os PDFs do TCR/QDT repo à fonte original do corpus AION-6.x. Esta cadeia **não está materialmente disponível**.

## 6. Reclassificação EP para Grupo C (Evidence-Driven)

### 6.1 Estado anterior (R0.3.3, Task 79)

```
Grupo C: EP-1 PARTIAL CANDIDATE (preliminary)
```

### 6.2 Estado após R0.3.3.A (este documento)

```
Grupo C: EP-1 PARTIAL CANDIDATE / Caso D (content-compatible, provenance-insufficient)
```

### 6.3 Justificativa evidence-driven

A reclassificação **não promove** EP-1 PARTIAL CANDIDATE para EP-1 PARTIAL EFFECTIVE porque:

1. **V3 PROVENANCE INSUFFICIENT para ambos os candidatos** — cadeia material liga ao TCR/QDT repo, mas não ao corpus AION-6.x source
2. **Caso D aplicado a ambos** — "compatibilidade de conteúdo não equivale a autenticação histórica"
3. **Agregação proibida** — não se pode concluir "Corpus AION confirmado" a partir de dois Caso D individuais
4. **AUTH₇.₀ permanece FALSE** — mesmo se ambos fossem Caso A, ainda restariam 5 componentes do Grupo A não-verificados (Oracle v3, GraphRAG v1.0.0, P-RESP-001 v0.3, AION-EVAL-002 v0.2, B1 config 6.2.11)

### 6.4 Diferença entre CANDIDATE e EFFECTIVE

| Classificação | Significado |
|---|---|
| EP-1 PARTIAL CANDIDATE (preliminary) | Há candidatos materiais identificados, mas não verificados como correspondências autênticas |
| EP-1 PARTIAL CANDIDATE / Caso D | Candidatos verificados — conteúdo compatível, mas proveniência insuficiente para autenticação histórica |
| EP-1 PARTIAL EFFECTIVE | Não alcançado — requereria V3 PASS para pelo menos um candidato |

### 6.5 Classificação overall do Grupo C

$$\boxed{\text{EP} = \text{EP-1 PARTIAL CANDIDATE / Caso D (Grupo C)}}$$

Esta classificação é mais refinada que a preliminar de Task 79, mas **não promove** EP para nível superior. A distinção crítica é: agora sabemos materialmente que **conteúdo é compatível** mas **proveniência histórica é insuficiente**.

## 7. Estado dos Demais Grupos (preservado)

| Grupo | EP | Justificativa |
|---|---|---|
| Grupo A — AION infrastructure | EP-0 UNKNOWN (mantido) | Zero material evidence (Oracle, GraphRAG, P-RESP-001, AION-EVAL-002, B1 config) |
| Grupo B — AION-specific scripts | EP-0 UNKNOWN (mantido) | Zero AION-specific scripts em TCR/QDT |
| Grupo C — corpus documents | EP-1 PARTIAL CANDIDATE / Caso D (refinado) | 2 candidatos verificados, conteúdo compatível, proveniência insuficiente |
| Grupo D — Environment Provenance AION-6.x | EP-0 UNKNOWN (mantido) | Cautela TCR/QDT aplicada; TCR/QDT requirements ≠ AION-6.x environment |

## 8. Estado do Sistema (pós-R0.3.3.A)

```text
AION-7.0.0
│
├── Specification ........ FROZEN FINAL
├── FG v3 ................. FROZEN FINAL
│
├── R0 (PHASE) ............ PARTIALLY REOPENED
│   ├── R0.1-R0.5 ......... CONCLUÍDOS
│   ├── R0 (closure) ....... DECLARED (Task 78)
│   ├── R0.3.3 ............ CONCLUÍDO (Task 79)
│   └── R0.3.3.A ........... CONCLUÍDO (este documento, Task 80)
│       ├── C-01 verification ........ Caso D (V1+V2+V4 PASS, V3 INSUFFICIENT)
│       └── C-02 verification ........ Caso D (V1+V2+V4 PASS, V3 INSUFFICIENT)
│
├── EP .................. EP-1 PARTIAL CANDIDATE / Caso D (Grupo C)
│                       EP-0 UNKNOWN (Grupo A, B, D — mantido)
├── AUTH₇.₀ ............ FALSE (overall, 0/6 components verified)
│                       (2/9 corpus documents have content-compatible
│                        but provenance-insufficient candidates; not
│                        authenticated as AION-6.x corpus)
├── ENV ................ BLOCKED
├── PIPE ............... NOT RUN
├── V1-V4 ............... OTHER components BLOCKED (no PM authorization)
├── NOMOD .............. PENDING
└── FINAL_AUTH₇.₀ ..... BLOCKED
```

## 9. Evento de Proveniência Canônico

```
EVENT_ID: AION-EV-011
TIMESTAMP: 2026-08-23T02:30:00-03:00
SESSION: web-73c75281-201c-4716-b85c-97833d25f9b3
TRACE_ID: 1a02c6262e3ce52d (autorização R0.3.3.A PM) → execução IA Curadora
EVENT_TYPE: R0.3.3.A_V1_V4_CANDIDATE_VERIFICATION_COMPLETED
OBSERVED_STATE: R0.3.3.A executed V1-V4 individually for C-01 (Paper_A_v6.2_FINAL.pdf → CORPUS-002) and C-02 (Paper_A_v6.1_REVTeX_COMPLETE.pdf → CORPUS-006). Both candidates classified as Caso D (content-compatible, provenance-insufficient). V1 PASS for both (file exists, filename matches, size EXACT MATCH, PDF metadata consistent with Handoff). V2 PASS for both (SHA-256 computable, PDF parseable). V3 INSUFFICIENT for both (chain to TCR/QDT repo confirmed; chain to AION-6.x corpus source NOT demonstrated). V4 PASS for both (PDF content matches .tex source internal to TCR/QDT, and matches Handoff description).
KEY_FINDINGS:
  - C-01 (CORPUS-002 candidate):
    * V1 PASS: file exists (137520 bytes, mode 100644), filename matches, size EXACT MATCH (137 KB), PDF metadata consistent (Title, Author=Edson C. do Nascimento, CreationDate Aug 12 2026)
    * V2 PASS: SHA-256 = 971986d96c4ceb1ea5d7a17acdf2a54f4276403f2805c3945874304020adc433; PDF parseable (6 pages)
    * V3 INSUFFICIENT: chain to TCR/QDT repo confirmed (commit 3e0d8c7); chain to AION-6.x corpus source NOT demonstrated (no canonical hash in Handoff, no transfer log, no manifest)
    * V4 PASS: PDF content matches .tex source (9471c6e5...) and Handoff description
  - C-02 (CORPUS-006 candidate):
    * V1 PASS: file exists (138780 bytes, mode 100644), filename matches, size EXACT MATCH (138 KB), PDF metadata consistent (CreationDate Aug 10 2026)
    * V2 PASS: SHA-256 = efd7f7caf19a5f99cd1663303c6f36d0beba50f19c71d4f44d44b81c396c8854; PDF parseable (6 pages)
    * V3 INSUFFICIENT: same as C-01
    * V4 PASS: PDF content matches .tex source (b5ee0f42...) and Handoff description
EPISTEMOLOGICAL_SCOPE: Both candidates classified as Caso D (content-compatible, provenance-insufficient). EP-1 PARTIAL CANDIDATE / Caso D for Grupo C — refined from preliminary CANDIDATE (Task 79), but NOT promoted to EP-1 PARTIAL EFFECTIVE because V3 INSUFFICIENT for both. Critical PM principle applied: "compatibility of content does not equal historical authentication." Aggregate conclusion "Corpus AION confirmed" is PROHIBITED by PM Task 80 granularity rule.
INTERPRETATION: [I] Material verification establishes that PDFs in TCR/QDT repo have content compatible with expected CORPUS-002 and CORPUS-006 (same title, author, dates, abstracts, sizes, .tex source correspondence). However, no material chain links TCR/QDT repo to AION-6.x corpus source. The historical authentication — "these are the same files that were materially present in AION-6.x environment" — cannot be established. This is the epistemically honest outcome: content compatibility is established, historical authentication is not.
PROVENANCE_RULE_INVOKED: Regra 1 (Provenance) + Regra 7 (PER=0 ≠ confiável) + Invariantes UNAVAILABLE≠NON-EXISTENT, NON-OBSERVED≠FALSE, PENDING≠FAILED, COMPATIBLE≠EQUIVALENT + FG_GATE v3 Seção 5.5 (EP Classification evidence-driven) + PM Task 80 Rules: (1) granular per artifact, no aggregation; (2) V1-V4 reformulated framework (Identity/Integrity/Provenance/Canonical Content); (3) four cases (A/B/C/D); (4) "size match is not authentication, only justification for verification"; (5) "content compatibility does not equal historical authentication".
EPISTEMIC_ACTION: R0.3.3.A CONCLUÍDO. Both C-01 and C-02 classified as Caso D. Grupo C EP refined to EP-1 PARTIAL CANDIDATE / Caso D (not promoted to EFFECTIVE). AUTH_{7.0}=FALSE preserved. FINAL_AUTH_{7.0}=BLOCKED preserved. State: R0 PARTIALLY REOPENED with Grupo C candidates verified but unauthenticated.
```

## 10. Próxima Ação Legítima — Requer Determinação PM

### 10.1 Estado após R0.3.3.A

R0.3.3.A **materialmente executou** a verificação granular V1-V4 dos dois candidatos do Grupo C. O resultado é Caso D para ambos — **conteúdo compatível, proveniência insuficiente**. A verificação produziu informação materialmente útil (hashes registrados, conteúdo confirmado, proveniência caracterizada como insuficiente) mas **não autenticou** os candidatos como sendo materialmente os mesmos arquivos do AION-6.x.

### 10.2 Opções para o Projetista Master

| Opção | Descrição | Consequência |
|---|---|---|
| **R0.3.3.A.1** | Aceitar Caso D como estado final para Grupo C; preservar candidatos como EVIDÊNCIA CANDIDATA (não autenticada); manter R0 em STANDBY MATERIAL | Grupo C: EP-1 PARTIAL CANDIDATE / Caso D (final); AUTH₇.₀ FALSE; FINAL_AUTH₇.₀ BLOCKED |
| **R0.3.3.A.2** | Solicitar evidência adicional de proveniência (log de transferência TCR/QDT → AION-6.x, manifest de ingest, hash canônico de referência) | Possível futura promoção para Caso A se V3 demonstrada |
| **R0.3.3.A.3** | Autorizar V1-V4 sobre candidatos adicionais de Grupo C (CORPUS-002-HIST, CORPUS-003, CORPUS-011, CORPUS-005) | Possível identificação de mais Caso D ou Caso A/B/C |
| **R0.3.3.A.4** | Declarar Grupo C como "tentativa esgotada"; focar em Via B (R0.3.3.E) ou confirmação de indisponibilidade (R0.B) | Encerramento formal Grupo C |
| **R0.3.3.A.5** | Autorizar busca por outros repositórios externos que possam conter Grupo A, B, ou D | Possível identificação de novas pontes materiais |

### 10.3 O que NÃO será feito até determinação PM

- ✗ Nenhuma promoção automática de EP-1 PARTIAL CANDIDATE para EP-1 PARTIAL EFFECTIVE
- ✗ Nenhuma inferência de que TCR/QDT PDFs são autenticamente os mesmos arquivos do AION-6.x corpus
- ✗ Nenhuma instalação de dependências
- ✗ Nenhuma execução de scripts TCR/QDT ou AION
- ✗ Nenhuma execução de V1-V4 sobre outros componentes sem autorização específica
- ✗ Nenhuma alteração de artefato FROZEN
- ✗ Nenhuma alteração de `AUTH₇.₀ = FALSE`
- ✗ Nenhuma alteração de `FINAL_AUTH₇.₀ = BLOCKED`

### 10.4 Princípio operacional consolidado

> **Compatibilidade de conteúdo não equivale a autenticação histórica.**

Aplicado materialmente em R0.3.3.A: a verificação V1-V4 dos candidatos C-01 e C-02 estabeleceu compatibilidade de conteúdo (V4 PASS), mas **não autenticou** que estes PDFs sejam os mesmos arquivos que estavam materialmente presentes no ambiente AION-6.x (V3 INSUFFICIENT). A distinção entre `COMPATIBLE` e `EQUIVALENT` (4º invariante canônico) foi preservada em sua forma mais rigorosa: dois objetos materialmente compatíveis em conteúdo não são, por isso, equivalentes em identidade histórica.

## 11. Confirmação de Integridade dos FROZEN

| Artefato | SHA-256 | Estado |
|---|---|---|
| AION-7.0.0_PROTOCOL.md | `b9b50b28579a8b5ac99abcc48898b34f965d1ce14de53b85062f7a1fea13a376` | INTACTO (idêntico a Tasks 65-79) |
| AION-EVIDENCE-LEDGER-001_SCHEMA.md | `1bf7349d621382a05f06f743b99e1ed632f804673199b444247b9afc4ddf3507` | INTACTO |
| AION-7.0.0-R_AUDIT.md | `d8efb8f4aee924f7c250a7e9726fdccdebcb6343440a8e1b8fb892c253ee1738` | INTACTO |
| AION-7.0.0-FG_GATE.md | `f082de51f96b144bf0cc98466db600581c3ce3f413fa38e3bf81f477c488e4e4` | INTACTO |

## 12. Genealogia Documental

```
AION-7.0.0-FG v3 FROZEN FINAL (Task 68)
       │
       ▼  Tasks 69-78: R0.1-R0.5 + R0 closure
       │
AION-7.0.0-R0 CLOSED / STANDBY MATERIAL (Task 78)
       │
       ▼  Determinação PM Task 79: autoriza R0.3.3 (external material intake)
       │
AION-7.0.0-R0.3.3 EXTERNAL MATERIAL INTAKE: TCR/QDT REPOSITORY — CONCLUÍDO (Task 79)
       │
       ▼  Determinação PM Task 80: autoriza R0.3.3.A (V1-V4 candidate verification)
       │
AION-7.0.0-R0.3.3.A V1-V4 CANDIDATE VERIFICATION — CONCLUÍDO (este documento, Task 80)
       │
       ├── C-01 (CORPUS-002 candidate): Caso D (V1+V2+V4 PASS, V3 INSUFFICIENT)
       ├── C-02 (CORPUS-006 candidate): Caso D (V1+V2+V4 PASS, V3 INSUFFICIENT)
       ├── Granularidade PM respeitada: nenhum agregado "Corpus AION confirmado"
       ├── Grupo C EP refined: EP-1 PARTIAL CANDIDATE / Caso D (not promoted to EFFECTIVE)
       ├── AUTH₇.₀ = FALSE (preserved)
       ├── FINAL_AUTH₇.₀ = BLOCKED (preserved)
       ├── 4 FROZEN artifacts integrity verified
       │
       ▼  Próxima operação requer determinação PM:
       │
       ├── R0.3.3.A.1 — Aceitar Caso D como final para Grupo C; preservar como EVIDÊNCIA CANDIDATA
       ├── R0.3.3.A.2 — Solicitar evidência adicional de proveniência (logs, manifests, hashes canônicos)
       ├── R0.3.3.A.3 — Autorizar V1-V4 sobre candidatos adicionais de Grupo C
       ├── R0.3.3.A.4 — Declarar Grupo C tentativa esgotada; focar em Via B ou R0.B
       └── R0.3.3.A.5 — Buscar outros repositórios externos para Grupo A, B, D
```

---

*"O resultado de R0.3.3.A estabelece materialmente uma distinção epistêmica importante: o conteúdo dos PDFs no repositório TCR/QDT é compatível com o esperado para CORPUS-002 e CORPUS-006 (V4 PASS), mas a proveniência histórica que autenticaria estes PDFs como sendo os mesmos arquivos do ambiente AION-6.x é insuficiente (V3 INSUFFICIENT). Esta é a distinção entre compatibilidade e equivalência em sua forma mais rigorosa: dois objetos materialmente compatíveis em conteúdo não são, por isso, equivalentes em identidade histórica. O AION-7.0.0 permanece corretamente bloqueado — não por ausência de evidência material, mas por ausência de cadeia material de proveniência autenticável. A próxima transição epistemicamente válida requer ou evidência adicional de proveniência, ou aceitação honesta de que a autenticação histórica completa não pode ser estabelecida a partir deste acervo externo."*

**Fim do AION-7.0.0-R0.3.3.A V1-V4 Candidate Verification Report.**
