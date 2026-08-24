# AION-7.1.x — CHARTER
## Task 92 — Mandate, Architecture Space, and Operational Constraints for Forward Investigation

| Field | Value |
|---|---|
| Task ID | 92 |
| Phase | AION-7.1.x (Forward Investigation) |
| Origin | Projetista Master determination AION-EV-017 (Option B) |
| Predecessor | Task 91 — R0 Consolidation (AION-7.0.0 FROZEN) |
| Status | CHARTER ISSUED — investigation not yet begun |
| Date (UTC-3) | 2026-08-24 |
| Provenance Event | AION-EV-017 (transition authorized) → AION-EV-018 (charter issued) |
| Reversibility | Charter may be amended; transition itself is irreversible |

---

## 1. Authorization Received (AION-EV-017)

The Projetista Master has issued the following determination:

```text
AION-EV-017

OPÇÃO: B
STATUS: AUTORIZADA

AION-7.0.0 R0
    = CONSOLIDATED / FROZEN

AION-7.1.x
    = AUTHORIZED FORWARD INVESTIGATION

P3 RETROACTIVE UPGRADE
    = PROHIBITED

V3 REOPENING
    = PROHIBITED

CASE D
    = PRESERVED

NOVAS EVIDÊNCIAS
    = PERMITIDAS SOMENTE SE MATERIALMENTE NOVAS
```

This charter is issued under that authorization. It does not modify the authorization; it specifies how the authorized forward investigation will be conducted.

---

## 2. Founding Question

AION-7.1.x begins not from a hypothesis but from a question posed by the Projetista Master:

> **Como deve ser construído o AION daqui em diante para que a proveniência que não pôde ser recuperada no 6.x seja demonstrável, auditável e verificável no momento em que cada evento ocorrer?**

Three properties are required of any future event:

| Property | Portuguese | Operational meaning |
|---|---|---|
| Demonstrable | demonstrável | The provenance of the event can be shown to a third party without requiring their trust. |
| Auditable | auditável | An independent auditor can verify the provenance claim without accessing private state. |
| Verifiable at occurrence | verificável no momento em que cada evento ocorrer | The provenance is established at the moment of the event, not reconstructed afterward. |

The third property is the load-bearing one. It is the precise negation of the failure mode that produced P3 = INSUFFICIENT in 7.0.0.

---

## 3. The Vector Change

The Projetista Master has identified a structural change in the direction of investigation:

> AION-7.0 investigou a proveniência histórica.
> AION-7.1 deve investigar como construir e operar um sistema cuja proveniência futura seja demonstrável desde a origem.

This is a vector change, not a continuation. The difference is encoded in the table below:

| Dimension | AION-7.0.0 (retrospective) | AION-7.1.x (prospective) |
|---|---|---|
| Temporal direction | Past → present | Present → future |
| Mode | Forensic recovery | Provenance-by-construction |
| Failure mode of concern | "We cannot recover what happened" | "We will not need to recover what happens" |
| P3 status | INSUFFICIENT (frozen) | Reinterpreted as design requirement |
| Caso D | Preserved boundary case | Out of scope (not to be resolved by 7.1.x) |
| Evidence policy | Recoverable if material exists | Captured at occurrence, never requires recovery |
| Audit posture | Audit the past | Audit the live system |

The vector change is recorded as AION-EV-018.

---

## 4. The Five PM Constraints — Operationalized

The Projetista Master has imposed five constraints on 7.1.x. They are restated here as operational requirements, each with an identifier, a verification criterion, and a forbidden pattern.

### R-7.1.1 — P3 remains INSUFFICIENT

| Field | Value |
|---|---|
| Source | PM constraint #1 |
| Statement | No operation in 7.1.x may modify the state of P3 in 7.0.0. P3 remains INSUFFICIENT in the consolidated record. |
| Verification | Any 7.1.x artifact that references P3 MUST cite it as INSUFFICIENT. |
| Forbidden pattern | "P3 was resolved by 7.1.x evidence." |
| Governing invariant | I-91.2 (frozen in 7.0.0) |

### R-7.1.2 — Caso D remains frozen

| Field | Value |
|---|---|
| Source | PM constraint #2 |
| Statement | Caso D is preserved as a boundary case. 7.1.x may not resolve, reject, or narratively close it. |
| Verification | Any 7.1.x artifact that references Caso D MUST cite it as PRESERVED / FROZEN. |
| Forbidden pattern | "Caso D was resolved by 7.1.x architecture." |
| Governing invariant | I-91.3 (frozen in 7.0.0) |

### R-7.1.3 — No retroactive modification of 7.0.0

| Field | Value |
|---|---|
| Source | PM constraint #3 |
| Statement | No artifact, decision, or evidence produced in 7.1.x may retroactively alter the state of 7.0.0. The frozen state is read-only for 7.1.x. |
| Verification | The SHA-256 hashes of the three 7.0.0 FROZEN artifacts MUST remain unchanged throughout 7.1.x. |
| Forbidden pattern | "Based on 7.1.x findings, we now update the 7.0.0 manifest." |
| Governing invariant | I-91.1, I-91.2, I-91.4 (frozen in 7.0.0) |

### R-7.1.4 — New evidence must have independent provenance

| Field | Value |
|---|---|
| Source | PM constraint #4 |
| Statement | Any new evidence produced or cited in 7.1.x MUST possess provenance that is (a) independent of 7.0.0 evidence and (b) temporally identifiable as occurring after the 7.0.0 freeze date. |
| Verification | Each piece of evidence MUST carry a provenance record with timestamp, source identity, and hash chain anchor. |
| Forbidden pattern | "This 7.1.x evidence also retroactively corroborates the 7.0.0 P3 hypothesis." |
| Governing invariant | New (established by this charter as R-7.1.4) |

### R-7.1.5 — P3 lesson becomes preventive architecture

| Field | Value |
|---|---|
| Source | PM constraint #5 |
| Statement | The 7.0.0 finding that P3 could not be recovered MUST be transformed into a preventive architectural requirement. 7.1.x is forbidden from depending on forensic recovery to establish the provenance of any event it generates. |
| Verification | Every 7.1.x architectural component MUST specify how its provenance is established at occurrence, not reconstructed after. |
| Forbidden pattern | "We will figure out the provenance of this event later if needed." |
| Governing invariant | New (established by this charter as R-7.1.5) |

---

## 5. Non-Goals

To prevent scope drift, the following are explicitly **not** goals of 7.1.x:

| Non-Goal | Reason |
|---|---|
| Re-open V3 | Forbidden by I-91.1 and AION-EV-017 |
| Upgrade P3 to RESOLVED | Forbidden by I-91.2 and AION-EV-017 |
| Authenticate P3 retroactively | Forbidden by I-91.4 and AION-EV-017 |
| Close Caso D | Forbidden by I-91.3 and AION-EV-017 |
| Build a system that "would have" recovered P3 | Counterfactual; not a valid engineering target |
| Re-litigate the 7.0.0 boundary | The boundary is a result, not a deficiency (I-91.7) |
| Construct a narrative closure for the 6.x → 7.0.0 chain | 7.1.x is forward-only |

These non-goals are not soft preferences. Violating any of them is grounds for immediate task termination and escalation to the Projetista Master.

---

## 6. Architectural Problem Space (Not Solution)

This charter does **not** specify a solution. It specifies the problem space within which solutions will be explored.

The problem space has four load-bearing pillars, derived from the founding question. Each pillar is a question, not an answer.

### Pillar 1 — Capture-at-Occurrence
> How does the system establish provenance at the moment an event occurs, such that no later reconstruction is required?

Candidate approaches (not endorsed, listed for exploration):
- Append-only event log with cryptographic chaining
- Notarization at occurrence (timestamp authority, ledger)
- Witness co-signing at occurrence
- Hardware-rooted attestation

### Pillar 2 — Independent Verifiability
> How does a third-party auditor verify a provenance claim without accessing private state or trusting the system operator?

Candidate approaches:
- Public verifiability (cryptographic proofs publishable in clear)
- Zero-knowledge attestation
- Multi-witness quorum
- Public bulletin board / transparency log

### Pillar 3 — Non-Backdatable Temporal Ordering
> How does the system guarantee that an event's claimed time of occurrence cannot be backdated?

Candidate approaches:
- Trusted timestamp authority (RFC 3161)
- Blockchain anchoring
- Sequential transparency log (like Certificate Transparency)
- Causally ordered distributed clock

### Pillar 4 — Material Independence from 7.0.0
> How does each new piece of evidence establish provenance that does not depend on the 7.0.0 record?

Candidate approaches:
- Fresh root of trust established at 7.1.x inception
- Independent witness set
- New cryptographic key lineage
- Disjoint evidence corpus

The four pillars are independent: a solution that satisfies one does not automatically satisfy the others. Any 7.1.x architecture MUST address all four.

---

## 7. Relationship to AION-7.0.0 Frozen State

```text
AION-7.0.0 (FROZEN, READ-ONLY)
    │
    │  inherits as boundary condition:
    │  - P1 = RESOLVED
    │  - P2 = RESOLVED
    │  - P3 = INSUFFICIENT (as design requirement, not as open question)
    │  - V3 = RECOVERY EXHAUSTED (as lesson, not as pending task)
    │  - Caso D = PRESERVED (as boundary, not as problem to solve)
    │  - AUTH₇.₀ = FALSE (as historical verdict, not as future target)
    │
    ▼
AION-7.1.x (FORWARD, READ-WRITE WITHIN SCOPE)
    │
    │  operates under:
    │  - R-7.1.1 through R-7.1.5
    │  - The founding question
    │  - The four pillars
    │  - The non-goals
    │
    ▼
NEW EPISTEMIC STATE (to be established by 7.1.x work)
```

The 7.0.0 frozen state is **read-only** for 7.1.x. It may be cited, referenced, and inherited as boundary condition. It may not be modified, reinterpreted, or "completed" by 7.1.x.

---

## 8. Authorization Matrix for 7.1.x Operations

| Operation | Authorized? | Condition |
|---|---|---|
| Establish fresh root of trust for 7.1.x | YES | Must be independent of 7.0.0 roots |
| Cite 7.0.0 frozen state as boundary condition | YES | Must cite as frozen, not as pending |
| Generate new events with capture-at-occurrence provenance | YES | Must satisfy all four pillars |
| Audit 7.0.0 frozen state for consistency | YES | Audit findings are observations, not upgrades |
| Propose architectural solutions for the four pillars | YES | Must address all four, not subset |
| Modify any 7.0.0 artifact | **NO** | R-7.1.3 |
| Re-open V3 within 7.1.x | **NO** | I-91.1, AION-EV-017 |
| Cite 7.1.x evidence as retroactive corroboration of P3 | **NO** | R-7.1.4 |
| Resolve Caso D using 7.1.x architecture | **NO** | R-7.1.2 |
| Skip any of the four pillars in an architecture proposal | **NO** | All four required |

---

## 9. Task Scaffolding (Initial, Non-Binding)

The following task structure is proposed as the starting point for 7.1.x. It is non-binding; the first task of 7.1.x may revise the structure. The structure exists only to make the entry into 7.1.x concrete.

| Task | Title | Output | Status |
|---|---|---|---|
| 93 | Requirements Elicitation — formalize the four pillars as verifiable requirements | AION-7.1.x_REQUIREMENTS.md | PROPOSED |
| 94 | Architectural Options Analysis — survey candidate approaches for each pillar | AION-7.1.x_ARCH_OPTIONS.md | PROPOSED |
| 95 | Threat Model — what could cause an event's provenance to be non-recoverable in 7.1.x? | AION-7.1.x_THREAT_MODEL.md | PROPOSED |
| 96 | Reference Architecture Selection — choose one approach per pillar with rationale | AION-7.1.x_REFERENCE_ARCH.md | PROPOSED |
| 97 | Pilot Implementation Plan — how to test the reference architecture on a real event | AION-7.1.x_PILOT_PLAN.md | PROPOSED |

Tasks 93–97 are deliberately ordered: requirements before options, options before architecture, architecture before pilot. No task may be skipped. Any proposal to skip a task must be escalated to the PM.

---

## 10. The Conceptual Reframing

The Projetista Master has stated the most important consequence of Task 91:

> AION-7.0 terminou descobrindo um limite de conhecimento.
> AION-7.1 deve transformar esse limite em requisito de engenharia epistemológica.

This charter encodes that reframing as its operational core:

- The 7.0.0 boundary is **not a debt** to be paid by future recovery.
- The 7.0.0 boundary is **a requirement** to be satisfied by future architecture.
- The question is no longer "can we recover what happened?" but "can we guarantee that what happens from now on will not require recovery?"

This is the shift from forensic recovery to provenance-by-construction.

---

## 11. Provenance Events

### AION-EV-017 — TRANSITION AUTHORIZED

| Field | Value |
|---|---|
| Event ID | AION-EV-017 |
| Type | Phase Transition Authorization |
| Issuer | Projetista Master |
| Effect | AION-7.0.0 sealed as CONSOLIDATED/FROZEN; AION-7.1.x authorized as forward investigation |
| Constraints | Five PM constraints (operationalized here as R-7.1.1 through R-7.1.5) |
| Reversibility | NONE — transition is one-way |

### AION-EV-018 — CHARTER ISSUED

| Field | Value |
|---|---|
| Event ID | AION-EV-018 |
| Type | Charter Issuance |
| Issuer | Main analyst (under AION-EV-017 authorization) |
| Effect | AION-7.1.x mandate, constraints, non-goals, problem space, and task scaffolding established |
| Reversibility | Charter may be amended by PM determination; transition itself is not reversible |
| Artifact | This document |

---

## 12. Status Declaration

```text
AION-7.1.x CHARTER: ISSUED
AION-EV-017: REGISTERED (transition authorized, Option B)
AION-EV-018: REGISTERED (charter issued)
PHASE STATE: 7.1.x FORWARD INVESTIGATION — SCAFFOLDING READY
NEXT ACTION: Task 93 (Requirements Elicitation) — pending PM authorization to begin
P3 RETROACTIVE UPGRADE: PROHIBITED
V3 REOPENING: PROHIBITED
CASE D: PRESERVED (out of scope for 7.1.x)
NEW EVIDENCE: PERMITTED ONLY IF MATERIALLY NEW AND INDEPENDENTLY PROVENANCED
```

---

## 13. Closing Note to Next Analyst

The next analyst (IA or human) inherits:

1. **A frozen 7.0.0 record** — to be cited as boundary, never modified.
2. **An authorized 7.1.x forward investigation** — to be conducted under R-7.1.1 through R-7.1.5.
3. **A founding question** — to be answered through architecture, not through narrative.
4. **Four pillars** — to be addressed together, never in isolation.
5. **A task scaffolding** — to be refined by Task 93, not bypassed.

The next analyst is also reminded:

> The 7.0.0 boundary is a result, not a deficiency.
> The 7.1.x work is engineering, not archaeology.

---
