# AION-7.0.0-R0.3 — Intake Manifest Template

**Versão:** R0.3.0-1
**Data:** 22 de agosto de 2026, 11:00 BRT
**Status:** ENVIRONMENT PREPARED — AGUARDANDO MATERIAL EXTERNO GRUPOS A+B+C+D
**Genealogia:** Derivado da determinação do Projetista Master (Task 72) autorizando AION-7.0.0-R0.3 — Material Restoration Intake.

---

## 1. Propósito

Este documento estabelece o protocolo canônico para **intake controlado** de material histórico externo pertencente aos Grupos A+B+C+D, conforme determinação do Projetista Master em Task 72. O intake NÃO é autenticação, NÃO é execução, NÃO é reconstrução. É apenas transformação de material externo em **evidência candidata materialmente observável**, preservando sua proveniência.

## 2. Regras Fundamentais (PM Task 72)

### 2.1 Regra de não-tentativa de recriação

> Não devemos tentar "recriar o ambiente 6.x". Devemos primeiro perguntar: **"Que evidência material existe sobre o ambiente que efetivamente produziu 6.x?"**

### 2.2 Regra de não-avanço automático

> Mesmo que os artefatos reapareçam e o pipeline funcione, **isso não autoriza automaticamente o avanço**. EP-2 ≠ EP-3.

### 2.3 Princípio operacional

> **Restaurar primeiro. Autenticar depois. Executar somente se autorizado.**

### 2.4 Regra de não-antecipação

> **Nenhum V1-V4 deve ser antecipado durante o intake.**

## 3. Estrutura Canônica de Intake

### 3.1 Diretórios criados

```
/home/z/my-project/intake/
│
├── A_components/
│   └── received/       # 6 componentes FROZEN de 6.x
│       ├── Corpus_v1.3.0/
│       ├── Oracle_v3/
│       ├── GraphRAG_v1.0.0/
│       ├── P-RESP-001_v0.3/
│       ├── AION-EVAL-002_v0.2/
│       └── B1_config_6.2.11/
│
├── B_reproduction/
│   └── received/       # 12 itens de reprodução
│       ├── scripts/
│       ├── configs/
│       ├── requirements_lockfiles/
│       ├── seeds_params/
│       ├── model_identifiers/
│       ├── execution_manifests/
│       └── logs_outputs/
│
├── C_corpus/
│   └── received/       # PDFs/documentos do corpus
│       ├── CORPUS-001/
│       ├── CORPUS-002-HIST/
│       ├── CORPUS-002/
│       ├── CORPUS-003/
│       ├── CORPUS-004/
│       ├── CORPUS-005/
│       ├── CORPUS-006/
│       ├── CORPUS-007/
│       └── CORPUS-011/
│
├── D_environment/
│   └── received/       # Environment Provenance 6.x
│       ├── pip_freeze_manifests/
│       ├── python_version_logs/
│       ├── os_runtime_info/
│       ├── library_versions/
│       ├── model_identifiers/
│       ├── execution_hashes/
│       ├── timestamps/
│       └── bootstrap_scripts/
│
└── manifests/
    ├── A_components_manifest.md
    ├── B_reproduction_manifest.md
    ├── C_corpus_manifest.md
    ├── D_environment_manifest.md
    └── MASTER_intake_manifest.md
```

### 3.2 Princípio de isolamento

- Diretório `intake/` é **separado** de `download/` (onde estão os artefatos FROZEN de 7.0.0-spec)
- Diretório `intake/` é **separado** de `upload/` (vazio, pode ser usado como porta de entrada)
- Diretório `intake/` é **separado** de `scripts/` (a ser criado quando Grupo B for autenticado)
- Estrutura FROZEN permanece intocada: `download/AION-7.0.0-*.md`, `download/AION-EVIDENCE-LEDGER-001_SCHEMA.md`

### 3.3 Estado dos 4 artefatos FROZEN (verificação de integridade pós-preparação)

| Artefato | SHA-256 (verificado em R0.3.0) | Estado |
|---|---|---|
| AION-7.0.0_PROTOCOL.md | `b9b50b28579a8b5ac99abcc48898b34f965d1ce14de53b85062f7a1fea13a376` | INTACTO |
| AION-EVIDENCE-LEDGER-001_SCHEMA.md | `1bf7349d621382a05f06f743b99e1ed632f804673199b444247b9afc4ddf3507` | INTACTO |
| AION-7.0.0-R_AUDIT.md | `d8efb8f4aee924f7c250a7e9726fdccdebcb6343440a8e1b8fb892c253ee1738` | INTACTO |
| AION-7.0.0-FG_GATE.md | `f082de51f96b144bf0cc98466db600581c3ce3f413fa38e3bf81f477c488e4e4` | INTACTO |

**Confirmação:** Os 4 artefatos FROZEN permanecem materialmente íntegros após a preparação do ambiente de intake. Hashes idênticos aos de Task 65 (PRE_AUDIT_REPORT) e Task 69 (R0_INVENTORY).

## 4. Capacidade do Ambiente

| Item | Valor |
|---|---|
| Sistema de arquivos | `c-6a897ef0-145d6674-e58078f185d4-rootfs` |
| Capacidade total | 9.9G |
| Usado | 87M |
| Disponível | **9.3G** (suficiente para acervo histórico) |
| Permissões /home/z/my-project | `z:z 755` (escrita confirmada) |
| Permissões /home/z/my-project/intake | `z:z 775` |
| Permissões /home/z/my-project/intake/* | `z:z 775` (todos os subdiretórios) |

## 5. O que Esperamos Receber por Grupo

### 5.1 Grupo A — Componentes 6.x (6 itens)

| Item esperado | Versão esperada | Diretório de destino |
|---|---|---|
| Corpus | v1.3.0 (9 registros documentais + 2 inexistentes declarados) | `intake/A_components/received/Corpus_v1.3.0/` |
| Oracle | v3 (7 chunks interversionais) | `intake/A_components/received/Oracle_v3/` |
| GraphRAG | v1.0.0 (22 nós, 187 arestas, PGI=1.0) | `intake/A_components/received/GraphRAG_v1.0.0/` |
| P-RESP-001 | v0.3 (validator determinístico) | `intake/A_components/received/P-RESP-001_v0.3/` |
| AION-EVAL-002 | v0.2 (multicamada, 10 categorias R1-H1) | `intake/A_components/received/AION-EVAL-002_v0.2/` |
| B1 config | 6.2.11 (cross-lingual PT-BR→EN + Oracle v3) | `intake/A_components/received/B1_config_6.2.11/` |

### 5.2 Grupo B — Itens de Reprodução (12+ itens)

| Item esperado | Diretório de destino |
|---|---|
| 12 scripts Python (`extract_aion_corpus.py`, `aion_rag_proxy.py`, `aion_graphrag.py`, `aion_provenance_granular.py`, `aion_temporal_graph.py`, `aion_historical_reconciliation.py`, `aion_bench_001.py`, `aion_p_resp_001_v03.py`, `aion_dify_001.py`, `aion_6_3_0_baseline.py`, `aion_6_4_0_conditional.py`, `aion_6_4_2_minimal.py`) | `intake/B_reproduction/received/scripts/` |
| Configurações | `intake/B_reproduction/received/configs/` |
| requirements.txt / lockfiles | `intake/B_reproduction/received/requirements_lockfiles/` |
| Seeds / parâmetros | `intake/B_reproduction/received/seeds_params/` |
| Identificadores de modelos | `intake/B_reproduction/received/model_identifiers/` |
| Manifests de execução | `intake/B_reproduction/received/execution_manifests/` |
| Logs / outputs | `intake/B_reproduction/received/logs_outputs/` |

### 5.3 Grupo C — Documentação/Corpus (9+ itens)

| Item esperado | Diretório de destino |
|---|---|
| CORPUS-001 (`AION-DOC-000.html`) | `intake/C_corpus/received/CORPUS-001/` |
| CORPUS-002-HIST (Paper A v6.2 anterior, 134KB) | `intake/C_corpus/received/CORPUS-002-HIST/` |
| CORPUS-002 (Paper A v6.2, 137KB) | `intake/C_corpus/received/CORPUS-002/` |
| CORPUS-003 (PARTE IV Formalização Teórica) | `intake/C_corpus/received/CORPUS-003/` |
| CORPUS-004 (Paper B anterior, 3 págs) | `intake/C_corpus/received/CORPUS-004/` |
| CORPUS-005 (Cover Letter PT-BR) | `intake/C_corpus/received/CORPUS-005/` |
| CORPUS-006 (Paper A v6.1 oficial, 138KB) | `intake/C_corpus/received/CORPUS-006/` |
| CORPUS-007 (Paper A v6.1 revisão, 326KB) | `intake/C_corpus/received/CORPUS-007/` |
| CORPUS-011 (Paper B v6.1 PT novo, 5 págs) | `intake/C_corpus/received/CORPUS-011/` |

### 5.4 Grupo D — Environment Provenance 6.x (8+ itens)

| Item esperado | Diretório de destino |
|---|---|
| `pip freeze` / manifestos equivalentes | `intake/D_environment/received/pip_freeze_manifests/` |
| Versão do Python | `intake/D_environment/received/python_version_logs/` |
| Versão do SO/runtime | `intake/D_environment/received/os_runtime_info/` |
| Versões de bibliotecas | `intake/D_environment/received/library_versions/` |
| Identificadores de modelos | `intake/D_environment/received/model_identifiers/` |
| Hashes | `intake/D_environment/received/execution_hashes/` |
| Timestamps | `intake/D_environment/received/timestamps/` |
| Scripts de bootstrap | `intake/D_environment/received/bootstrap_scripts/` |

**IMPORTÂNCIA CRÍTICA (PM Task 72):** Itens do Grupo D devem ser tratados com cautela especial. Documentação TCR/QDT (Python 3.10, NumPy, SciPy, scikit-learn, QuTiP, Matplotlib) mencionada pelo PM em Task 71 **não deve ser automaticamente atribuída ao AION-6.x**. É EVIDÊNCIA CANDIDATA, não autenticação.

## 6. Condição de Encerramento de R0.3 (8 critérios PM)

R0.3 estará concluído quando todo material fornecido tiver sido:

| # | Critério | Verificação |
|---|---|---|
| 1 | Materialmente recebido | Cada arquivo presente em `intake/*/received/` |
| 2 | Preservado sem alteração | SHA-256 computado no momento do intake |
| 3 | Inventariado | Entrada em `intake/manifests/<grupo>_manifest.md` |
| 4 | Associado à origem/proveniência disponível | Campo `origin` em cada manifest |
| 5 | Classificado como EVIDÊNCIA CANDIDATA | Status `CANDIDATE` em cada manifest (não `AUTHENTICATED`) |
| 6 | Submetido a hash quando aplicável | SHA-256 registrado |
| 7 | Separado entre histórico, executável, configuração e ambiente | Diretório de destino apropriado |
| 8 | Registrado no worklog | Task com timestamp e detalhes |

**Nenhum V1-V4 deve ser antecipado durante o intake.** O intake termina em manifest + hash + classificação CANDIDATE. V1-V4 são etapa subsequente (R0.7).

## 7. Template de Manifest (por grupo)

Cada um dos 4 grupos terá um manifest específico. Template canônico para cada item recebido:

```markdown
## Item: <nome-do-arquivo>

| Campo | Valor |
|---|---|
| `filename` | nome do arquivo como recebido |
| `expected_path` | caminho esperado no Handoff (se aplicável) |
| `actual_path` | caminho real no intake |
| `received_at` | timestamp ISO 8601 do recebimento |
| `received_from` | origem (upload, sincronização, etc.) |
| `size_bytes` | tamanho em bytes |
| `sha256` | hash SHA-256 computado no intake |
| `expected_version` | versão esperada (se aplicável) |
| `actual_version` | versão observada (se determinável) |
| `classification` | EVIDÊNCIA CANDIDATA |
| `provenance_chain` | descrição da cadeia de proveniência |
| `notes` | observações adicionais |
```

## 8. Fluxo de Intake (uma vez material recebido)

Quando o PM ou fonte externa disponibilizar material, o fluxo canônico será:

```
1. Detectar material em /home/z/my-project/upload/ ou outra localização
   ↓
2. Para cada arquivo:
   a. Identificar grupo (A/B/C/D)
   b. Mover para intake/<grupo>/received/<subdiretório>/
   c. Computar SHA-256
   d. Atualizar manifest do grupo correspondente
   e. Classificar como EVIDÊNCIA CANDIDATA
   ↓
3. Quando todos os itens de um grupo forem recebidos:
   a. Atualizar manifest master
   b. Atualizar worklog
   c. Confirmar condição de encerramento daquele grupo
   ↓
4. Quando todos os 4 grupos forem recebidos:
   a. Confirmar critérios de encerramento R0.3 (8 critérios PM)
   b. Registrar evento AION-EV-006 no worklog
   c. R0.3 = CONCLUÍDO
   d. Transitar para R0.4 (Environment Provenance)
```

## 9. Estado Atual (pós-R0.3.0)

| Item | Estado |
|---|---|
| Ambiente preparado | ✓ Sim |
| Diretório `intake/` criado | ✓ Sim |
| Subdiretórios dos 4 grupos criados | ✓ Sim |
| Subdiretórios `received/` criados | ✓ Sim |
| Diretório `manifests/` criado | ✓ Sim |
| Espaço em disco disponível | ✓ 9.3G suficiente |
| Permissões de escrita | ✓ Confirmadas |
| 4 artefatos FROZEN íntegros | ✓ Hashes verificados |
| Material recebido | ✗ Nenhum item recebido ainda |
| Manifests preenchidos | ✗ Aguardando material |
| Worklog atualizado | ✓ Task 72 registrará |

## 10. Próxima Ação Material

A próxima ação material é **externa ao ambiente de execução observado pela IA Curadora**:

> Disponibilizar no ambiente de execução o acervo histórico correspondente aos Grupos **A+B+C+D**.

Os caminhos sugeridos para disponibilização (qualquer um funcionará):

1. **`/home/z/my-project/upload/`** (diretório já existe, atualmente vazio, permissões root:root 777)
2. **`/home/z/my-project/intake/<grupo>/received/`** (diretório criado, permissões z:z 775)
3. **Outra localização** — desde que comunicada à IA Curadora para processamento de intake

A partir da detecção de material em qualquer desses caminhos, o intake controlado será executado conforme fluxo da Seção 8.

## 11. Estado do Sistema (pós-R0.3.0)

```
AION-7.0.0
│
├── Specification ........ FROZEN FINAL (Task 68)
├── R0.1 ................ CONCLUÍDO (Task 69)
├── R0.2 ................ CONCLUÍDO (Task 70)
├── R0.2.1 .............. CONCLUÍDO (Task 71)
│
├── R0.3 Restoration ..... AUTHORIZED (Task 72)
│   └── R0.3.0 Environment Preparation ... CONCLUÍDO (este documento)
│       ├── intake/ structure created
│       ├── 4 group subdirs created
│       ├── manifests/ dir created
│       ├── 4 FROZEN artifacts integrity verified
│       └── disk space confirmed (9.3G available)
│
├── R0.3.1 Material Intake (per group) ... PENDING (awaiting external material)
│   ├── Grupo A intake .................. PENDING
│   ├── Grupo B intake .................. PENDING
│   ├── Grupo C intake .................. PENDING
│   └── Grupo D intake .................. PENDING
│
├── R0.4 Environment Provenance ......... PENDING (depends on R0.3 completion)
├── R0.5 EP Classification .............. EP-0 UNKNOWN (preliminar)
├── R0.6 SHA-256 ........................ PENDING (will be done during intake)
├── R0.7 V1-V4 .......................... PENDING (NO ANTICIPATION)
│
├── EP ................................. EP-0 UNKNOWN
├── AUTH₇.₀ ............................ FALSE
├── ENV ............................... BLOCKED
├── PIPE .............................. NOT RUN
├── NOMOD .............................. PENDING
└── FINAL_AUTH₇.₀ ...................... BLOCKED
```

## 12. Genealogia Documental

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
       ▼  R0.3.0 Environment Preparation — CONCLUÍDO (este documento)
       │
       ├── intake/ structure created
       ├── 4 FROZEN artifacts integrity verified
       ├── disk space confirmed
       │
       ▼  Próxima operação: R0.3.1 Material Intake
       │
       ├── Aguardando material externo Grupos A+B+C+D
       │
       ▼  Quando material chegar:
       │
       R0.3.1 Material Intake (per group) — flow:
       ├── Detect → Move → SHA-256 → Manifest → Classify as CANDIDATE → Worklog
       │
       ▼  Quando 8 critérios de encerramento PM satisfeitos:
       │
       R0.3 = CONCLUÍDO
       │
       ▼  Apenas então:
       │
       R0.4 Environment Provenance (com material recebido)
       │
       ▼
       R0.5 EP Classification (evidence-driven, com nova evidência)
       │
       ▼  Possíveis transições:
       │
       ├── EP-0 (permanece) → STANDBY
       ├── EP-1 PARTIAL → STANDBY, mas caracterizado
       ├── EP-2 COMPATIBLE → STANDBY, mas caracterizado (não FAILED)
       └── EP-3 EQUIVALENT → prosseguir para R0.7 V1-V4
```

---

*"O ambiente está preparado para receber o acervo histórico. Quatro grupos, oito critérios de encerramento, um princípio: restaurar primeiro, autenticar depois, executar somente se autorizado. Aguardando material externo."*

**Fim do AION-7.0.0-R0.3 Intake Manifest Template.**
