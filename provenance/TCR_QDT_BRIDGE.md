# TCR/QDT Bridge Status

## Bridge definition

The "TCR/QDT bridge" refers to a material connection between:

- **Source side:** TCR/QDT repository (`github.com/TCR-QDT/Coerencia_Relacional`, captured locally on 2026-08-23)
- **Target side:** AION-6.x corpus source (declared in AION-MVP-001 Handoff)

A bridge would be established if material evidence connects specific files in TCR/QDT to specific CORPUS-IDs in AION-6.x.

## Current status

```
BRIDGE STATUS: NOT AUTHENTICATED
```

## Evidence examined

### Source side (TCR/QDT)

| ID | Material | Location in TCR/QDT | SHA-256 | V1 | V2 | V3 | V4 |
|---|---|---|---|---|---|---|---|
| C-01 | `Paper_A_v6.2_FINAL.pdf` | `docs/pdfs/Paper_A_v6.2_FINAL.pdf` | `971986d96c4ceb1ea5d7a17acdf2a54f4276403f2805c3945874304020adc433` | ✓ PASS | ✓ PASS | ⚠ INSUFFICIENT | ✓ PASS |
| C-02 | `Paper_A_v6.1_REVTeX_COMPLETE.pdf` | `docs/pdfs/Paper_A_v6.1_REVTeX_COMPLETE.pdf` | `efd7f7caf19a5f99cd1663303c6f36d0beba50f19c71d4f44d44b81c396c8854` | ✓ PASS | ✓ PASS | ⚠ INSUFFICIENT | ✓ PASS |

### Target side (AION-6.x corpus source)

| ID | CORPUS-ID | Description (Handoff) | Materially accessible? |
|---|---|---|---|
| T-01 | CORPUS-002 | Paper A v6.2 (137KB, CURRENT/AUTHORITATIVE, 12/08/2026) | ✗ NOT MATERIALLY ACCESSIBLE |
| T-02 | CORPUS-006 | Paper A v6.1 oficial (138KB, HISTORICAL, 10/08/2026) | ✗ NOT MATERIALLY ACCESSIBLE |

## Bridge verification

For each candidate pair (C-01 ↔ CORPUS-002, C-02 ↔ CORPUS-006), the bridge requires:

1. **V1 Identity** — file metadata matches Handoff declaration
2. **V2 Integrity** — file is parseable, hash computable
3. **V3 Provenance** — material chain linking file to AION-6.x corpus source
4. **V4 Canonical Content** — content matches expected corpus content

### C-01 ↔ CORPUS-002

| Gate | Result | Notes |
|---|---|---|
| V1 | ✓ PASS | filename, size (137520 bytes ≈ 137KB EXACT MATCH), PDF metadata consistent with Handoff |
| V2 | ✓ PASS | SHA-256 `971986d9...` computable, PDF parseable |
| V3 | ⚠ INSUFFICIENT | chain to TCR/QDT confirmed; chain to AION-6.x corpus source NOT demonstrated |
| V4 | ✓ PASS | content matches `.tex` source in TCR/QDT and Handoff description |

**Classification:** Caso D — content compatible, provenance insufficient.

### C-02 ↔ CORPUS-006

| Gate | Result | Notes |
|---|---|---|
| V1 | ✓ PASS | filename, size (138780 bytes ≈ 138KB EXACT MATCH), PDF metadata consistent |
| V2 | ✓ PASS | SHA-256 `efd7f7ca...` computable, PDF parseable |
| V3 | ⚠ INSUFFICIENT | chain to TCR/QDT confirmed; chain to AION-6.x corpus source NOT demonstrated |
| V4 | ✓ PASS | content matches `.tex` source and Handoff description |

**Classification:** Caso D — content compatible, provenance insufficient.

## What would establish the bridge

The bridge would be established if any of the following material evidence becomes available:

1. **Manifest of AION-6.x ingestion** declaring `CORPUS-002 ↔ hash 971986d9... ↔ Paper_A_v6.2_FINAL.pdf` (or equivalent for CORPUS-006)
2. **Independent historical hash** registered in an AION-6.x artifact predating this recovery
3. **Log of transfer** TCR/QDT → AION-6.x (or reverse)
4. **Snapshot of AION-6.x environment** containing the file with matching hash
5. **Alternative Git repository** containing AION-6.x infrastructure with verifiable reference to these hashes

## What would NOT establish the bridge

The following do NOT establish the bridge:

- Narrative corroboration (e.g., `MEMORIAS_DE_UMA_CONSTRUCAO.md` mentions `CORPUS-002#chunk_001`)
- Textual description in the Handoff
- Authorship overlap (Edson Carvalho do Nascimento is author of both TCR/QDT and AION-MVP-001)
- Temporal consistency (TCR/QDT commit on 13/08/2026 is 1 day after AION corpus consolidation declared on 12/08/2026)
- Filename similarity

## Status history

| Date | Event | Status |
|---|---|---|
| 2026-08-21 | AION-7.0.0 specification phase begins (Task 60) | Bridge not yet investigated |
| 2026-08-23 | R0.3.3 — TCR/QDT repository captured (Task 79) | Candidates C-01, C-02 identified |
| 2026-08-23 | R0.3.3.A — V1-V4 verification (Task 80) | Caso D for both candidates |
| 2026-08-23 | R0.3.3.A.2 — Provenance bridge search in TCR/QDT (Task 81) | Bridge NOT found in TCR/QDT repo |
| 2026-08-23 | R0.3.3.A.2.4 — External AION-6.x archive search (Task 82) | Bridge NOT found in observable environment |
| 2026-08-23 | R0.3.3.A.2.4.A.1 — Historical conversation analysis (Task 85) | Bridge NOT found in `MEMORIAS_DE_UMA_CONSTRUCAO.md` |
| 2026-08-23 | AION-6.x-Provenance-Register initialization (this commit) | Bridge status: NOT AUTHENTICATED |

## Current epistemic state

```
BRIDGE STATUS: NOT AUTHENTICATED
C-01 (CORPUS-002): Caso D — content compatible, provenance insufficient
C-02 (CORPUS-006): Caso D — content compatible, provenance insufficient
```

This register records the **current state** of the bridge investigation. It does NOT authenticate the bridge. Future evidence may promote or refute the bridge status.

---

*"O status da ponte TCR/QDT → AION-6.x permanece NÃO AUTENTICADO. Conteúdo compatível (V4 PASS) não equivale a autenticação histórica (V3 PASS). A distinção entre `COMPATIBLE` e `EQUIVALENT` é rigorosamente preservada."*
