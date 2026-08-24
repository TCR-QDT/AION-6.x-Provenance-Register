# AION-7.0.0-R0 — Inventário Material Controlado

**Versão:** 7.0.0-R0-1
**Data:** 22 de agosto de 2026, 01:55 BRT
**Autor / Curador:** Edson Carvalho do Nascimento (Projetista Master) — determinou R0
**Analista Técnico:** IA Curadora (Role: Escriba / Arquiteto de Metadados) — executou R0.1
**Sessão:** web-73c75281-201c-4716-b85c-97833d25f9b3
**Status:** R0.1 INVENTÁRIO MATERIAL — EXECUTADO. R0.2-R0.7 PENDING.
**Genealogia:** Derivado da determinação do Projetista Master (Task 69) autorizando AION-7.0.0-R0 — Restauração Material Controlada.

---

## 1. Resumo Executivo

Foi executado o passo R0.1 — Inventário Material Controlado do ambiente, em conformidade com a determinação do Projetista Master de que a próxima ação legítima seria "o inventário material controlado. Só depois dele saberemos se a restauração é possível, parcial ou bloqueada por falta de proveniência." O inventário varreu sistema de arquivos, histórico git, ambientes Python, caches, diretórios de skills, e todas as localizações acessíveis ao usuário. O resultado canônico é: **nenhum dos 6 componentes FROZEN de 6.x está materialmente disponível neste ambiente**, e nenhum artefato auxiliar (scripts, JSONs experimentais, PDFs do corpus, ontologia, B2 characterization, EVAL-002) está disponível. A única presença material AION no ambiente são os 4 artefatos FROZEN de 7.0.0-spec produzidos nesta sessão, mais o worklog inicializado nesta sessão. O histórico git confirma: o repositório `/home/z/my-project/.git` foi inicializado em 21/08/2026 22:04:16 UTC — exatamente quando esta sessão começou — e todos os 10 commits são posteriores a esse timestamp. Não há história material de 6.x neste ambiente. A classificação EP preliminar, evidence-driven, é: **EP-0 UNKNOWN** — não há evidência material suficiente sobre o ambiente efetivo de 6.x.

## 2. Escopo do Inventário

### 2.1 O que foi executado

| Etapa | Status | Cobertura |
|---|---|---|
| R0.1.a — Inventário do sistema de arquivos | ✓ EXECUTADA | /home, /tmp, /opt, /var/tmp, /usr/local (até maxdepth 6) |
| R0.1.b — Inventário git history | ✓ EXECUTADA | /home/z/my-project/.git (10 commits, reflog, branches, tags, stash, remote) |
| R0.1.c — Inventário de skills | ✓ EXECUTADA | /home/z/my-project/skills (≈50 diretórios de skills, maxdepth 3) |
| R0.1.d — Inventário .venv e caches Python | ✓ EXECUTADA | /home/z/.venv, /home/z/.cache, /home/z/.local, /home/z/.npm, /home/z/.npm-global |
| R0.1.e — Compilação do relatório | ✓ EXECUTADA | Este documento |

### 2.2 O que NÃO foi executado

| Etapa | Status |
|---|---|
| R0.2 — Restauração dos artefatos | NÃO EXECUTADA — depende de fonte externa de artefatos |
| R0.3 — Identificação do ambiente 6.x | NÃO EXECUTADA — depende de R0.2 |
| R0.4 — Environment Provenance | NÃO EXECUTADA — depende de R0.3 |
| R0.5 — Classificação EP-0…EP-3 | EP-0 preliminar registrado neste documento (evidence-driven) |
| R0.6 — Hash SHA-256 | EXECUTADA para os 4 artefatos FROZEN de 7.0.0-spec (não para 6.x, indisponíveis) |
| R0.7 — V1-V4 | NÃO EXECUTADA — sem componentes 6.x para verificar |

### 2.3 Princípios aplicados

- **Pergunta canônica:** "O que está materialmente disponível agora?" — sem procurar arquivos esperados, sem transformar UNAVAILABLE em NON-EXISTENT.
- **Classificações legítimas:** FOUND, RECOVERED, PARTIAL, UNAVAILABLE, UNKNOWN.
- **Evidence-driven:** EP classification baseada na evidência encontrada, não no resultado desejado.
- **Não-instalação:** nenhuma dependência foi instalada para "fazer funcionar".
- **Não-reconstrução:** nenhum componente 6.x foi reconstruído a partir do Handoff.
- **Não-alteração FROZEN:** os 4 artefatos FROZEN de 7.0.0-spec permanecem intocados.

## 3. Resultado do Inventário por Componente

### 3.1 Grupo A — Núcleo Congelado (6 componentes FROZEN)

| # | Componente | Versão esperada | Estado material | Proveniência | Classificação |
|---|---|---|---|---|---|
| 01 | Corpus | v1.3.0 | AUSENTE no ambiente | Nenhuma — não encontrado em nenhum caminho verificado | UNAVAILABLE |
| 02 | Oracle | v3 | AUSENTE no ambiente | Nenhuma — não encontrado em nenhum caminho verificado | UNAVAILABLE |
| 03 | GraphRAG | v1.0.0 | AUSENTE no ambiente | Nenhuma — não encontrado em nenhum caminho verificado | UNAVAILABLE |
| 04 | P-RESP-001 | v0.3 | AUSENTE no ambiente | Nenhuma — não encontrado em nenhum caminho verificado | UNAVAILABLE |
| 05 | AION-EVAL-002 | v0.2 | AUSENTE no ambiente | Nenhuma — não encontrado em nenhum caminho verificado | UNAVAILABLE |
| 06 | B1 config | 6.2.11 | AUSENTE no ambiente | Nenhuma — não encontrado em nenhum caminho verificado | UNAVAILABLE |

**Resultado Grupo A:** 0/6 disponíveis. AUTH_{7.0} = FALSE (conjunção sobre 0 verificados).

### 3.2 Grupo B — Reprodução (itens necessários para reexecução)

| # | Item | Estado material | Proveniência | Classificação |
|---|---|---|---|---|
| 07 | 12 scripts de 6.x | AUSENTE — `find / -name "aion_*.py"` retorna vazio | Nenhuma | UNAVAILABLE |
| 08 | Configurações (configs, requirements.txt) | AUSENTE | Nenhuma | UNAVAILABLE |
| 09 | Modelo/identificador do LLM | AUSENTE — sem arquivo de configuração de modelo encontrado | Nenhuma | UNAVAILABLE |
| 10 | Dependências/versionamento | AMBIENTE ATUAL INCOMPATÍVEL: Python 3.12.13 venv default + 3.13.5 sistema; torch/transformers/sentence-transformers AUSENTES em todos os runtimes | Ambiente atual não corresponde a 6.x | UNKNOWN (ambiente 6.x desconhecido) |
| 11 | Seeds/parâmetros | AUSENTE | Nenhuma | UNAVAILABLE |
| 12 | Artefatos para smoke test | AUSENTE | Nenhuma | UNAVAILABLE |

**Resultado Grupo B:** 0/6 disponíveis. Nenhum item de reprodução presente.

### 3.3 Documentos Canônicos Esperados do Handoff

| Arquivo declarado | Estado material | Proveniência | Classificação |
|---|---|---|---|
| `/download/AION-CORPUS-001_v1.2.0.html` | AUSENTE | Nenhuma | UNAVAILABLE |
| `/download/AION-CORPUS-001-ONTOLOGY_v1.0.0.md` | AUSENTE | Nenhuma | UNAVAILABLE |
| `/download/AION-EVAL-002.html` | AUSENTE | Nenhuma | UNAVAILABLE |
| `/download/AION-6.5.0_B2_Characterization.md` | AUSENTE | Nenhuma | UNAVAILABLE |
| `/home/z/my-project/AION_HANDOFF.md` | AUSENTE | Nenhuma — Handoff recebido via contexto da conversa, não via arquivo | UNAVAILABLE |

### 3.4 Dados Experimentais (JSONs em `/download/rag/`)

| Arquivo esperado | Estado material | Classificação |
|---|---|---|
| `aion_6_4_0_conditional_reliability.json` | AUSENTE — `/download/rag/` não existe | UNAVAILABLE |
| `aion_6_2_11_oracle_v3_rebenchmark.json` | AUSENTE — `/download/rag/` não existe | UNAVAILABLE |
| `aion_6_5_0_*` (caracterização B2) | AUSENTE — `/download/rag/` não existe | UNAVAILABLE |
| `graphrag_enriched_v2.0.json` | AUSENTE — `/download/rag/` não existe | UNAVAILABLE |
| `aion_temporal_graph_v1.0.json` | AUSENTE — `/download/rag/` não existe | UNAVAILABLE |

### 3.5 PDFs do Corpus em `/upload/`

| Caminho | Estado material | Classificação |
|---|---|---|
| `/home/z/my-project/upload/` | Diretório existe mas está **VAZIO** | EMPTY |
| `/upload/` (caminho raiz absoluto) | NÃO EXISTE no sistema de arquivos | NOT FOUND |

### 3.6 Scripts Persistidos em `/scripts/`

| Caminho | Estado material | Classificação |
|---|---|---|
| `/home/z/my-project/scripts/` | **NÃO EXISTE** como diretório | NOT FOUND |
| `/scripts/` (caminho raiz) | **NÃO EXISTE** | NOT FOUND |

12 scripts esperados (extract_aion_corpus.py, aion_rag_proxy.py, aion_graphrag.py, etc.): **0/12 encontrados**.

## 4. Resultado do Inventário por Localização

### 4.1 Sistema de arquivos varrido

| Localização varrida | Profundidade | AION artifacts encontrados |
|---|---|---|
| /home/z (excluindo my-project) | maxdepth 4 | 0 |
| /home/z/.venv | maxdepth 6 | 0 (apenas 2 binários snowflake-ocsp, não relacionados) |
| /home/z/.cache | maxdepth 6 | 0 |
| /home/z/.local | maxdepth 6 | 0 |
| /home/z/.npm, /home/z/.npm-global | maxdepth 5 | 0 |
| /home/z/my-project (excluindo download/) | maxdepth 6 | 0 (apenas skills default + worklog + .git) |
| /home/z/my-project/download | — | 5 AION artifacts (4 FROZEN + 1 PRE_AUDIT_REPORT) |
| /tmp | maxdepth 3 | 0 (apenas /tmp/my-project com snapshot idêntico) |
| /tmp/my-project | — | 5 AION artifacts idênticos (snapshot) |
| /opt | — | 0 (diretório vazio) |
| /var/tmp | — | 0 (diretório vazio) |
| /usr/local | maxdepth 6 | 0 (apenas tectonic binário, não relacionado) |
| /home/official_skills | — | 0 (apenas .zip de skills default, nenhum AION) |
| /home/user_skills | — | 0 (vazio ou sem acesso) |
| /home/bun, /home/sync | — | Sem permissão de leitura |
| /workspace, /data, /projects, /aion | — | NÃO EXISTEM no sistema |
| /root | — | Sem permissão de leitura |

### 4.2 Busca por conteúdo (strings "AION", "CORPUS-002")

Foram executadas buscas por string em todos os arquivos do sistema acessíveis ao usuário. Resultado:

| String buscada | Arquivos encontrados contendo a string |
|---|---|
| "AION" | Apenas os 5 artefatos AION-7.0.0-* em /home/z/my-project/download/, snapshot idêntico em /tmp/my-project/download/, /home/z/my-project/worklog.md, /home/z/my-project/.git/index, /tmp/tectonic (falso-positivo), /home/z/TODO (metadados de TODO list do próprio agente) |
| "CORPUS-002" | Apenas referências em AION-7.0.0_PROTOCOL.md, AION-7.0.0-R_AUDIT.md, AION-EVIDENCE-LEDGER-001_SCHEMA.md (todas em /home/z/my-project/download/, com snapshot em /tmp/my-project/) |

**Nenhum arquivo contém materialmente o conteúdo do Corpus-002, Oracle v3, GraphRAG v1.0.0, etc.** As únicas menções a "CORPUS-002" são referências textuais nos artefatos de especificação que produzimos nesta sessão.

## 5. Inventário Git History

### 5.1 Repositório `/home/z/my-project/.git`

| Item | Valor |
|---|---|
| Total de commits | 10 |
| Branch ativa | main |
| Branches remotas | nenhuma (sem remote configurado) |
| Tags | nenhuma |
| Stashes | nenhum |
| Reflog | 10 entradas (todas da sessão atual) |

### 5.2 Cronologia dos commits

| # | Hash | Timestamp (UTC) | Conteúdo |
|---|---|---|---|
| 1 | 754ade3 | 2026-08-21 22:04:16 | Initial commit — apenas .env, .gitignore, download/README.md (3 arquivos) |
| 2 | a68acf8 | 2026-08-21 23:19:10 | Task 60: AION-7.0.0_PROTOCOL.md + AION-EVIDENCE-LEDGER-001_SCHEMA.md + worklog.md (805 linhas) |
| 3 | 99026c1 | 2026-08-21 23:27:15 | Task 61: AION-7.0.0-R_AUDIT.md + updates Protocol + worklog |
| 4 | e13576c | 2026-08-21 23:38:44 | Task 62: correções epistemológicas (instrumento vs evidência, gate conjuntivo) |
| 5 | 3fa0829 | 2026-08-21 23:45:07 | Task 63: confirmação standby |
| 6 | 4d21680 | 2026-08-22 00:06:30 | Task 64: AION-7.0.0-FG_GATE.md (633 linhas) |
| 7 | 78233f8 | 2026-08-22 00:19:33 | Task 65: AION-7.0.0-PRE_AUDIT_REPORT.md (454 linhas) |
| 8 | 384aa61 | 2026-08-22 00:32:40 | Task 66: FG_GATE estendido com Environment Provenance |
| 9 | 4ee9c5b | 2026-08-22 00:35:50 | Task 67: FG_GATE estendido com EP Classification |
| 10 | 348fb0b | 2026-08-22 01:47:40 | Task 68: encerramento fase especificação + worklog update |

### 5.3 Interpretação canônica do histórico git

**O repositório git de /home/z/my-project/.git foi inicializado em 21/08/2026 22:04:16 UTC — exatamente quando esta sessão começou.** Não há história material de 6.x neste repositório. Todos os 10 commits são posteriores a esse timestamp e correspondem à produção da especificação 7.0.0 nesta sessão.

Isto é uma **evidência material forte** de que o ambiente observado nesta sessão **não contém materialmente os artefatos de 6.x** — eles foram trazidos para a sessão apenas como texto no Handoff (mensagem inicial do usuário), não como artefatos em disco.

### 5.4 Implicação para proveniência

A proveniência dos componentes FROZEN de 6.x não está materialmente presente neste ambiente. Para que eles se tornem materialmente disponíveis, seria necessário:

1. Re-anexá-los a este ambiente por alguma via externa (upload, montagem de volume, sincronização com repositório externo, etc.).
2. Ou definir formalmente que o ambiente 6.x não é mais acessível e proceder com Via B (nova determinação metodológica do Projetista Master).

Nenhuma das duas ações foi executada em R0.1. R0.1 foi estritamente observacional.

## 6. Hash SHA-256 dos Artefatos Presentes (R0.6 parcial)

Embora R0.6 seja passo futuro na sequência canônica (após R0.2 restauração), é legitimo computar hashes SHA-256 dos 4 artefatos FROZEN de 7.0.0-spec agora, porque eles já estão materialmente presentes. Estes hashes servem como baseline para futura verificação de integridade (se algum dia houver suspeita de modificação).

| Artefato | SHA-256 |
|---|---|
| AION-7.0.0_PROTOCOL.md | `b9b50b28579a8b5ac99abcc48898b34f965d1ce14de53b85062f7a1fea13a376` |
| AION-EVIDENCE-LEDGER-001_SCHEMA.md | `1bf7349d621382a05f06f743b99e1ed632f804673199b444247b9afc4ddf3507` |
| AION-7.0.0-R_AUDIT.md | `d8efb8f4aee924f7c250a7e9726fdccdebcb6343440a8e1b8fb892c253ee1738` |
| AION-7.0.0-FG_GATE.md | `f082de51f96b144bf0cc98466db600581c3ce3f413fa38e3bf81f477c488e4e4` |
| AION-7.0.0-PRE_AUDIT_REPORT.md | `521285dbfaa499e534b5e31d9811209e82c51160a4323e1ee749c4896888a72e` |
| worklog.md | `a7873579f7d2c38961c49530994756796b7c7dd73eddbd8cf3d07356626865fe` |

Estes hashes NÃO constituem autenticação de componentes 6.x (porque nenhum componente 6.x está presente). Constituem apenas baseline dos artefatos produzidos nesta sessão.

## 7. Classificação EP Preliminar (Evidence-Driven)

Conforme Seção 5.5 do FG_GATE v3, a classificação EP deve ser evidence-driven — baseada na evidência encontrada, não no resultado desejado.

### 7.1 Evidência encontrada em R0.1

Para classificar EP, precisamos de evidência material sobre o **ambiente efetivo de 6.x**. Evidência material inclui:
- Logs de ambiente 6.x
- Configs de ambiente 6.x
- requirements.txt de 6.x
- Declarações de versão de runtime de 6.x
- Qualquer artefato que permita provar qual exatamente era o runtime utilizado em 6.x

**Resultado da busca:** **ZERO artefatos** contendo evidência sobre o ambiente efetivo de 6.x foram encontrados.

### 7.2 Classificação EP preliminar

$$\boxed{\text{EP} = \text{EP-0 UNKNOWN}}$$

**Justificativa (evidence-driven):** Não há evidência material suficiente sobre o ambiente efetivo de 6.x no ambiente observado. Nenhum log, nenhum requirements.txt, nenhuma declaração de versão de runtime de 6.x, nenhum arquivo de configuração que permita identificar o ambiente que produziu os resultados de 6.x.

### 7.3 Consequência para o Gate

Conforme Seção 5.5.4 do FG_GATE v3:

```
EP-0 UNKNOWN
   └── BLOCKED
```

Portanto:

$$\text{ENV} = \text{BLOCKED}$$

E por consequência:

$$\text{FINAL\_AUTH}_{7.0} = \text{FALSE}$$

### 7.4 Esta classificação é preliminar, não final

A classificação EP-0 é preliminar porque a sequência canônica de R0 ainda não foi completada — especificamente, **R0.2 (restauração dos artefatos) ainda não foi executada**. Se em R0.2 o Projetista Master ou fonte externa fornecer artefatos de 6.x contendo evidência de ambiente, a classificação EP pode ser revista (evidence-driven: nova evidência → nova classificação).

A classificação EP-0 neste momento significa apenas: **com a evidência material atualmente disponível no ambiente observado, não há base para classificar acima de EP-0**. Não significa que a evidência nunca existiu (UNAVAILABLE ≠ NON-EXISTENT). Não significa que o ambiente 6.x não existiu (NON-OBSERVED ≠ FALSE). Não significa que a restauração falhou (PENDING ≠ FAILED).

## 8. Estado Final do Inventário R0.1

### 8.1 Tabela consolidada

| Categoria | Itens esperados | Itens encontrados | Estado |
|---|---|---|---|
| Grupo A — Componentes FROZEN | 6 | 0 | UNAVAILABLE |
| Grupo B — Itens de reprodução | 6 | 0 | UNAVAILABLE / UNKNOWN |
| Documentos canônicos esperados | 5 | 0 | UNAVAILABLE |
| JSONs experimentais | 5+ | 0 | UNAVAILABLE |
| PDFs do corpus | 9 (em /upload/) | 0 (diretório vazio) | EMPTY |
| Scripts persistidos | 12 | 0 (diretório /scripts/ não existe) | NOT FOUND |
| Artefatos FROZEN de 7.0.0-spec | 4 | 4 | PRESENT (produzidos nesta sessão) |
| PRE_AUDIT_REPORT | 1 | 1 | PRESENT (produzido nesta sessão) |
| worklog.md | 1 | 1 | PRESENT (inicializado nesta sessão) |
| Histórico git | 10 commits esperados (Tasks 60-68) | 10 commits encontrados | CONSISTENT |
| Evidência de ambiente 6.x | qualquer | 0 | UNAVAILABLE |

### 8.2 Consequência canônica

$$\text{AUTH}_{7.0} = \bigwedge_{i=1}^{6}(E_i \land V_i \land H_i \land C_i) = \text{FALSE}$$

$$\text{EP} = \text{EP-0 UNKNOWN}$$

$$\text{ENV} = \text{BLOCKED}$$

$$\text{FINAL\_AUTH}_{7.0} = \text{FALSE / BLOCKED}$$

### 8.3 Estado do sistema

```
AION-7.0.0-R0
│
├── R0.1 INVENTÁRIO MATERIAL .......... CONCLUÍDO
│   ├── Grupo A (6 componentes) ........ 0/6 FOUND
│   ├── Grupo B (6 itens reprodução) ... 0/6 FOUND
│   ├── Documentos canônicos esperados . 0/5 FOUND
│   ├── JSONs experimentais ............ 0/5+ FOUND
│   ├── PDFs corpus (/upload/) ......... EMPTY
│   ├── Scripts (/scripts/) ............ NOT FOUND
│   ├── Evidência ambiente 6.x ......... UNAVAILABLE
│   └── Histórico git .................. 10 commits TODOS desta sessão
│
├── R0.2 RESTAURAÇÃO DOS ARTEFATOS .... PENDING (requer fonte externa)
├── R0.3 IDENTIFICAÇÃO AMBIENTE 6.x ... PENDING (depende de R0.2)
├── R0.4 ENVIRONMENT PROVENANCE ....... PENDING (depende de R0.3)
├── R0.5 CLASSIFICAÇÃO EP ............. EP-0 UNKNOWN (preliminar, evidence-driven)
├── R0.6 HASH SHA-256 ................. EXECUTADO para artefatos 7.0.0-spec; PENDING para 6.x
└── R0.7 V1-V4 ....................... PENDING (sem componentes 6.x para verificar)

AUTH₇.₀ .... FALSE
ENV ........ BLOCKED (EP-0)
PIPE ....... NOT RUN
NOMOD ...... PENDING
FINAL_AUTH₇.₀ ... BLOCKED
```

## 9. Evento de Proveniência Canônico

```
EVENT_ID: AION-EV-003
TIMESTAMP: 2026-08-22T01:55:00-03:00
SESSION: web-73c75281-201c-4716-b85c-97833d25f9b3
TRACE_ID: 1a0272fe5ff08b11 (autorização R0) → 1a02725c6cde1ce5... (execução R0.1)
EVENT_TYPE: R0.1_MATERIAL_INVENTORY_COMPLETED
OBSERVED_STATE: R0.1 inventory executed across /home, /tmp, /opt, /var/tmp, /usr/local (maxdepth 6), .git history (10 commits), .venv, .cache, .local, .npm, .npm-global, /home/official_skills, /home/user_skills. No AION 6.x artifacts found anywhere accessible.
KEY_FINDINGS:
  - 0/6 Grupo A components materialmente presentes
  - 0/6 Grupo B reprodução items materialmente presentes
  - 0/5 documentos canônicos esperados do Handoff materialmente presentes
  - 0/5+ JSONs experimentais materialmente presentes
  - /upload/ existe mas está EMPTY
  - /scripts/ NÃO EXISTE como diretório
  - /home/z/my-project/.git inicializado em 21/08/2026 22:04:16 UTC (início desta sessão)
  - 10/10 commits no git history são desta sessão (Tasks 60-68)
  - ZERO evidência material sobre ambiente efetivo de 6.x
EPISTEMOLOGICAL_SCOPE: EP classification preliminary = EP-0 UNKNOWN (evidence-driven). Não é NON-EXISTENT, não é FAILED. É ausência de evidência material observável.
INTERPRETATION: [I] O ambiente observado nesta sessão NÃO CONTÉM materialmente os artefatos de 6.x. O Handoff foi trazido como texto na conversa, não como artefatos em disco. A restauração material requer fonte externa (upload, sincronização, etc.).
PROVENANCE_RULE_INVOKED: Regra 1 (Provenance) + Regra 7 (PER=0 ≠ confiável) + Invariantes UNAVAILABLE≠NON-EXISTENT, NON-OBSERVED≠FALSE, PENDING≠FAILED, COMPATIBLE≠EQUIVALENT + FG_GATE v3 Seção 5.5 (EP Classification evidence-driven).
EPISTEMIC_ACTION: R0.1 concluído com classificação EP-0 UNKNOWN preliminar. AUTH_{7.0}=FALSE confirmado. FINAL_AUTH_{7.0}=BLOCKED confirmado. Estado permanece STANDBY. Próxima operação: R0.2 restauração requer fonte externa OU Via B (nova determinação metodológica do Projetista Master).
```

## 10. Próxima Ação Legítima

A execução de R0.1 identifica que **a próxima ação material requer uma fonte externa de artefatos 6.x**. Sem essa fonte externa, R0.2 não pode ser executada (não há nada a restaurar).

As opções para o Projetista Master são:

### 10.1 Opção R0.A — Restauração via fonte externa

O Projetista Master (ou o ambiente de execução) fornece materialmente os artefatos 6.x via:
- Upload de arquivos para `/home/z/my-project/upload/` ou outra localização canônica
- Sincronização com repositório externo
- Montagem de volume
- Ou outra via materialmente legítima

Neste caso, R0.2 prossegue com a restauração dos artefatos recebidos, e a sequência canônica R0.2 → R0.3 → R0.4 → R0.5 (revisão EP) → R0.6 → R0.7 → gates FG continua.

### 10.2 Opção R0.B — Confirmação de indisponibilidade

O Projetista Master confirma formalmente que os artefatos 6.x não estão disponíveis para restauração material neste ambiente. Neste caso:
- A classificação EP-0 UNKNOWN é confirmada como final (não preliminar)
- `ENV = BLOCKED` permanece
- `FINAL_AUTH_{7.0} = FALSE` permanence
- O estado STANDBY continua indefinidamente
- Ou o Projetista Master ativa Via B (nova determinação metodológica) para redefinir o experimento sem depender de 6.x

### 10.3 Opção R0.C — Via B (nova determinação metodológica)

O Projetista Master emite nova determinação que altera formalmente o contrato — por exemplo, redefinindo o experimento sem depender de restauração de 6.x, ou criando uma nova genealogia experimental. Neste caso, a genealogia documental deve ser preservada (Regra 9: Substituição não é apagamento).

### 10.4 Não-opção: continuar inventariando

Não há sentido em continuar executando R0.1 em variantes diferentes — o inventário foi exaustivo em todas as localizações acessíveis ao usuário. Continuar inventariando seria adicionar atividade sem adicionar informação.

## 11. Genealogia Documental

```
AION-7.0.0-FG v3 (FROZEN FINAL — Task 68)
       │
       ▼  Determinação Projetista Master: autoriza R0 (Task 69)
       │
AION-7.0.0-R0 (RESTAURAÇÃO MATERIAL CONTROLADA — autorizada)
       │
       ▼  R0.1 INVENTÁRIO MATERIAL (este documento)
       │
AION-7.0.0-R0_INVENTORY.md (relatório canônico do inventário)
       │
       ├── Resultado: 0/6 componentes Grupo A encontrados
       ├── Resultado: 0/6 itens Grupo B encontrados
       ├── Resultado: 0 evidência material sobre ambiente 6.x
       ├── EP classification preliminar: EP-0 UNKNOWN (evidence-driven)
       ├── AUTH_{7.0}=FALSE confirmado
       ├── FINAL_AUTH_{7.0}=BLOCKED confirmado
       │
       ▼  Próxima operação requer decisão do Projetista Master:
       │
       ├── R0.A Restauração via fonte externa → R0.2 prossegue
       ├── R0.B Confirmação de indisponibilidade → EP-0 final, STANDBY indefinido
       └── R0.C Via B: nova determinação metodológica
```

---

*"O inventário material é o primeiro produto experimentalmente útil do AION-7.0.0. Não produz uma métrica científica do objeto de estudo — produz um estado material auditável da infraestrutura. E esse estado é: com a evidência material atualmente disponível no ambiente observado, não há base para classificar acima de EP-0. A restauração requer fonte externa ou Via B. Sem uma das duas, o baseline permanece legitimamente bloqueado."*

**Fim do AION-7.0.0-R0_INVENTORY.md.**
