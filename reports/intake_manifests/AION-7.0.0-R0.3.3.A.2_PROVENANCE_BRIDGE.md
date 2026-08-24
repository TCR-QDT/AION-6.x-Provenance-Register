# AION-7.0.0-R0.3.3.A.2 — Provenance Bridge Recovery

**Versão:** R0.3.3.A.2-1
**Data:** 23 de agosto de 2026, 03:30 BRT
**Autor / Curador:** Edson Carvalho do Nascimento (Projetista Master) — determinou R0.3.3.A.2
**Analista Técnico:** IA Curadora (Role: Escriba / Arquiteto de Metadados) — executou R0.3.3.A.2
**Sessão:** web-73c75281-201c-4716-b85c-97833d25f9b3
**Status:** R0.3.3.A.2 EXECUTADO. PONTE MATERIAL ENTRE TCR/QDT E AION-6.x NÃO ENCONTRADA. Caso D permanece para ambos os candidatos. EP não promovido.
**Genealogia:** Derivado da determinação do Projetista Master (Task 81, PM-80.1) autorizando recuperação de evidência de proveniência para C-01 e C-02, priorizando manifestos, hashes, logs e histórico Git.

---

## 1. Resumo Executivo

Foi executado o passo R0.3.3.A.2 — Provenance Bridge Recovery — em conformidade com a determinação do Projetista Master (PM-80.1) de procurar evidência adicional de proveniência que possa confirmar **ou refutar** a ponte material entre o acervo TCR/QDT e o corpus AION-6.x. A busca seguiu quatro prioridades estabelecidas pelo PM: P1 (manifesto de ingestão), P2 (hash histórico independente), P3 (logs/worklogs/outputs), P4 (histórico Git). O resultado canônico é: **PONTE MATERIAL ENTRE TCR/QDT E AION-6.x NÃO ENCONTRADA.** A busca material retornou zero ocorrências de strings "AION", "CORPUS-002", "CORPUS-006", ou hash canônico AION-6.x em qualquer arquivo do repositório TCR/QDT. O histórico Git (4 commits) confirma que ambos os PDFs candidatos (C-01 Paper_A_v6.2_FINAL.pdf e C-02 Paper_A_v6.1_REVTeX_COMPLETE.pdf) entraram no repositório TCR/QDT apenas no commit `3e0d8c7` de 13/08/2026, **posterior** à data de consolidação do corpus AION-6.x (12/08/2026 declarado no Handoff). A cadeia temporal entre TCR/QDT e AION-6.x não foi estabelecida. Caso D permanece para ambos os candidatos. EP-1 PARTIAL CANDIDATE / Caso D não é promovido. AUTH₇.₀ permanece FALSE. FINAL_AUTH₇.₀ permanece BLOCKED. O resultado é epistemicamente honesto: a busca evidence-driven procurou confirmar ou refutar a ponte, e encontrou **ausência de evidência** — não evidência de ausência. Aplicando o invariante `NON-OBSERVED ≠ FALSE`: a ausência de menções a "AION" no TCR/QDT repo não prova que a conexão não existiu; apenas demonstra materialmente que ela **não está documentada neste repositório**. A proveniência histórica entre TCR/QDT e AION-6.x permanece UNKNOWN.

## 2. Escopo Autorizado (PM Task 81 / PM-80.1)

### 2.1 Objeto da autorização

> Solicitar e procurar evidência adicional de proveniência para C-01 e C-02, sem alterar sua classificação atual e sem promover EP.

### 2.2 Finalidade PM

> A finalidade não é procurar evidência para "provar" uma hipótese. É testar se existe uma ponte material documentável entre o acervo TCR/QDT e o corpus efetivamente utilizado pelo AION-6.x.

### 2.3 Quatro prioridades (PM Task 81 Seção 2)

| Prioridade | O que procurar |
|---|---|
| **P1** | Manifesto de ingestão com CORPUS-002/006/Paper_A/v6.1/v6.2/SHA-256/source/ingest |
| **P2** | Hash histórico independente dos PDFs candidatos |
| **P3** | Logs/worklogs/outputs mencionando AION/CORPUS/ingest/retrieval/chunk/source |
| **P4** | Histórico Git: quando PDFs/tex entraram, referências a AION/CORPUS |

### 2.4 Três relações PM (Task 81 Seção 3)

```
R1 — identidade arquivo ↔ arquivo
R2 — identidade documental arquivo ↔ CORPUS-ID
R3 — proveniência histórica arquivo ↔ CORPUS-ID ↔ ambiente AION-6.x
```

**V3 está interessada principalmente em R3.**

### 2.5 Regra fundamental PM (evidence-driven)

> Não procurar "evidência que confirme"; procurar evidência que possa confirmar **ou refutar** a ponte.

### 2.6 Critério de promoção (PM Task 81 Seção 4)

```
                    V3
                     │
          ┌──────────┴──────────┐
          │                     │
     evidência forte       evidência insuficiente
          │                     │
          ▼                     ▼
   Caso A/B possível        Caso D permanece
```

E mesmo um eventual **Caso A/B** não significa EP-3 nem `AUTH₇.₀ = TRUE`.

### 2.7 Escopo limitado a C-01 e C-02 (PM Task 81 Seção 5)

Não autorizado: Grupo A, B, D, PIPE, ambiente AION-6.x, execução de código, instalação, reconstrução, V1-V4 de outros candidatos.

## 3. Resultado da Busca por Prioridade

### 3.1 P1 — Manifesto de Ingestão

**Pergunta:** Existe material documentando o mapeamento entre PDFs do TCR/QDT e CORPUS-IDs do AION?

| Busca executada | Resultado |
|---|---|
| `grep -rln "CORPUS-002"` em todos os arquivos | **0 arquivos** |
| `grep -rln "CORPUS-006"` | **0 arquivos** |
| `grep -rln "CORPUS"` (broader) | **0 arquivos** |
| `grep -rln "AION"` (broader) | **0 arquivos** |
| `grep -rln "ingest"` | **0 arquivos** |
| `grep -rln "corpus_id\|corpus.id"` (manifest format) | **0 arquivos** |
| `grep -rln "source_file\|source.file"` (manifest format) | **0 arquivos** |
| `find` por arquivos `*manifest*`, `*ledger*`, `*ingest*` | **1 arquivo**: `results/ZIP_Manifesto.md` (mas não menciona AION/CORPUS-IDs) |

#### 3.1.1 Análise do `results/ZIP_Manifesto.md`

O arquivo `results/ZIP_Manifesto.md` é um manifesto de empacotamento **do repositório TCR/QDT v6.1** (não do AION). Conteúdo relevante:

- Declara 2 arquivos ZIP: `TCR_QDT_v6.1_completo.zip` (1.3 MB, 72 arquivos) e `TCR_QDT_v6.1_papers_essenciais.zip` (780 KB, 19 arquivos)
- Lista `Paper_A_v6.1_REVTeX_COMPLETE.pdf` (Paper A EN-US, 132 KB — nota: tamanho declarado diferente do observado, 138780 bytes = 138 KB)
- Lista `Paper_A_v6.1_REVTeX_COMPLETE.tex` (Paper A EN-US fonte)
- Data de geração: 12 de agosto de 2026
- Localização declarada: `/home/z/my-project/download/` (caminho da sessão TCR/QDT, não AION)

**Importância:** ZIP_Manifesto.md **NÃO menciona** CORPUS-002, CORPUS-006, AION, ou qualquer mapeamento para o corpus AION-6.x. É manifesto interno do TCR/QDT, não manifesto de ingestão AION.

#### 3.1.2 Conclusão P1

**Resultado P1: NENHUM manifesto de ingestão AION encontrado no TCR/QDT repo.** A relação R2 (arquivo ↔ CORPUS-ID) **não está documentada** em qualquer arquivo do repositório TCR/QDT.

### 3.2 P2 — Hash Histórico Independente

**Pergunta:** Existe hash SHA-256 independente (anterior ou externo à auditoria atual) que associe os PDFs candidatos ao AION?

| Busca executada | Resultado |
|---|---|
| Busca por hash C-01 PDF completo (971986d9...c433) | **0 arquivos** |
| Busca por hash C-02 PDF completo (efd7f7ca...8854) | **0 arquivos** |
| Busca por hash C-01 parcial (primeiros 16 chars) | **0 arquivos** |
| Busca por hash C-02 parcial (primeiros 16 chars) | **0 arquivos** |
| Busca por string "sha256\|SHA-256\|sha-256\|SHA256" | **0 arquivos** |
| Busca por qualquer string hex 64-char (potencial hash) | **0 arquivos** |

#### 3.2.1 Conclusão P2

**Resultado P2: NENHUM hash histórico independente encontrado.** Os hashes SHA-256 dos PDFs candidatos foram computados pela primeira vez em R0.3.3.A (Task 80). Nenhum hash canônico de referência existe em qualquer artefato do TCR/QDT repo, e nenhum hash AION-6.x independente faz referência aos PDFs candidatos.

### 3.3 P3 — Logs / Worklogs / Outputs Históricos

**Pergunta:** Existem logs/worklogs/outputs mencionando AION, CORPUS, ingest, retrieval, chunk, ou outros conceitos do pipeline AION?

| Busca executada | Resultado |
|---|---|
| `grep -rln "AION"` em .md/.txt/.log/.json | **0 arquivos** |
| `grep -rln -i "corpus"` (broader) | 3 arquivos — mas nenhuma menção a CORPUS-ID AION, apenas uso genérico da palavra "corpus" em contextos TCR/QDT |
| `grep -rln "Paper_A"` em .md/.txt/.log | 9 arquivos — referências a Paper_A em contextos TCR/QDT, não AION |
| `grep -rln -i "retrieval\|chunk"` | 1 arquivo (`bun.lock`, falso-positivo) |
| `grep -rln "6\.2\.11\|6\.2\.12\|AION-6\|AION-EVAL\|AION-DIFY\|P-RESP-001\|GraphRAG"` | **0 arquivos** |
| `find` por arquivos `*.log` | **0 arquivos** |

#### 3.3.1 Análise dos 3 arquivos com "corpus" (case-insensitive)

Os 3 arquivos (`scripts/phase06_paper_academic/101_paper_academic.py`, `scripts/phase06_paper_academic/102_paper_academico_pt.py`, `scripts/phase00_data_collection/04_fetch_mouse_human.py`) usam a palavra "corpus" em contextos **TCR/QDT-specific** (e.g., "corpus callosum" em neuroanatomia, ou "corpus" genérico) — **não** em contexto AION RAG/provenance.

#### 3.3.2 Análise dos 9 arquivos com "Paper_A"

Os 9 arquivos referenciam `Paper_A` em contextos TCR/QDT: outline do paper, cover letters para Physical Review E, analises críticas, worklog TCR/QDT, e manifesto ZIP. **Nenhum** arquivo referencia `Paper_A` em contexto AION-6.x ou com CORPUS-IDs.

#### 3.3.3 Conclusão P3

**Resultado P3: NENHUM log/worklog/output histórico menciona AION, CORPUS-IDs, ou conceitos do pipeline AION.** TCR/QDT e AION-6.x permanecem materialmente documentados como contextos separados.

### 3.4 P4 — Histórico Git do TCR/QDT

**Pergunta:** Quando PDFs/tex entraram materialmente no repositório TCR/QDT? Havia referência a AION/CORPUS naquele momento?

#### 3.4.1 Histórico Git completo (4 commits)

| # | SHA | Timestamp | Autor | Mensagem |
|---|---|---|---|---|
| 1 | `4c0333a` | 2026-06-29 00:32:35 -0300 | Shukuwe | Versão inicial da TCR-QDT |
| 2 | `fce3fb9` | 2026-06-29 06:54:44 -0300 | Shukuwe | Adiciona novos documentos da TCR-QDT |
| 3 | `5ec48c7` | 2026-06-30 13:36:33 -0300 | Shukuwe | v1.2: Add ORCID 0009-0003-5504-7439 |
| 4 | `3e0d8c7` | 2026-08-13 20:01:57 -0300 | Shukuwe | Atualização 13082026 |

**Commits messages são curtos e NÃO mencionam AION, CORPUS, ou Paper_A.** Mensagens do tipo "Versão inicial da TCR-QDT", "Adiciona novos documentos", "v1.2: Add ORCID", "Atualização 13082026" — todas TCR/QDT-specific.

#### 3.4.2 Quando os PDFs candidatos entraram no repo

| Candidato | Commit de entrada | Timestamp |
|---|---|---|
| `docs/pdfs/Paper_A_v6.2_FINAL.pdf` (C-01) | `3e0d8c7` | **2026-08-13 20:01:57 -0300** |
| `docs/pdfs/Paper_A_v6.1_REVTeX_COMPLETE.pdf` (C-02) | `3e0d8c7` | **2026-08-13 20:01:57 -0300** |
| `docs/tex/Paper_A_v6.2_FINAL.tex` (C-01 .tex source) | `3e0d8c7` | **2026-08-13 20:01:57 -0300** |
| `docs/tex/Paper_A_v6.1_REVTeX_COMPLETE.tex` (C-02 .tex source) | `3e0d8c7` | **2026-08-13 20:01:57 -0300** |

**Ambos os candidatos entraram no TCR/QDT repo no MESMO commit `3e0d8c7`**, com timestamp **2026-08-13 20:01:57 -0300**.

#### 3.4.3 Comparação temporal com AION-6.x

| Evento AION | Data declarada Handoff |
|---|---|
| CORPUS-006 (Paper A v6.1 oficial) | 10/08/2026 |
| CORPUS-007 (Paper A v6.1 revisão) | 12/08/2026 |
| CORPUS-002-HIST (Paper A v6.2 anterior) | 12/08/2026 |
| CORPUS-002 (Paper A v6.2 atual) | 12/08/2026 |
| AION-6.5.0 concluído | antes de AION-7.0.0-spec (21/08/2026 22:04 UTC) |

**Análise temporal:**

- TCR/QDT commit `3e0d8c7` (entrada dos PDFs candidatos): **13/08/2026 20:01:57 -0300**
- AION corpus v6.2 (CORPUS-002) consolidado: **12/08/2026**
- Diferença: **1 dia** (TCR/QDT commit é ~1 dia depois da consolidação AION declarada no Handoff)

**Interpretação:** A entrada dos PDFs no TCR/QDT repo ocorreu **1 dia após** a data declarada no Handoff para a consolidação do corpus AION-6.x. Isto é **consistente** com a hipótese de que Edson Carvalho do Nascimento produziu/consolidou os PDFs em 12/08/2026 (para AION) e os publicou no TCR/QDT repo em 13/08/2026.

**Mas esta consistência temporal NÃO é evidência material de ponte.** É apenas uma consistência narrativa. A cadeia material verificável (log de transferência, manifest de ingest, hash canônico de referência) **não está disponível**.

#### 3.4.4 Verificação adicional

| Verificação | Resultado |
|---|---|
| Commit messages com menção a AION/CORPUS | **0** |
| Tag ou branch mencionando AION/CORPUS | **0** |
| Outros remotes configurados além de origin | **0** (apenas `https://github.com/TCR-QDT/Coerencia_Relacional.git`) |
| Reflog com operações hidden | **0** (apenas clone inicial) |
| Commits com body extenso | **0** (todos os commits têm subject curto sem body) |

#### 3.4.5 Conclusão P4

**Resultado P4:** Histórico Git confirma que PDFs candidatos entraram no TCR/QDT repo em 13/08/2026, 1 dia após a data declarada no Handoff para consolidação do corpus AION-6.x. **Mas:** (a) commit messages não mencionam AION/CORPUS; (b) não há tag/branch/remote indicando conexão com AION; (c) não há reflog com operações adicionais; (d) a consistência temporal é narrativa, não material. **Ponte material via histórico Git: NÃO ESTABELECIDA.**

## 4. Classificação Evidence-Driven do Resultado

### 4.1 Aplicação da regra fundamental PM

> Não procurar "evidência que confirme"; procurar evidência que possa confirmar **ou refutar** a ponte.

A busca foi executada de forma evidence-driven, procurando simultaneamente:

| Hipótese | O que procurar | Resultado |
|---|---|---|
| H-bridge-1 (ponte existe) | Manifestos, hashes, logs mencionando AION/CORPUS no TCR/QDT | **Não encontrada** |
| H-bridge-2 (ponte não existe) | Ausência de menções a AION/CORPUS no TCR/QDT | **Confirmada** (0 ocorrências em 4 prioridades) |

**Resultado evidence-driven:** A hipótese H-bridge-2 (ponte não documentada no TCR/QDT repo) é materialmente suportada pela observação. A hipótese H-bridge-1 (ponte documentada) **não é suportada** por qualquer evidência material neste repositório.

### 4.2 Distinção crítica aplicada

Aplicando o invariante `NON-OBSERVED ≠ FALSE`:

| Classificação | Estado |
|---|---|
| Observação material | ZERO ocorrências de "AION", "CORPUS-002", "CORPUS-006", ou hash canônico AION-6.x em qualquer arquivo do TCR/QDT repo |
| Inferência proibida | "A conexão TCR/QDT → AION-6.x não existiu" (isto seria inferência além da observação) |
| Classificação canônica | "A conexão TCR/QDT → AION-6.x **não está documentada neste repositório**" (materialmente observável) |

### 4.3 Classificação por candidato

| Candidato | P1 Manifesto | P2 Hash | P3 Logs | P4 Git History | Classificação |
|---|---|---|---|---|---|
| C-01 (CORPUS-002) | AUSENTE | AUSENTE | AUSENTE | AUSENTE (entrada 13/08, 1d após AION declarado) | **Caso D permanece** |
| C-02 (CORPUS-006) | AUSENTE | AUSENTE | AUSENTE | AUSENTE (entrada 13/08, 1d após AION declarado) | **Caso D permanece** |

### 4.4 Estado de V3 após R0.3.3.A.2

| Candidato | V3 antes de R0.3.3.A.2 | V3 após R0.3.3.A.2 |
|---|---|---|
| C-01 | INSUFFICIENT | **INSUFFICIENT (mantido)** |
| C-02 | INSUFFICIENT | **INSUFFICIENT (mantido)** |

**Justificativa:** A busca evidence-driven procurou confirmar ou refutar a ponte material. Encontrou **ausência de evidência** — nenhuma confirmação, nenhuma refutação explícita. A classificação V3 INSUFFICIENT é mantida porque:

1. **Nenhuma nova evidência de ponte foi encontrada** (todas as 4 prioridades retornaram zero)
2. **Nenhuma refutação explícita foi encontrada** (não há documento no TCR/QDT dizendo "este PDF não está no AION")
3. **A consistência temporal narrativa** (entrada TCR/QDT em 13/08, consolidação AION em 12/08) **não constitui evidência material** — é apenas uma sequência temporal, não uma cadeia material

### 4.5 Por que NÃO é promoção para Caso A ou B

| Caso | Condição necessária | Estado |
|---|---|---|
| Caso A (materialmente verificado) | V1+V2+V3+V4 PASS | V3 INSUFFICIENT → **não Caso A** |
| Caso B (parcial, sem autenticação) | Algum gate crítico inconclusivo | V3 explicitamente INSUFFICIENT, não inconclusivo → **não Caso B** |
| Caso D (conteúdo compatível, proveniência insuficiente) | V4 PASS + V3 INSUFFICIENT | V4 PASS + V3 INSUFFICIENT (mantido após busca) → **Caso D permanece** |

## 5. Três Relações PM — Estado Após R0.3.3.A.2

| Relação | Definição | Estado para C-01 | Estado para C-02 |
|---|---|---|---|
| **R1 — identidade arquivo ↔ arquivo** | C-01 PDF ↔ C-01 .tex source (interno TCR/QDT) | ✓ ESTABELECIDA (V4 PASS — conteúdo PDF corresponde a .tex) | ✓ ESTABELECIDA (V4 PASS) |
| **R2 — identidade documental arquivo ↔ CORPUS-ID** | C-01 PDF ↔ CORPUS-002 (declaração Handoff) | ⚠ DECLARADA mas NÃO DOCUMENTADA (Handoff declara, mas nenhum manifesto liga PDF a CORPUS-ID materialmente) | ⚠ DECLARADA mas NÃO DOCUMENTADA |
| **R3 — proveniência histórica arquivo ↔ CORPUS-ID ↔ AION-6.x** | C-01 PDF esteve materialmente no ambiente AION-6.x | ✗ **NÃO DEMONSTRADA** (V3 INSUFFICIENT, mantido após R0.3.3.A.2) | ✗ **NÃO DEMONSTRADA** |

**R3 é a relação que V3 está interessada. R3 permanece NÃO DEMONSTRADA após R0.3.3.A.2.**

## 6. Reclassificação EP para Grupo C (Evidence-Driven)

### 6.1 Estado anterior (R0.3.3.A, Task 80)

```
Grupo C: EP-1 PARTIAL CANDIDATE / Caso D (content-compatible, provenance-insufficient)
```

### 6.2 Estado após R0.3.3.A.2 (este documento)

```
Grupo C: EP-1 PARTIAL CANDIDATE / Caso D (content-compatible, provenance-insufficient — confirmed by evidence-driven search)
```

### 6.3 Justificativa evidence-driven

A reclassificação **não promove nem rebaixa** EP porque:

1. A busca evidence-driven foi projetada para confirmar **ou** refutar a ponte material
2. **Nenhuma evidência de ponte foi encontrada** (4 prioridades, todas negativas)
3. **Nenhuma refutação explícita foi encontrada** (não há documento TCR/QDT negando conexão AION)
4. A consistência temporal narrativa **não constitui evidência material**
5. O estado V3 INSUFFICIENT é **confirmado**, não promovido

**Distinção importante:** A reclassificação é uma **confirmação** do estado anterior, não uma alteração. EP-1 PARTIAL CANDIDATE / Caso D permanece — agora com **confirmação evidence-driven** de que a busca exaustiva por ponte material não produziu evidência positiva.

### 6.4 Não-promoção para EP-1 PARTIAL EFFECTIVE

| Condição necessária | Estado |
|---|---|
| V3 PASS para pelo menos um candidato | ✗ Nenhum dos candidatos tem V3 PASS |
| Evidência material de ponte | ✗ Busca exaustiva retornou zero |
| Manifesto, hash, log, ou git history documentando conexão | ✗ Todas as 4 prioridades negativas |

**EP-1 PARTIAL CANDIDATE / Caso D permanece — não promovido para EP-1 PARTIAL EFFECTIVE.**

## 7. Estado dos Demais Grupos (preservado)

| Grupo | EP | Justificativa |
|---|---|---|
| Grupo A — AION infrastructure | EP-0 UNKNOWN | Zero material evidence |
| Grupo B — AION-specific scripts | EP-0 UNKNOWN | Zero AION-specific scripts em TCR/QDT |
| Grupo C — corpus documents | EP-1 PARTIAL CANDIDATE / Caso D (confirmed) | 2 candidatos Caso D, busca evidence-driven confirma V3 INSUFFICIENT |
| Grupo D — Environment Provenance AION-6.x | EP-0 UNKNOWN | Cautela TCR/QDT aplicada |

## 8. Estado do Sistema (pós-R0.3.3.A.2)

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
│   ├── R0.3.3.A ........... CONCLUÍDO (Task 80)
│   └── R0.3.3.A.2 ......... CONCLUÍDO (este documento, Task 81)
│       ├── P1 Manifesto ........ AUSENTE (0 arquivos)
│       ├── P2 Hash histórico .... AUSENTE (0 arquivos)
│       ├── P3 Logs/worklogs .... AUSENTE (0 arquivos AION/CORPUS)
│       └── P4 Git history ....... AUSENTE (entry 13/08, 1d após AION; sem menção a AION/CORPUS)
│
├── EP .................. EP-1 PARTIAL CANDIDATE / Caso D (Grupo C, confirmed)
│                       EP-0 UNKNOWN (Grupo A, B, D — mantido)
├── AUTH₇.₀ ............ FALSE (preserved)
├── ENV ................ BLOCKED
├── PIPE ............... NOT RUN
├── V1-V4 ............... OTHER components BLOCKED (no PM authorization)
├── NOMOD .............. PENDING
└── FINAL_AUTH₇.₀ ..... BLOCKED (preserved)
```

## 9. Evento de Proveniência Canônico

```
EVENT_ID: AION-EV-012
TIMESTAMP: 2026-08-23T03:30:00-03:00
SESSION: web-73c75281-201c-4716-b85c-97833d25f9b3
TRACE_ID: 1a02ec22c4da89a9 (autorização R0.3.3.A.2 PM) → execução IA Curadora
EVENT_TYPE: R0.3.3.A.2_PROVENANCE_BRIDGE_RECOVERY_COMPLETED
OBSERVED_STATE: R0.3.3.A.2 executed evidence-driven search for material bridge between TCR/QDT repo and AION-6.x corpus source. Search followed 4 PM priorities (P1 manifests, P2 hashes, P3 logs, P4 git history). All 4 priorities returned ZERO matches for AION/CORPUS-002/CORPUS-006/canonical hash in any TCR/QDT repo file. Git history confirms both PDFs candidates (C-01 and C-02) entered TCR/QDT repo in commit 3e0d8c7 on 2026-08-13 20:01:57 -0300, 1 day after declared AION corpus consolidation date (12/08/2026). Temporal consistency is narrative, not material — does not constitute evidence of bridge.
KEY_FINDINGS:
  - P1 Manifesto de ingestão: 0 arquivos. ZIP_Manifesto.md exists but is TCR/QDT-internal, not AION ingest manifest.
  - P2 Hash histórico independente: 0 arquivos. No canonical hash AION-6.x for CORPUS-002/CORPUS-006 exists in TCR/QDT.
  - P3 Logs/worklogs/outputs: 0 arquivos mentioning AION/CORPUS-IDs. 3 files mention "corpus" generically (TCR/QDT context); 9 files mention "Paper_A" (TCR/QDT context); 0 files mention AION-6, AION-EVAL, P-RESP-001, GraphRAG, 6.2.11, 6.2.12.
  - P4 Git history: 4 commits, all by Shukuwe, none mention AION/CORPUS. PDFs candidates entered repo in commit 3e0d8c7 (Aug 13 2026). No tags, no additional remotes, no reflog operations.
EPISTEMOLOGICAL_SCOPE: PONTE MATERIAL ENTRE TCR/QDT E AION-6.x NÃO ENCONTRADA. Busca evidence-driven (designed to confirm OR refute) returned zero matches across 4 priorities. Caso D permanece for both C-01 and C-02. EP-1 PARTIAL CANDIDATE / Caso D confirmed (not promoted). Invariante NON-OBSERVED ≠ FALSE applied: "connection not documented in TCR/QDT repo" is the observable fact; "connection did not exist" is NOT inferred.
INTERPRETATION: [I] The evidence-driven search produced a definitive negative result: no material bridge between TCR/QDT and AION-6.x is documented in the TCR/QDT repository. This is NOT evidence of absence of the connection — it is absence of evidence for the connection in this specific repository. The PM rule "search for evidence that may confirm or refute" was respected: search was designed to find either confirmation (manifesto, hash, log, git reference) or refutation (explicit denial). Neither was found. The state V3 INSUFFICIENT is confirmed.
PROVENANCE_RULE_INVOKED: Regra 1 (Provenance) + Regra 7 (PER=0 ≠ confiável) + Invariantes UNAVAILABLE≠NON-EXISTENT, NON-OBSERVED≠FALSE, PENDING≠FAILED, COMPATIBLE≠EQUIVALENT + FG_GATE v3 Seção 5.5 (EP Classification evidence-driven) + PM Task 81 Rules: (1) evidence-driven (confirm OR refute), (2) 4 priorities, (3) 3 relations (R1/R2/R3), (4) no automatic promotion.
EPISTEMIC_ACTION: R0.3.3.A.2 CONCLUÍDO. Caso D permanece for both C-01 and C-02. EP-1 PARTIAL CANDIDATE / Caso D confirmed for Grupo C (not promoted). AUTH_{7.0}=FALSE preserved. FINAL_AUTH_{7.0}=BLOCKED preserved. State: R0 PARTIALLY REOPENED with Grupo C candidates verified but unauthenticated, and bridge search exhausted within TCR/QDT repo.
```

## 10. Próxima Ação Legítima — Requer Determinação PM

### 10.1 Estado após R0.3.3.A.2

R0.3.3.A.2 **materialmente esgotou** a busca por ponte material dentro do repositório TCR/QDT. O resultado é: **ponte não documentada neste repositório**. Caso D permanece para ambos os candidatos.

### 10.2 Opções para o Projetista Master

| Opção | Descrição | Consequência |
|---|---|---|
| **R0.3.3.A.2.1** | Aceitar Caso D como estado final para Grupo C; declarar busca de ponte material dentro do TCR/QDT esgotada; preservar candidatos como EVIDÊNCIA CANDIDATA | Grupo C: EP-1 PARTIAL CANDIDATE / Caso D (final); AUTH₇.₀ FALSE; FINAL_AUTH₇.₀ BLOCKED |
| **R0.3.3.A.2.2** | Autorizar V1-V4 sobre candidatos adicionais de Grupo C (CORPUS-002-HIST, CORPUS-003, CORPUS-011, CORPUS-005) | Possível identificação de mais candidatos Caso D ou diferente |
| **R0.3.3.A.2.3** | Autorizar busca por outros repositórios externos que possam conter ponte material para AION-6.x | Possível identificação de nova fonte |
| **R0.3.3.A.2.4** | Solicitar do PM evidência adicional de proveniência (manifesto de ingestão AION-6.x original, hash canônico, log de transferência) | Possível futura reavaliação V3 se evidência fornecida |
| **R0.3.3.A.2.5** | Confirmar que acervo TCR/QDT é o único externo relevante; declarar EP-0 final para Grupo A, B, D; declarar Caso D final para Grupo C; focar em Via B | Encerramento formal Grupo A, B, D como UNAVAILABLE; Grupo C como Caso D final |
| **R0.3.3.A.2.6** | Via B — Nova determinação metodológica (redefinir experimento sem depender de AION-6.x infrastructure) | Nova genealogia experimental |

### 10.3 O que NÃO será feito até determinação PM

- ✗ Nenhuma promoção automática de EP-1 PARTIAL CANDIDATE para EP-1 PARTIAL EFFECTIVE
- ✗ Nenhuma inferência de que TCR/QDT PDFs são autenticamente os mesmos arquivos do AION-6.x corpus
- ✗ Nenhuma instalação de dependências
- ✗ Nenhuma execução de scripts TCR/QDT ou AION
- ✗ Nenhuma execução de V1-V4 sobre outros componentes sem autorização específica
- ✗ Nenhuma alteração de artefato FROZEN
- ✗ Nenhuma alteração de `AUTH₇.₀ = FALSE`
- ✗ Nenhuma alteração de `FINAL_AUTH₇.₀ = BLOCKED`
- ✗ Nenhuma nova busca no TCR/QDT repo sem nova hipótese específica

### 10.4 Princípio operacional consolidado

> **Busca evidence-driven produz ausência de evidência — não evidência de ausência.**

Aplicado materialmente em R0.3.3.A.2: a busca exaustiva por ponte material dentro do TCR/QDT repo não encontrou evidência positiva da conexão TCR/QDT → AION-6.x. Mas isto **não constitui prova** de que a conexão não existiu — apenas demonstra materialmente que **a conexão não está documentada neste repositório**.

A distinção entre "ausência de evidência" e "evidência de ausência" é materialmente preservada. Aplicando o invariante `NON-OBSERVED ≠ FALSE`: a não-observação de ponte material não implica a falsidade da existência da ponte.

## 11. Confirmação de Integridade dos FROZEN

| Artefato | SHA-256 | Estado |
|---|---|---|
| AION-7.0.0_PROTOCOL.md | `b9b50b28579a8b5ac99abcc48898b34f965d1ce14de53b85062f7a1fea13a376` | INTACTO (idêntico a Tasks 65-80) |
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
       ▼  Determinação PM Task 79: autoriza R0.3.3
       │
AION-7.0.0-R0.3.3 EXTERNAL MATERIAL INTAKE: TCR/QDT REPOSITORY — CONCLUÍDO (Task 79)
       │
       ▼  Determinação PM Task 80: autoriza R0.3.3.A
       │
AION-7.0.0-R0.3.3.A V1-V4 CANDIDATE VERIFICATION — CONCLUÍDO (Task 80)
       │
       ├── C-01: Caso D (V1+V2+V4 PASS, V3 INSUFFICIENT)
       ├── C-02: Caso D (V1+V2+V4 PASS, V3 INSUFFICIENT)
       │
       ▼  Determinação PM Task 81 (PM-80.1): autoriza R0.3.3.A.2
       │
AION-7.0.0-R0.3.3.A.2 PROVENANCE BRIDGE RECOVERY — CONCLUÍDO (este documento, Task 81)
       │
       ├── P1 Manifesto de ingestão: AUSENTE (0 arquivos)
       ├── P2 Hash histórico: AUSENTE (0 arquivos)
       ├── P3 Logs/worklogs: AUSENTE (0 arquivos AION/CORPUS)
       ├── P4 Git history: AUSENTE (entry 13/08, 1d após AION; sem menção AION/CORPUS)
       │
       ├── C-01: Caso D permanece (V3 INSUFFICIENT confirmed by evidence-driven search)
       ├── C-02: Caso D permanece (V3 INSUFFICIENT confirmed by evidence-driven search)
       ├── EP-1 PARTIAL CANDIDATE / Caso D confirmed (not promoted)
       ├── AUTH₇.₀ = FALSE (preserved)
       ├── FINAL_AUTH₇.₀ = BLOCKED (preserved)
       ├── 4 FROZEN artifacts integrity verified
       │
       ▼  Próxima operação requer determinação PM:
       │
       ├── R0.3.3.A.2.1 — Aceitar Caso D como final; declarar busca esgotada em TCR/QDT
       ├── R0.3.3.A.2.2 — Autorizar V1-V4 sobre candidatos adicionais de Grupo C
       ├── R0.3.3.A.2.3 — Buscar outros repositórios externos
       ├── R0.3.3.A.2.4 — Solicitar evidência adicional de PM (manifesto, hash, log)
       ├── R0.3.3.A.2.5 — Confirmar TCR/QDT como único externo; declarar EP-0 final para A/B/D, Caso D final para C
       └── R0.3.3.A.2.6 — Via B (nova determinação metodológica)
```

---

*"O resultado de R0.3.3.A.2 é epistemicamente honesto: a busca evidence-driven procurou confirmar ou refutar a ponte material entre TCR/QDT e AION-6.x. Encontrou ausência de evidência — não evidência de ausência. As quatro prioridades (manifesto, hash, logs, git history) retornaram zero ocorrências de strings AION, CORPUS-002, CORPUS-006, ou hash canônico AION-6.x em qualquer arquivo do TCR/QDT repo. O histórico Git confirma que os PDFs candidatos entraram no TCR/QDT em 13/08/2026, 1 dia após a consolidação AION declarada no Handoff — consistência temporal narrativa, não material. A distinção entre 'ausência de evidência' e 'evidência de ausência' foi rigorosamente preservada. Caso D permanece para ambos os candidatos. A próxima transição epistemicamente válida requer nova fonte de evidência ou nova determinação metodológica do Projetista Master."*

**Fim do AION-7.0.0-R0.3.3.A.2 Provenance Bridge Recovery Report.**
