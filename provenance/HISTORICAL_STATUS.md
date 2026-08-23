# Historical Status of AION-6.x Components

## Overview

This document records the historical status of AION-6.x components as declared in the AION-MVP-001 Handoff, with the current state of material recovery.

## Components declared in Handoff (Section 3)

| Component | Version | State (Handoff) | Current material status |
|---|---|---|---|
| Corpus | v1.3.0 | FROZEN — 9 registros documentais + 2 inexistentes | NOT MATERIALLY ACCESSIBLE |
| Oracle | v3 | FROZEN — 7 chunks interversionais | NOT MATERIALLY ACCESSIBLE |
| GraphRAG | v1.0.0 | FROZEN — 22 nós, 187 arestas, PGI=1.0 | NOT MATERIALLY ACCESSIBLE |
| P-RESP-001 | v0.3 | FROZEN — validator determinístico pós-geração | NOT MATERIALLY ACCESSIBLE |
| AION-EVAL-002 | v0.2 | FROZEN — multicamada (10 categorias R1-H1) | NOT MATERIALLY ACCESSIBLE |
| AION-DIFY-001 | Aprovado | FROZEN — workflow de 5 blocos | NOT MATERIALLY ACCESSIBLE |
| B1 Retrieval | 6.2.11 | FROZEN — cross-lingual PT-BR→EN + Oracle v3 | NOT MATERIALLY ACCESSIBLE |
| Temporal Index | v1.0 | TPC=1.0000 | NOT MATERIALLY ACCESSIBLE |
| Ontologia | v1.0.0 | 13 conceitos, 4 clusters, citações [E] | NOT MATERIALLY ACCESSIBLE |

## Narrative corroboration

The recovered historical document `MEMORIAS_DE_UMA_CONSTRUCAO.md` (PR-001) provides narrative corroboration of the existence of several of these components:

| Component | Narrative reference in PR-001 | Match with Handoff? |
|---|---|---|
| AION-6.2 | line 569 — "encerrado para handoff" in 20/08/2026 | ✓ matches |
| AION-6.3 | lines 597, 601, 1027 — next steps: geração, proveniência, fabricação | ✓ matches |
| CORPUS-002 | line 267, 459 — including example F3 `CORPUS-002#chunk_001` | ✓ matches Handoff Section 5.1 |
| CORPUS-006 | line 265, 433 — including chunk Oracle v3 `CORPUS-006#p1_01` | ✓ matches Handoff Section 3 |
| R^α genealogy | lines 259, 265, 267 — CORPUS-006 10/ago → CORPUS-002 12/ago | ✓ matches Handoff Section 6 |
| B1 resolution | lines 425-433 — 3/3 Top-1/Top-3/Top-5 | ✓ matches Handoff Section 4 |
| P-RESP-001 v0.3 | line 503 — "barreira epistemológica" | ✓ matches Handoff Section 3 |
| GraphRAG | lines 306, 707 | ✓ matches Handoff |

## Critical absence

The recovered document does NOT contain:

- SHA-256 hashes of CORPUS-002 or CORPUS-006 files
- Manifest of AION-6.x ingestion
- Log of transfer TCR/QDT → AION-6.x
- Snapshot of AION-6.x environment
- URL of any AION-6.x Git repository containing infrastructure

## Epistemic interpretation

The narrative corroboration confirms that AION-6.x existed as a research context and that the canonical components described in the Handoff were real. However, narrative corroboration does NOT authenticate material provenance.

Applying:
- PM Task 80 principle: **"compatibility of content does not equal historical authentication"**
- 4th canonical invariant: **`COMPATIBLE ≠ EQUIVALENT`**

The components listed above remain `NOT MATERIALLY ACCESSIBLE` until material evidence (artifact, manifest, hash, log, snapshot) is provided.

## Status history

| Date | Event | Status |
|---|---|---|
| 2026-08-21 | AION-7.0.0 specification phase begins | Components declared FROZEN per Handoff; not yet investigated |
| 2026-08-23 | R0.1-R0.5 (Tasks 69-77) | All components confirmed NOT MATERIALLY ACCESSIBLE in observable environment |
| 2026-08-23 | R0.3.3 (Task 79) — TCR/QDT captured | TCR/QDT provides content-compatible candidates for CORPUS-002, CORPUS-006 (Caso D); other components remain NOT FOUND |
| 2026-08-23 | R0.3.3.A.2.4.A.1 (Task 85) — Historical document analyzed | Narrative corroboration of component existence; no material bridge |
| 2026-08-23 | AION-6.x-Provenance-Register initialization (this commit) | Components remain NOT MATERIALLY ACCESSIBLE; narrative corroboration recorded |

## Future evidence incorporation

When new material evidence becomes available for any component, this document should be updated with:

1. Date of evidence incorporation
2. Source of evidence
3. SHA-256 of evidence artifact
4. Re-evaluation of material accessibility status
5. Updated classification per component

---

*"Os componentes AION-6.x permanecem NÃO MATERIALMENTE ACESSÍVEIS. A corroboração narrativa confirma sua existência histórica, mas não autentica materialmente sua proveniência. A busca por ponte material continua."*
