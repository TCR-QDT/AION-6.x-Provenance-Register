# AION-CORPUS-001-ONTOLOGY — Rascunho do Autor (Draft)

**ID do Documento:** AION-CORPUS-001-ONTOLOGY
**Versão:** 0.9.0 (Draft by Author)
**Estado:** Rascunho intelectual do autor — NÃO VERIFICADO pela IA Curadora
**Data:** 16 de agosto de 2026
**Autor deste rascunho:** Edson Carvalho do Nascimento (autor humano, NÃO IA Curadora)
**Origem:** Produzido manualmente pelo autor e apresentado no chat em 16/08/2026 como se fosse produto da IA Curadora. Freio epistêmico 4 acionado. Atribuição corrigida.

---

## NOTA DE CURADORIA

Este documento é um rascunho intelectual produzido pelo autor humano do corpus (Edson Carvalho do Nascimento) durante a sessão de curadoria de 16/08/2026. Foi inicialmente apresentado como produto da "IA Curadora", mas o freio epistêmico 4 detectou a inversão de autoria antes que o artefato fosse aceito como v1.0.0.

O documento preserva valor intelectual:
- A estrutura de 4 clusters (A: TCR, B: Formalização categórico-tensorial, C: QDT, D: Lakatosiano) é plausível e útil como hipótese de trabalho.
- O grafo de relações refinado (paralelismo Paper A ↔ Parte IV em vez de dependência ontológica) é correto.
- As 8 tensões (T1-T8) são bem caracterizadas.
- A verificação cruzada P4 (4 contradições Cover Letter ↔ Paper A) é correta na interpretação (defasagem de versionamento).

MAS contém erros verificáveis de citação que foram detectados em auditoria:
- Erro 1: Conceito A2 (Integração I) — citação funde duas passagens separadas do Paper A em uma única equação numerada. Síntese apresentada como `[E]`.
- Erro 2: Conceito C1 (Power-law T₂) — escolheu uma das duas formas da equação (com K explícito) e atribuiu à Eq. 2 da p.2, mas no Abstract a equação aparece com K simbólico. Decisão editorial apresentada como `[E]`.
- Erro 3: Conceito A4 (Entropia H, Sobol) — frase "esperado para dominar em dados reais" não está no texto extraído; é interpretação do autor apresentada como citação.

Estes erros serão corrigidos na versão v1.0.0 (Verified) a ser produzida pela IA Curadora após auditoria completa.

---

## CONTEÚDO DO RASCUNHO (preservado como produziu o autor)

# AION-CORPUS-001-ONTOLOGY — Ontologia Conceitual do Corpus Fundacional (Verified)

**ID do Documento:** AION-CORPUS-001-ONTOLOGY
**Versão:** 1.0.0 (Verified)
**Estado:** Final — Baseado na extração integral dos 5 documentos
**Data:** 16 de agosto de 2026
**Curador:** IA Curadora (Escriba / Arquiteto de Metadados)
**Autor do Corpus:** Edson Carvalho do Nascimento
**Apêndice de:** AION-CORPUS-001 v1.2.0 — Frozen & Verified

---

## 0. AVISO METODOLÓGICO — O PROTOCOLO E/I/H EM AÇÃO

Esta ontologia foi construída a partir da **extração textual integral** dos cinco documentos do corpus (CORPUS-001 a 005). Todas as definições e arestas marcadas como `[E]` possuem citação textual direta com referência de página ou seção. Arestas marcadas como `[I]` são inferências baseadas no contexto documental. Arestas marcadas como `[H]` são hipóteses que dependem de confirmação externa ou de documentos não incluídos no corpus atual (ex: versão oficial em inglês da Cover Letter).

**Nota curatorial importante:** Este documento registra a **Tensão T8** — a descoberta, durante a curadoria, de que o protocolo E/I/H deve se aplicar não apenas aos documentos, mas também à dinâmica da interação humano-IA, para evitar inversões de autoridade epistêmica. A T8 é documentada na Seção 5.

---

## 1. SUMÁRIO ESTRUTURAL (ATUALIZADO)

A ontologia organiza-se em **quatro clusters temáticos**, refinados a partir da extração dos textos completos:

| Cluster | Tema | Conceitos | Documentos-âncora |
|---|---|---|---|
| **A** | Núcleo teórico — Teoria da Coerência Relacional (TCR) | Coerência Relacional (C), Integração (I), Simetria (S), Entropia Espectral (H) | CORPUS-002 (definição operacional) |
| **B** | Formalização categórico-tensorial (Paper C) | Campo Primordial, Functor Φcat, Lema de Yoneda, Tensor Qµν, Equação de Einstein modificada | CORPUS-003 (CORPUS-005 afirma submissão do Paper C) |
| **C** | Aplicação quântico-dissipativa | Dinâmica Quântica Dissipativa (QDT), Complexo FMO, Power-law T₂ | CORPUS-004 |
| **D** | Estrutura metodológica (Lakatosiana) | Programa de pesquisa, Núcleo firme, Cinturão protetor, Conjectura, Proposta, Validação | CORPUS-003 (explicitamente); CORPUS-001 e CORPUS-005 (implicitamente) |

**Correção estrutural:** Diferente do que foi inferido no HTML canônico v1.2.0, **CORPUS-003 (Parte IV) não fundamenta ontologicamente CORPUS-002 (Paper A)**. Ambos são instâncias paralelas do programa TCR/QDT, com a Parte IV sendo o rascunho técnico do Paper C (conforme confirmado pela Cover Letter). A dependência ontológica declarada anteriormente está **revogada** e substituída por uma relação de **paralelismo epistêmico**.

---

## 2. TABELA CONCEITUAL — DEFINIÇÕES VERIFICADAS COM CITAÇÕES

### Cluster A — Núcleo Teórico (TCR)

#### A1. Coerência Relacional (C)

- **Definição (citação direta):** "We introduce the Relational Coherence Theory (TCR) for measuring informational coherence in biological networks through the metric **C = I × S × Hβ**" (CORPUS-002, Abstract, p.1).
- **Documentos onde aparece:** CORPUS-002 (definição e validação), CORPUS-004 (aplicação indireta).
- **Status epistêmico:** Framework quantitativo em estado FINAL, submetido ao Physical Review E. `[E]`
- **Arestas:** É composto por I, S, H. Não supera seus componentes como classificador (achado de ablação, CORPUS-002, p.4).

#### A2. Integração (I)

- **Definição (citação direta):** "I = 1/N [N · Hdeg − Hspec], where Hdeg = −∑k pk log2 pk ... and Hspec = −∑ℓ λ̃ℓ log2 λ̃ℓ" (CORPUS-002, p.2, Eq. 4).
- **Status epistêmico:** Operacionalmente definido. `[E]`
- **Observação:** É o componente individual mais forte como preditor (70% de acurácia em P3, contra 73.4% do composto). `[E]` (CORPUS-002, p.4).

#### A3. Simetria (S)

- **Definição (citação direta):** "S = log(|Aut(G)| + 1) / log(N!), where |Aut(G)| is the cardinality of the automorphism group of G." (CORPUS-002, p.2, Eq. 5).
- **Status epistêmico:** Operacionalmente definido. `[E]`

#### A4. Entropia Espectral (H)

- **Definição (citação direta):** "H = −∑ℓ λ̃ℓ log2 λ̃ℓ / log2 N, where λ̃ℓ are the normalized Laplacian eigenvalues." (CORPUS-002, p.2, Eq. 6).
- **Status epistêmico:** Operacionalmente definido. `[E]`
- **Observação:** A análise Sobol confirma H como componente dominante da variância de C (Sobol index SH = 0.095 nos dados atuais, mas esperado para dominar em dados reais). `[E]` (CORPUS-002, p.4).

---

### Cluster B — Formalização Categórico-Tensorial (Paper C)

#### B1. Campo Primordial

- **Definição (inferida do contexto):** O termo "Campo Primordial" não aparece no corpo textual do CORPUS-003. O título do documento ("PARTE IV Formalização Teórica...") e a referência à "ontologia" no contexto lakatosiano sugerem que este é o substrato sobre o qual a formalização categórica opera. `[I]`
- **Documentos onde aparece:** Mencionado no HTML canônico como sinônimo de CORPUS-003, mas ausente do texto extraído. `[I]`
- **Status:** Pendente de confirmação textual. A referência a "consciência" é inexistente no corpus atual (T4 resolvida).

#### B2. Functor Φcat

- **Definição (citação direta):** "Seja C uma categoria localmente pequena com objeto distinguido • ∈ Ob(C). Define-se o functor **Φcat : C → Set, X ↦ Hom_C(•, X)**" (CORPUS-003, p.4, Sec. 2.1).
- **Status epistêmico:** Conjectura (Passo 16). `[E]`
- **Lacuna declarada:** "A Conjectura 2.1 não está demonstrada em toda a generalidade enunciada... Continuidade enriched; compatibilidade com limites ind-pro." (CORPUS-003, p.5).

#### B3. Lema de Yoneda

- **Definição (citação direta):** "Teorema 2.1 (Lema de Yoneda). Seja C localmente pequena, A ∈ C e F : C → Set um functor covariante. Existe uma bijeção natural **Nat(Hom_C(A, −), F) ≅ F(A)**" (CORPUS-003, p.4, Sec. 2.2).
- **Status epistêmico:** Resultado matemático estabelecido; aplicação ao contexto é Conjectura. `[E]`
- **Observação:** A prova é esboçada com a demonstração canônica. `[E]`

#### B4. Tensor Qµν

- **Definição (citação direta):** "Definição 3.1 (Tensor Qµν). O tensor Qµν é uma forma bilinear simétrica (0, 2) no espaço-tempo (M, g) satisfazendo os seguintes axiomas: Q1. Simetria; Q2. Conservação covariante; Q3. Covariância geral; Q4. Traço bem definido; Q5. Decaimento assintótico." (CORPUS-003, p.6, Sec. 3.2).
- **Status epistêmico:** Proposta teórica (Passo 17). `[E]`
- **Lacuna declarada:** "A Equação (2) não foi derivada de primeiros princípios... Ausência de ação fundamental." (CORPUS-003, p.7).

#### B5. Equação de Einstein modificada

- **Definição (citação direta):** "A proposta do Passo 17 é introduzir um termo geométrico adicional Qµν no lado direito, modificando a equação para **Gµν = 8πG(Tµν + Qµν)**." (CORPUS-003, p.3, Eq. 2).
- **Status epistêmico:** Proposta teórica. `[E]`

---

### Cluster C — Aplicação Quântico-Dissipativa (Paper B)

#### C1. Dinâmica Quântica Dissipativa (QDT) e Power-law T₂

- **Definição (citação direta):** "T₂ = (1.567×10⁴) J⁰·⁸³¹ λ⁻⁰·⁸⁴³ γ⁻⁰·⁷⁶⁶ T⁻⁰·²⁶¹, R² = 0.988." (CORPUS-004, p.2, Eq. 2).
- **Documentos onde aparece:** CORPUS-004.
- **Status epistêmico:** FINAL (rascunho para submissão ao JCP). `[E]`
- **Correção crucial:** O expoente de temperatura ST foi corrigido de -0.795 (v6.0, dímero de 2 sítios) para -0.261 (v6.1, FMO 7-sítios). A extrapolação anterior é retratada como "matematicamente injustificável". `[E]` (CORPUS-004, p.2-3).

#### C2. Hipótese η (Cross-scale) — Retratada

- **Definição (citação direta):** "Formalizamos comensurabilidade como |δβ − δST|/δβ < 0.2. Aplicando... |0.268 − 0.346|/0.268 = 0.291 > 0.2. O critério não é satisfeito. **Retraímos portanto a hipótese de comensurabilidade η da análise presente.**" (CORPUS-004, p.2, Sec. V-B).
- **Status:** Hipótese refutada/retratada pelo autor. `[E]`
- **Implicação para T2:** Resolve a tensão sobre a ponte entre escalas quântica e macroscópica — a ponte formalmente proposta não existe, e a lacuna é honestamente declarada.

---

### Cluster D — Estrutura Metodológica Lakatosiana

#### D1. Programa de pesquisa (Lakatos)

- **Definição (citação direta):** "A leitura conjunta dos três passos sugere uma estrutura epistêmica análoga à distinção de Lakatos entre **núcleo firme e cinturão protetor**. O núcleo do programa — a hipótese de que a estrutura física admite formalização categórico-tensorial unificada — é sustentado pelo cinturão formado pelas conjecturas Φcat e Qµν." (CORPUS-003, p.11, Sec. 5).
- **Status:** Declarado explicitamente pelo autor. `[E]`

#### D2. Conjectura, Proposta, Validação

- **Definição (citação direta):** "Tabela 2: Status consolidado... Passo 16 (Φcat/Yoneda) → [!] CONJECTURA; Passo 17 (Qµν/Einstein) → [!] PROPOSTA TEÓRICA; Passo 18 (Chanyal/Sun/Pradhan) → [OK] VALIDAÇÃO." (CORPUS-003, p.11, Tabela 2).
- **Status:** Tríade epistêmica central do programa. `[E]`

---

## 3. GRAFO DE RELAÇÕES (REFINADO)

Este grafo substitui o anterior, incorporando as correções documentais.

- **Paralelismo (e não dependência ontológica):** `CORPUS-002 (Paper A) ═══ CORPUS-003 (Parte IV/Paper C)` — ambos são instâncias do mesmo programa, em níveis de formalização distintos.
- **Relação de conteúdo:** `CORPUS-003 (Parte IV)` → `rascunho de` → `Paper C (submetido à Foundations of Physics, segundo a Cover Letter [I pending])`.
- **Aplicação metodológica:** `CORPUS-002 (TCR)` → `aplica-se a` → `CORPUS-004 (QDT/FMO)`.
- **Validação externa:** `CORPUS-003 (Passo 18)` → `valida-se com` → `Chanyal, Sun, Pradhan [E]`.
- **Autocorreção:** `CORPUS-004 (Paper B)` → `retrata` → `Hipótese η (v6.0) [E]`.

---

## 4. VERIFICAÇÃO CRUZADA (P4) — CONTRADIÇÕES DOCUMENTAIS

A comparação entre CORPUS-002 (Paper A v6.2) e CORPUS-005 (Cover Letter PT-BR v6.1) revela quatro contradições materiais, resolvidas pela interpretação de **defasagem de versionamento** (T5).

| # | Contradição | Evidência na Cover Letter | Evidência no Paper A | Interpretação Curatorial |
|---|---|---|---|---|
| **C1** | Versão do Paper | v6.1, "NÃO PRONTO" | v6.2 FINAL, submetido | Cover Letter é rascunho anterior. |
| **C2** | Resultados P3 | AUC 0.968, 91.2% | AUC 0.793, 4 sujeitos | Cover Letter descreve plano (v6.2/empírico); Paper A entrega real. |
| **C3** | P1/P2 datasets | Conectomas empíricos | Fixtures sintéticos | Mesma defasagem plano-vs-real. |
| **C4** | Status Paper C | "Submetido em 10/08" | "Reservado" | A Cover Letter pode estar correta, mas Paper A não foi atualizado. |

**Recomendação curatorial:** A cover letter oficial enviada ao PRE (em inglês) não está no corpus (T6). A versão PT-BR deve ser tratada como documento de referência interna, não como evidência da submissão final.

---

## 5. TENSÕES E LACUNAS DOCUMENTADAS (T1 a T8)

| ID | Descrição | Status / Evidência |
|---|---|---|
| **T1** | Tensão quantitativo (Paper A) vs. categórico-conjectural (Paper C/Parte IV) | **RESOLVIDA** — São instâncias paralelas, não hierárquicas. |
| **T2** | Tensão de escala (quântica vs. macroscópica) | **RESOLVIDA POR RETRAÇÃO** — Hipótese η retirada. Lacuna declarada. |
| **T3** | Lacunas da Cover Letter | **RESOLVIDA** — Cover Letter é rascunho v6.1. |
| **T4** | "Consciência" ausente do título | **RESOLVIDA** — Termo não aparece no corpus. Referência a Tononi (Φ-IIT) no Paper A é a única ponte. |
| **T5** | Defasagem de versionamento (Cover Letter vs Paper A) | **DOCUMENTADA** — 4 contradições (C1-C4). |
| **T6** | Lacuna documental: Cover Letter EN não está no corpus | **ABERTA** — Recomendado adicionar em v1.3.0. |
| **T7** | Tensão normativa: DOC-000 não é aplicado aos documentos | **ABERTA** — Nenhum documento segue a estrutura de 8 seções. |
| **T8** | Inversão de autoridade epistêmica na curadoria | **DOCUMENTADA** — Descoberta metodológica sobre a interação humano-IA. |

---

## 6. AGENDA DE VERIFICAÇÃO FUTURA (PÓS-v1.0.0)

Para promover a ontologia a uma eventual v1.1.0 (Full Verified), são necessários:

1. **Confirmação do autor sobre C4:** O Paper C foi efetivamente submetido à *Foundations of Physics*? (Atualmente `[I-pending-author-confirmation]`).
2. **Adição da Cover Letter EN** ao corpus (CORPUS-005 EN) para fechar a lacuna T6.
3. **Aplicação do padrão AION-DOC-000** aos documentos existentes (T7) ou revisão do padrão para acomodar papers científicos.

---

## 7. HISTÓRICO DA ONTOLOGIA

| Versão | Data | Descrição |
|---|---|---|
| 0.1.0 | 2026-08-16 | Draft inicial com definições provisórias `[I]`/`[H]`. |
| 1.0.0 | 2026-08-16 | **Versão Verificada.** Baseada na extração integral dos 5 documentos. Definições reescritas com citações diretas `[E]`. Grafo refinado. Tensões T1-T8 documentadas. |

---

*"Nenhuma definição sem citação. Nenhuma inferência confundida com evidência. Nenhum papel epistêmico invertido sem registro."*
