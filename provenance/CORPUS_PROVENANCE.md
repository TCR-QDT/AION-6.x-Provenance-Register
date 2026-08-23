# Corpus Provenance Status

## Overview

This document tracks the provenance status of each CORPUS-ID declared in the AION-MVP-001 Handoff (Section 3.1 — Corpus v1.3.0 composition).

For each CORPUS-ID, the status is one of:

| Status | Meaning |
|---|---|
| `MATERIALLY ACCESSIBLE` | File is present and verifiable in an accessible location |
| `CONTENT_COMPATIBLE_CANDIDATE` | A candidate file with matching content exists, but historical provenance is unverified |
| `CANDIDATE_NOT_VERIFIED` | A candidate file was identified but could not be verified |
| `NOT_FOUND` | No candidate file was found in any accessible location |
| `DOES_NOT_EXIST` | The CORPUS-ID is declared as non-existent (per Handoff) |

## Corpus v1.3.0 composition (per Handoff AION-MVP-001 Section 3.1)

| CORPUS-ID | Document | State (Handoff) | Size (Handoff) |
|---|---|---|---|
| CORPUS-001 | AION-DOC-000.html | CURRENT | not specified |
| CORPUS-002-HIST | Paper A v6.2 anterior | SUPERSEDED | 134KB |
| CORPUS-002 | Paper A v6.2 | CURRENT/AUTHORITATIVE | 137KB |
| CORPUS-003 | PARTE IV Formalização Teórica | CURRENT | not specified |
| CORPUS-004 | Paper B anterior (3 págs) | HISTORICAL | not specified |
| CORPUS-005 | Cover Letter PT-BR | CURRENT | not specified |
| CORPUS-006 | Paper A v6.1 oficial | HISTORICAL | 138KB |
| CORPUS-007 | Paper A v6.1 revisão | HISTORICAL/SCIENTIFIC_REVISION | 326KB |
| CORPUS-011 | Paper B v6.1 PT novo (5 págs) | CURRENT | not specified |
| Paper A v6.0 | (does not exist) | DOES NOT EXIST | n/a |
| Paper B v6.0 | (does not exist) | DOES NOT EXIST | n/a |

## Current provenance status (as of 2026-08-23)

| CORPUS-ID | Status | Candidate material | Candidate SHA-256 | V1 | V2 | V3 | V4 | Classification |
|---|---|---|---|---|---|---|---|---|
| CORPUS-001 | NOT_FOUND | none | n/a | n/a | n/a | n/a | n/a | n/a |
| CORPUS-002-HIST | CANDIDATE_NOT_VERIFIED | `docs/pdfs/Paper_A_v6.2_REVTeX_REAL_P3.pdf` (TCR/QDT) | (not computed in this register) | ⚠ partial | n/a | ⚠ INSUFFICIENT | n/a | not formally verified |
| CORPUS-002 | CONTENT_COMPATIBLE_CANDIDATE | `docs/pdfs/Paper_A_v6.2_FINAL.pdf` (TCR/QDT) | `971986d96c4ceb1ea5d7a17acdf2a54f4276403f2805c3945874304020adc433` | ✓ PASS | ✓ PASS | ⚠ INSUFFICIENT | ✓ PASS | Caso D |
| CORPUS-003 | CANDIDATE_NOT_VERIFIED | `docs/pdfs/PARTE_IV_Formalizacao_Teorica_PT-BR.pdf` (TCR/QDT) | (not computed in this register) | ⚠ partial | n/a | ⚠ INSUFFICIENT | n/a | not formally verified |
| CORPUS-004 | NOT_FOUND | none | n/a | n/a | n/a | n/a | n/a | n/a |
| CORPUS-005 | CANDIDATE_NOT_VERIFIED | multiple `Cover_Letter_Paper_*_PT-BR.md` (TCR/QDT) | (not computed in this register) | ⚠ partial | n/a | ⚠ INSUFFICIENT | n/a | not formally verified |
| CORPUS-006 | CONTENT_COMPATIBLE_CANDIDATE | `docs/pdfs/Paper_A_v6.1_REVTeX_COMPLETE.pdf` (TCR/QDT) | `efd7f7caf19a5f99cd1663303c6f36d0beba50f19c71d4f44d44b81c396c8854` | ✓ PASS | ✓ PASS | ⚠ INSUFFICIENT | ✓ PASS | Caso D |
| CORPUS-007 | NOT_FOUND | none (no 326KB Paper A v6.1 file in TCR/QDT) | n/a | n/a | n/a | n/a | n/a | n/a |
| CORPUS-011 | CANDIDATE_NOT_VERIFIED | `docs/pdfs/Paper_B_QDT_JCP_v6.1_PT-BR.pdf` (TCR/QDT) | (not computed in this register) | ⚠ partial | n/a | ⚠ INSUFFICIENT | n/a | not formally verified |
| Paper A v6.0 | DOES_NOT_EXIST | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| Paper B v6.0 | DOES_NOT_EXIST | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Summary

- **2 CORPUS-IDs formally verified as Caso D** (CORPUS-002, CORPUS-006)
- **4 CORPUS-IDs with unverified candidates** (CORPUS-002-HIST, CORPUS-003, CORPUS-005, CORPUS-011)
- **3 CORPUS-IDs NOT_FOUND** (CORPUS-001, CORPUS-004, CORPUS-007)
- **2 CORPUS-IDs declared as DOES_NOT_EXIST** (Paper A v6.0, Paper B v6.0)

## Notes on V3 INSUFFICIENT for all candidates

For all candidates, V3 PROVENANCE is INSUFFICIENT because:

1. No material chain links TCR/QDT files to AION-6.x corpus source
2. No independent historical hash is registered in any AION-6.x artifact
3. No log of transfer TCR/QDT → AION-6.x exists
4. No snapshot of AION-6.x environment is accessible
5. No alternative Git repository containing AION-6.x infrastructure is accessible

Applying PM Task 80 principle: **"compatibility of content does not equal historical authentication"**. All candidates remain Caso D until material bridge evidence is provided.

## Future evidence incorporation

When new material evidence becomes available (manifest, hash, log, snapshot), this document should be updated with:

1. Date of evidence incorporation
2. Source of evidence
3. SHA-256 of evidence artifact
4. Re-evaluation of V3 for affected CORPUS-IDs
5. Updated classification (Caso A/B/C/D per candidate)

---

*"O status de proveniência do corpus AION-6.x permanece NÃO AUTENTICADO para todos os CORPUS-IDs. Candidatos materialmente compatíveis (Caso D) não constituem autenticação histórica. A busca por ponte material continua."*
