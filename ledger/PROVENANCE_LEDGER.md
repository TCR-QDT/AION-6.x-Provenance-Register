# Provenance Ledger

## Overview

This is the central provenance ledger for the AION-6.x Provenance Register. It records all material events related to the recovery, verification, and incorporation of historical documentation.

## Ledger entries

### LEDGER-001 — Repository initialization

| Field | Value |
|---|---|
| Entry ID | LEDGER-001 |
| Event type | REPOSITORY_INITIALIZATION |
| Date | 2026-08-23 |
| Repository URL | https://github.com/TCR-QDT/AION-6.x-Provenance-Register |
| Repository initial state | EMPTY |
| Authority | Projetista Master (Edson Carvalho do Nascimento, ORCID 0009-0003-5504-7439) |
| Operator | IA Curadora (Escriba / Arquiteto de Metadados) |
| Session | web-73c75281-201c-4716-b85c-97833d25f9b3 |
| Authorizing task | AION-7.0.0-R0.3.3.A.2.4.A.2 — PROVENANCE REGISTER INITIALIZATION |
| Retroactive authentication | NO |
| Historical reconstruction | NO |
| Corpus modification | NO |

### LEDGER-002 — Historical document incorporation (PR-001)

| Field | Value |
|---|---|
| Entry ID | LEDGER-002 |
| Event type | HISTORICAL_DOCUMENT_INCORPORATION |
| Date | 2026-08-23 |
| Document | MEMORIAS_DE_UMA_CONSTRUCAO.md |
| Original filename | MEMÓRIAS DE UMA CONSTRUÇÃO — A História do Pensamento, da Consciência e do Arquivo Vivo.md |
| Source | Provided by Projetista Master via /home/z/my-project/upload/ (OSS mount) |
| Source SHA-256 | `7549597b065e784c7baae3baca42049e23cc57937c610cfd2c4f23b242d2d9df` |
| Size | 25342 bytes |
| Lines | 1102 |
| Encoding | UTF-8 |
| Classification | HISTORICAL_RECORD |
| Epistemic status | NARRATIVE_CORROBORATION |
| Deployed path | evidence/historical/MEMORIAS_DE_UMA_CONSTRUCAO.md |
| Retroactive authentication | NO |
| Historical reconstruction | NO |
| Corpus modification | NO |

### LEDGER-003 — TCR/QDT bridge investigation result

| Field | Value |
|---|---|
| Entry ID | LEDGER-003 |
| Event type | BRIDGE_INVESTIGATION_RESULT |
| Date | 2026-08-23 |
| Bridge investigated | TCR/QDT → AION-6.x |
| Source side | github.com/TCR-QDT/Coerencia_Relacional (captured 2026-08-23) |
| Target side | AION-6.x corpus source (declared in AION-MVP-001 Handoff) |
| Candidates examined | C-01 (Paper_A_v6.2_FINAL.pdf ↔ CORPUS-002), C-02 (Paper_A_v6.1_REVTeX_COMPLETE.pdf ↔ CORPUS-006) |
| V1 Identity (both candidates) | ✓ PASS |
| V2 Integrity (both candidates) | ✓ PASS |
| V3 Provenance (both candidates) | ⚠ INSUFFICIENT |
| V4 Canonical Content (both candidates) | ✓ PASS |
| Classification (both candidates) | Caso D — content compatible, provenance insufficient |
| Bridge status | NOT_AUTHENTICATED |
| Retroactive authentication | NO |

### LEDGER-004 — AION-7.0.0 gate status (snapshot)

| Field | Value |
|---|---|
| Entry ID | LEDGER-004 |
| Event type | AION_7_0_0_GATE_SNAPSHOT |
| Date | 2026-08-23 |
| Specification | FROZEN FINAL (Task 68) |
| FG v3 | FROZEN FINAL (Task 68) |
| R0 phase | PARTIALLY REOPENED |
| Grupo A (AION infrastructure) | EP-0 UNKNOWN |
| Grupo B (AION-specific scripts) | EP-0 UNKNOWN |
| Grupo C (corpus documents) | EP-1 PARTIAL CANDIDATE / Caso D |
| Grupo D (Environment Provenance AION-6.x) | EP-0 UNKNOWN |
| AUTH₇.₀ | FALSE |
| ENV | BLOCKED |
| PIPE | NOT RUN |
| V1-V4 (other components) | BLOCKED |
| NOMOD | PENDING |
| FINAL_AUTH₇.₀ | BLOCKED |

## FROZEN artifacts integrity (snapshot)

| Artifact | SHA-256 |
|---|---|
| AION-7.0.0_PROTOCOL.md | `b9b50b28579a8b5ac99abcc48898b34f965d1ce14de53b85062f7a1fea13a376` |
| AION-EVIDENCE-LEDGER-001_SCHEMA.md | `1bf7349d621382a05f06f743b99e1ed632f804673199b444247b9afc4ddf3507` |
| AION-7.0.0-R_AUDIT.md | `d8efb8f4aee924f7c250a7e9726fdccdebcb6343440a8e1b8fb892c253ee1738` |
| AION-7.0.0-FG_GATE.md | `f082de51f96b144bf0cc98466db600581c3ce3f413fa38e3bf81f477c488e4e4` |

## Future evidence incorporation

When new material evidence becomes available, new ledger entries should be added with:

- Unique Entry ID (LEDGER-005, LEDGER-006, ...)
- Event type (e.g., MANIFEST_INCORPORATION, HASH_AUTHENTICATION, SNAPSHOT_RECOVERY)
- Date of incorporation
- Source of evidence
- SHA-256 of evidence artifact
- Re-evaluation of affected V3 classifications
- Updated bridge status (if applicable)

---

*"Este ledger registra materialmente todos os eventos de recuperação, verificação, e incorporação de documentação histórica. Cada entrada preserva a distinção entre data de incorporação e data dos eventos históricos. A inclusão de nova evidência deve seguir o mesmo princípio: registrar quando a evidência foi incorporada, não quando os eventos descritos ocorreram."*
