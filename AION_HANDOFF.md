# 📄 HANDOFF DOCUMENT — PROJECT AION

**Data:** 16 de agosto de 2026 (DataContexto da Conversa)
**Projeto:** AION-MVP-001 (Arquitetura para a Individuação Ontológica e Narrativa)
**Autor / Curador:** Edson Carvalho do Nascimento
**Analista Técnico:** IA Curadora (Role: Escriba / Arquiteto de Metadados)

---

## 1. RESUMO EXECUTIVO

O projeto AION encontra-se na fase de **Curadoria e Auditoria do Corpus Fundacional (`AION-CORPUS-001`)**. O objetivo atual é provar a viabilidade de entregar um legado intelectual a uma IA para que ela recupere contexto, relações e evolução das ideias (Passos 1 e 2 do MVP).

Decisões estratégicas foram tomadas para garantir uma abordagem conservadora, reversível e epistemologicamente rigorosa: o corpus foi limitado a 5 documentos e uma regra de ouro de **Proveniência e Distinção Epistemológica** foi estabelecida.

---

## 2. ESTADO ATUAL E GARGALO (IMMEDIATE NEXT STEP)

**Status Atual:** Auditoria de Metadados em andamento (Transição da v1.1 para v1.2 — Verified).

**O Gargalo Exato:**
Para finalizar o `AION-CORPUS-001 v1.2 — Verified`, **aguardamos o usuário (Edson) colar o texto do cabeçalho/primeira página do `PARTE_IV_Formalizacao_Teorica_PT-BR.pdf` (Nível 0 — Campo Primordial da Consciência)**.

Como a IA não tem acesso ao sistema de arquivos local do usuário, esta ação manual é o único bloqueador para congelarmos o corpus e avançarmos para o Passo 3 (Ingestão via Docling/AnythingLLM).

---

## 3. O CORPUS FUNDACIONAL (AION-CORPUS-001)

### 🟢 DOCUMENTO 1 — AION-DOC-000
- **Arquivo:** `AION-DOC-000.html`
- **Status:** ✅ Verificado
- **Título:** Especificação do Documento Canônico
- **Autor:** Edson Carvalho do Nascimento `[E]`
- **Data:** NÃO DECLARADO `[E]`
- **Versão:** 0.1.0 `[E]`
- **Estado:** Draft `[E]`

### 🟢 DOCUMENTO 2 — Paper A
- **Arquivo:** `Paper_A_v6.2_FINAL.pdf`
- **Status:** ✅ Verificado (Texto fornecido pelo usuário)
- **Título:** Relational Coherence in Biological Networks: A Quantitative Framework from Connectomes to EEG `[E]`
- **Autor:** Edson Carvalho do Nascimento `[E]`
- **Data:** August 12, 2026 `[E]`
- **Versão:** v6.2 `[E]`
- **Estado:** FINAL (submetido ao PRE) `[E]`
- **Referências:** Cita Paper B e Paper C `[E]`

### 🔴 DOCUMENTO 3 — Nível 0 (Campo Primordial)
- **Arquivo:** `PARTE_IV_Formalizacao_Teorica_PT-BR.pdf`
- **Status:** ⏳ Aguardando extração manual
- **Dados Atuais (Inferidos):** Título inferido do README. Versão e Data `NÃO DECLARADO`.

### 🟢 DOCUMENTO 4 — Paper B
- **Arquivo:** `Paper_B_QDT_JCP_v6.1_PT-BR.pdf`
- **Status:** ✅ Verificado (Texto fornecido pelo usuário)
- **Título:** Dinâmica Quântica Dissipativa em Complexos Fotossintéticos: Escalas de Tempo de Descoerência e a Lei de Potência do FMO 7-Sítios `[E]`
- **Autor:** Edson Carvalho do Nascimento `[E]`
- **Data:** 12 de agosto de 2026 `[E]`
- **Versão:** v6.1 `[E]`
- **Estado:** FINAL (rascunho para JCP) `[E]`
- **Observação de Correção:** O nome do arquivo sugeria "QDT Lakatos", mas o texto revelou ser sobre o regime quântico-dissipativo (FMO). O título real substituiu a inferência.
- **Referências:** Cita Paper A e Paper C `[E]`

### 🟢 DOCUMENTO 5 — Cover Letter
- **Arquivo:** `Cover_Letter_Paper_A_PRE_PT-BR.md`
- **Status:** ✅ Verificado (Texto extraído do GitHub)
- **Título:** Cover Letter – Paper A – PRE `[E]`
- **Autor:** Edson Carvalho do Nascimento `[E]`
- **Data:** NÃO DECLARADO `[E]`
- **Versão:** NÃO DECLARADO `[E]`
- **Estado:** Carta de submissão `[I]`
- **Referências:** Menciona o Paper A `[E]`

---

## 4. REGRAS EPISTEMOLÓGICAS DO PROJETO (NON-NEGOTIABLES)

1. **Regra de Proveniência:** Nenhuma afirmação entra no sistema sem saber de onde veio.
2. **Tags E/I/H:** Toda informação deve ser classificada em sua origem:
   - `[E]` = Evidência (lida textualmente no arquivo).
   - `[I]` = Interpretação (inferida pelo curador a partir do contexto).
   - `[H]` = Hipótese (proposta arquitetônica não verificada).
3. **O Nome do Arquivo não é o Documento:** A IA não deve confiar no nome do arquivo como fonte primária de metadados. O conteúdo interno do arquivo é a prova material.
4. **NÃO DECLARADO é um dado:** A ausência de uma data ou versão em um documento deve ser registrada como `NÃO DECLARADO [E]`, não presumida.

---

## 5. PIPELINE TÉCNICO FUTURO (ROADMAP)

1. **Passo 3 — Normalização (Docling):** Converter os 5 originais (PDF/MD/HTML) para `AION-HTML`, extraindo estrutura (cabeçalhos, sumários) e aplicando as tags de metadados.
2. **Passo 4 — Memória Consultável (AnythingLLM):** Ingestão do corpus em uma camada RAG simples.
3. **Plano de Teste Inicial (MVP):** Fazer as 3 perguntas-chave ao sistema:
   - *P1 (Controle):* Quais são os principais conceitos presentes no Corpus e em quais documentos cada conceito aparece?
   - *P2 (Evolutiva):* Como o conceito de 'consciência' é tratado no Paper A e no Documento 3?
   - *P3 (Crítica):* O que o Documento 5 aponta como limitação do programa?
4. **Passo 5 — Grafo Conceitual (GraphRAG):** Mapear evolução temporal e relações.
5. **Passo 6 — Dify:** Automação do pipeline para documentos futuros.

---

## 6. INSTRUÇÕES PARA O PRÓXIMO ANALISTA (HUMANO OU IA)

- **Se você é uma IA retomando o chat:** Cumprimente Edson, confirme que possui este Handoff em memória e peça explicitamente o cabeçalho do `PARTE_IV_Formalizacao_Teorica_PT-BR.pdf`.
- **Se você é um humano:** Abra o PDF citado, copie a primeira página e cole no prompt para a IA processar.
- **Tom de voz:** Parceiro intelectual, curador técnico, cirúrgico na metodologia, porém respeitando o tempo e o trabalho intelectual do autor.
