# AION — Epistemic Provenance Architecture

> **A system for establishing what we are authorized to assert, not merely what we wish were true.**

AION is an epistemic engineering project that builds a provenance-by-construction architecture from the lessons of a recoverability failure. It transitions from *forensic recovery* (attempting to reconstruct what happened) to *provenance-by-construction* (establishing what is authorized to be claimed at the moment each event occurs).

This repository contains the canonical artifacts of the **AION-7.0.0 → AION-7.1.x** transition: the consolidation of a recoverability boundary (Task 90–91), the charter for forward investigation (Task 92), the formal requirements (Task 93), and the architectural options analysis (Task 94).

---

## Table of Contents

- [Origin](#origin)
- [The Core Distinction](#the-core-distinction)
- [Phase Architecture](#phase-architecture)
- [Repository Structure](#repository-structure)
- [The Founding Question](#the-founding-question)
- [Key Concepts](#key-concepts)
- [Provenance Event Chain](#provenance-event-chain)
- [Compliance Matrix Summary](#compliance-matrix-summary)
- [Verification](#verification)
- [Governance Rules](#governance-rules)
- [GitHub Integration](#github-integration)
- [Reading Order](#reading-order)
- [Status](#status)

---

## Origin

AION-7.0.0 began as a **provenance investigation** — an attempt to recover the historical provenance of artifacts whose chain of custody could not be independently verified. The investigation reached three conclusions:

| Domain | State | Tier |
|---|---|---|
| P1 | RESOLVED | DEMONSTRADO |
| P2 | RESOLVED | DEMONSTRADO |
| P3 | INSUFFICIENT | DESCONHECIDO |

P3 — the question of whether a specific historical manifest existed — could not be resolved from currently accessible material. The investigation did not fail to find evidence; it **formally classified the limit of recoverability**.

This classification is the **methodological result** of AION-7.0.0, not its failure. The boundary is what 7.0.0 adds to the inherited record.

---

## The Core Distinction

AION is built on a single, load-bearing distinction that recurs at every level:

```text
PROPRIEDADE TECNOLÓGICA        ≠        GARANTIA EPISTÊMICA
```

| Technological Property | (does NOT imply) | Epistemic Guarantee |
|---|---|---|
| Has a timestamp | ≠ | Prevents backdating |
| Has a hash | ≠ | Proves prior existence |
| Is append-only | ≠ | Is independently verifiable |
| Is on a blockchain | ≠ | Has sufficient provenance |
| Uses hardware attestation | ≠ | Resolves the L1/L2/L3 chain |

A system satisfies a requirement only when it provides the **epistemic guarantee** the requirement demands — not merely the technological property that resembles it. Every analytical artifact in this repository enforces this distinction.

---

## Phase Architecture

```text
AION-7.0.0 (FROZEN, READ-ONLY)
    │
    │  R0 Provenance Investigation
    │       │
    │       ├── Task 90 — BOUNDARY (provenance frontier classified)
    │       └── Task 91 — CONSOLIDATION (R0 frozen)
    │
    │  Consolidated state:
    │  ├── P1 = RESOLVED
    │  ├── P2 = RESOLVED
    │  ├── P3 = INSUFFICIENT
    │  ├── V3 = RECOVERY EXHAUSTED
    │  ├── CASE D = PRESERVED / FROZEN
    │  ├── EP-1 = FROZEN
    │  └── AUTH₇.₀ = FALSE
    │
    ▼
AION-7.1.x (FORWARD, READ-WRITE WITHIN SCOPE)
    │
    │  Provenance-by-Construction
    │       │
    │       ├── Task 92 — CHARTER (mandate, constraints, problem space)
    │       ├── Task 93 — REQUIREMENTS (20 verifiable requirements)
    │       ├── Task 94 — ARCH OPTIONS (8 classes × 20 reqs matrix)
    │       ├── Task 95 — THREAT MODEL (PROPOSED)
    │       ├── Task 96 — REFERENCE ARCHITECTURE (PROPOSED)
    │       └── Task 97 — PILOT IMPLEMENTATION PLAN (PROPOSED)
    │
    ▼
NEW EPISTEMIC STATE (to be established)
```

The transition from 7.0.0 to 7.1.x is **one-way and irreversible**. The 7.0.0 frozen state is read-only for all subsequent work; any modification is forbidden by invariant I-91.1 through I-91.7 and operational constraint R-7.1.3.

---

## Repository Structure

```
.
├── README.md                              ← this file
├── worklog.md                             ← shared multi-agent work log (append-only)
├── .gitignore                             ← ignores workspace state; tracks canonical artifacts
│
├── download/                              ← canonical FROZEN and ISSUED artifacts
│   │
│   │  ── AION-7.0.0 (FROZEN) ──
│   ├── AION-7.0.0_R0_CONSOLIDATION_MANIFEST.md
│   ├── AION-7.0.0_EPISTEMIC_STATE_FREEZE.md
│   ├── AION-7.0.0_PROVENANCE_BOUNDARY.md
│   │
│   │  ── AION-7.1.x (FORWARD INVESTIGATION) ──
│   ├── AION-7.1.x_CHARTER.md
│   ├── AION-7.1.x_REQUIREMENTS.md
│   ├── AION-7.1.x_ARCH_OPTIONS.md
│   │
│   │  ── GitHub Integration ──
│   └── .github/
│       ├── CODEOWNERS                     ← enforces review on protected paths
│       ├── CONTRIBUTING.md                ← contribution protocol (epistemic, not casual)
│       ├── CODE_OF_CONDUCT.md             ← four epistemic commitments
│       ├── SECURITY.md                    ← vulnerability reporting policy
│       ├── PULL_REQUEST_TEMPLATE.md       ← R-7.1.x + I-91.x compliance declaration
│       ├── branch-protection.md           ← branch protection rules documentation
│       ├── ISSUE_TEMPLATE/
│       │   ├── config.yml                 ← disables blank issues
│       │   ├── invariant-violation-escalation.md  ← phase-8.0.0 escalation path
│       │   ├── task-proposal.md           ← R-7.1.x pre-checked task proposal
│       │   └── audit-finding.md           ← independent audit (confirms, never upgrades)
│       └── workflows/
│           └── aion-verify.yml            ← CI gate: 4 verification scripts + append-only check
│
└── scripts/                               ← verification scripts (persisted, re-runnable)
    ├── aion_r0_consolidation_verify.py
    ├── aion_71x_charter_verify.py
    ├── aion_71x_requirements_verify.py
    └── aion_71x_archoptions_verify.py
```

### Artifact Inventory

| Artifact | Task | Size | SHA-256 |
|---|---|---|---|
| `AION-7.0.0_R0_CONSOLIDATION_MANIFEST.md` | 91 | 10175 B | `fa14c4eb…12b2b8b4` |
| `AION-7.0.0_EPISTEMIC_STATE_FREEZE.md` | 91 | 7649 B | `964e02fa…f0eb58f6` |
| `AION-7.0.0_PROVENANCE_BOUNDARY.md` | 91 | 5581 B | `1e42245e…5605c72c` |
| `AION-7.1.x_CHARTER.md` | 92 | 14572 B | `e9254e55…8e128f84` |
| `AION-7.1.x_REQUIREMENTS.md` | 93 | 40133 B | `d80c2d8b…dfadc9d94` |
| `AION-7.1.x_ARCH_OPTIONS.md` | 94 | 45531 B | `a1fb82a3…2d699e726` |

Hash anchors are verified at every task issuance by the corresponding script in `scripts/`. Mismatch indicates tampering or corruption.

---

## The Founding Question

AION-7.1.x does not begin from a hypothesis. It begins from a question posed by the Projetista Master:

> **Como deve ser construído o AION daqui em diante para que a proveniência que não pôde ser recuperada no 6.x seja demonstrável, auditável e verificável no momento em que cada evento ocorrer?**

Three properties are required of every future event:

| Property | Meaning |
|---|---|
| **Demonstrable** | The provenance of the event can be shown to a third party without requiring their trust. |
| **Auditable** | An independent auditor can verify the provenance claim without accessing private state. |
| **Verifiable at occurrence** | The provenance is established at the moment of the event, not reconstructed afterward. |

The third property is load-bearing. It is the precise negation of the failure mode that produced `P3 = INSUFFICIENT` in 7.0.0.

---

## Key Concepts

### Three-Layer Provenance Distinction

Every provenance record `P(E)` in AION-7.1.x is a composite of three sub-records:

```text
P(E) = ⟨ P_L1(E), P_L2(E), P_L3(E) ⟩

  P_L1(E) = event provenance       (what happened)
  P_L2(E) = artifact provenance    (what object participated)
  P_L3(E) = assertion provenance   (how to verify the claim)
```

Layer 3 is **load-bearing**. Without it, the system reproduces the P3 failure mode at a different level: it would have records of what happened but no chain to verify claims about it.

> The problem encountered in P3 was not simply the absence of files; it was the absence of a chain capable of transforming a historical assertion into an independently verifiable assertion.

### Epistemic Non-Backdating

A property stronger than mere timestamping:

```text
timestamp declarado        ≠        tempo verificável de existência
```

A declared timestamp is an assertion made by the record itself. A verifiable time of existence is evidence, **independent of the system operator**, that the record existed at or before `T + ε` (where ε is the maximum tolerable clock skew).

Three conditions must hold:

1. External evidence establishes that the record existed at or before `T + ε`.
2. The external evidence cannot be fabricated retroactively by the operator.
3. The external evidence references the record by cryptographic hash, so it cannot be repurposed.

### The Vector Change

```text
AION-7.0    investigated historical provenance     (forensic recovery)
AION-7.1    must guarantee future provenance        (provenance-by-construction)
```

The 7.0.0 boundary is **not a debt** to be paid by future recovery. It is a **requirement** to be satisfied by future architecture.

> AION-7.0 terminou descobrindo um limite de conhecimento.
> AION-7.1 deve transformar esse limite em requisito de engenharia epistemológica.

---

## Provenance Event Chain

Every state transition in AION is recorded as a canonical provenance event. The chain is append-only.

| Event | Type | Effect |
|---|---|---|
| AION-EV-016 | Consolidation / Freeze | R0 frozen; P1/P2/P3 state terminal |
| AION-EV-017 | Phase Transition Authorization | 7.0.0 sealed; 7.1.x authorized (Option B) |
| AION-EV-018 | Charter Issuance | 7.1.x mandate, constraints, problem space established |
| AION-EV-019 | Task Authorization | Task 93 (Requirements) authorized |
| AION-EV-020 | Requirements Issuance | 20 requirements issued |
| AION-EV-021 | Task Authorization | Task 94 (Arch Options) authorized |
| AION-EV-022 | Analysis Issuance | 8-class survey + compliance matrix produced |
| AION-EV-023 | *(pending)* | Task 95 (Threat Model) — proposed |

---

## Compliance Matrix Summary

Task 94 surveyed 8 classes of candidate mechanisms against the 20 requirements. The headline result:

> **No single class satisfies all 20 requirements.** Combination is necessary.

| Class | Score | Notable Strength |
|---|---|---|
| C1 — Append-only log + hash chaining | 55% | Cheap local capture |
| C2 — RFC 3161 / Trusted Timestamping | 80% | Strong external temporal anchor |
| C3 — Witness co-signing | 70% | Distributed trust |
| **C4 — Transparency logs** | **95%** | **Best standalone; public verifiability** |
| C5 — Blockchain anchoring | 80% | Consensus-anchored ordering |
| C6 — Hardware-rooted attestation | 75% | Strong capture-at-occurrence |
| C7 — Zero-knowledge attestation | 75% | Strongest independent verifiability |
| C8 — Quorum / multi-witness | 70% | BFT-style threshold |

Four critical findings:

1. No single class satisfies all 20 requirements.
2. Pillar 3 (Non-Backdatable Temporal Ordering) is the hardest pillar.
3. REQ-NB.3 (monotonic temporal order) requires a C4- or C5-like sequence mechanism.
4. REQ-XC.2 (no recovery mode) is universally `≈` or `✗` — it requires architectural-level mitigation.

The full 8 × 20 matrix with rationale per cell is in `AION-7.1.x_ARCH_OPTIONS.md`.

---

## Verification

Every task in AION is verified at issuance by a persisted script. To re-verify the integrity of the entire repository:

```bash
# Verify 7.0.0 consolidation (Task 91)
python3 scripts/aion_r0_consolidation_verify.py

# Verify 7.1.x charter (Task 92)
python3 scripts/aion_71x_charter_verify.py

# Verify 7.1.x requirements (Task 93)
python3 scripts/aion_71x_requirements_verify.py

# Verify 7.1.x arch options (Task 94)
python3 scripts/aion_71x_archoptions_verify.py
```

Each script:

1. Computes the SHA-256 of its corresponding artifact.
2. Verifies that all 7.0.0 FROZEN artifacts remain unchanged (REQ-MI.3 compliance).
3. Verifies that all prior 7.1.x artifacts remain unchanged.
4. Appends a structured entry to `worklog.md`.

A mismatch in any hash indicates tampering or corruption and must be escalated.

---

## Governance Rules

AION-7.0.0 is governed by **seven non-negotiable invariants** that constrain all 7.x reasoning:

| ID | Invariant |
|---|---|
| I-91.1 | V3 SHALL NOT be reopened within the same methodological line. |
| I-91.2 | P3 state SHALL remain INSUFFICIENT — no retroactive upgrade permitted. |
| I-91.3 | Caso D SHALL remain PRESERVED — no resolution by narrative. |
| I-91.4 | AUTH₇.₀ SHALL remain FALSE — no retroactive authentication. |
| I-91.5 | The three-domain distinction SHALL NOT be collapsed. |
| I-91.6 | Memories (≈) do not constitute proof (✓). Corroboration is not demonstration. |
| I-91.7 | The provenance boundary is a methodological result, not a deficiency. |

AION-7.1.x operates under **five operational constraints** inherited from the Charter:

| ID | Constraint |
|---|---|
| R-7.1.1 | P3 remains INSUFFICIENT. |
| R-7.1.2 | Caso D remains frozen. |
| R-7.1.3 | No retroactive modification of 7.0.0. |
| R-7.1.4 | New evidence must have independent provenance. |
| R-7.1.5 | The P3 lesson becomes preventive architecture. |

Any proposed operation that violates these rules is **out of scope for AION-7.x** and requires escalation to a new major phase (8.0.0+).

---

## GitHub Integration

This repository ships with a complete governance layer in `.github/`. The governance layer is the **operational enforcement** of the invariants and constraints documented in the artifacts. It is not optional.

### Issue Templates

Blank issues are disabled (`config.yml`). Every issue must use one of three structured templates:

| Template | Purpose |
|---|---|
| `invariant-violation-escalation.md` | Propose escalation when an invariant (I-91.x) or constraint (R-7.1.x) is violated. Includes hash verification for 7.0.0 frozen artifacts. |
| `task-proposal.md` | Propose a new task within 7.1.x. Pre-checks R-7.1.1 – R-7.1.5, forbidden patterns, and the four pillars. |
| `audit-finding.md` | Report findings from an independent audit. Auditor declares independence and respects the rule that audit may confirm but never upgrade. |

### Pull Request Template

Every PR must complete the compliance declaration in `PULL_REQUEST_TEMPLATE.md`:

- **R-7.1.1 – R-7.1.5** (five operational constraints)
- **I-91.1 – I-91.7** (seven frozen-state invariants)
- **Methodological pre-checks**: PROPERTY ≠ GUARANTEE, three-layer model, Epistemic Non-Backdating, forward-only
- **Hash verification**: 7.0.0 frozen artifacts must match Task 91 anchors
- **Script verification**: all four verification scripts must pass locally
- **Scope classification**: additive / amendment / correction / forbidden

A PR with an incomplete declaration is rejected without review.

### CI Workflow (`.github/workflows/aion-verify.yml`)

Runs on every push to `main` and `7.1.x`, and on every PR targeting those branches. The workflow:

1. Verifies that the three 7.0.0 FROZEN artifacts match their Task 91 hash anchors (R-7.1.3 / REQ-MI.3).
2. Verifies that the three 7.1.x artifacts match their issuance hash anchors.
3. Runs all four verification scripts (`aion_r0_consolidation_verify.py`, `aion_71x_charter_verify.py`, `aion_71x_requirements_verify.py`, `aion_71x_archoptions_verify.py`).
4. Verifies that `worklog.md` is append-only (prior sections not modified).

A failure on any step blocks the PR. The summary is published to the GitHub Actions run page.

### CODEOWNERS

The `CODEOWNERS` file enforces review on protected paths:

| Path | Reviewers |
|---|---|
| `download/AION-7.0.0_*.md` | `@projetista-master` (frozen; CI blocks any change) |
| `download/AION-7.1.x_*.md` | `@projetista-master`, `@aion-analyst` |
| `worklog.md` | `@aion-analyst` (append-only; CI verifies) |
| `scripts/` | `@aion-maintainer` (changes affect the integrity gate) |
| `.github/` | `@aion-maintainer` |
| `download/README.md` | `@projetista-master`, `@aion-maintainer` |

### Branch Protection

Branch protection rules for `main` and `7.1.x` are documented in `.github/branch-protection.md`. The rules require:

- PR before merging (≥1 approval, CODEOWNERS enforced)
- Status checks pass (the `AION Verification` workflow is required)
- Conversation resolution before merging
- Signed commits (GPG or SSH)
- Linear history (rebase + squash; no merge commits)
- No force pushes
- No administrator bypass

### Contributing

Read `.github/CONTRIBUTING.md` before opening a PR. The contribution protocol is **epistemic, not casual**: contributors must understand the seven invariants, the five constraints, the PROPERTY ≠ GUARANTEE distinction, the three-layer model, and the forward-only policy.

### Code of Conduct

`.github/CODE_OF_CONDUCT.md` defines four epistemic commitments: truth over convenience, boundary over closure, forward over backward, audit over trust. Violations of invariants and constraints are handled through the issue templates, not through punishment.

### Security Policy

`.github/SECURITY.md` defines what counts as a vulnerability in this repository (e.g., any condition that allows a 7.0.0 frozen artifact to be modified) and how to report it (private security advisory, not a public issue).

---

## Reading Order

A new reader (analyst, auditor, or contributor) should read the artifacts in this order:

1. **This README** — orientation.
2. **`.github/CONTRIBUTING.md`** — the contribution protocol.
3. **`AION-7.0.0_PROVENANCE_BOUNDARY.md`** — what the boundary is and why it is a result.
4. **`AION-7.0.0_EPISTEMIC_STATE_FREEZE.md`** — the three-domain architecture and non-collapsibility rules.
5. **`AION-7.0.0_R0_CONSOLIDATION_MANIFEST.md`** — the full frozen state, invariants, and decision options.
6. **`AION-7.1.x_CHARTER.md`** — the mandate, constraints, and four pillars.
7. **`AION-7.1.x_REQUIREMENTS.md`** — the 20 verifiable requirements and the three-layer model.
8. **`AION-7.1.x_ARCH_OPTIONS.md`** — the 8-class survey and compliance matrix.
9. **`.github/branch-protection.md`** — how the governance is enforced technically.
10. **`worklog.md`** — the chronological record of every task and provenance event.

The 7.0.0 artifacts are **read-only**. Reading them in order establishes the boundary condition under which 7.1.x operates.

---

## Status

```text
AION-7.0.0: CONSOLIDATED / FROZEN
AION-7.1.x: FORWARD INVESTIGATION — IN PROGRESS
  ├── Task 92 (Charter):           ISSUED
  ├── Task 93 (Requirements):      ISSUED
  ├── Task 94 (Arch Options):      ISSUED
  ├── Task 95 (Threat Model):      PROPOSED — pending PM authorization
  ├── Task 96 (Reference Arch):    PROPOSED
  └── Task 97 (Pilot Plan):        PROPOSED

P3 RETROACTIVE UPGRADE:  PROHIBITED
V3 REOPENING:            PROHIBITED
CASE D:                  PRESERVED (out of scope for 7.1.x)
7.0.0 FROZEN STATE:     UNCHANGED (verified at every task)
```

---

## License & Attribution

This repository contains epistemic engineering artifacts produced under the direction of the Projetista Master. The methodological framework — including the three-layer provenance distinction, Epistemic Non-Backdating, and the PROPERTY ≠ GUARANTEE analytical distinction — is documented in the artifacts themselves.

Cite as: **AION-7.1.x — Epistemic Provenance Architecture**, version 7.1.x, Task 94 issuance, 2026-08-24.

---

> The boundary is a result, not a deficiency.
> The work is engineering, not archaeology.
