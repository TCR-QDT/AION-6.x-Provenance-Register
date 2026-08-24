# HANDOFF DOCUMENT — AION-MVP-001 (Fase 7.0.0)

**Data:** 24 de agosto de 2026
**Projeto:** AION-MVP-001 — Arquitetura para a Individuação Ontológica e Narrativa
**Fase:** AION-7.0.0 — Núcleo Epistêmico (Especificação + Restauração Material + Provenance Boundary)
**Autor / Curador:** Edson Carvalho do Nascimento (Projetista Master)
**Analista Técnico:** IA Curadora (Role: Escriba / Arquiteto de Metadados)
**Sessão:** web-73c75281-201c-4716-b85c-97833d25f9b3
**Período:** 21–24 de agosto de 2026
**Tasks executadas:** 60–90 (31 tasks)
**Worklog:** `/home/z/my-project/worklog.md` (2513+ linhas)

---

## 1. RESUMO EXECUTIVO

O projeto AION encontra-se na fase de **Consolidação do Núcleo Epistêmico (AION-7.0.0)**, tendo transicionado da unidade de análise "QUESTION → ANSWER" (6.x) para "QUESTION → EVIDENCE → CLAIM → PROVENANCE → VALIDATION → EPISTEMIC ACCEPTANCE" (7.x). A especificação 7.0.0 foi produzida, congelada (FROZEN FINAL), e submetida a um processo de restauração material controlada (R0) que investigou exaustivamente a possibilidade de autenticar a infraestrutura histórica do AION-6.x.

**Resultado canônico consolidado:** A especificação 7.0.0 está FROZEN FINAL em 4 artefatos canônicos. O processo R0 (Restauração Material) investigou 4 classes de evidência contemporânea (manifest, log, snapshot, git histórico) — todas retornaram AUSENTE. Um Provenance Register público foi criado em `github.com/TCR-QDT/AION-6.x-Provenance-Register`, estabelecendo P1 (integridade documental ✓) e P2 (proveniência da incorporação ✓), mas P3 (proveniência histórica AION-6.x) permanece INSUFFICIENT — HISTORICAL EVIDENCE NOT RECOVERABLE FROM CURRENTLY ACCESSIBLE MATERIAL. A fronteira epistemológica foi formalmente declarada: o sistema sabe o que demonstrou, o que corroborou narrativamente, e o que não pode demonstrar materialmente. AUTH₇.₀ = FALSE. FINAL_AUTH₇.₀ = BLOCKED. O baseline experimental N=100 permanece não autorizado.

---

## 2. ESTADO ATUAL E PRÓXIMA AÇÃO

**Status:** AION-7.0.0 — Specification FROZEN FINAL. R0 Partially Reopened. Provenance Boundary formally declared. Recovery exhausted.

**Próxima ação:** Requer determinação do Projetista Master. As opções são:
1. Aceitar a fronteira epistemológica como estado consolidado; declarar R0 CLOSED com P3 INSUFFICIENT — NOT RECOVERABLE; STANDBY MATERIAL permanente até nova evidência externa ou Via B.
2. Ativar Via B — Nova determinação metodológica (redefinir o experimento AION-7.0.0 sem depender de AION-6.x infrastructure).
3. Fornecer nova evidência material histórica contemporânea (manifest de ingestão AION-6.x original com hashes, snapshot do ambiente, ou URL de repositório Git AION-6.x com infrastructure).

**Bloqueador:** P3 INSUFFICIENT — a evidência histórica necessária para autenticar a ponte TCR/QDT → AION-6.x não é recuperável do material atualmente acessível. Sem V3 PASS, AUTH₇.₀ permanece FALSE e FINAL_AUTH₇.₀ permanece BLOCKED.

---

## 3. COMPONENTES DO SISTEMA

### 3.1 Artefatos FROZEN de 7.0.0-spec (4 canônicos)

| Artefato | Versão | Caminho | SHA-256 | Estado |
|---|---|---|---|---|
| AION-7.0.0_PROTOCOL.md | 7.0.0-spec (FROZEN) | `/download/` | `b9b50b28579a8b5ac99abcc48898b34f965d1ce14de53b85062f7a1fea13a376` | FROZEN FINAL |
| AION-EVIDENCE-LEDGER-001_SCHEMA.md | 1.0.0-spec (FROZEN) | `/download/` | `1bf7349d621382a05f06f743b99e1ed632f804673199b444247b9afc4ddf3507` | FROZEN FINAL |
| AION-7.0.0-R_AUDIT.md | 7.0.0-R-spec (FROZEN) | `/download/` | `d8efb8f4aee924f7c250a7e9726fdccdebcb6343440a8e1b8fb892c253ee1738` | FROZEN FINAL |
| AION-7.0.0-FG_GATE.md | v3 (FROZEN) | `/download/` | `f082de51f96b144bf0cc98466db600581c3ce3f413fa38e3bf81f477c488e4e4` | FROZEN FINAL |

### 3.2 Relatórios R0 produzidos (não-FROZEN, dados históricos)

| Arquivo | Conteúdo | Task |
|---|---|---|
| `AION-7.0.0-PRE_AUDIT_REPORT.md` | Pré-auditoria material do ambiente (Task 65) | 65 |
| `AION-7.0.0-R0_INVENTORY.md` | Inventário material inicial (R0.1) | 69 |
| `AION-7.0.0-R0.2_RECOVERY.md` | Recuperação material histórica (R0.2) | 70 |
| `AION-7.0.0-R0.2.1_RECONCILIATION.md` | Reconciliação do acervo histórico (R0.2.1) | 71 |
| `AION-7.0.0-R0.4_ENVIRONMENT_PROVENANCE_REPORT.md` | Auditoria de environment provenance (R0.4) | 76 |
| `AION-7.0.0-R0.5_EP_TRANSITION_GATE.md` | EP classification & transition gate (R0.5) | 77 |
| `AION-7.0.0-R0.3.3_EXTERNAL_INTAKE.md` | Intake do TCR/QDT repository (R0.3.3) | 79 |
| `AION-7.0.0-R0.3.3.A_V1-V4_VERIFICATION.md` | V1-V4 verification de C-01 e C-02 (R0.3.3.A) | 80 |
| `AION-7.0.0-R0.3.3.A.2_PROVENANCE_BRIDGE.md` | Provenance bridge recovery em TCR/QDT (R0.3.3.A.2) | 81 |
| `AION-7.0.0-R0.3.3.A.2.4_EXTERNAL_AION6x_BRIDGE.md` | External AION-6.x bridge search (R0.3.3.A.2.4) | 82 |
| `AION-7.0.0-R0.3.3.A.2.4.A_URL_CLASSIFICATION.md` | URL classification (ChatGPT conversation) | 84 |
| `AION-7.0.0-R0.3.3.A.2.4.A.1_HISTORICAL_SOURCE.md` | Historical source analysis (MEMORIAS) | 85 |

### 3.3 Provenance Register (GitHub)

| Item | Valor |
|---|---|
| URL | `https://github.com/TCR-QDT/AION-6.x-Provenance-Register` |
| Organização | TCR-QDT |
| Estado inicial | EMPTY REPOSITORY (antes do push PM) |
| Push timestamp | 2026-08-23 19:47:53 -0300 |
| Push executor | Edson Carvalho do Nascimento (PM, shukuwe@gmail.com) |
| Commit SHA (push) | `83b75ec105618c2d61ff8e142df197a4194a2b3e` |
| Commit SHA (local) | `ab20bf67abf522f9a2738a55409c3f4a8a57e747` |
| Total de arquivos | 8 |
| Estrutura | `README.md`, `provenance/{README, TCR_QDT_BRIDGE, CORPUS_PROVENANCE, HISTORICAL_STATUS}.md`, `manifests/AION-6.x_CORPUS_PROVENANCE.yaml`, `evidence/historical/MEMORIAS_DE_UMA_CONSTRUCAO.md`, `ledger/PROVENANCE_LEDGER.md` |
| tar.gz | `/download/AION-6.x-Provenance-Register.tar.gz` (SHA-256 `c2777cca60c3c1ece90dc885b22712556130e40fad1ca681d923c4c288df32cc`) |
| Discrepância GitHub | NON-OBSERVED / UNRECONCILED (PM reporta página pública vazia; IA Curadora verificou 8 arquivos via clone em Task 88) |

### 3.4 Repositórios externos capturados

| Repositório | URL | Captura | Commit SHA | Arquivos |
|---|---|---|---|---|
| TCR/QDT (Coerencia_Relacional) | `github.com/TCR-QDT/Coerencia_Relacional` | Task 79 (2026-08-23) | `3e0d8c7e0a3752b515d7dca4c81d861fa4eb50c3` | 190 (12MB) |
| AION-6.x-Provenance-Register | `github.com/TCR-QDT/AION-6.x-Provenance-Register` | Task 87 (2026-08-23) | `ab20bf67...` (local) / `83b75ec...` (GitHub) | 8 |

### 3.5 Documento histórico recuperado

| Item | Valor |
|---|---|
| Filename | `MEMÓRIAS DE UMA CONSTRUÇÃO — A História do Pensamento, da Consciência e do Arquivo Vivo.md` |
| SHA-256 | `7549597b065e784c7baae3baca42049e23cc57937c610cfd2c4f23b242d2d9df` |
| Tamanho | 25342 bytes, 1102 linhas |
| Classificação | HISTORICAL_RECORD |
| Status epistêmico | NARRATIVE_CORROBORATION |
| Fornecido por | Projetista Master (via `/upload/` em Task 85) |
| Âncoras canônicas AION encontradas | CORPUS-002, CORPUS-006, R^α genealogy, F3 example (CORPUS-002#chunk_001), Oracle chunk (CORPUS-006#p1_01), B1 3/3, P-RESP-001 v0.3, GraphRAG, AION-6.2, AION-6.3, AION-7.0.0-R0.3.3.A.2.4.A, Task ID 83 |
| Ponte material criptográfica | ✗ AUSENTE (zero hashes C-01/C-02, zero manifests, zero URLs Git) |

### 3.6 Componentes 6.x FROZEN (Handoff AION-MVP-001)

| Componente | Versão | Estado em 7.0.0 |
|---|---|---|
| Corpus | v1.3.0 | NOT MATERIALLY ACCESSIBLE |
| Oracle | v3 | NOT MATERIALLY ACCESSIBLE |
| GraphRAG | v1.0.0 | NOT MATERIALLY ACCESSIBLE |
| P-RESP-001 | v0.3 | NOT MATERIALLY ACCESSIBLE |
| AION-EVAL-002 | v0.2 | NOT MATERIALLY ACCESSIBLE |
| B1 Retrieval config | 6.2.11 | NOT MATERIALLY ACCESSIBLE |
| Temporal Index | v1.0 | NOT MATERIALLY ACCESSIBLE |
| Ontologia | v1.0.0 | NOT MATERIALLY ACCESSIBLE |

### 3.7 Ambiente de execução observado

| Item | Valor |
|---|---|
| OS | Debian GNU/Linux 13 (trixie) |
| Kernel | 5.10.134-013.8.3.kangaroo.al8.x86_64 |
| Container | Kata (FC_FUNCTION_NAME ws-bf41a584-...) |
| Region | cn-hongkong (Alibaba Cloud Function Compute) |
| Memory | 4096 MB |
| Python default | 3.12.13 (/home/z/.venv/) |
| Python sistema | 3.13.5 (/usr/bin/python3.13) |
| Projeto ativo | z-agent v0.1.0 (598 packages em uv.lock) — NÃO AION-6.x |
| Bibliotecas AUSENTES | torch, transformers, sentence-transformers |
| Git history | Inicializado em 2026-08-21 22:04:16 UTC (início desta sessão) |
| Espaço disponível | 9.3G |
| Mounts | 3 ossfs (official_skills, sync, upload) + 2 PolarFS (tmp/my-project, user_skills) |

---

## 4. ESTADO DO BENCHMARK B1-B7 (herdado de 6.x)

| Teste | Status | Detalhe |
|---|---|---|
| B1 | RESOLVED | Top-1=3/3, determinístico, cross-lingual + Oracle v3 |
| B2 | CHARACTERIZED / CONTROLLED LIMITATION | F3 caracterizado, CFR≈47%, EBA≈68%, VR=100%, H-TEMP confound |
| B3 | FAIL-SYSTEM | Não investigado em 6.2 |
| B4 | PARTIAL | |
| B5 | PASS-SEMANTIC | |
| B6 | PARTIAL / TEMPORALLY BOUNDED | Janela 12/08/2026, NOT CLOSED |
| B7 | PASS-SEMANTIC | |

---

## 5. TRAJETÓRIA COMPLETA AION-7.0.0 (TASKS 60-90)

### 5.1 Fase de Especificação (Tasks 60-68)

| Task | Ação | Resultado |
|---|---|---|
| 60 | Receber Handoff AION-MVP-001; produzir framework canônico | Protocol + Ledger Schema produzidos |
| 61 | Consolidar Opção B (Specification-Only) | R_AUDIT + FG_GATE produzidos; AION-EV-001 registrado |
| 62 | Correções epistemológicas PM | Instrumento≠evidência; gate conjuntivo AUTH₇.₀; AION-EV-001 reclassificação |
| 63 | Confirmação standby | 3 invariantes canônicos + estrutura 2 níveis registrados |
| 64 | Formal Execution Gate | FG_GATE v1 produzido (7 gates, Via A/B, state machine) |
| 65 | Pré-auditoria material | Ambiente caracterizado; divergência PM vs IA Curadora registrada |
| 66 | Environment Provenance | FG_GATE v2 (Seção 5.4 — Environment Provenance + fórmula ENV=VERIFIED ⟺ E_env^{6.x} ≅ E_env^{restaurado}) |
| 67 | EP Classification | FG_GATE v3 (Seção 5.5 — EP-0/EP-1/EP-2/EP-3 + 4º invariante COMPATIBLE≠EQUIVALENT) |
| 68 | Encerramento fase de especificação | 4 artefatos FROZEN FINAL; auto-disciplina Curador estabelecida |

### 5.2 Fase de Restauração Material R0 (Tasks 69-78)

| Task | Ação | Resultado |
|---|---|---|
| 69 | R0.1 Inventário Material | 0/6 componentes, 0/12 scripts, 0 PDFs, /upload/ EMPTY |
| 70 | R0.2 Recuperação Material Histórica | 0 artefatos 6.x em qualquer localização acessível |
| 71 | R0.2.1 Reconciliação do Acervo Histórico | 9 registros históricos catalogados, 0 materialmente presentes como arquivo independente |
| 72 | R0.3.0 Environment Preparation | intake/ structure created; 4 FROZEN integrity verified |
| 73 | R0.3.1 Material Intake Detection | MATERIAL_DETECTED = FALSE; INPUT_PENDING |
| 74 | R0.3.2 Material Provisioning | intake subdirs perdidos entre sessões → recriados; 4 FROZEN intact |
| 75 | R0.3.2.1 Detection | MATERIAL_DETECTED = FALSE; INPUT_PENDING |
| 76 | R0.4 Environment Provenance Readiness | 6 perguntas canônicas: 0/12 evidências disponíveis; nenhuma ponte material legítima |
| 77 | R0.5 EP Classification & Transition Gate | EP-0 UNKNOWN formally consolidated; AUTH₇.₀=FALSE; FINAL_AUTH₇.₀=BLOCKED |
| 78 | R0 Closure | R0 CLOSED / MATERIAL STANDBY; WAITING_FOR_EXTERNAL_MATERIAL |

### 5.3 Fase de Ponte Material Externa (Tasks 79-90)

| Task | Ação | Resultado |
|---|---|---|
| 79 | R0.3.3 External Material Intake (TCR/QDT) | Repositório capturado: 190 arquivos, 12MB; 2 EXACT matches (CORPUS-002, CORPUS-006); 0 para Grupo A/B/D |
| 80 | R0.3.3.A V1-V4 Candidate Verification | C-01 e C-02 classificados Caso D (V1+V2+V4 PASS, V3 INSUFFICIENT) |
| 81 | R0.3.3.A.2 Provenance Bridge Recovery (TCR/QDT) | 4 prioridades (P1-P4): todas ZERO matches no TCR/QDT repo |
| 82 | R0.3.3.A.2.4 External AION-6.x Bridge Search | 5 prioridades: todas AUSENTE; acervo AION-6.x não materializado |
| 83 | R0.3.3.A.2.4.A Authorization | URL_PENDING; 12 pontos de escopo PM registrados |
| 84 | URL Classification | URL recebida = ChatGPT Shared Conversation (NÃO Git repo); HTTP 403; REPOSITORY_PENDING |
| 85 | R0.3.3.A.2.4.A.1 Historical Source Analysis | MEMORIAS_DE_UMA_CONSTRUCAO.md analisado; corroboração narrativa significativa; ponte material criptográfica AUSENTE |
| 86 | AION-6.x-DOC-001 Draft Preparation | 4 documentos DRAFT preparados localmente (MEMORIAS + PROVENANCE_REGISTER + INGESTION_EVENT + README_DEPLOYMENT) |
| 87 | R0.3.3.A.2.4.A.2 Provenance Register Initialization | Clone + 8 documentos + commit local (ab20bf67...); push falhou (credenciais GitHub ausentes); tar.gz criado |
| 88 | Provenance Register Material Audit | 8 artefatos auditados no GitHub; hashes C-01/C-02 encontrados em 3 arquivos como candidate_sha256 (não historical); V3 INSUFFICIENT mantido |
| 89 | AION-6.x Provenance Evidence Recovery | 4 classes (V3-A manifest, V3-B log, V3-C snapshot, V3-D git histórico): todas AUSENTE |
| 90 | Provenance Boundary & Irrecoverability Determination | P3 INSUFFICIENT — NOT RECOVERABLE; RECOVERY EXHAUSTED; NO RETROACTIVE CLAIM; CASE D PRESERVED; fronteira epistemológica formalmente declarada |

---

## 6. ARQUITETURA CANÔNICA 7.0.0

### 6.1 Cadeia epistêmica (Nível 1 — Objeto de Estudo)

```
QUESTION → EVIDENCE → CLAIM → EVIDENCE-CLAIM BINDING → PROVENANCE → VALIDATION → EPISTEMIC ACCEPTANCE
```

### 6.2 Cadeia de infraestrutura (Nível 2 — AION próprio)

```
ARTEFATO → EXISTÊNCIA (V1) → VERSÃO (V2) → INTEGRIDADE (V3) → CONTEÚDO CANÔNICO (V4) → AMBIENTE (ENV) → PIPELINE (PIPE) → NÃO-MODIFICAÇÃO (NOMOD) → AUTORIZAÇÃO DE EXECUÇÃO (FINAL_AUTH₇.₀)
```

### 6.3 Fórmulas canônicas

**AUTH₇.₀ (componentes):**
$$\text{AUTH}_{7.0} = \bigwedge_{i=1}^{6}(E_i \land V_i \land H_i \land C_i)$$

**FINAL_AUTH₇.₀ (gate completo):**
$$\text{FINAL\_AUTH}_{7.0} = \text{AUTH}_{7.0} \land \text{ENV} \land \text{PIPE} \land \text{NOMOD}$$

**Gate IV (Environment):**
$$\text{ENV} = \text{VERIFIED} \iff E_{env}^{6.x} \cong E_{env}^{restaurado}$$

**EP Classification:**
$$\text{ENV} = \begin{cases} \text{VERIFIED} & \text{se EP-3} \\ \text{BLOCKED} & \text{se EP-0, EP-1, EP-2} \end{cases}$$

### 6.4 4 invariantes canônicos

$$\boxed{\text{UNAVAILABLE} \neq \text{NON-EXISTENT}}$$
$$\boxed{\text{NON-OBSERVED} \neq \text{FALSE}}$$
$$\boxed{\text{PENDING} \neq \text{FAILED}}$$
$$\boxed{\text{COMPATIBLE} \neq \text{EQUIVALENT}}$$

### 6.5 8 métricas do baseline 7.0.0

| Métrica | Definição |
|---|---|
| ERR | P(Evidence Retrieved \| Query) |
| SCR | P(Semantic Claim \| Query) |
| PER | P(Provenance Emitted \| Query) |
| PV | P(Provenance Valid \| Provenance Emitted) |
| PM | P(Provenance Matches Evidence \| Provenance Valid) |
| ECB | P(E ⊨ C \| Provenance) |
| VR | P(Validator Intercepts \| Invalid) |
| EAR | P(Epistemic Acceptance) |

### 6.6 8 estados terminais do Evidence Ledger

ACCEPTED, INCOMPLETE_NO_EVIDENCE, INCOMPLETE_NO_CLAIM, INCOMPLETE_NO_PROVENANCE, REJECTED_PROVENANCE_INVALID, REJECTED_PROVENANCE_MISMATCH, REJECTED_BINDING, INTERCEPTED

### 6.7 Hipóteses congeladas

- **H-ECB:** Uma resposta semanticamente correta não implica necessariamente que exista uma cadeia válida e auditável entre o claim produzido e a evidência que o sustenta.
- **H-EPISTEMIC:** A avaliação epistemológica de uma resposta exige a decomposição independente de recuperação, claim, provenance, binding e validação.

### 6.8 Sequência canônica de gates (15 passos)

```
1. RESTAURAÇÃO MATERIAL
2. INVENTÁRIO DOS ARTEFATOS
3. ENVIRONMENT PROVENANCE
4. EP CLASSIFICATION
5. SHA-256
6. V1 — EXISTÊNCIA
7. V2 — VERSÃO
8. V3 — INTEGRIDADE
9. V4 — CONTEÚDO CANÔNICO
10. AUTH₇.₀
11. GATE IV — ENV
12. GATE V — PIPE / SMOKE TEST
13. GATE VI — NOMOD
14. GATE VII — FINAL_AUTH₇.₀
15. [SE TRUE] BASELINE 7.0.0 / [SE FALSE] BLOCKED
```

---

## 7. PROVENANCE INVESTIGATION — RESULTADO CONSOLIDADO

### 7.1 Três níveis de prova (P1/P2/P3)

| Nível | O que prova | Estado |
|---|---|---|
| **P1 — Integridade documental** | Documento no GitHub = documento recuperado | ✓ RESOLVIDA |
| **P2 — Proveniência da incorporação** | Quando e qual documentação foi incorporada ao Provenance Register | ✓ RESOLVIDA |
| **P3 — Proveniência histórica AION-6.x** | PDFs TCR/QDT = PDFs do corpus AION-6.x original | ✗ INSUFFICIENT — NOT RECOVERABLE |

### 7.2 Candidatos verificados (Caso D)

| Candidato | CORPUS-ID | SHA-256 (candidate) | Tamanho | V1 | V2 | V3 | V4 | Classificação |
|---|---|---|---|---|---|---|---|---|
| C-01 | CORPUS-002 | `971986d9...` | 137520 bytes | ✓ PASS | ✓ PASS | ⚠ INSUFFICIENT | ✓ PASS | Caso D |
| C-02 | CORPUS-006 | `efd7f7ca...` | 138780 bytes | ✓ PASS | ✓ PASS | ⚠ INSUFFICIENT | ✓ PASS | Caso D |

### 7.3 Evolução metodológica: dimensões do hash

O hash deixou de ser um valor isolado e passou a ter 6 dimensões:

```
HASH
 ├── origem (quem computou/registrou)
 ├── timestamp (quando foi registrado)
 ├── contexto (em que artefato, em que sistema)
 ├── artefato que o registrou (manifest, log, snapshot, repo)
 ├── relação com CORPUS-ID (mapeamento declarado)
 └── independência da evidência recuperada (registrado antes ou independentemente)
```

**candidate_sha256** (presente): computado pela IA Curadora em Task 80 (2026-08-23)
**historical_sha256** (ausente): requereria registro durante ingestão AION-6.x (10-12/08/2026)

### 7.4 Recovery Exhausted

| Classe | Investigada? | Resultado |
|---|---|---|
| V3-A Manifest histórico | ✓ Sim | AUSENTE |
| V3-B Log de ingestão | ✓ Sim | AUSENTE |
| V3-C Snapshot do ambiente | ✓ Sim | AUSENTE |
| V3-D Git histórico AION-6.x | ✓ Sim | AUSENTE |

### 7.5 Fronteira epistemológica formal

```
EVIDÊNCIA DEMONSTRADA          CORROBORAÇÃO NARRATIVA         DESCONHECIMENTO HISTÓRICO
       │                              │                              │
   P1 ✓ PASS                    MEMORIAS_DE_UMA                P3 ✗ INSUFFICIENT
   P2 ✓ PASS                    CONSTRUCAO.md                  NOT RECOVERABLE
       │                        (confirma existência                 │
       │                         AION-6.x, mas não                    │
       │                         autentica materialmente)             │
       └──────────────────────────────┴──────────────────────────────┘
                                      │
                            FRONTIER: não reversível
                            por inferência retroativa
```

---

## 8. GENEALOGIA DOCUMENTAL DO PAPER A (herdada de 6.x)

```
CORPUS-006 (10/08, v6.1, C=0.968, R^α PRESENTE)
       ↓ SCIENTIFIC_REVISION
CORPUS-007 (12/08, v6.1-revision, C=0.793±0.133, R^α PRESENTE)
       ↓ CONSOLIDATION (R^α: PRESENTE → ABSENT, version bump v6.1→v6.2)
CORPUS-002-HIST (12/08, v6.2 anterior, 134KB) — SUPERSEDED
       ↓ TEXTUAL_EQUIVALENT_REPLACEMENT
CORPUS-002 (12/08, v6.2, 137KB) — CURRENT/AUTHORITATIVE
```

---

## 9. REGRAS EPISTEMOLÓGICAS (NON-NEGOTIABLES)

### 9.1 10 regras herdadas de AION-MVP-001

1. **Regra de Proveniência:** Nenhuma afirmação entra no sistema sem saber de onde veio.
2. **Tags E/I/H:** `[E]`=Evidência, `[I]`=Interpretação, `[H]`=Hipótese.
3. **O Nome do Arquivo não é o Documento:** Conteúdo interno > nome do arquivo.
4. **NÃO DECLARADO é um dado:** Ausência de data/versão é registrada como `NÃO DECLARADO [E]`.
5. **T8:** Projetista Master tem precedência de comando. IA Curadora executa, registra e apoia.
6. **FR = PER × CFR:** Fabricação observada é composta por emissão × confiabilidade condicional.
7. **PER=0 ≠ confiável:** Ausência de provenance não significa ausência de risco.
8. **Oracle não pode ser relaxado porque retrieval falhou.**
9. **Substituição não é apagamento:** Genealogia documental deve ser preservada.
10. **H-TEMP é confound, não conclusão.**

### 9.2 Regras adicionais estabelecidas em 7.0.0

11. **Não basta encontrar o hash. Precisamos saber: Qual é a origem do hash?** (Task 88)
12. **Compatibilidade de conteúdo não equivale a autenticação histórica.** (Task 80)
13. **Corroboração narrativa não constitui autenticação material.** (Task 85)
14. **Busca evidence-driven produz ausência de evidência — não evidência de ausência.** (Task 81)
15. **A próxima evidência deve vir do acervo, não da nossa memória sobre o acervo.** (Task 78)
16. **Persistência nominal do ambiente ≠ persistência material dos artefatos.** (Task 74)
17. **Não procurar evidência para confirmar a hipótese; procurar material que possa confirmar ou refutar.** (Task 81)
18. **O gate não verifica se o resultado será favorável. O gate verifica se temos autorização epistêmica para medir.** (Task 64)
19. **Restaurar primeiro. Autenticar depois. Executar somente se autorizado.** (Task 72)
20. **R0 passa a ter uma fronteira formalmente fechada. A partir dela, qualquer avanço deixa de ser operação de auditoria interna e passa a depender de evento externo observável.** (Task 77)

---

## 10. ARTEFATOS PRODUZIDOS

### 10.1 Documentos canônicos FROZEN (4)

| Arquivo | Caminho |
|---|---|
| AION-7.0.0_PROTOCOL.md | `/home/z/my-project/download/` |
| AION-EVIDENCE-LEDGER-001_SCHEMA.md | `/home/z/my-project/download/` |
| AION-7.0.0-R_AUDIT.md | `/home/z/my-project/download/` |
| AION-7.0.0-FG_GATE.md | `/home/z/my-project/download/` |

### 10.2 Relatórios R0 (8)

| Arquivo | Caminho |
|---|---|
| AION-7.0.0-PRE_AUDIT_REPORT.md | `/home/z/my-project/download/` |
| AION-7.0.0-R0_INVENTORY.md | `/home/z/my-project/download/` |
| AION-7.0.0-R0.2_RECOVERY.md | `/home/z/my-project/download/` |
| AION-7.0.0-R0.2.1_RECONCILIATION.md | `/home/z/my-project/download/` |
| AION-7.0.0-R0.4_ENVIRONMENT_PROVENANCE_REPORT.md | `/home/z/my-project/download/` |
| AION-7.0.0-R0.5_EP_TRANSITION_GATE.md | `/home/z/my-project/download/` |
| AION-7.0.0-R0.3.3_EXTERNAL_INTAKE.md | `/home/z/my-project/intake/manifests/` |
| AION-7.0.0-R0.3.3.A_V1-V4_VERIFICATION.md | `/home/z/my-project/intake/manifests/` |

### 10.3 Manifests de intake (8)

| Arquivo | Caminho |
|---|---|
| INTAKE_MANIFEST_TEMPLATE.md | `/home/z/my-project/intake/manifests/` |
| AION-7.0.0-R0.3.1_INTAKE_MANIFEST.md | `/home/z/my-project/intake/manifests/` |
| AION-7.0.0-R0.3.2_PROVISIONING.md | `/home/z/my-project/intake/manifests/` |
| AION-7.0.0-R0.3.3.A.2_PROVENANCE_BRIDGE.md | `/home/z/my-project/intake/manifests/` |
| AION-7.0.0-R0.3.3.A.2.4_EXTERNAL_AION6x_BRIDGE.md | `/home/z/my-project/intake/manifests/` |
| AION-7.0.0-R0.3.3.A.2.4.A_URL_CLASSIFICATION.md | `/home/z/my-project/intake/manifests/` |
| AION-7.0.0-R0.3.3.A.2.4.A.1_HISTORICAL_SOURCE.md | `/home/z/my-project/intake/manifests/` |
| AION-7.0.0-R0.3.2_PROVISIONING.md | `/home/z/my-project/intake/manifests/` |

### 10.4 Pacote preparatório AION-6.x-DOC-001 (4)

| Arquivo | Caminho |
|---|---|
| MEMORIAS_DE_UMA_CONSTRUCAO.md | `/home/z/my-project/intake/aion-6x-provenance-prep/` |
| PROVENANCE_REGISTER.md | `/home/z/my-project/intake/aion-6x-provenance-prep/` |
| INGESTION_EVENT_2026-08-23.md | `/home/z/my-project/intake/aion-6x-provenance-prep/` |
| README_DEPLOYMENT.md | `/home/z/my-project/intake/aion-6x-provenance-prep/` |

### 10.5 Provenance Register no GitHub (8 arquivos)

| Arquivo | Caminho no repositório |
|---|---|
| README.md | `AION-6.x-Provenance-Register/` |
| provenance/README.md | `provenance/` |
| provenance/TCR_QDT_BRIDGE.md | `provenance/` |
| provenance/CORPUS_PROVENANCE.md | `provenance/` |
| provenance/HISTORICAL_STATUS.md | `provenance/` |
| manifests/AION-6.x_CORPUS_PROVENANCE.yaml | `manifests/` |
| evidence/historical/MEMORIAS_DE_UMA_CONSTRUCAO.md | `evidence/historical/` |
| ledger/PROVENANCE_LEDGER.md | `ledger/` |

### 10.6 tar.gz

| Arquivo | Caminho | SHA-256 |
|---|---|---|
| AION-6.x-Provenance-Register.tar.gz | `/home/z/my-project/download/` | `c2777cca60c3c1ece90dc885b22712556130e40fad1ca681d923c4c288df32cc` |

### 10.7 Worklog

| Arquivo | Caminho | Linhas |
|---|---|---|
| worklog.md | `/home/z/my-project/worklog.md` | 2513+ (Tasks 60-90) |

---

## 11. EVENTOS DE PROVENIÊNCIA CANÔNICOS

| Event ID | Task | Descrição |
|---|---|---|
| AION-EV-001 | 60 | MATERIAL_STATE_VERIFICATION — components FROZEN absent from environment |
| AION-EV-002 | 61 | PRE_AUDIT_MATERIAL_EXECUTION |
| AION-EV-003 | 69 | R0.1_INVENTORY_COMPLETED |
| AION-EV-004 | 70 | R0.2_RECOVERY_COMPLETED |
| AION-EV-005 | 71 | R0.2.1_RECONCILIATION_COMPLETED |
| AION-EV-006 | 73 | R0.3.1_DETECTION_COMPLETED — INPUT_PENDING |
| AION-EV-007 | 74 | R0.3.2.0_RE_PREPARATION — intake subdirs lost, re-created |
| AION-EV-008 | 76 | R0.4_ENVIRONMENT_PROVENANCE_READINESS — 0/12 evidence available |
| AION-EV-009 | 77 | R0.5_EP_TRANSITION_GATE — EP-0 consolidated |
| AION-EV-010 | 79 | R0.3.3_EXTERNAL_INTAKE — TCR/QDT captured |
| AION-EV-011 | 80 | R0.3.3.A_V1_V4_VERIFICATION — both Caso D |
| AION-EV-012 | 81 | R0.3.3.A.2_PROVENANCE_BRIDGE — bridge not found in TCR/QDT |
| AION-EV-013 | 82 | R0.3.3.A.2.4_EXTERNAL_AION6x_BRIDGE — not materialized |
| AION-EV-014 | 84 | R0.3.3.A.2.4.A_URL_CLASSIFICATION — ChatGPT conversation, not Git repo |
| AION-EV-015 | 85 | R0.3.3.A.2.4.A.1_HISTORICAL_SOURCE — narrative corroboration, no material bridge |

---

## 12. DISTINÇÃO CRÍTICA PM — TRÊS NÍVEIS

```
TCR/QDT              →  AION-6.x              →  AION-7.0.0
(repositório            (arquitetura             (fase de especificação
 capturado em            computacional            do gate epistêmico
 Task 79; PDFs           RAG/provenance           para baseline 7.0.0;
 C-01, C-02 têm          investigada em          este Handoff)
 conteúdo compatível     6.x; corpus
 V4 PASS, mas V3         source não
 INSUFFICIENT)           materialmente
                          acessível; recovery
                          EXHAUSTED)
```

**Esta distinção NUNCA foi colapsada.** Os três níveis permanecem materialmente distintos em toda a trajetória 60-90.

---

## 13. INSTRUÇÕES PARA O PRÓXIMO ANALISTA

* **Se você é uma IA retomando o chat:** Cumprimente Edson, confirme que possui este Handoff em memória, e peça para determinar a próxima ação (aceitar fronteira, Via B, ou fornecer nova evidência).
* **Se você é um humano:** Leia `/home/z/my-project/worklog.md` (Tasks 60-90, 2513+ linhas) para o registro completo. Leia `/home/z/my-project/download/AION-7.0.0-FG_GATE.md` para o gate formal. Leia `https://github.com/TCR-QDT/AION-6.x-Provenance-Register` para o Provenance Register.
* **Tom de voz:** Parceiro intelectual, curador técnico, cirúrgico na metodologia, respeitando o tempo e o trabalho intelectual do autor.
* **Princípio operacional:** Cada nova tecnologia precisa provar que merece ocupar espaço no AION. A ausência de evidência não é evidência de ausência. A compatibilidade de conteúdo não equivale a autenticação histórica.

---

## 14. ARQUIVOS PRINCIPAIS

| Caminho | Conteúdo |
|---|---|
| `/home/z/my-project/worklog.md` | Worklog completo (Tasks 60-90, 2513+ linhas) |
| `/home/z/my-project/download/AION-7.0.0_PROTOCOL.md` | Protocolo 7.0.0 (FROZEN FINAL) |
| `/home/z/my-project/download/AION-7.0.0-FG_GATE.md` | Formal Execution Gate v3 (FROZEN FINAL) |
| `/home/z/my-project/download/AION-7.0.0-R_AUDIT.md` | Audit Protocol (FROZEN) |
| `/home/z/my-project/download/AION-EVIDENCE-LEDGER-001_SCHEMA.md` | Ledger Schema (FROZEN) |
| `/home/z/my-project/download/AION-7.0.0-R0.5_EP_TRANSITION_GATE.md` | EP Transition Gate (R0.5 final) |
| `/home/z/my-project/download/AION-6.x-Provenance-Register.tar.gz` | tar.gz para deployment GitHub |
| `/home/z/my-project/intake/external_repositories/Coerencia_Relacional/` | TCR/QDT repo capturado |
| `/home/z/my-project/intake/external_repositories/AION-6.x-Provenance-Register/` | Provenance Register local (com commit) |
| `/home/z/my-project/intake/aion-6x-provenance-prep/` | Pacote DRAFT para deployment |
| `https://github.com/TCR-QDT/AION-6.x-Provenance-Register` | Provenance Register no GitHub |
| `https://github.com/TCR-QDT/Coerencia_Relacional` | Repositório TCR/QDT no GitHub |

---

## 15. ESTADO CANÔNICO FINAL

```text
╔══════════════════════════════════════════════════════════════╗
║              AION-7.0.0 — CANONICAL STATE                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Specification ............... FROZEN FINAL                  ║
║  FG v3 ........................ FROZEN FINAL                  ║
║  R_AUDIT ...................... FROZEN                        ║
║  Ledger Schema ................. FROZEN                        ║
║                                                              ║
║  H-ECB ......................... FROZEN                        ║
║  H-EPISTEMIC ................... FROZEN                        ║
║  Interventions ................. NONE                          ║
║                                                              ║
║  R0 (PHASE) ................... PARTIALLY REOPENED            ║
║    R0.1-R0.5 .................. CONCLUÍDOS                    ║
║    R0 (closure) ............... DECLARED (Task 78)            ║
║    R0.3.3-R0.3.3.A.2.4.A.2 ... CONCLUÍDOS                     ║
║    Task 88 AUDIT .............. P1 ✓, P2 ✓, P3 ✗ (frozen)    ║
║    Task 89 RECOVERY ........... 4/4 AUSENTE                    ║
║    Task 90 BOUNDARY ........... RECOVERY EXHAUSTED              ║
║                                NO RETROACTIVE CLAIM            ║
║                                CASE D PRESERVED                ║
║                                                              ║
║  Provenance Register ......... POPULATED (GitHub, commit       ║
║                                83b75ec, 2026-08-23)           ║
║  GitHub discrepancy .......... NON-OBSERVED / UNRECONCILED    ║
║                                                              ║
║  Provenance Boundary ......... FORMALLY DECLARED              ║
║    P1 Documentary Integrity .. ✓ RESOLVED                     ║
║    P2 Incorporation Provenance  ✓ RESOLVED                     ║
║    P3 Historical AION-6.x ..... ✗ INSUFFICIENT                ║
║                                  NOT RECOVERABLE               ║
║                                                              ║
║  C-01 (CORPUS-002) ........... CASE D (CONGELADO)             ║
║  C-02 (CORPUS-006) ........... CASE D (CONGELADO)             ║
║                                                              ║
║  EP (Grupo C) ................. EP-1 PARTIAL CANDIDATE /      ║
║                                Caso D (CONGELADO)              ║
║  EP (Grupo A, B, D) .......... EP-0 UNKNOWN                    ║
║                                                              ║
║  AUTH₇.₀ ..................... FALSE                           ║
║  ENV ......................... BLOCKED                         ║
║  PIPE ........................ NOT RUN                         ║
║  V1-V4 ....................... BLOCKED                         ║
║  NOMOD ....................... PENDING                         ║
║  FINAL_AUTH₇.₀ ............... BLOCKED                         ║
║                                                              ║
║  BASELINE 7.0.0 .............. NOT AUTHORIZED                  ║
║                                                              ║
║  NEXT EVENT:                 Determinação do                  ║
║                             Projetista Master                 ║
║                             (aceitar fronteira,               ║
║                              Via B, ou nova                   ║
║                              evidência externa)               ║
╚══════════════════════════════════════════════════════════════╝
```

---

*"Nenhuma memória sem proveniência. Nenhuma inferência confundida com evidência. Nenhuma limitação experimental transformada em propriedade permanente do sistema. A fronteira entre o que foi demonstrado, o que foi corroborado, e o que não pode ser demonstrado — é, ela própria, um resultado epistêmico válido."*

**Fim do Documento de Handoff — AION-7.0.0.**
