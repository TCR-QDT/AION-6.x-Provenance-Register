# AION-CORPUS-001-ONTOLOGY — Ontologia Conceitual do Corpus Fundacional

**ID do Documento:** AION-CORPUS-001-ONTOLOGY
**Versão:** 0.1.0 (Draft)
**Estado:** Pendente de validação pelo autor
**Data:** 16 de agosto de 2026
**Curador:** IA Curadora (Escriba / Arquiteto de Metadados)
**Autor do Corpus:** Edson Carvalho do Nascimento
**Apêndice de:** AION-CORPUS-001 v1.2.0 — Frozen & Verified

---

## 0. AVISO EPISTEMOLÓGICO — LEIA ANTES DE USAR

**Limitação de material-fonte declarada.** Esta ontologia foi construída exclusivamente a partir dos seguintes materiais efetivamente fornecidos na conversa até a presente data:

1. O HTML canônico `AION-CORPUS-001 v1.2.0 — Frozen & Verified`, que contém metadados verificados de cada um dos 5 documentos, suas relações ontológicas/metodológicas declaradas e uma lista de 12+ conceitos transversais.
2. O Handoff Document original, que registra o histórico de curadoria.
3. Os títulos e metadados de cada documento (extraídos da página de rosto / cabeçalho / tags `<meta>`).

**Não foi fornecido nesta sessão o corpo textual completo** de Paper A, Paper B, Parte IV, Cover Letter ou DOC-000. Em consequência, esta v0.1.0 da ontologia opera sob uma restrição forte: as **definições provisórias** dos conceitos são, em sua maioria, inferências `[I]` baseadas nos títulos (que são bastante descritivos no caso de Edson) ou hipóteses `[H]` baseadas em conhecimento de domínio público sobre os termos técnicos empregados (Yoneda, tensor métrico, FMO, Lakatos). Nenhuma definição provisória deve ser tratada como citação textual do autor — isso só será possível após a ingestão dos textos completos no Passo 3 (Docling) e sua verificação no Passo 4 (AnythingLLM).

Esta limitação não é um defeito do processo; é, ela própria, um dado. Ela demonstra que o protocolo E/I/H está funcionando: quando não há texto-fonte, declaramos a ausência e marcamos como `[I]` ou `[H]`, jamais como `[E]`. A versão v1.0.0 desta ontologia só será declarada quando cada definição puder ser reescrita com citação direta extraída do corpus ingestado.

---

## 1. SUMÁRIO ESTRUTURAL

A ontologia organiza-se em **quatro clusters temáticos**, derivados diretamente dos títulos e relações declaradas no HTML canônico v1.2.0:

| Cluster | Tema | Conceitos | Documentos-âncora |
|---|---|---|---|
| **A** | Núcleo teórico — Teoria da Coerência Relacional (TCR) | Coerência Relacional | CORPUS-002 (definição operacional), CORPUS-003 (fundamentação ontológica) |
| **B** | Formalização categórico-tensorial | Campo Primordial, Functor Φcat, Lema de Yoneda, Tensor Qµν, Equação de Einstein modificada | CORPUS-003 |
| **C** | Aplicação quântico-dissipativa | Dinâmica Quântica Dissipativa (QDT), Complexo FMO | CORPUS-004 |
| **D** | Estrutura metodológica (Lakatosiana) | Lakatos, Programa de pesquisa, Conjectura, Proposta, Validação | CORPUS-003 (explicitamente); CORPUS-001, CORPUS-005 (implicitamente) |

A divisão em clusters não é arbitrária; ela reflete a estrutura epistêmica já declarada pelo autor no HTML v1.2.0: CORPUS-002 (Paper A) é o framework quantitativo que aplica TCR, CORPUS-003 (Parte IV) fornece a formalização teórica de fundo, e CORPUS-004 (Paper B) é uma instância aplicada ao regime quântico-dissipativo. O cluster D atravessa todos os documentos, mas é explicitamente invocado na Parte IV através da sequência Passo 16 (Conjectura) → Passo 17 (Proposta) → Passo 18 (Validação).

---

## 2. TABELA CONCEITUAL — DEFINIÇÕES, PROVENIÊNCIA E STATUS

### Cluster A — Núcleo Teórico (TCR)

#### A1. Coerência Relacional

- **Documentos onde aparece:** CORPUS-002 (núcleo), CORPUS-003 (fundamentação), CORPUS-004 (aplicação).
- **Definição provisória:** Conceito central da Teoria da Coerência Relacional (TCR), apresentado no Paper A como um framework quantitativo para descrever coerência em redes biológicas, indo de conectomes a sinais de EEG. `[I]` — inferido do título de CORPUS-002: "*Relational Coherence in Biological Networks: A Quantitative Framework from Connectomes to EEG*".
- **Status epistêmico:** Framework quantitativo em estado FINAL, submetido ao Physical Review E. `[E]` — declarado na página de rosto.
- **Relações declaradas:** Fundamenta-se ontologicamente em Campo Primordial (B1) e é operacionalizada metodologicamente pela Dinâmica Quântica Dissipativa (C1). `[E]` — declarado no HTML v1.2.0, seção 3.
- **Lacuna para v1.0.0:** Definição formal, equação operacional e métrica quantitativa precisam ser extraídas do corpo de CORPUS-002.

---

### Cluster B — Formalização Categórico-Tensorial

#### B1. Campo Primordial

- **Documentos onde aparece:** CORPUS-003 (âncora). No Handoff original, este conceito também era associado ao Documento 3 como subtítulo descritivo ("Nível 0 — Campo Primordial da Consciência"). `[E]`
- **Definição provisória:** Noção ontológica de um campo fundamental que dá unidade ao sistema teórico — possivelmente a base sobre a qual a TCR opera e da qual a formalização categórica (Functor Φcat) extrai estrutura. `[I]` — inferido do título e da dependência ontológica declarada em CORPUS-002 → CORPUS-003.
- **Status epistêmico:** Provavelmente conjectural ou proposicional (a confirmar). `[H]` — hipótese baseada no fato de CORPUS-003 estar organizado em passos Conjectura/Proposta/Validação.
- **Lacuna para v1.0.0:** Definição técnica formal, equação de campo (se houver) e relação explícita com a noção coloquial de "consciência" mencionada no Handoff.

#### B2. Functor Φcat

- **Documentos onde aparece:** CORPUS-003. `[E]` — citado no título verificado.
- **Definição provisória:** Functor (no sentido da teoria das categorias) denotado pelo símbolo Φcat, proposto como instrumento formal de mapeamento entre estruturas — provavelmente entre o Campo Primordial e a estrutura fenomênica observável. A notação com subscrito "cat" sugere a âncora categórica. `[I]` — inferido do título e do contexto categórico.
- **Status epistêmico:** Conjectura (Passo 16, conforme HTML v1.2.0). `[E]`
- **Relações declaradas:** Vincula-se ao Lema de Yoneda (B3) — provavelmente como aplicação ou fundamento. `[I]`
- **Lacuna para v1.0.0:** Definição precisa das categorias de domínio e contra-domínio, bem como o motivo de usar Yoneda especificamente.

#### B3. Lema de Yoneda

- **Documentos onde aparece:** CORPUS-003. `[E]`
- **Definição provisória:** Resultado clássico da teoria das categorias que estabelece que um objeto é determinado (a menos de isomorfismo) pelos morfismos que entram nele. No contexto de CORPUS-003, é provavelmente invocado como justificativa formal para identificar o Campo Primordial via suas relações com outros objetos. `[H]` — definido a partir de conhecimento matemático padrão; a interpretação específica no contexto de CORPUS-003 é hipótese.
- **Status epistêmico:** Resultado matemático estabelecido (no plano formal); aplicação a CORPUS-003 conjectural. `[H]`
- **Lacuna para v1.0.0:** Como exatamente Yoneda é aplicado — quais funtores Hom são considerados, qual categoria-alvo, qual objeto representável.

#### B4. Tensor Qµν

- **Documentos onde aparece:** CORPUS-003. `[E]` — citado no título verificado.
- **Definição provisória:** Tensor denotado por Q com índices covariantes µ e ν, sugerindo um tensor rank-2 em notação de relatividade geral. Pelo título, é proposto como modificação da equação de Einstein — sugerindo um termo adicional ao tensor de energia-momento ou à métrica efetiva. `[I]` — inferido da menção conjunta "Tensor Qµν e Modificação da Equação de Einstein" no título.
- **Status epistêmico:** Proposta (Passo 17, conforme HTML v1.2.0). `[E]`
- **Relações declaradas:** Modifica a Equação de Einstein (B5); conecta-se com trabalhos de Chanyal, Sun e Pradhan. `[E]`
- **Lacuna para v1.0.0:** Forma explícita do tensor, equação modificada completa, e derivação do termo Qµν a partir de princípios.

#### B5. Equação de Einstein modificada

- **Documentos onde aparece:** CORPUS-003. `[E]`
- **Definição provisória:** Versão estendida da equação de campo de Einstein Gµν + Λgµν = (8πG/c⁴)Tµν, com a inserção do termo Qµν (B4) — seja como correção ao lado geométrico, seja como contribuição adicional ao lado material. `[H]` — forma genérica inferida; estrutura específica é hipótese.
- **Status epistêmico:** Proposta (vinculada ao Passo 17). `[I]`
- **Relações declaradas:** Conecta-se aos trabalhos de Chanyal, Sun e Pradhan (referências externas ao corpus, citadas no título). `[E]`
- **Lacuna para v1.0.0:** Forma final da equação, interpretação física do termo Qµν e limite clássico (recuperação da equação de Einstein original).

---

### Cluster C — Aplicação Quântico-Dissipativa

#### C1. Dinâmica Quântica Dissipativa (QDT)

- **Documentos onde aparece:** CORPUS-004 (âncora); referenciado em CORPUS-002. `[E]`
- **Definição provisória:** Regime de evolução quântica de sistemas abertos, no qual a coexistência entre coerência quântica e dissipação ambiental é modelada — tipicamente via equações mestras do tipo Lindblad ou redfieldianas. No contexto do Paper B, é aplicada especificamente a complexos fotossintéticos. `[I]` — inferido do título de CORPUS-004.
- **Status epistêmico:** FINAL (rascunho para submissão ao JCP). `[E]`
- **Relações declaradas:** É uma aplicação da TCR (A1) ao regime quântico-dissipativo. `[E]` — declarado no HTML v1.2.0, seção 3.
- **Lacuna para v1.0.0:** Forma específica da equação mestra usada, parâmetros experimentais de ajuste e a métrica quantitativa de "lei de potência" mencionada no título.

#### C2. Complexo FMO (Fenna-Matthews-Olson)

- **Documentos onde aparece:** CORPUS-004. `[E]`
- **Definição provisória:** Complexo proteico fotossintético encontrado em bactérias verdes sulfurosas, amplamente estudado como sistema modelo para coerência quântica em biologia. O Paper B trata especificamente do caso FMO 7-sítios e deriva uma lei de potência para suas escalas de tempo de descoerência. `[I]` — conhecimento padrão da literatura + título de CORPUS-004.
- **Status epistêmico:** FINAL (rascunho). `[E]`
- **Relações declaradas:** Caso de estudo concreto para a QDT (C1). `[E]`
- **Lacuna para v1.0.0:** Resultado quantitativo da lei de potência (expoente, ajuste), e como este caso valida a TCR.

---

### Cluster D — Estrutura Metodológica Lakatosiana

#### D1. Lakatos (referência)

- **Documentos onde aparece:** Não diretamente citado em nenhum título, mas o nome do arquivo original de CORPUS-004 sugeria "QDT_Lakatos" (antes da correção). `[E]` — registrado no Handoff original como observação de correção.
- **Definição provisória:** Referência a Imre Lakatos, filósofo da ciência cuja noção de "programa de pesquisa científico" (núcleo duro + cinturão protetor) parece estruturar a auto-compreensão metodológica do projeto AION. `[I]`
- **Status epistêmico:** Não declarado. `[E]` — flagrado pela correção do nome do arquivo, mas sem uso textual confirmado.
- **Lacuna para v1.0.0:** Confirmar uso explícito do framework lakatosiano no corpo dos documentos e em quais passos.

#### D2. Programa de pesquisa

- **Documentos onde aparece:** Provavelmente CORPUS-003 (estrutura de passos), e implicitamente em todo o corpus. `[I]`
- **Definição provisória:** Estrutura metodológica lakatosiana: um núcleo duro de conjecturas não-abandonáveis (provavelmente TCR + Campo Primordial) e um cinturão protetor de propostas ajustáveis (Tensor Qµν, aplicações específicas). `[H]` — interpretação baseada em Lakatos padrão + inferência do corpus.
- **Status epistêmico:** Implícito. `[I]`
- **Lacuna para v1.0.0:** Confirmação textual da auto-designação do projeto como programa lakatosiano e identificação explícita do núcleo duro.

#### D3. Conjectura

- **Documentos onde aparece:** CORPUS-003 (Passo 16). `[E]`
- **Definição provisória:** Primeiro estágio da estrutura tripartite Conjectura → Proposta → Validação em CORPUS-003; possivelmente associado ao Functor Φcat. `[I]` — associação ao Passo 16 é `[E]`, mas associação a Φcat é `[I]`.
- **Status epistêmico:** Conjectura (status mais fraco da sequência). `[E]`

#### D4. Proposta

- **Documentos onde aparece:** CORPUS-003 (Passo 17). `[E]`
- **Definição provisória:** Segundo estágio; possivelmente associado ao Tensor Qµν e à modificação da Equação de Einstein. `[I]`
- **Status epistêmico:** Proposta (intermediário). `[E]`

#### D5. Validação

- **Documentos onde aparece:** CORPUS-003 (Passo 18). `[E]`
- **Definição provisória:** Terceiro estágio; possivelmente associado às conexões empíricas com Chanyal, Sun e Pradhan. `[I]`
- **Status epistêmico:** Validação (mais forte). `[E]`
- **Lacuna para v1.0.0:** Critério declarado de validação, e se já foi atingido ou é prospectivo.

---

## 3. GRAFO DE RELAÇÕES (TEXTUAL)

O grafo abaixo declara relações entre conceitos (não entre documentos). Cada aresta tem tipo e proveniência.

```
                ┌──────────────────────────────────────────┐
                │           CAMPO PRIMORDIAL (B1)          │
                │         [Conjectura, CORPUS-003]         │
                └───────────────────┬──────────────────────┘
                                    │
                          funda ontologicamente [E]
                                    │
                                    ▼
                ┌──────────────────────────────────────────┐
                │       COERÊNCIA RELACIONAL (A1/TCR)      │
                │  [FINAL, CORPUS-002; aplicada em -004]   │
                └───────────────────┬──────────────────────┘
                                    │
                          operacionaliza metodologicamente [E]
                                    │
                                    ▼
                ┌──────────────────────────────────────────┐
                │     DINÂMICA QUÂNTICA DISSIPATIVA (C1)   │
                │            [FINAL, CORPUS-004]           │
                └───────────────────┬──────────────────────┘
                                    │
                          aplicada a caso concreto [E]
                                    │
                                    ▼
                ┌──────────────────────────────────────────┐
                │          COMPLEXO FMO 7-SÍTIOS (C2)      │
                │            [FINAL, CORPUS-004]           │
                └──────────────────────────────────────────┘

Eixo paralelo de formalização (CORPUS-003):

  Functor Φcat ──── aplica/invoca ──── Lema de Yoneda
   (Conjectura,                          (ferramenta
    Passo 16)                             matemática)
       │
       │ formaliza
       ▼
  Tensor Qµν ───── modifica ───── Equação de Einstein
   (Proposta,                        modificada
    Passo 17)                            │
                                        │ valida-se com
                                        ▼
                                  Chanyal, Sun, Pradhan
                                  (Passo 18, Validação)

Cluster D atravessa tudo:

  Lakatos → Programa de pesquisa → (Conjectura → Proposta → Validação)
```

**Arestas declaradas `[E]` (do HTML v1.2.0):**
1. `CORPUS-002 → CORPUS-003` (dependência ontológica)
2. `CORPUS-002 → CORPUS-004` (dependência metodológica)
3. `CORPUS-004 → CORPUS-002` (referência explícita)
4. `CORPUS-005 → CORPUS-002` (referência direta)
5. `CORPUS-003 → Chanyal/Sun/Pradhan` (conexão externa)
6. `Conjectura → Proposta → Validação` (sequência Passos 16→17→18)

**Arestas inferidas `[I]` (do título de CORPUS-003):**
7. `Φcat → Yoneda` (uso conjunto no título)
8. `Qµν → Einstein modificado` (menção conjunta no título)
9. `Φcat → Qµν` (encadeamento formal: functor → tensor → equação)

**Arestas hipotéticas `[H]` (a verificar no Passo 3):**
10. `Campo Primordial → Φcat` (o functor seria a "extração de estrutura" do campo)
11. `Lakatos → programa AION` (auto-designação)
12. `TCR ↔ Einstein modificado` (unificação entre micro e macro — não declarado)

---

## 4. CONTRADIÇÕES E TENSÕES APARENTES

Esta seção registra tensões epistemológicas observáveis a partir do material disponível. Elas não são defeitos do corpus — são precisamente o tipo de questão que o Plano de Teste P2 (evolutiva) e P3 (crítica) deverá endereçar.

### T1. Tensão quantitativo × categórico-conjectural

Paper A (CORPUS-002) é apresentado como "*Quantitative Framework*" — um framework operacional, com métricas, conectomes e EEG. Parte IV (CORPUS-003) é apresentada como "*Formalização Teórica*" estruturada em Conjectura → Proposta → Validação, com ferramentas categóricas (Yoneda) e tensoriais (Einstein modificado). Há uma tensão epistemológica genuína entre o **estatuto empírico-quantitativo** do Paper A e o **estatuto formal-conjectural** da Parte IV. `[I]` — observável a partir dos títulos e estados.

Questão para P2: a Parte IV é o fundamento teórico que justifica o Paper A, ou é uma proposta paralela em estágio epistêmico mais fraco? Se for fundamento, então um paper FINAL está apoiado em conjecturas — o que é metodologicamente legítimo em Lakatos (o núcleo duro é irrefutável por construção), mas exige transparência declarada.

### T2. Tensão de escala: quântico-dissipativo × conectomes/EEG

Paper B (CORPUS-004) trata do regime quântico-dissipativo em escala molecular (FMO, 7 sítios). Paper A (CORPUS-002) vai de conectomes a EEG — escala macroscópica neural. A TCR é apresentada como aplicável a ambos, mas a ponte entre escalas não é evidente a partir dos títulos. `[I]`

Questão para P3: existe um argumento formal de escala (renormalização, lei de potência, auto-similaridade) que conecta as duas escalas? A "lei de potência do FMO 7-sítios" (mencionada no título de CORPUS-004) é candidata natural a ser a ponte — mas isso é hipótese `[H]`.

### T3. Lacunas de proveniência em Cover Letter

CORPUS-005 (Cover Letter) tem data e versão marcadas como `NÃO DECLARADO [E]`, e seu estado epistêmico é `Carta de submissão [I]`. A Cover Letter menciona o Paper A, mas não sabemos (sem o texto) se ela também posiciona o programa lakatosiano, se endereça revisores específicos, ou se antecipa críticas. `[I]`

Questão para P3 (do Handoff original): "*O que o Documento 5 aponta como limitação do programa?*" — esta pergunta não pode ser respondida a partir do material atualmente disponível. Será endereçada no Passo 4 (ingestão RAG).

### T4. "Consciência" como termo ausente dos títulos verificados

O Handoff original referia-se ao Documento 3 como "Nível 0 — Campo Primordial da Consciência". O título verificado em v1.2.0 não contém a palavra "consciência" — fala apenas em "Campo Primordial", "Functor Φcat", "Tensor Qµν" e "Equação de Einstein modificada". `[E]`

Questão para P2 (evolutiva): a noção de "consciência" foi explicitamente abandonada na v1.0 de CORPUS-003, ou permanece como pano de fundo filosófico sem entrar no título? Esta é uma questão empírica que só a ingestão do texto completo pode resolver.

---

## 5. O QUE ESTA ONTOLOGIA JÁ PERMITE (E O QUE NÃO PERMITE)

**Permite:**
- Servir de checklist conceitual para a ingestão via Docling (Passo 3): cada conceito acima deve ser localizável no texto-fonte, com seção/página.
- Servir de gabarito para o Plano de Teste P1 (conceitual): as 13 entradas acima são os conceitos que o sistema RAG deve recuperar, com a proveniência correta.
- Servir de base para o GraphRAG futuro (Passo 5): as arestas `[E]` já são arestas congeladas; as `[I]` e `[H]` são candidatos a arestas a serem confirmadas ou refutadas pela ingestão.

**Não permite:**
- Citação direta do autor para qualquer conceito. Todas as "definições provisórias" aqui são inferência ou hipótese.
- Responder P2 e P3 do Plano de Teste em sua forma completa. P2 (tratamento de "consciência") só pode ser respondido após ingestão; P3 (limitações apontadas pela Cover Letter) idem.
- Substituir a leitura do corpus. Esta ontologia é um mapa, não o território.

---

## 6. PRÓXIMOS PASSOS PARA v1.0.0 DA ONTOLOGIA

Para promover esta ontologia de v0.1.0 (Draft) para v1.0.0 (Verified), são necessários:

1. **Ingestão dos 5 textos completos** via Docling (Passo 3 do roadmap AION).
2. **Reescrita de cada definição provisória** como citação textual extraída do corpus, com referência de seção/página.
3. **Promoção de arestas `[I]` e `[H]`** para `[E]` (confirmadas) ou remoção (refutadas).
4. **Resolução das tensões T1-T4** com evidência textual.
5. **Validação pelo autor** (Edson) — a ontologia v1.0.0 só será declarada após assinatura do curador humano.

Até que estes passos sejam concluídos, esta ontologia v0.1.0 deve ser tratada como **documento de trabalho**, não como fonte de verdade canônica. A única fonte de verdade canônica do corpus permanece sendo `AION-CORPUS-001 v1.2.0 — Frozen & Verified`.

---

*"Nenhuma definição sem citação. Nenhuma inferência confundida com evidência."*
