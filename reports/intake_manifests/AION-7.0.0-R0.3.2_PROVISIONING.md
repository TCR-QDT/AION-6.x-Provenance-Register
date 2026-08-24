# AION-7.0.0-R0.3.2 — Material Provisioning / Acervo Histórico

**Versão:** R0.3.2-1
**Data:** 22 de agosto de 2026, 21:00 BRT
**Autor / Curador:** Edson Carvalho do Nascimento (Projetista Master) — determinou R0.3.2
**Analista Técnico:** IA Curadora (Role: Escriba / Arquiteto de Metadados) — executou R0.3.2.0
**Sessão:** web-73c75281-201c-4716-b85c-97833d25f9b3
**Status:** R0.3.2 AUTORIZADO — R0.3.2.0 Environment Re-Preparation CONCLUÍDO — R0.3.2.1 Material Provisioning PENDING (external action required)
**Genealogia:** Derivado da determinação do Projetista Master (Task 74) autorizando R0.3.2 após R0.3.1 ter retornado INPUT_PENDING.

---

## 1. Resumo Executivo

Foi recebida autorização formal do Projetista Master para AION-7.0.0-R0.3.2 — Material Provisioning / Acervo Histórico, após R0.3.1 (Task 73) ter retornado canonicamente `INPUT_PENDING` como resultado materialmente observável. A autorização PM estabelece que a próxima ação pertence ao fornecimento material do acervo, não à Curadoria: "Disponibilizar materialmente o acervo histórico 6.x. Não reconstruir, não instalar, não executar e não autenticar. Após a disponibilização, executar novamente a detecção e o intake controlado." Durante a preparação para R0.3.2 (R0.3.2.0), a IA Curadora identificou materialmente que **a estrutura de subdiretórios `intake/{A_components,B_reproduction,C_corpus,D_environment}/received/` criada em Task 72 havia sido perdida entre sessões** — apenas `intake/manifests/` permanecia. Os 4 artefatos FROZEN de 7.0.0-spec permaneceram íntegros (hashes idênticos a Tasks 65-73). A estrutura de intake foi recriada conforme Task 72. O ambiente está novamente preparado para receber material externo. **R0.3.2.0 = CONCLUÍDO, R0.3.2.1 = PENDING (aguardando fornecimento material externo).** O critério de sucesso de R0.3.2 não é "recuperar tudo", mas "saber materialmente quais artefatos foram disponibilizados, preservá-los integralmente e estabelecer sua proveniência de chegada". Três resultados são possíveis: evidência suficiente (EP poderá subir), evidência parcial (EP-1 poderá ser considerado), ou material insuficiente (EP-0 permanece). Nenhum desses resultados será decidido antecipadamente.

## 2. Determinação PM Recebida (Task 74)

### 2.1 Objetivo PM

> Disponibilizar materialmente o acervo histórico necessário para que a Curadoria possa sair de `EVIDÊNCIA CANDIDATA = ∅` e `EP-0 UNKNOWN` sem reconstrução ou inferência.

### 2.2 Autorização

> R0.3.2 AUTORIZADO — exclusivamente para disponibilização/recepção material, não para execução experimental.

### 2.3 Regra de captura PM (quando material chegar)

```
MATERIAL DISPONIBILIZADO
        ↓
DETECT
        ↓
CAPTURE/PRESERVE
        ↓
SHA-256
        ↓
MANIFEST
        ↓
EVIDÊNCIA CANDIDATA
        ↓
PROVENIÊNCIA DE RECEPÇÃO
        ↓
WORKLOG
        ↓
CONFIRMAÇÃO
```

### 2.4 Sequência pós-intake (PM)

```
R0.4 Environment Provenance
        ↓
R0.5 EP Classification
        ↓
V1 → V2 → V3 → V4
```

Nenhum desses passos deve ser antecipado.

### 2.5 Critério de sucesso PM

O sucesso **não** é "recuperar tudo". É:

> Saber materialmente quais artefatos foram disponibilizados, preservá-los integralmente e estabelecer sua proveniência de chegada.

### 2.6 Três resultados possíveis (PM)

```
material recebido
      │
      ├── evidência suficiente → EP poderá subir
      │
      ├── evidência parcial ───→ EP-1 poderá ser considerado
      │
      └── material insuficiente → EP-0 permanece
```

Nenhum desses resultados será decidido antecipadamente.

### 2.7 Determinação final PM

> Disponibilizar materialmente o acervo histórico 6.x. Não reconstruir, não instalar, não executar e não autenticar. Após a disponibilização, executar novamente a detecção e o intake controlado.

> A partir daqui, **a próxima ação não pertence à Curadoria**: pertence ao fornecimento material do acervo. Só depois da chegada de arquivos reais haverá uma nova operação legítima.

## 3. Observação Material Crítica em R0.3.2.0

### 3.1 Estado observado do ambiente no início de R0.3.2.0

Durante a verificação de integridade pré-fornecimento, a IA Curadora identificou materialmente:

| Item esperado (conforme Task 72) | Estado observado |
|---|---|
| `/home/z/my-project/intake/A_components/received/` | **AUSENTE** — diretório não existe |
| `/home/z/my-project/intake/B_reproduction/received/` | **AUSENTE** — diretório não existe |
| `/home/z/my-project/intake/C_corpus/received/` | **AUSENTE** — diretório não existe |
| `/home/z/my-project/intake/D_environment/received/` | **AUSENTE** — diretório não existe |
| `/home/z/my-project/intake/manifests/` | **PRESENTE** — contém INTAKE_MANIFEST_TEMPLATE.md + AION-7.0.0-R0.3.1_INTAKE_MANIFEST.md |

### 3.2 Verificação de integridade dos 4 artefatos FROZEN

| Artefato | SHA-256 verificado | Estado |
|---|---|---|
| AION-7.0.0_PROTOCOL.md | `b9b50b28579a8b5ac99abcc48898b34f965d1ce14de53b85062f7a1fea13a376` | **INTACTO** (idêntico a Tasks 65, 69, 70, 71, 72, 73) |
| AION-EVIDENCE-LEDGER-001_SCHEMA.md | `1bf7349d621382a05f06f743b99e1ed632f804673199b444247b9afc4ddf3507` | **INTACTO** |
| AION-7.0.0-R_AUDIT.md | `d8efb8f4aee924f7c250a7e9726fdccdebcb6343440a8e1b8fb892c253ee1738` | **INTACTO** |
| AION-7.0.0-FG_GATE.md | `f082de51f96b144bf0cc98466db600581c3ce3f413fa38e3bf81f477c488e4e4` | **INTACTO** |

### 3.3 Interpretação canônica

**Os 4 artefatos FROZEN de 7.0.0-spec permaneceram íntegros entre sessões** — seus hashes são materialmente idênticos aos verificados em Tasks 65, 69, 70, 71, 72, 73. A continuidade material da especificação FROZEN está demonstrada criptograficamente.

**A estrutura de intake (diretórios vazios preparados em Task 72) foi perdida entre sessões.** Isto é uma observação materialmente relevante que precisa ser registrada canonicamente:

- Os diretórios vazios não tinham hashes (eram estrutura, não conteúdo)
- O sistema de arquivos do ambiente pode ter sido re-inicializado entre sessões
- Isto não constitui perda de artefatos FROZEN (estes permanecem íntegros)
- Isto constitui perda de infraestrutura de intake (estrutura temporária para receber material)

### 3.4 Aplicação de invariantes canônicos

| Invariante | Aplicação |
|---|---|
| UNAVAILABLE ≠ NON-EXISTENT | A estrutura de intake perdida entre sessões não significa que ela "não exista" — significa apenas que não está mais materialmente disponível neste ambiente observado. Pode ter existido em Task 72 e sido perdida. |
| NON-OBSERVED ≠ FALSE | Não observamos a causa da perda. Não inferimos que houve reset de ambiente. Apenas observamos o estado atual. |
| PENDING ≠ FAILED | A perda de infraestrutura de intake não é falha do AION — é um evento material que precisa ser registrado. A estrutura foi recriada. |

### 3.5 Ação corretiva tomada

A estrutura de intake foi **recriada conforme Task 72**:

```bash
mkdir -p /home/z/my-project/intake/A_components/received
mkdir -p /home/z/my-project/intake/B_reproduction/received
mkdir -p /home/z/my-project/intake/C_corpus/received
mkdir -p /home/z/my-project/intake/D_environment/received
```

**Nenhum artefato FROZEN foi alterado** durante esta ação corretiva. Apenas diretórios vazios de infraestrutura foram recriados.

## 4. Lote Esperado (PM Task 74)

### 4.1 Grupo A — 6 componentes congelados de 6.x

| # | Componente | Versão | Diretório de destino |
|---|---|---|---|
| 1 | Corpus | v1.3.0 (9 registros + 2 inexistentes) | `intake/A_components/received/Corpus_v1.3.0/` |
| 2 | Oracle | v3 (7 chunks interversionais) | `intake/A_components/received/Oracle_v3/` |
| 3 | GraphRAG | v1.0.0 (22 nós, 187 arestas, PGI=1.0) | `intake/A_components/received/GraphRAG_v1.0.0/` |
| 4 | P-RESP-001 | v0.3 (validator determinístico) | `intake/A_components/received/P-RESP-001_v0.3/` |
| 5 | AION-EVAL-002 | v0.2 (multicamada, 10 categorias) | `intake/A_components/received/AION-EVAL-002_v0.2/` |
| 6 | B1 config | 6.2.11 (cross-lingual PT-BR→EN + Oracle v3) | `intake/A_components/received/B1_config_6.2.11/` |

### 4.2 Grupo B — Itens de reprodução

| Item | Diretório de destino |
|---|---|
| scripts (12 esperados: extract_aion_corpus.py, aion_rag_proxy.py, aion_graphrag.py, aion_provenance_granular.py, aion_temporal_graph.py, aion_historical_reconciliation.py, aion_bench_001.py, aion_p_resp_001_v03.py, aion_dify_001.py, aion_6_3_0_baseline.py, aion_6_4_0_conditional.py, aion_6_4_2_minimal.py) | `intake/B_reproduction/received/scripts/` |
| configurações | `intake/B_reproduction/received/configs/` |
| lockfiles (requirements.txt, etc.) | `intake/B_reproduction/received/requirements_lockfiles/` |
| seeds / parâmetros | `intake/B_reproduction/received/seeds_params/` |
| identificadores de modelos | `intake/B_reproduction/received/model_identifiers/` |
| manifests | `intake/B_reproduction/received/execution_manifests/` |

### 4.3 Grupo C — Corpus/documentos

| ID | Documento | Estado esperado | Diretório de destino |
|---|---|---|---|
| CORPUS-001 | AION-DOC-000.html | CURRENT | `intake/C_corpus/received/CORPUS-001/` |
| CORPUS-002-HIST | Paper A v6.2 anterior (134KB) | SUPERSEDED | `intake/C_corpus/received/CORPUS-002-HIST/` |
| CORPUS-002 | Paper A v6.2 (137KB) | CURRENT/AUTHORITATIVE | `intake/C_corpus/received/CORPUS-002/` |
| CORPUS-003 | PARTE IV Formalização Teórica | CURRENT | `intake/C_corpus/received/CORPUS-003/` |
| CORPUS-004 | Paper B anterior (3 págs) | HISTORICAL | `intake/C_corpus/received/CORPUS-004/` |
| CORPUS-005 | Cover Letter PT-BR | CURRENT | `intake/C_corpus/received/CORPUS-005/` |
| CORPUS-006 | Paper A v6.1 oficial (138KB) | HISTORICAL | `intake/C_corpus/received/CORPUS-006/` |
| CORPUS-007 | Paper A v6.1 revisão (326KB) | HISTORICAL/SCIENTIFIC_REVISION | `intake/C_corpus/received/CORPUS-007/` |
| CORPUS-011 | Paper B v6.1 PT novo (5 págs) | CURRENT | `intake/C_corpus/received/CORPUS-011/` |

### 4.4 Grupo D — Environment Provenance 6.x

| Item | Diretório de destino |
|---|---|
| pip freeze / manifestos equivalentes | `intake/D_environment/received/pip_freeze_manifests/` |
| Versão do Python | `intake/D_environment/received/python_version_logs/` |
| Versão do SO/runtime | `intake/D_environment/received/os_runtime_info/` |
| Versões de bibliotecas | `intake/D_environment/received/library_versions/` |
| Identificadores de modelos | `intake/D_environment/received/model_identifiers/` |
| Hashes | `intake/D_environment/received/execution_hashes/` |
| Timestamps | `intake/D_environment/received/timestamps/` |
| Scripts de bootstrap | `intake/D_environment/received/bootstrap_scripts/` |

**IMPORTÂNCIA CRÍTICA (PM Task 71):** Itens do Grupo D devem ser tratados com cautela especial. Documentação TCR/QDT (Python 3.10, NumPy, SciPy, scikit-learn, QuTiP, Matplotlib) mencionada pelo PM em Task 71 **não deve ser automaticamente atribuída ao AION-6.x**. É EVIDÊNCIA CANDIDATA, não autenticação.

### 4.5 Princípio PM Task 74

> **Não é necessário que todos existam.** O importante é que aquilo que existir seja disponibilizado sem reconstrução.

## 5. Estado do Ambiente Após R0.3.2.0

### 5.1 Estrutura de intake recriada e verificada

```
/home/z/my-project/intake/
│
├── A_components/
│   └── received/       ✓ recriado
│
├── B_reproduction/
│   └── received/       ✓ recriado
│
├── C_corpus/
│   └── received/       ✓ recriado
│
├── D_environment/
│   └── received/       ✓ recriado
│
└── manifests/
    ├── INTAKE_MANIFEST_TEMPLATE.md              ✓ presente (Task 72)
    └── AION-7.0.0-R0.3.1_INTAKE_MANIFEST.md     ✓ presente (Task 73)
```

### 5.2 Capacidade do ambiente

| Item | Valor |
|---|---|
| Sistema de arquivos | `c-6a8a069e-145d6674-b6f53cf761b3-rootfs` |
| Capacidade total | 9.9G |
| Usado | 87M |
| Disponível | **9.3G** (suficiente para acervo histórico) |
| Permissões /home/z/my-project | `z:z 755` (escrita confirmada) |
| Permissões /home/z/my-project/intake | `z:z 775` |

### 5.3 4 artefatos FROZEN verificados íntegros

| Artefato | SHA-256 | Estado |
|---|---|---|
| AION-7.0.0_PROTOCOL.md | `b9b50b28579a8b5ac99abcc48898b34f965d1ce14de53b85062f7a1fea13a376` | INTACTO |
| AION-EVIDENCE-LEDGER-001_SCHEMA.md | `1bf7349d621382a05f06f743b99e1ed632f804673199b444247b9afc4ddf3507` | INTACTO |
| AION-7.0.0-R_AUDIT.md | `d8efb8f4aee924f7c250a7e9726fdccdebcb6343440a8e1b8fb892c253ee1738` | INTACTO |
| AION-7.0.0-FG_GATE.md | `f082de51f96b144bf0cc98466db600581c3ce3f413fa38e3bf81f477c488e4e4` | INTACTO |

## 6. Caminhos Canônicos de Entrada Monitorados

A IA Curadora monitora os seguintes caminhos canônicos para detecção de material externo:

| # | Caminho | Permissões | Estado |
|---|---|---|---|
| 1 | `/home/z/my-project/upload/` | root:root 777 | VAZIO |
| 2 | `/home/z/my-project/intake/A_components/received/` | z:z 775 | VAZIO |
| 3 | `/home/z/my-project/intake/B_reproduction/received/` | z:z 775 | VAZIO |
| 4 | `/home/z/my-project/intake/C_corpus/received/` | z:z 775 | VAZIO |
| 5 | `/home/z/my-project/intake/D_environment/received/` | z:z 775 | VAZIO |

**Adicional:** qualquer outra localização explicitamente comunicada pelo Projetista Master será tratada como caminho canônico.

## 7. Fluxo de Detecção Automática (Preparado)

Quando o PM ou fonte externa disponibilizar material, o fluxo canônico de intake (conforme PM Task 73 Seção 11 e Task 74 Seção 2.3) será executado:

```
1. DETECT     → verificar material efetivamente disponibilizado em qualquer caminho canônico
2. CAPTURE    → copiar/preservar sem modificar a origem
3. HASH       → SHA-256 do material recebido
4. MANIFEST   → registrar nome, tamanho, origem, timestamp e hash
5. CLASSIFY   → EVIDÊNCIA CANDIDATA (não AUTENTICADA)
6. PROVENANCE → registrar como o material chegou ao ambiente
7. WORKLOG    → registrar o evento
8. CONFIRM    → verificar os 8 critérios de encerramento
```

Após R0.3.2 concluído (8 critérios satisfeitos):

```
R0.4 ENVIRONMENT PROVENANCE
       ↓
R0.5 EP CLASSIFICATION (evidence-driven, com nova evidência)
       ↓
SHA-256 final dos candidatos
       ↓
V1 EXISTENCE → V2 VERSION → V3 INTEGRITY → V4 CANONICAL CONTENT
       ↓
AUTH₇.₀
       ↓
ENV → PIPE → NOMOD
       ↓
FINAL_AUTH₇.₀
```

## 8. Evento de Proveniência Canônico

```
EVENT_ID: AION-EV-007
TIMESTAMP: 2026-08-22T21:00:00-03:00
SESSION: web-73c75281-201c-4716-b85c-97833d25f9b3
TRACE_ID: 1a02b443c0424929 (autorização R0.3.2 PM) → execução IA Curadora
EVENT_TYPE: R0.3.2_AUTHORIZED_ENVIRONMENT_RE_PREPARATION_COMPLETED
OBSERVED_STATE: R0.3.2.0 Environment Re-Preparation executed. Material observation: intake subdirectories A_components/, B_reproduction/, C_corpus/, D_environment/ (with received/ subdirs) created in Task 72 were found MISSING at start of R0.3.2.0. Only intake/manifests/ remained. 4 FROZEN artifacts of 7.0.0-spec verified intact (hashes identical to Tasks 65-73). Intake structure re-created. Environment ready to receive external material.
KEY_FINDINGS:
  - 4 FROZEN artifacts intact: hashes identical to Tasks 65, 69, 70, 71, 72, 73
  - Intake subdirectories (4 of them) were lost between sessions — material observation, not inferred
  - Only intake/manifests/ persisted (containing INTAKE_MANIFEST_TEMPLATE.md from Task 72 + AION-7.0.0-R0.3.1_INTAKE_MANIFEST.md from Task 73)
  - Intake structure re-created with mkdir -p
  - Disk space confirmed: 9.3G available
  - Permissions confirmed: z:z 775 on intake/* subdirs
EPISTEMOLOGICAL_SCOPE: R0.3.2.0 = CONCLUÍDO (environment re-prepared). R0.3.2.1 = PENDING (awaiting external material provisioning). Material loss of intake subdirectories between sessions does NOT constitute loss of FROZEN artifacts — those remain cryptographically intact. The loss is of empty infrastructure directories, which have been re-created.
INTERPRETATION: [I] The environment can be reset between sessions, but the FROZEN specification artifacts persist via their cryptographic hashes. This is itself a demonstration of the AION principle: continuity of identity requires verifiable material evidence (hashes), not nominal continuity (filenames). The intake infrastructure is replaceable; the FROZEN specification is authenticated.
PROVENANCE_RULE_INVOKED: Regra 1 (Provenance) + Regra 7 (PER=0 ≠ confiável) + Invariantes UNAVAILABLE≠NON-EXISTENT, NON-OBSERVED≠FALSE, PENDING≠FAILED, COMPATIBLE≠EQUIVALENT + FG_GATE v3 Seção 5.5 (EP Classification evidence-driven) + PM Task 74 Rules: (1) success = knowing materially what was provided, not "recovering everything"; (2) three results possible (sufficient/partial/insufficient), none decided in advance.
EPISTEMIC_ACTION: R0.3.2.0 CONCLUÍDO. R0.3.2.1 PENDING (external action required). AUTH_{7.0}=FALSE confirmed. FINAL_AUTH_{7.0}=BLOCKED confirmed. State remains STANDBY. Next legitimate operation: external material provisioning → R0.3.2.1 DETECT re-execution → controlled intake → provenance → EP classification.
```

## 9. Estado do Sistema (pós-R0.3.2.0)

```
AION-7.0.0
│
├── Specification ........ FROZEN FINAL (Task 68)
│   ├── 4 FROZEN artifacts verified intact (hashes identical to Tasks 65-73)
│   └── AION-EV-007 recorded (intake subdir loss observation)
│
├── R0.1 ................. CONCLUÍDO (Task 69)
├── R0.2 ................. CONCLUÍDO (Task 70)
├── R0.2.1 ............... CONCLUÍDO (Task 71)
├── R0.3.0 ............... CONCLUÍDO (Task 72)
├── R0.3.1 ................ CONCLUÍDO / INPUT_PENDING (Task 73)
│
├── R0.3.2 ................ AUTHORIZED (Task 74)
│   └── R0.3.2.0 Environment Re-Preparation ... CONCLUÍDO
│       ├── Intake subdirs missing observed → re-created
│       ├── 4 FROZEN artifacts integrity verified
│       ├── Disk space confirmed (9.3G available)
│       └── Permissions confirmed (z:z 775)
│
├── R0.3.2.1 Material Provisioning ...... PENDING (external action required)
│   ├── Grupo A intake .................. PENDING
│   ├── Grupo B intake .................. PENDING
│   ├── Grupo C intake .................. PENDING
│   └── Grupo D intake .................. PENDING
│
├── R0.4 Environment Provenance ......... PENDING (depends on R0.3.2.1 completion)
├── R0.5 EP Classification .............. EP-0 UNKNOWN (mantido)
├── R0.6 SHA-256 ....................... PENDING (will be done during intake)
├── R0.7 V1-V4 .......................... PENDING (NO ANTICIPATION)
│
├── EP ................................. EP-0 UNKNOWN
├── AUTH₇.₀ ............................ FALSE
├── ENV ............................... BLOCKED
├── PIPE .............................. NOT RUN
├── NOMOD ............................. PENDING
└── FINAL_AUTH₇.₀ ..................... BLOCKED
```

## 10. Próxima Ação Legítima — EXTERNA

Conforme PM Task 74 Seção 2.7:

> A partir daqui, **a próxima ação não pertence à Curadoria**: pertence ao fornecimento material do acervo. Só depois da chegada de arquivos reais haverá uma nova operação legítima.

### 10.1 O que é necessário

O Projetista Master precisa **materialmente disponibilizar o acervo histórico 6.x** — por:

- Upload/anexo de arquivo (`.zip`, `.tar`, diretório exportado, ou arquivos individuais)
- Fonte conectada acessível ao ambiente (repositório, volume montado, etc.)
- Outra via materialmente legítima comunicada à IA Curadora

### 10.2 Onde disponibilizar

Qualquer um dos caminhos canônicos de entrada monitorados (Seção 6) funcionará. Recomenda-se `/home/z/my-project/upload/` como porta de entrada principal (permissões root:root 777).

### 10.3 O que NÃO será feito

Até a chegada de evidência material:

- ✗ Nenhuma reconstrução
- ✗ Nenhuma instalação de dependências
- ✗ Nenhuma execução experimental
- ✗ Nenhuma inferência de continuidade
- ✗ Nenhuma antecipação de V1-V4
- ✗ Nenhuma classificação automática como EP-3
- ✗ Nenhuma produção de dados experimentais 7.0.0

### 10.4 Princípio operacional consolidado

> **A próxima evidência deve vir do acervo, não da nossa memória sobre o acervo.**

## 11. Genealogia Documental

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
       ▼  Determinação PM Task 71: autoriza R0.2.1
       │
AION-7.0.0-R0.2.1 RECONCILIAÇÃO DO ACERVO HISTÓRICO CONCLUÍDO (Task 71)
       │
       ▼  Determinação PM Task 72: autoriza R0.3
       │
AION-7.0.0-R0.3 MATERIAL RESTORATION INTAKE — AUTHORIZED
       │
       ▼  R0.3.0 Environment Preparation CONCLUÍDO (Task 72)
       │
AION-7.0.0-R0.3.0 — intake/ structure created, 4 FROZEN integrity verified
       │
       ▼  Determinação PM Task 73: autoriza R0.3.1
       │
AION-7.0.0-R0.3.1 MATERIAL INTAKE DETECTION & CAPTURE — EXECUTADO (Task 73)
       │
       ├── F1 DETECT: 5 caminhos varridos, 0 arquivos 6.x detectados
       ├── F2-F7: N/A (sem material)
       ├── F8 CONFIRM: 1/8 critérios (worklog); classificação INPUT_PENDING
       │
       ▼  Determinação PM Task 74: autoriza R0.3.2 (Material Provisioning)
       │
AION-7.0.0-R0.3.2 MATERIAL PROVISIONING / ACERVO HISTÓRICO — AUTHORIZED
       │
       ▼  R0.3.2.0 Environment Re-Preparation CONCLUÍDO (este documento)
       │
       ├── Material observation: intake subdirs were lost between sessions
       ├── 4 FROZEN artifacts verified intact (hashes identical to Tasks 65-73)
       ├── Intake structure re-created
       ├── Disk space and permissions confirmed
       ├── AION-EV-007 recorded
       │
       ▼  R0.3.2.1 Material Provisioning — PENDING (external action required)
       │
       ├── Aguardando PM ou fonte externa disponibilizar acervo 6.x
       │   ├── Grupo A: 6 componentes FROZEN
       │   ├── Grupo B: 12+ itens reprodução
       │   ├── Grupo C: 9+ PDFs corpus
       │   └── Grupo D: environment provenance 6.x
       │
       ▼  Quando material chegar:
       │
       R0.3.2.1 DETECT → CAPTURE → HASH → MANIFEST → CLASSIFY → PROVENANCE → WORKLOG → CONFIRM
       │
       ▼  Quando 8 critérios de encerramento satisfeitos:
       │
       R0.3.2 = COMPLETE
       │
       ▼  Apenas então:
       │
       R0.4 Environment Provenance (com material recebido)
       │
       ▼
       R0.5 EP Classification (evidence-driven, com nova evidência)
       │
       ▼  Possíveis transições (evidence-driven, não decididas antecipadamente):
       │
       ├── EP-0 (permanece) → STANDBY
       ├── EP-1 PARTIAL → STANDBY, mas caracterizado
       ├── EP-2 COMPATIBLE → STANDBY, mas caracterizado (não FAILED)
       └── EP-3 EQUIVALENT → prosseguir para R0.7 V1-V4
```

---

*"O resultado de R0.3.2.0 não é uma falha do AION-7.0.0. É a observação materialmente correta de que a infraestrutura de intake foi perdida entre sessões — mas os 4 artefatos FROZEN de 7.0.0-spec permanecem criptograficamente íntegros. Isto é, em si, uma demonstração do princípio do AION: a continuidade da identidade requer evidência material verificável (hashes), não continuidade nominal (nomes de arquivos). A infraestrutura de intake é substituível; a especificação FROZEN é autenticada. Aguardando fornecimento material do acervo 6.x."*

**Fim do AION-7.0.0-R0.3.2 Material Provisioning Report.**
