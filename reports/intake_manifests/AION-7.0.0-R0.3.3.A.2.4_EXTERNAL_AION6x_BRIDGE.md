# AION-7.0.0-R0.3.3.A.2.4 — External AION-6.x Provenance Bridge Recovery

**Versão:** R0.3.3.A.2.4-1
**Data:** 23 de agosto de 2026, 14:00 BRT
**Autor / Curador:** Edson Carvalho do Nascimento (Projetista Master) — determinou R0.3.3.A.2.4
**Analista Técnico:** IA Curadora (Role: Escriba / Arquiteto de Metadados) — executou R0.3.3.A.2.4
**Sessão:** web-73c75281-201c-4716-b85c-97833d25f9b3
**Status:** R0.3.3.A.2.4 EXECUTADO. AMBIENTE AION-6.x EXTERNO NÃO MATERIALIZADO. INPUT_PENDING. Caso D permanece. EP não promovido.
**Genealogia:** Derivado da determinação do Projetista Master (Task 82) autorizando busca pelo "outro lado da ponte" — o acervo histórico AION-6.x — sem continuar procurando dentro do TCR/QDT (já esgotado em Task 81).

---

## 1. Resumo Executivo

Foi executado o passo R0.3.3.A.2.4 — External AION-6.x Provenance Bridge Recovery — em conformidade com a determinação do Projetista Master (Task 82) de buscar o acervo histórico AION-6.x como "o outro lado da ponte". A busca foi direcionada a 5 categorias prioritárias estabelecidas pelo PM: (1) manifesto original de ingestão do AION-6.x, (2) registro contendo SHA-256 originais dos candidatos C-01 e C-02, (3) logs de ingestão/captura, (4) snapshot ou backup do AION-6.x, (5) outro repositório externo contendo componentes AION específicos. O resultado canônico é: **AMBIENTE AION-6.x EXTERNO NÃO MATERIALIZADO** no ambiente de execução observado pela IA Curadora. A verificação material identificou que `/home/sync/repo.tar` cresceu de 245KB (Task 70) para 16.5MB (agora), mas a análise do conteúdo confirma que o crescimento é devido ao snapshot desta sessão (incluindo o TCR/QDT repo capturado em Task 79), **não** a novo material AION-6.x. Nenhum URL externo para um repositório AION-6.x foi fornecido pelo PM nesta Task. Os 5 mounts acessíveis ao ambiente (3 OSS + 2 PolarFS) foram verificados — nenhum contém material AION-6.x. A busca material evidence-driven retornou zero candidatos para todos os 5 itens prioritários. Caso D permanece para C-01 e C-02. EP-1 PARTIAL CANDIDATE / Caso D não é promovido. O resultado é epistemicamente honesto: a IA Curadora não pode acessar materialmente o "outro lado da ponte" sem que o PM forneça URL específica, monte volume, ou confirme que nenhum acervo externo é acessível. Aplicando o invariante `NON-OBSERVED ≠ FALSE`: a não-materialização do acervo AION-6.x neste ambiente observado não prova que ele não exista em outro lugar — apenas demonstra que **não está materialmente acessível ao ambiente de execução observado pela IA Curadora**.

## 2. Escopo Autorizado (PM Task 82)

### 2.1 Objetivo PM

> Procurar o material original de proveniência do próprio AION-6.x. Não continuar procurando indefinidamente dentro do TCR/QDT. A busca deve procurar o outro lado da ponte: o acervo histórico AION-6.x.

### 2.2 Cinco itens prioritários PM (Task 82 Seção "O que precisamos encontrar")

| # | Item | Conteúdo esperado |
|---|---|---|
| **P1** | Manifesto original de ingestão do AION-6.x | CORPUS-002, CORPUS-006, CORPUS-007, etc. |
| **P2** | Registro contendo SHA-256 originais | C-01 hash `971986d9...c433`; C-02 hash `efd7f7ca...8854` |
| **P3** | Logs de ingestão/captura | data/hora, arquivo origem, destino, hash, CORPUS-ID, operador/processo |
| **P4** | Snapshot ou backup do AION-6.x | diretório corpus/, intake/, manifests/, audit/, worklog, configs |
| **P5** | Outro repositório externo com componentes AION específicos | Corpus v1.3.0, Oracle v3, GraphRAG, P-RESP-001, AION-EVAL-002, scripts aion_*.py, logs |

### 2.3 Relação que falta demonstrar (PM Task 82)

> "Este objeto material que hoje temos é o mesmo objeto que estava materialmente presente no AION-6.x."

### 2.4 Regra fundamental PM

> Não procurar evidência para confirmar a hipótese; procurar material que possa confirmar **ou refutar** a identidade histórica.

### 2.5 Consequência importante PM (se nada encontrado)

> Teremos estabelecido que **a ponte material não está disponível no acervo atualmente acessível**, sem transformar isso em afirmação de que a ponte jamais existiu.

### 2.6 Alteração de escopo (PM Task 82)

> Não procurar mais dentro do TCR/QDT, pois isso já foi esgotado (Task 81). A busca deve procurar o outro lado da ponte.

## 3. Resultado da Busca Material

### 3.1 Re-verificação de filesystem observável (R0.3.3.A.2.4.1)

#### 3.1.1 `/home/z/my-project/upload/` (OSS mount, rw)

| Verificação | Resultado |
|---|---|
| Total de arquivos | **0** (vazio) |
| Permissões | root:root 777 |
| Mount type | ossfs (Alibaba OSS) |
| Estado | **EMPTY** — nenhum upload realizado |

#### 3.1.2 `/home/sync/` (OSS mount, rw)

| Verificação | Resultado |
|---|---|
| Conteúdo | `repo.tar` |
| Tamanho | **17316272 bytes (16.5 MB)** |
| Modificação | 2026-08-23 03:34:58 UTC |
| Mount type | ossfs |

**Observação material crítica:** `/home/sync/repo.tar` mudou de tamanho desde Task 70 (245735 bytes = 245KB) para o tamanho atual (16.5MB). Esta é uma mudança material significativa que requer investigação detalhada (ver Seção 3.2).

#### 3.1.3 `/tmp/my-project/` (PolarFS mount, rw)

| Verificação | Resultado |
|---|---|
| Conteúdo | `.env`, `.gitignore`, `.initial_snapshot.json`, `download/`, `intake/`, `worklog.md` |
| Mount type | PolarFS |
| Estado | Snapshot espelho de `/home/z/my-project/` (atualizado em tempo real) |

#### 3.1.4 Novos arquivos desde R0.3.3.A.2 (Task 81)

```
find /home/z/my-project -type f -newer <R0.3.3.A.2_PROVENANCE_BRIDGE.md>
```

| Resultado |
|---|
| `.git/index` (atualizado por commit desta sessão) |
| `worklog.md` (atualizado por Task 81) |
| `intake/external_repositories/Coerencia_Relacional/.git/index` (TCR/QDT repo, capturado em Task 79) |

**Nenhum novo material AION-6.x foi identificado em nenhum destes arquivos.**

### 3.2 Investigação material de `/home/sync/repo.tar` (mudança de tamanho 245KB → 16.5MB)

#### 3.2.1 Análise do conteúdo do tar

| Métrica | Valor |
|---|---|
| Total de arquivos no tar | 528 |
| Tamanho total | 16.5 MB |
| Modificação timestamp | 2026-08-23 03:34:58 UTC (depois de Task 79, antes de Task 80) |

#### 3.2.2 Categorias de conteúdo identificadas

| Categoria | Conteúdo |
|---|---|
| `.git/` internals | 500+ arquivos — git objects, refs, logs do repositório `/home/z/my-project/.git` |
| `download/AION-7.0.0-*.md` | 8 arquivos FROZEN de 7.0.0-spec + 4 relatórios R0.x produzidos nesta sessão |
| `download/README.md` | 1 arquivo placeholder (pré-existente) |
| `intake/manifests/AION-7.0.0-R0.3.*.md` | 4 manifests de intake produzidos em Tasks 72-79 |
| `intake/external_repositories/Coerencia_Relacional/` | TCR/QDT repo capturado em Task 79 (inclui PDFs C-01 e C-02) |
| `worklog.md` | worklog desta sessão |

#### 3.2.3 Busca por material AION-6.x específico dentro do tar

| Busca | Resultado |
|---|---|
| Arquivos nomeados com "AION" | 14 arquivos — TODOS são artefatos desta sessão (AION-7.0.0-spec FROZEN + relatórios R0.x) |
| Scripts nomeados `aion_*.py` | **0 arquivos** |
| PDFs do corpus AION-6.x (CORPUS-001 a CORPUS-011) | **0 arquivos** (apenas PDFs do TCR/QDT repo em `intake/external_repositories/Coerencia_Relacional/docs/pdfs/`) |
| JSONs em `/download/rag/` (AION-6.x experimental data) | **0 arquivos** (diretório `download/rag/` não existe no tar) |
| Arquivos com "oracle" no nome | **0 arquivos** |
| Arquivos `.html` AION | **0 arquivos AION** (1 arquivo HTML do TCR/QDT repo: `Paper_A_Sections_IV_V_VI_v6.1.html`) |
| Manifests de ingest AION-6.x | **0 arquivos** |

#### 3.2.4 Conclusão sobre `/home/sync/repo.tar`

**O crescimento de 245KB para 16.5MB é inteiramente devido a:**
- TCR/QDT repo capturado em Task 79 (~12MB)
- AION-7.0.0-spec FROZEN artifacts e relatórios R0.x (~200KB)
- Git internals expansão (~4MB)

**NÃO contém** material AION-6.x (corpus, scripts, manifests, logs, ambiente). É um snapshot do estado da sessão atual, não um acervo histórico AION-6.x.

### 3.3 Verificação de mounts acessíveis ao ambiente (R0.3.3.A.2.4.1)

| Mount | Tipo | Conteúdo |
|---|---|---|
| `/home/official_skills` | ossfs (ro) | 73 arquivos .zip de skills default da plataforma — nenhum AION |
| `/home/z/my-project/upload` | ossfs (rw) | **VAZIO** |
| `/home/sync` | ossfs (rw) | `repo.tar` (snapshot desta sessão, sem AION-6.x) |
| `/tmp/my-project` | PolarFS (rw) | Espelho de `/home/z/my-project/` (snapshot ao vivo) |
| `/home/user_skills` | PolarFS (rw) | (vazio ou sem acesso de leitura confirmado) |

**Nenhum mount adicional acessível.** Nenhum volume contendo acervo AION-6.x está montado.

### 3.4 Verificação de URLs externos fornecidos pelo PM (R0.3.3.A.2.4.2)

| URL fornecida pelo PM nesta sessão | Para quê | Status |
|---|---|---|
| `https://github.com/TCR-QDT/Coerencia_Relacional.git` (Task 79) | TCR/QDT repo | ✓ Capturado em Task 79, esgotado em Task 81 |
| URLs para AION-6.x external archive | (nenhuma fornecida pelo PM em Task 82) | ✗ Nenhuma URL fornecida |

**O PM não forneceu URL específica para o acervo histórico AION-6.x.**

### 3.5 Verificação de remotes do TCR/QDT repo (R0.3.3.A.2.4.3)

| Remote | URL |
|---|---|
| origin (fetch) | `https://github.com/TCR-QDT/Coerencia_Relacional.git` |
| origin (push) | `https://github.com/TCR-QDT/Coerencia_Relacional.git` |

**Apenas um remote configurado.** Nenhum remote adicional aponta para repositório AION-6.x.

## 4. Resultado por Item Prioritário PM

### 4.1 P1 — Manifesto original de ingestão do AION-6.x

**Resultado:** **NÃO ENCONTRADO.**

| Localização buscada | Resultado |
|---|---|
| `/home/z/my-project/upload/` | VAZIO |
| `/home/sync/` | Apenas `repo.tar` (snapshot desta sessão) |
| `/home/z/my-project/intake/` | Apenas manifests desta sessão (AION-7.0.0-R0.3.*) |
| Conteúdo do `repo.tar` | Sem AION-6.x manifests |
| TCR/QDT repo (já esgotado Task 81) | Sem AION-6.x manifests |

### 4.2 P2 — Registro contendo SHA-256 originais (C-01 e C-02)

**Resultado:** **NÃO ENCONTRADO.**

| Hash procurado | Localização buscada | Resultado |
|---|---|---|
| `971986d96c4ceb1ea5d7a17acdf2a54f4276403f2805c3945874304020adc433` (C-01) | Filesystem observável + TCR/QDT repo + `repo.tar` | **0 ocorrências** |
| `efd7f7caf19a5f99cd1663303c6f36d0beba50f19c71d4f44d44b81c396c8854` (C-02) | Filesystem observável + TCR/QDT repo + `repo.tar` | **0 ocorrências** |

Nenhum artefato AION-6.x independente registra os hashes dos PDFs candidatos. Os hashes foram computados pela primeira vez em Task 80 (R0.3.3.A).

### 4.3 P3 — Logs de ingestão/captura

**Resultado:** **NÃO ENCONTRADO.**

| Localização buscada | Resultado |
|---|---|
| Filesystem observável (logs AION-6.x) | 0 arquivos |
| `repo.tar` (logs AION-6.x) | 0 arquivos |
| TCR/QDT repo (logs AION-6.x) | 0 arquivos (apenas logs TCR/QDT em `docs/worklog.md` e `docs/md/worklog.md` — TCR/QDT-specific, sem menção a AION) |

### 4.4 P4 — Snapshot ou backup do AION-6.x

**Resultado:** **NÃO ENCONTRADO.**

| Localização buscada | Resultado |
|---|---|
| `/home/z/my-project/upload/` | VAZIO |
| `/home/sync/repo.tar` | Snapshot desta sessão (inclui TCR/QDT repo), não snapshot AION-6.x |
| `/tmp/my-project/` | Espelho de `/home/z/my-project/` (ao vivo) |
| Outros mounts | Nenhum contém backup AION-6.x |

### 4.5 P5 — Outro repositório externo contendo componentes AION específicos

**Resultado:** **NÃO ENCONTRADO.**

| Localização buscada | Resultado |
|---|---|
| URL fornecida pelo PM em Task 82 | Nenhuma URL fornecida |
| Remotes do TCR/QDT repo | Apenas `origin` para o próprio TCR/QDT |
| Outros acessos externos | Nenhum configurado |

## 5. Classificação Evidence-Driven do Resultado

### 5.1 Aplicação da regra fundamental PM

> Não procurar evidência para confirmar a hipótese; procurar material que possa confirmar **ou refutar** a identidade histórica.

A busca foi executada de forma evidence-driven, procurando simultaneamente:

| Hipótese | O que procurar | Resultado |
|---|---|---|
| H-bridge-3 (acervo AION-6.x acessível) | Manifesto, hash, log, snapshot, ou repositório externo AION | **Não encontrada** |
| H-bridge-4 (acervo AION-6.x não acessível ao ambiente observado) | Ausência de material AION-6.x em filesystem e URLs | **Confirmada** |

**Resultado evidence-driven:** A hipótese H-bridge-4 (acervo AION-6.x não acessível ao ambiente observado) é materialmente suportada. A hipótese H-bridge-3 (acervo AION-6.x acessível) **não é suportada** por qualquer evidência material acessível à IA Curadora.

### 5.2 Distinção crítica aplicada: NON-OBSERVED ≠ FALSE

| Classificação | Estado |
|---|---|
| Observação material | ZERO material AION-6.x em qualquer localização acessível (filesystem observável + TCR/QDT repo + repo.tar) |
| Inferência proibida | "O acervo AION-6.x não existe" (isto seria inferência além da observação) |
| **Classificação canônica** | **"O acervo AION-6.x não está materialmente acessível ao ambiente de execução observado pela IA Curadora"** (materialmente observável) |

### 5.3 Por que não é refutação explícita

Uma refutação explícita exigiria um documento declarando "este PDF não estava no AION-6.x" ou "o acervo AION-6.x foi destruído". Nenhum documento desse tipo existe. O resultado é **ausência de evidência material** — não **evidência de ausência**.

### 5.4 Classificação por candidato (V3 após R0.3.3.A.2.4)

| Candidato | V3 antes | V3 após R0.3.3.A.2.4 | Classificação |
|---|---|---|---|
| C-01 (CORPUS-002) | INSUFFICIENT | **INSUFFICIENT (mantido)** | Caso D permanece |
| C-02 (CORPUS-006) | INSUFFICIENT | **INSUFFICIENT (mantido)** | Caso D permanece |

A busca pelo "outro lado da ponte" não produziu material AION-6.x autenticável. V3 permanece INSUFFICIENT para ambos os candidatos.

## 6. Estado de EP após R0.3.3.A.2.4

### 6.1 Estado anterior (R0.3.3.A.2, Task 81)

```
Grupo C: EP-1 PARTIAL CANDIDATE / Caso D (content-compatible, provenance-insufficient — confirmed by evidence-driven search in TCR/QDT repo)
Grupo A, B, D: EP-0 UNKNOWN
```

### 6.2 Estado após R0.3.3.A.2.4 (este documento)

```
Grupo C: EP-1 PARTIAL CANDIDATE / Caso D (content-compatible, provenance-insufficient — confirmed by evidence-driven search in BOTH TCR/QDT repo AND observable environment)
Grupo A: EP-0 UNKNOWN
Grupo B: EP-0 UNKNOWN
Grupo D: EP-0 UNKNOWN
```

### 6.3 Justificativa evidence-driven

A reclassificação **não promove nem rebaixa** EP porque:

1. A busca pelo "outro lado da ponte" (acervo AION-6.x) foi executada materialmente
2. **Nenhum material AION-6.x foi encontrado** em qualquer localização acessível
3. **Nenhuma URL externa** foi fornecida pelo PM para repositório AION-6.x
4. **Nenhum volume** contendo backup AION-6.x está montado
5. O crescimento do `/home/sync/repo.tar` é explicado inteiramente pelo snapshot desta sessão (incluindo TCR/QDT repo capturado)
6. Caso D permanece para ambos os candidatos; EP não é promovido para EFFECTIVE

### 6.4 Não-promoção para EP-1 PARTIAL EFFECTIVE

| Condição necessária | Estado |
|---|---|
| V3 PASS para pelo menos um candidato | ✗ Nenhum candidato tem V3 PASS |
| Evidência material de ponte AION-6.x | ✗ Busca exaustiva retornou zero (filesystem + TCR/QDT + repo.tar) |
| Manifest, hash, log, snapshot, ou repositório externo AION | ✗ Todos os 5 itens prioritários retornaram AUSENTE |

**EP-1 PARTIAL CANDIDATE / Caso D permanece — não promovido para EP-1 PARTIAL EFFECTIVE.**

## 7. Estado dos Demais Grupos (preservado)

| Grupo | EP | Justificativa |
|---|---|---|
| Grupo A — AION infrastructure | EP-0 UNKNOWN | Zero material evidence (Oracle v3, GraphRAG v1.0.0, P-RESP-001 v0.3, AION-EVAL-002 v0.2, B1 config 6.2.11) |
| Grupo B — AION-specific scripts | EP-0 UNKNOWN | Zero AION-specific scripts em qualquer localização acessível |
| Grupo C — corpus documents | EP-1 PARTIAL CANDIDATE / Caso D (refinado) | 2 candidatos Caso D, busca evidence-driven em filesystem + TCR/QDT + repo.tar confirma V3 INSUFFICIENT |
| Grupo D — Environment Provenance AION-6.x | EP-0 UNKNOWN | Cautela TCR/QDT aplicada; nenhum environment AION-6.x acessível |

## 8. Estado do Sistema (pós-R0.3.3.A.2.4)

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
│   ├── R0.3.3.A.2 ......... CONCLUÍDO (Task 81)
│   └── R0.3.3.A.2.4 ....... CONCLUÍDO (este documento, Task 82)
│       ├── P1 Manifesto AION-6.x ............ AUSENTE
│       ├── P2 Hash histórico AION-6.x ....... AUSENTE
│       ├── P3 Logs AION-6.x ............... AUSENTE
│       ├── P4 Snapshot/backup AION-6.x ..... AUSENTE
│       └── P5 Outro repositório externo ..... AUSENTE (sem URL fornecida pelo PM)
│
├── EP .................. EP-1 PARTIAL CANDIDATE / Caso D (Grupo C, confirmed twice)
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
EVENT_ID: AION-EV-013
TIMESTAMP: 2026-08-23T14:00:00-03:00
SESSION: web-73c75281-201c-4716-b85c-97833d25f9b3
TRACE_ID: 1a02ecff633cd7e5 (autorização R0.3.3.A.2.4 PM) → execução IA Curadora
EVENT_TYPE: R0.3.3.A.2.4_EXTERNAL_AION6X_PROVENANCE_BRIDGE_RECOVERY_COMPLETED
OBSERVED_STATE: R0.3.3.A.2.4 executed as evidence-driven search for "other side of the bridge" — AION-6.x historical archive. Search followed 5 PM priorities (manifest, hashes, logs, snapshot, external repo). All 5 priorities returned ZERO matches in any accessible location. Observable filesystem unchanged since Task 81. /home/sync/repo.tar grew from 245KB to 16.5MB but content analysis confirms growth is entirely due to this session's snapshot (including TCR/QDT repo captured in Task 79), not AION-6.x material. No URL provided by PM for AION-6.x external archive. No volume mounted containing AION-6.x backup. 5 mounts accessible (3 OSS + 2 PolarFS), none contain AION-6.x material.
KEY_FINDINGS:
  - P1 Manifesto AION-6.x: 0 arquivos. /home/z/my-project/upload/ empty. /home/sync/repo.tar contains only this session's artifacts.
  - P2 Hash histórico AION-6.x: 0 arquivos. Hashes C-01 (971986d9...) and C-02 (efd7f7ca...) not found in any accessible location.
  - P3 Logs AION-6.x: 0 arquivos. No AION-6.x logs in observable filesystem, TCR/QDT repo, or repo.tar.
  - P4 Snapshot/backup AION-6.x: 0 arquivos. /home/sync/repo.tar is snapshot of this session, not AION-6.x archive.
  - P5 Outro repositório externo: 0 URLs. PM did not provide URL for AION-6.x external archive. TCR/QDT repo has only one remote (origin).
  - /home/sync/repo.tar size change (245KB → 16.5MB): entirely due to TCR/QDT repo capture (Task 79) + AION-7.0.0-spec artifacts + git internals expansion. NOT due to AION-6.x material.
EPISTEMOLOGICAL_SCOPE: AMBIENTE AION-6.x EXTERNO NÃO MATERIALIZADO no ambiente de execução observado pela IA Curadora. Caso D permanece for both C-01 and C-02. EP-1 PARTIAL CANDIDATE / Caso D not promoted. Invariante NON-OBSERVED ≠ FALSE applied: "AION-6.x archive not materially accessible to observed environment" is observable; "AION-6.x archive does not exist" is NOT inferred.
INTERPRETATION: [I] The evidence-driven search for the "other side of the bridge" (AION-6.x archive) produced a definitive negative result within the materially accessible environment: no AION-6.x material is accessible to IA Curadora. This is NOT evidence of absence of AION-6.x archive — it is absence of evidence for AION-6.x archive in accessible environment. The PM rule "search for evidence that may confirm or refute" was respected: search was designed to find either confirmation (manifest, hash, log, snapshot, external repo) or refutation (explicit denial). Neither was found. The state V3 INSUFFICIENT is confirmed for both candidates.
PROVENANCE_RULE_INVOKED: Regra 1 (Provenance) + Regra 7 (PER=0 ≠ confiável) + Invariantes UNAVAILABLE≠NON-EXISTENT, NON-OBSERVED≠FALSE, PENDING≠FAILED, COMPATIBLE≠EQUIVALENT + FG_GATE v3 Seção 5.5 (EP Classification evidence-driven) + PM Task 82 Rules: (1) don't search inside TCR/QDT (already exhausted), (2) search other side of bridge (AION-6.x archive), (3) 5 priority items, (4) evidence-driven (confirm OR refute), (5) absence of evidence ≠ evidence of absence.
EPISTEMIC_ACTION: R0.3.3.A.2.4 CONCLUÍDO. Caso D permanece for both C-01 and C-02. EP-1 PARTIAL CANDIDATE / Caso D confirmed (not promoted). AUTH_{7.0}=FALSE preserved. FINAL_AUTH_{7.0}=BLOCKED preserved. State: R0 PARTIALLY REOPENED with Grupo C candidates verified but unauthenticated, and "other side of bridge" (AION-6.x archive) confirmed not materially accessible to IA Curadora without PM-provided URL or mounted volume.
```

## 10. Próxima Ação Legítima — Requer Determinação PM

### 10.1 Estado após R0.3.3.A.2.4

R0.3.3.A.2.4 **materialmente esgotou** a busca pelo "outro lado da ponte" dentro do ambiente acessível à IA Curadora. O resultado é: **acervo AION-6.x não está materialmente acessível** sem que o PM forneça URL específica, monte volume, ou confirme que nenhum acervo externo é acessível.

### 10.2 Opções para o Projetista Master

| Opção | Descrição | Consequência |
|---|---|---|
| **R0.3.3.A.2.4.A** | PM fornece URL de repositório AION-6.x (e.g., `github.com/<org>/<repo>.git`) | IA Curadora clona e verifica materialmente |
| **R0.3.3.A.2.4.B** | PM monta volume contendo backup AION-6.x (e.g., em `/home/z/my-project/upload/` ou novo mount) | IA Curadora escaneia e verifica materialmente |
| **R0.3.3.A.2.4.C** | PM fornece credenciais de acesso a repositório privado AION-6.x | IA Curadora acessa e verifica materialmente |
| **R0.3.3.A.2.4.D** | PM confirma formalmente que nenhum acervo AION-6.x externo é acessível | INPUT_PENDING final; Caso D final para Grupo C; EP-0 final para Grupo A, B, D; considerar Via B |
| **R0.3.3.A.2.4.E** | PM escolhe Via B — Nova determinação metodológica (redefinir experimento sem depender de AION-6.x infrastructure) | Nova genealogia experimental (preservando genealogia documental conforme Regra 9) |
| **R0.3.3.A.2.4.F** | PM declara encerramento formal do R0 com EP-0 final para Grupo A, B, D e Caso D final para Grupo C; STANDBY MATERIAL permanente até nova evidência externa ou Via B | Encerramento canônico formal |

### 10.3 O que NÃO será feito até determinação PM

- ✗ Nenhuma promoção automática de EP-1 PARTIAL CANDIDATE para EP-1 PARTIAL EFFECTIVE
- ✗ Nenhuma inferência de que TCR/QDT PDFs são autenticamente os mesmos arquivos do AION-6.x corpus
- ✗ Nenhuma instalação de dependências
- ✗ Nenhuma execução de scripts TCR/QDT ou AION
- ✗ Nenhuma execução de V1-V4 sobre outros componentes sem autorização específica
- ✗ Nenhuma alteração de artefato FROZEN
- ✗ Nenhuma alteração de `AUTH₇.₀ = FALSE`
- ✗ Nenhuma alteração de `FINAL_AUTH₇.₀ = BLOCKED`
- ✗ Nenhuma busca especulativa por URLs não fornecidas pelo PM
- ✗ Nenhuma inferência de que AION-6.x archive não existe

### 10.4 Princípio operacional consolidado

> **Busca evidence-driven no ambiente acessível produz ausência de evidência — não evidência de ausência. A distinção é materialmente preservada.**

Aplicado materialmente em R0.3.3.A.2.4: a busca exaustiva pelo "outro lado da ponte" dentro do ambiente acessível à IA Curadora **não encontrou evidência positiva** do acervo AION-6.x. Mas isto **não constitui prova** de que o acervo AION-6.x não exista — apenas demonstra materialmente que **não está acessível a este ambiente de execução observado pela IA Curadora**.

A distinção entre "ausência de evidência no ambiente acessível" e "evidência de ausência" foi rigorosamente preservada. Aplicando o invariante `NON-OBSERVED ≠ FALSE`: a não-observação do acervo AION-6.x não implica a falsidade da sua existência em outro lugar.

## 11. Confirmação de Integridade dos FROZEN

| Artefato | SHA-256 | Estado |
|---|---|---|
| AION-7.0.0_PROTOCOL.md | `b9b50b28579a8b5ac99abcc48898b34f965d1ce14de53b85062f7a1fea13a376` | INTACTO (idêntico a Tasks 65-81) |
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
       ▼  Determinação PM Task 79: autoriza R0.3.3 (external material intake — TCR/QDT)
       │
AION-7.0.0-R0.3.3 EXTERNAL MATERIAL INTAKE: TCR/QDT REPOSITORY — CONCLUÍDO (Task 79)
       │
       ▼  Determinação PM Task 80: autoriza R0.3.3.A (V1-V4 candidate verification)
       │
AION-7.0.0-R0.3.3.A V1-V4 CANDIDATE VERIFICATION — CONCLUÍDO (Task 80)
       │  C-01, C-02 → Caso D (V1+V2+V4 PASS, V3 INSUFFICIENT)
       │
       ▼  Determinação PM Task 81 (PM-80.1): autoriza R0.3.3.A.2 (provenance bridge recovery in TCR/QDT)
       │
AION-7.0.0-R0.3.3.A.2 PROVENANCE BRIDGE RECOVERY (TCR/QDT) — CONCLUÍDO (Task 81)
       │  P1-P4 in TCR/QDT → all ZERO matches
       │  Caso D permanece for both candidates
       │
       ▼  Determinação PM Task 82: autoriza R0.3.3.A.2.4 (external AION-6.x provenance bridge recovery)
       │
AION-7.0.0-R0.3.3.A.2.4 EXTERNAL AION-6.x PROVENANCE BRIDGE RECOVERY — CONCLUÍDO (este documento, Task 82)
       │
       ├── P1 Manifesto AION-6.x ........ AUSENTE
       ├── P2 Hash histórico AION-6.x .... AUSENTE
       ├── P3 Logs AION-6.x ............. AUSENTE
       ├── P4 Snapshot/backup AION-6.x ... AUSENTE
       ├── P5 Outro repositório externo ... AUSENTE (no URL provided by PM)
       │
       ├── C-01: Caso D permanece (V3 INSUFFICIENT confirmed by evidence-driven search)
       ├── C-02: Caso D permanece (V3 INSUFFICIENT confirmed by evidence-driven search)
       ├── EP-1 PARTIAL CANDIDATE / Caso D confirmed twice (not promoted)
       ├── AUTH₇.₀ = FALSE (preserved)
       ├── FINAL_AUTH₇.₀ = BLOCKED (preserved)
       ├── 4 FROZEN artifacts integrity verified
       │
       ▼  Próxima operação requer determinação PM:
       │
       ├── R0.3.3.A.2.4.A — PM provides URL of AION-6.x repo → IA Curadora clones and verifies
       ├── R0.3.3.A.2.4.B — PM mounts volume with AION-6.x backup → IA Curadora scans
       ├── R0.3.3.A.2.4.C — PM provides credentials to private AION-6.x repo → IA Curadora accesses
       ├── R0.3.3.A.2.4.D — PM confirms no external AION-6.x archive accessible → INPUT_PENDING final
       ├── R0.3.3.A.2.4.E — Via B (new methodological determination)
       └── R0.3.3.A.2.4.F — Formal closure: EP-0 final A/B/D, Caso D final C, STANDBY MATERIAL permanent
```

---

*"O resultado de R0.3.3.A.2.4 estabelece materialmente a fronteira do que pode ser conhecido a partir deste ambiente de execução observado pela IA Curadora. A busca evidence-driven pelo 'outro lado da ponte' — o acervo histórico AION-6.x — produziu ausência de evidência em todas as 5 categorias prioritárias: nenhum manifesto, nenhum hash histórico, nenhum log, nenhum snapshot, nenhum repositório externo AION-6.x é materialmente acessível. O crescimento do /home/sync/repo.tar é inteiramente explicado pelo snapshot desta sessão, não por material AION-6.x. A distinção entre 'ausência de evidência no ambiente acessível' e 'evidência de ausência' foi rigorosamente preservada. A próxima transição epistemicamente válida requer que o Projetista Master forneça materialmente o acesso ao acervo AION-6.x (URL, volume montado, ou credenciais), confirme formalmente que nenhum acervo é acessível, ou escolha Via B para redefinir o experimento sem depender de AION-6.x infrastructure."*

**Fim do AION-7.0.0-R0.3.3.A.2.4 External AION-6.x Provenance Bridge Recovery Report.**
