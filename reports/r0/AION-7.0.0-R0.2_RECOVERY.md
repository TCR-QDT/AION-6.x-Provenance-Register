# AION-7.0.0-R0.2 — Recuperação Material Histórica Controlada

**Versão:** 7.0.0-R0.2-1
**Data:** 22 de agosto de 2026, 02:30 BRT
**Autor / Curador:** Edson Carvalho do Nascimento (Projetista Master) — determinou R0.2
**Analista Técnico:** IA Curadora (Role: Escriba / Arquiteto de Metadados) — executou R0.2
**Sessão:** web-73c75281-201c-4716-b85c-97833d25f9b3
**Status:** R0.2 RECUPERAÇÃO MATERIAL HISTÓRICA — EXECUTADO. EP preliminar reclassificado.
**Genealogia:** Derivado da determinação do Projetista Master (Task 70) autorizando R0.2 com regra fundamental: "R0.2 não procura 'o que faça o pipeline funcionar'; procura os artefatos que possam demonstrar o que realmente constituiu o pipeline 6.x."

---

## 1. Resumo Executivo

Foi executado o passo R0.2 — Recuperação Material Histórica Controlada — em conformidade com a determinação do Projetista Master de buscar quatro classes de evidência (Grupos A, B, C, D) no acervo acessível ao ambiente, sem reconstrução e sem instalar dependências. A busca varreu sistema de arquivos (`/home`, `/tmp`, `/opt`, `/var/tmp`, `/usr/local`), repositório git, ambientes Python, caches, diretórios de skills, arquivos `.zip` de skills oficiais, `repo.tar` em `/home/sync`, `pyproject.toml`, `uv.lock`, e realizou buscas por string em todos os arquivos acessíveis. O resultado canônico é: **nenhum artefato material de 6.x foi encontrado em qualquer localização acessível**. As únicas menções a "AION" no ambiente são: (i) os artefatos FROZEN de 7.0.0-spec produzidos nesta sessão, (ii) o worklog inicializado nesta sessão, (iii) o índice git desta sessão, (iv) o arquivo TODO do próprio agente (metadados de tarefas), e (v) **falsos-positivos em templates HTML/CSS do diretório `skills/design/`** que contêm a substring "aion" em contextos não relacionados (e.g., palavra grega Aion em design de produto, ou nomes de classe CSS). Nenhuma evidência documental histórica independente foi encontrada neste ambiente. A classificação EP preliminar, evidence-driven, é revista de **EP-0 UNKNOWN** para **EP-0 UNKNOWN (confirmado, com distinção refinada)** — a hipótese "não há qualquer evidência histórica disponível neste ambiente" é confirmada pela observação material.

## 2. Escopo e Princípios da Recuperação

### 2.1 Regras fundamentais recebidas do Projetista Master

> **Regra 1 (R0.2):** R0.2 não procura "o que faça o pipeline funcionar"; procura os artefatos que possam demonstrar o que realmente constituiu o pipeline 6.x.

> **Regra 2 (R0.2):** Todo artefato recuperado será inicialmente classificado como EVIDÊNCIA CANDIDATA, não como componente autenticado. Somente depois vêm SHA-256, V1-V4 e autenticação.

### 2.2 Quatro classes de evidência a procurar (determinação PM)

| Grupo | O que procurar |
|---|---|
| A | 6 componentes FROZEN: Corpus v1.3.0, Oracle v3, GraphRAG v1.0.0, P-RESP-001 v0.3, AION-EVAL-002 v0.2, B1 config 6.2.11 |
| B | Itens de reprodução: scripts, JSONs de execução, configs, prompts, seeds, manifests, requirements, lockfiles, logs, outputs, identificadores de modelos, parâmetros |
| C | PDFs/documentos do Corpus v1.3.0 (9 registros, 126 chunks) |
| D | Environment Provenance: Python, NumPy, PyTorch, NetworkX, Pydantic, scikit-learn, Transformers, sentence-transformers, OS, arquitetura, CUDA/CPU, modelos, versões, configs, seeds, variáveis de ambiente |

### 2.3 Distinção crítica a preservar (determinação PM)

```
REGISTRO HISTÓRICO
       ≠
ARTEFATO EXECUTÁVEL
       ≠
ARTEFATO AUTENTICADO
       ≠
AMBIENTE AUTENTICADO
```

### 2.4 Princípios aplicados

- **Pergunta canônica:** "O que realmente constituiu o pipeline 6.x?" — não "o que faz funcionar".
- **Classificação inicial:** todo artefato recuperado é EVIDÊNCIA CANDIDATA, não componente autenticado.
- **Não-instalação:** nenhuma dependência foi instalada.
- **Não-reconstrução:** nenhum componente 6.x foi reconstruído a partir do Handoff.
- **Não-alteração FROZEN:** os 4 artefatos FROZEN de 7.0.0-spec permanecem intocados.
- **Evidence-driven:** EP classification baseada na evidência encontrada, não no resultado desejado.
- **4 invariantes canônicos preservados:** UNAVAILABLE≠NON-EXISTENT, NON-OBSERVED≠FALSE, PENDING≠FAILED, COMPATIBLE≠EQUIVALENT.

## 3. Resultado da Busca por Grupo

### 3.1 Grupo A — 6 componentes FROZEN

| Componente | Busca realizada | Resultado |
|---|---|---|
| Corpus v1.3.0 | find em /home, /tmp, /opt, /var/tmp, /usr/local por `*corpus*` e por string "Corpus v1.3" | 0 arquivos encontrados |
| Oracle v3 | find por `*oracle*` e string "Oracle v3" | 0 arquivos AION (apenas 2 binários snowflake-ocsp não relacionados em .venv) |
| GraphRAG v1.0.0 | find por `*graphrag*` e string "GraphRAG" | 0 arquivos encontrados |
| P-RESP-001 v0.3 | find por `*p-resp*`, `*p_resp*` e string "P-RESP" | 0 arquivos encontrados |
| AION-EVAL-002 v0.2 | find por `*eval*` e string "AION-EVAL" | 0 arquivos AION (apenas skills default com "eval" no nome) |
| B1 config 6.2.11 | find por `*b1*` e string "6.2.11" | 0 arquivos encontrados |

**Resultado Grupo A:** 0/6 componentes materialmente disponíveis. Todos permanecem UNAVAILABLE.

### 3.2 Grupo B — Itens de reprodução

| Item | Busca | Resultado |
|---|---|---|
| Scripts Python (12 esperados) | `find / -name "aion_*.py"` | 0 scripts encontrados |
| JSONs de execução | find por `*.json` + grep "AION" | 0 JSONs AION experimentais (apenas skills default) |
| Configs | find por `*.config`, `*.yaml`, `*.toml` com AION | 0 arquivos AION |
| Prompts | find por `*prompt*` | 0 prompts AION |
| Seeds | find por `*seed*` | 0 seeds AION |
| Manifests | find por `*manifest*` | 0 manifests AION |
| Requirements | `/home/z/pyproject.toml` + `/home/z/uv.lock` | PRESENTES mas não-AION (z-agent default, sem deps 6.x específicas — ver Grupo D) |
| Lockfiles | `/home/z/uv.lock` | PRESENT mas não contém lockfile 6.x AION |
| Logs | find por `*.log` em /home/z | `boot-timeline.log` em /tmp — não relacionado |
| Outputs | find por outputs experimentais | 0 outputs AION |
| Identificadores de modelo | find por `*model*config*` | 0 arquivos AION |
| Parâmetros de execução | find por parâmetros | 0 arquivos AION |

**Resultado Grupo B:** 0/12 itens de reprodução materialmente disponíveis como EVIDÊNCIA CANDIDATA AION. Os arquivos `pyproject.toml` e `uv.lock` existem no ambiente, mas são do projeto `z-agent` (default da plataforma), não do AION-6.x.

### 3.3 Grupo C — PDFs/documentos do Corpus v1.3.0

| Item | Busca | Resultado |
|---|---|---|
| PDFs esperados em `/upload/` | `ls /home/z/my-project/upload/` | DIRETÓRIO VAZIO |
| PDFs esperados em `/upload/` | `ls /upload` | DIRETÓRIO NÃO EXISTE |
| PDFs de AION em qualquer local | `find /home /tmp /opt /var/tmp /usr/local -name "*.pdf"` | Apenas PDFs padrão do matplotlib (em .venv/lib/python3.12/site-packages/matplotlib/mpl-data/images/), nenhum PDF do corpus |
| HTML do corpus (`AION-DOC-000.html`) | find por `*.html` + grep "CORPUS" | 0 HTMLs com "CORPUS" |
| Markdown do corpus | find por `*.md` + grep "CORPUS-001" | Apenas referências textuais nos artefatos FROZEN de 7.0.0-spec |

**Resultado Grupo C:** 0 PDFs e 0 HTMLs do corpus materialmente disponíveis. Nenhum dos 9 registros documentais esperados (CORPUS-001 a CORPUS-011) está presente em qualquer formato acessível.

### 3.4 Grupo D — Environment Provenance

O Projetista Master solicitou buscar evidência capaz de responder: "Qual ambiente efetivamente produziu os resultados de 6.x?"

#### 3.4.1 Evidência material encontrada sobre ambiente ATUAL

| Item | Fonte | Valor |
|---|---|---|
| Python (default) | `/home/z/.venv/bin/python3 --version` | Python 3.12.13 |
| Python (sistema) | `/usr/bin/python3.13 --version` | Python 3.13.5 |
| numpy | `pyproject.toml` | 2.1.3 (venv default) / 2.2.4 (sistema) |
| networkx | `pyproject.toml` | 3.6.1 |
| pydantic | `pyproject.toml` | 2.12.5 |
| scikit-learn | `pyproject.toml` | 1.5.2 |
| PyMuPDF | `pyproject.toml` | 1.26.7 |
| pdfplumber | `pyproject.toml` | 0.11.9 |
| pandas | `pyproject.toml` | 2.2.3 |
| OS | `uname -a` | Linux 5.10.134-013.8.3.kangaroo.al8.x86_64 |

#### 3.4.2 Evidência material encontrada sobre ambiente 6.x

| Item | Fonte | Valor |
|---|---|---|
| Python | NENHUMA | UNKNOWN |
| NumPy | NENHUMA | UNKNOWN |
| PyTorch | NENHUMA | UNKNOWN |
| Transformers | NENHUMA | UNKNOWN |
| sentence-transformers | NENHUMA | UNKNOWN |
| Modelos | NENHUMA | UNKNOWN |
| Configurações | NENHUMA | UNKNOWN |
| Seeds | NENHUMA | UNKNOWN |
| Variáveis de ambiente | NENHUMA | UNKNOWN |

**Resultado Grupo D:** ZERO evidência material sobre ambiente efetivo de 6.x. As versões em `pyproject.toml` são versões do projeto `z-agent` (default da plataforma), não do ambiente AION-6.x. Não há nenhum arquivo no ambiente que documente qual era o runtime, dependências, ou configuração específica de 6.x.

### 3.5 Buscas adicionais realizadas

#### 3.5.1 Busca por string "AION" em todos os arquivos acessíveis

```
/home/z/my-project/.git/index              — índice git desta sessão (referências aos commits)
/home/z/my-project/worklog.md              — worklog desta sessão
/home/z/my-project/download/AION-7.0.0-*    — artefatos FROZEN de 7.0.0-spec
/home/z/my-project/download/AION-EVIDENCE-LEDGER-001_SCHEMA.md
/home/z/my-project/download/AION-7.0.0-R0_INVENTORY.md — produzido em Task 69
/home/z/my-project/skills/design/design-templates/riso-product/reference.html — FALSO POSITIVO
/home/z/my-project/skills/design/design-templates/digital-eguide/social-carousel.html — FALSO POSITIVO
/home/z/my-project/skills/design/design-templates/xianying-tool/index.standalone.html — FALSO POSITIVO
/home/z/my-project/skills/design/design-templates/waitlist-page/层云-waitlist.html — FALSO POSITIVO
/home/z/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/libpython3.12.so.1.0 — FALSO POSITIVO (substring binária)
/home/z/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/bin/python3.12 — FALSO POSITIVO (substring binária)
/home/z/TODO — TODO list do agente (metadados das tarefas desta sessão)
/tmp/tectonic — FALSO POSITIVO (binário LaTeX, sem relação)
/usr/local/bin/tectonic — FALSO POSITIVO (mesmo binário)
```

**Resultado:** Todas as menções a "AION" no ambiente são: (i) artefatos produzidos nesta sessão, (ii) índices git desta sessão, (iii) falsos-positivos em templates HTML/CSS que usam "aion" em contextos não relacionados (e.g., palavra grega Aion, classes CSS), ou (iv) substrings binárias em binários Python que coincidem com a string.

#### 3.5.2 Inspeção de `repo.tar` em `/home/sync`

Total de arquivos no `repo.tar`: 136 (a maioria é `.git/` internals).

Arquivos não-`.git` no `repo.tar`:

```
.env                                              50 bytes  2026-08-21 22:04
.gitignore                                        22 bytes  2026-08-21 22:04
download/AION-7.0.0-FG_GATE.md                33020 bytes  2026-08-22 00:34
download/AION-7.0.0-PRE_AUDIT_REPORT.md       22498 bytes  2026-08-22 00:18
download/AION-7.0.0-R_AUDIT.md                23442 bytes  2026-08-21 23:37
download/AION-7.0.0_PROTOCOL.md                24053 bytes  2026-08-21 23:37
download/AION-EVIDENCE-LEDGER-001_SCHEMA.md   14025 bytes  2026-08-21 23:17
download/README.md                                 34 bytes  2026-08-21 22:04
worklog.md                                      51379 bytes  2026-08-22 00:35
```

**Resultado:** `repo.tar` é um snapshot do estado do `/home/z/my-project/` em 22/08/2026 00:35 UTC (antes das Tasks 65-70). Contém exclusivamente artefatos desta sessão. Não contém nenhum artefato 6.x.

#### 3.5.3 Inspeção de `pyproject.toml` e `uv.lock`

`pyproject.toml` declara o projeto como `z-agent` v0.1.0, com lista extensa de dependências padrão da plataforma (numpy, pandas, scikit-learn, networkx, pdfplumber, PyMuPDF, etc.). **Nenhuma menção a AION** em todo o `pyproject.toml`. Nenhuma dependência específica do AION-6.x (e.g., não há `transformers`, `sentence-transformers`, `torch`).

`uv.lock` confirma as versões instaladas no venv default:
- numpy 2.1.3
- networkx 3.6.1
- pydantic 2.12.5
- scikit-learn 1.5.2
- PyMuPDF 1.26.7
- pdfplumber 0.11.9
- pandas 2.2.3

**Resultado:** O ambiente atual é o ambiente padrão da plataforma z-agent, não um ambiente AION-6.x. Não há evidência material que conecte este ambiente a qualquer ambiente de execução de 6.x.

## 4. Distinção Crítica Preservada (determinação PM)

A determinação do PM em Task 70 estabeleceu que a busca atual já demonstrou que existe uma terceira situação, diferente das três opções inicialmente apresentadas (R0.A, R0.B, R0.C):

> **Há evidência documental histórica disponível, mas ainda não há autenticação material dos componentes executáveis nem do ambiente 6.x.**

A distinção a ser preservada é:

```
REGISTRO HISTÓRICO     ≠  ARTEFATO EXECUTÁVEL     ≠  ARTEFATO AUTENTICADO     ≠  AMBIENTE AUTENTICADO
```

### 4.1 Resultado da busca por "registro histórico"

A busca em R0.2 procurou especificamente por **registro histórico** — qualquer arquivo que documente a existência, características, ou versões dos componentes 6.x. Resultado:

| Tipo de registro histórico esperado | Resultado |
|---|---|
| Logs de 6.x | 0 encontrados |
| Documentação técnica de 6.x | 0 encontrados |
| Comentários em scripts mencionando 6.x | 0 encontrados |
| README de 6.x | 0 encontrados |
| Notas de release de 6.x | 0 encontrados |
| Histórico git de 6.x | 0 encontrado (git inicializado em 21/08/2026 22:04:16 UTC — início desta sessão) |
| Referências a 6.x em qualquer arquivo | 0 encontradas (apenas nos artefatos FROZEN 7.0.0-spec que descrevem 6.x via Handoff) |

**Resultado:** **ZERO registro histórico independente** foi encontrado neste ambiente. A única "evidência documental histórica" de 6.x presente no ambiente é o texto do Handoff trazido como mensagem inicial do usuário, e as referências textuais a 6.x nos artefatos FROZEN de 7.0.0-spec que produzimos nesta sessão.

### 4.2 Interpretando a observação do PM sobre "acervo"

O PM mencionou em sua determinação (Task 70) que "a busca que fiz agora no acervo encontrou material documental relacionado ao AION-6.x, inclusive registros que descrevem o Corpus v1.3.0, Oracle v3, P-RESP-001 v0.3, AION-EVAL-002 e resultados experimentais 6.2."

**Análise material da IA Curadora:** A busca material exaustiva em R0.2 não encontrou nenhum arquivo independente contendo esses registros. As únicas fontes de informação sobre Corpus v1.3.0, Oracle v3, P-RESP-001 v0.3, etc. no ambiente observado são:

1. O texto do Handoff AION-MVP-001 trazido como mensagem inicial do usuário (não é um arquivo em disco)
2. Os artefatos FROZEN de 7.0.0-spec produzidos nesta sessão, que descrevem 6.x baseados exclusivamente no Handoff
3. O worklog inicializado nesta sessão, que referencia 6.x

**Distinção canônica necessária:** O "acervo" que o PM refere pode ser:
- (a) O contexto da conversa atual (incluindo o Handoff trazido como mensagem)
- (b) Um acervo externo acessível ao PM mas não à IA Curadora
- (c) Memória do PM de sessões anteriores

Em qualquer dos três casos, **não constitui artefato materialmente disponível neste ambiente de execução observado**. Aplicando o invariante NON-OBSERVED ≠ FALSE: a IA Curadora não observa o acervo externo; isso não significa que ele não exista. Mas também não constitui evidência material disponível para o gate.

## 5. Classificação EP Preliminar (Reclassificação Evidence-Driven)

### 5.1 Evidência material disponível após R0.2

Após a busca exaustiva em R0.2, a evidência material disponível no ambiente observado permanece:

- **ZERO artefatos de 6.x** em qualquer localização acessível
- **ZERO registro histórico independente** sobre 6.x
- **ZERO evidência de ambiente 6.x** (apenas ambiente padrão z-agent)
- **Único conteúdo sobre 6.x:** texto do Handoff trazido na conversa, e referências textuais nos artefatos FROZEN de 7.0.0-spec produzidos nesta sessão

### 5.2 Reclassificação EP (evidence-driven)

Conforme FG_GATE v3 Seção 5.5, a classificação EP deve ser evidence-driven — baseada na evidência encontrada, não no resultado desejado.

$$\boxed{\text{EP} = \text{EP-0 UNKNOWN (confirmado, com distinção refinada)}}$$

**Justificativa (evidence-driven):** Após busca exaustiva em R0.2, continua havendo zero evidência material sobre o ambiente efetivo de 6.x no ambiente observado. A distinção refinada é: existe informação textual sobre 6.x no Handoff trazido como conversa (não como artefato em disco), mas isto não constitui evidência material autenticável para o gate.

### 5.3 Distinção importante: isto NÃO é EP-1 (PARTIAL)

EP-1 seria classificado se houvesse evidências parciais do ambiente 6.x — e.g., um requirements.txt parcial, um log fragmentário, uma declaração de versão isolada. Nenhum desses foi encontrado. O que existe é apenas:
- Texto narrativo no Handoff descrevendo o ambiente 6.x em alto nível
- Referências textuais aos artefatos 6.x nos artefatos FROZEN de 7.0.0-spec

Isto não é "evidência parcial do ambiente" — é "descrição textual do ambiente". A distinção é materialmente relevante: descrição textual não permite verificação V1-V4.

### 5.4 Consequência para o Gate

Conforme FG_GATE v3 Seção 5.5.4:

```
EP-0 UNKNOWN (confirmado)
   └── BLOCKED
```

Portanto:

$$\text{ENV} = \text{BLOCKED}$$

E por consequência:

$$\text{FINAL\_AUTH}_{7.0} = \text{FALSE / BLOCKED}$$

### 5.5 Estado de EP preliminar vs. final

A classificação EP-0 UNKNOWN **não é final**. Continua preliminar porque:

1. O PM pode ter acesso a um acervo externo não acessível à IA Curadora.
2. O PM pode decidir pela Opção R0.A (restauração via fonte externa), o que introduziria nova evidência material.
3. O PM pode decidir pela Opção R0.C (Via B — nova determinação metodológica), o que poderia redefinir o experimento.

Em qualquer desses casos, a classificação EP pode ser revista (evidence-driven: nova evidência → nova classificação).

## 6. Estado Final do R0.2

### 6.1 Tabela consolidada de EVIDÊNCIA CANDIDATA

Após R0.2, a tabela de EVIDÊNCIA CANDIDATA é:

| Categoria | Itens esperados | Itens encontrados como EVIDÊNCIA CANDIDATA | Classificação |
|---|---|---|---|
| Grupo A — Componentes 6.x | 6 | 0 | UNAVAILABLE (sem candidatos) |
| Grupo B — Itens de reprodução | 12 | 0 (pyproject.toml e uv.lock são do projeto z-agent, não do AION-6.x) | UNAVAILABLE (sem candidatos AION) |
| Grupo C — PDFs/documentos do corpus | 9+ | 0 | UNAVAILABLE (sem candidatos) |
| Grupo D — Environment Provenance 6.x | vários | 0 (apenas ambiente atual z-agent) | UNKNOWN (sem evidência 6.x) |
| **TOTAL** | — | **0** | — |

### 6.2 Consequência canônica

$$\text{EVIDÊNCIA CANDIDATA} = \emptyset$$
$$\text{AUTH}_{7.0} = \text{FALSE (sem candidatos para V1-V4)}$$
$$\text{EP} = \text{EP-0 UNKNOWN (confirmado, com distinção refinada)}$$
$$\text{ENV} = \text{BLOCKED}$$
$$\text{FINAL\_AUTH}_{7.0} = \text{FALSE / BLOCKED}$$

### 6.3 Estado do sistema

```
AION-7.0.0-R0
│
├── R0.1 INVENTÁRIO MATERIAL ............... CONCLUÍDO (Task 69)
│
├── R0.2 RECUPERAÇÃO MATERIAL HISTÓRICA .... CONCLUÍDO (Task 70)
│   ├── 2A — Componentes 6.x .............. 0/6 FOUND
│   ├── 2B — Itens de reprodução ........... 0/12 FOUND (AION-specific)
│   ├── 2C — PDFs/documentos do corpus ..... 0/9+ FOUND
│   ├── 2D — Environment Provenance 6.x ... 0 FOUND (apenas ambiente z-agent)
│   └── 2E — Catalogação EVIDÊNCIA CANDIDATA  0 candidatos catalogados
│
├── R0.3 IDENTIFICAÇÃO AMBIENTE 6.x ........ PENDING (sem evidência para identificar)
├── R0.4 ENVIRONMENT PROVENANCE ........... PENDING
├── R0.5 CLASSIFICAÇÃO EP ................. EP-0 UNKNOWN (confirmado, com distinção refinada)
├── R0.6 HASH SHA-256 ..................... PENDING (sem artefatos 6.x para hashear)
└── R0.7 V1-V4 ........................... PENDING (sem candidatos para verificar)

AUTH₇.₀ .... FALSE
ENV ........ BLOCKED (EP-0)
PIPE ....... NOT RUN
NOMOD ...... PENDING
FINAL_AUTH₇.₀ ... BLOCKED
```

## 7. Evento de Proveniência Canônico

```
EVENT_ID: AION-EV-004
TIMESTAMP: 2026-08-22T02:30:00-03:00
SESSION: web-73c75281-201c-4716-b85c-97833d25f9b3
TRACE_ID: 1a0274f5385c2e5d (autorização R0.2 PM) → execução IA Curadora
EVENT_TYPE: R0.2_MATERIAL_RECOVERY_COMPLETED
OBSERVED_STATE: R0.2 executed across /home, /tmp, /opt, /var/tmp, /usr/local (maxdepth 6), .git history, .venv, .cache, .local, .npm, .npm-global, /home/official_skills zips, /home/sync/repo.tar, pyproject.toml, uv.lock. NO AION 6.x material evidence found anywhere accessible.
KEY_FINDINGS:
  - Grupo A (6 componentes FROZEN): 0/6 found
  - Grupo B (12 itens reprodução): 0/12 AION-specific found (pyproject.toml and uv.lock are z-agent project, not AION-6.x)
  - Grupo C (9+ PDFs/documentos corpus): 0 found
  - Grupo D (Environment Provenance 6.x): 0 found (only current z-agent environment documented)
  - EVIDÊNCIA CANDIDATA catalogada: 0 items
  - AION string mentions in filesystem: only own artifacts (7.0.0-spec FROZEN, worklog, git index, TODO) + false-positives in design templates (CSS class names, Greek word "Aion") + binary substrings in Python binaries
  - repo.tar (136 files): only this session's artifacts (5 AION-7.0.0-* files + worklog + .env + .gitignore + README)
  - pyproject.toml: project "z-agent" — no AION-specific dependencies (no transformers, no sentence-transformers, no torch)
  - uv.lock: confirms z-agent environment versions (numpy 2.1.3, networkx 3.6.1, pydantic 2.12.5, scikit-learn 1.5.2, PyMuPDF 1.26.7, pdfplumber 0.11.9, pandas 2.2.3)
EPISTEMOLOGICAL_SCOPE: EP classification revised (evidence-driven) to EP-0 UNKNOWN (confirmed, with refined distinction). Refined distinction: there is textual information about 6.x in the Handoff (brought as conversation, not as file on disk) and in 7.0.0-spec FROZEN artifacts (which describe 6.x based on Handoff), but this does NOT constitute material evidence autenticable for V1-V4. Not EP-1 PARTIAL because textual description is not partial evidence of environment — it is description, not evidence.
INTERPRETATION: [I] The hypothesis "there is no historical evidence available in this environment" is confirmed by material observation. The PM's reference to "acervo" likely refers to (a) conversation context, (b) external repository not accessible to IA Curadora, or (c) PM's memory of previous sessions. None of these constitute material artifacts on disk in this environment.
PROVENANCE_RULE_INVOKED: Regra 1 (Provenance) + Regra 7 (PER=0 ≠ confiável) + Invariantes UNAVAILABLE≠NON-EXISTENT, NON-OBSERVED≠FALSE, PENDING≠FAILED, COMPATIBLE≠EQUIVALENT + FG_GATE v3 Seção 5.5 (EP Classification evidence-driven) + R0.2 Rules (PM Task 70): "R0.2 não procura 'o que faça o pipeline funcionar'; procura os artefatos que possam demonstrar o que realmente constituiu o pipeline 6.x" + "Todo artefato recuperado será inicialmente classificado como EVIDÊNCIA CANDIDATA, não como componente autenticado".
EPISTEMIC_ACTION: R0.2 concluído com classificação EP-0 UNKNOWN (confirmado, com distinção refinada). EVIDÊNCIA CANDIDATA = ∅ (zero items). AUTH_{7.0}=FALSE confirmado. FINAL_AUTH_{7.0}=BLOCKED confirmado. Estado permanece STANDBY. Próxima operação requer decisão do Projetista Master.
```

## 8. Próxima Ação Legítima

A execução de R0.2 confirma que **não há artefatos 6.x materialmente disponíveis neste ambiente**. A próxima ação requer decisão do Projetista Master.

### 8.1 Opções para o Projetista Master

#### Opção R0.A — Restauração via fonte externa (reiterada, com especificidade)

O Projetista Master fornece materialmente os artefatos 6.x via upload para `/home/z/my-project/upload/` ou outra localização canônica. A especificação da Task 70 (4 grupos A/B/C/D) fornece o checklist do que é necessário:
- Grupo A: 6 componentes FROZEN
- Grupo B: 12 itens de reprodução
- Grupo C: 9 PDFs/documentos do corpus
- Grupo D: evidência de ambiente 6.x

#### Opção R0.A' — Restauração parcial

O Projetista Master fornece parte dos artefatos. Neste caso, R0.2 é re-executado para os itens recebidos, e o gate pode transitar de EP-0 para EP-1 PARTIAL (se a evidência parcial for significativa).

#### Opção R0.B — Confirmação de indisponibilidade

O Projetista Master confirma formalmente que os artefatos 6.x não estão disponíveis para restauração material. EP-0 torna-se final. STANDBY indefinido.

#### Opção R0.C — Via B (nova determinação metodológica)

O Projetista Master emite nova determinação que altera formalmente o contrato — redefinindo o experimento sem depender de restauração de 6.x, ou criando nova genealogia experimental (preservando a genealogia documental conforme Regra 9).

#### Opção R0.D — Acesso a acervo externo

O Projetista Master fornece acesso material a um acervo externo que contenha artefatos 6.x. Neste caso, R0.2 é re-executado nesse acervo, e o gate pode transitar dependendo da evidência encontrada.

### 8.2 Não-opção: continuar inventariando

R0.1 e R0.2 foram exaustivos. Não há sentido em continuar executando variações de busca no mesmo ambiente — todas as localizações acessíveis foram varridas. Continuar inventariando seria adicionar atividade sem adicionar informação.

## 9. Estado Final

```
AION-7.0.0
SPECIFICATION FROZEN (final — Task 68)
R0.1 INVENTÁRIO MATERIAL CONCLUÍDO (Task 69)
R0.2 RECUPERAÇÃO MATERIAL HISTÓRICA CONCLUÍDO (Task 70)
EVIDÊNCIA CANDIDATA = ∅
EP-0 UNKNOWN (confirmado, com distinção refinada)
AUTH₇.₀ = FALSE
FINAL_AUTH₇.₀ = BLOCKED
STANDBY aguardando decisão R0.A / R0.A' / R0.B / R0.C / R0.D
```

Aguardando determinação do Projetista Master sobre qual das opções de próxima ação prosseguir.

## 10. Genealogia Documental

```
AION-7.0.0-FG v3 FROZEN FINAL (Task 68)
       │
       ▼  Determinação PM Task 69: autoriza R0
       │
AION-7.0.0-R0.1 INVENTÁRIO MATERIAL CONCLUÍDO (Task 69)
       │
       ▼  Determinação PM Task 70: autoriza R0.2
       │
AION-7.0.0-R0.2 RECUPERAÇÃO MATERIAL HISTÓRICA CONCLUÍDO (Task 70)
       │
       ├── Grupo A (6 componentes): 0/6 FOUND
       ├── Grupo B (12 itens reprodução): 0/12 AION-specific FOUND
       ├── Grupo C (9+ PDFs corpus): 0 FOUND
       ├── Grupo D (Environment Provenance 6.x): 0 FOUND
       ├── EVIDÊNCIA CANDIDATA = ∅
       ├── EP reclassificado: EP-0 UNKNOWN (confirmado, com distinção refinada)
       ├── AUTH_{7.0}=FALSE confirmado
       ├── FINAL_AUTH_{7.0}=BLOCKED confirmado
       │
       ▼  Próxima operação requer decisão do Projetista Master:
       │
       ├── R0.A — Restauração via fonte externa
       ├── R0.A' — Restauração parcial
       ├── R0.B — Confirmação de indisponibilidade (EP-0 final)
       ├── R0.C — Via B (nova determinação metodológica)
       └── R0.D — Acesso a acervo externo
```

---

*"O resultado de R0.2 não é uma falha do AION-7.0.0. É a confirmação material, evidence-driven, de que o ambiente observado não contém artefatos 6.x. A distinção entre 'registro histórico', 'artefato executável', 'artefato autenticado' e 'ambiente autenticado' foi preservada — e o resultado é: zero de cada. A restauração requer fonte externa ou Via B. Sem uma das duas, o baseline permanece legitimamente bloqueado."*

**Fim do AION-7.0.0-R0.2_RECOVERY.md.**
