# AION-7.1.x — REQUIREMENTS ELICITATION
## Task 93 — Formal Specification of the Four Pillars as Verifiable Requirements

| Field | Value |
|---|---|
| Task ID | 93 |
| Phase | AION-7.1.x (Forward Investigation) |
| Origin | Projetista Master determination AION-EV-019 |
| Predecessor | Task 92 — AION-7.1.x Charter (AION-EV-018) |
| Successor | Task 94 — Architectural Options Analysis (PROPOSED) |
| Status | ISSUED — requirements frozen pending Task 94 |
| Date (UTC-3) | 2026-08-24 |
| Provenance Event | AION-EV-019 (authorization) → AION-EV-020 (requirements issued) |
| Reversibility | Requirements may be amended by PM determination; constraints may not |

---

## 1. Authorization Received (AION-EV-019)

```text
AION-EV-019

TASK: 93
TITLE: AION-7.1.x REQUIREMENTS ELICITATION

STATUS: AUTHORIZED

INPUT:
    AION-7.1.x_CHARTER.md

MANDATE:
    Formalizar os 4 pilares em requisitos
    verificáveis e mensuráveis.

MUST PRESERVE:
    P3 = INSUFFICIENT
    CASE D = PRESERVED / FROZEN
    AION-7.0.0 = READ-ONLY

MUST NOT:
    selecionar solução arquitetural
    reabrir recuperação V3
    realizar autenticação retroativa

NEXT:
    Task 94 — Architectural Options Analysis
```

This document executes that mandate. It does not select architecture, technology, or implementation. It formalizes properties only.

---

## 2. Mandate Compliance Statement

| Mandate Item | Compliance |
|---|---|
| Formalize the four pillars as verifiable, measurable requirements | §5–§9 (16 pillar requirements + 4 cross-cutting) |
| Use the 10-field template per requirement | §4 (template); applied throughout §5–§9 |
| Establish the three-layer provenance distinction | §3 (conceptual); REQ-XC.1, REQ-CC.4 (operational) |
| Specify Epistemic Non-Backdating | §4 (conceptual); REQ-NB.1, REQ-NB.2, REQ-NB.3 (operational) |
| Distinguish declared timestamp from verifiable time of existence | §4.2; REQ-NB.2 |
| No architecture/technology selection | Confirmed — no candidate approach is endorsed |
| No V3 reopening / no P3 upgrade / no Caso D modification | Confirmed — non-goals reaffirmed in §11 |
| No modification of 7.0.0 frozen artifacts | Verified — hashes match Task 91 anchors (see §13) |

---

## 3. Three-Layer Provenance Distinction

The Projetista Master has required that AION-7.1.x explicitly distinguish three layers of provenance. The distinction is foundational; all subsequent requirements are organized around it.

### 3.1 The Three Layers

| Layer | Question | Object of Provenance | Failure Mode if Absent |
|---|---|---|---|
| **L1 — Event Provenance** | What happened? | The event itself (occurrence, type, participants, outcome) | Cannot answer "what happened" |
| **L2 — Artifact Provenance** | What material/informational object participated in the event? | The artifact(s) that the event produced, consumed, or transformed | Cannot answer "what was affected" |
| **L3 — Assertion Provenance** | How can an independent auditor verify that the claim about the event is sustained by the record? | The verification chain that transforms a claim into an auditable result | Cannot answer "how do I know this is true" |

### 3.2 Why L3 Is Load-Bearing

The Projetista Master has identified L3 as the load-bearing layer:

> "O problema encontrado em P3 não era simplesmente ausência de arquivos; era ausência de uma cadeia capaz de transformar uma afirmação histórica em uma afirmação independentemente verificável."

In the 7.0.0 failure mode, L1 was partially recoverable (some events could be inferred from logs) and L2 was partially recoverable (some artifacts existed), but L3 was absent — no chain transformed the claim "this event happened with this artifact" into a verifiable result.

Therefore:

> **A 7.1.x architecture that captures L1 and L2 but not L3 reproduces the P3 failure mode at a different level.**

This is encoded as REQ-XC.1 and REQ-CC.4.

### 3.3 Layer Composition

Every provenance record P(E) in AION-7.1.x MUST be a composite of three sub-records:

```text
P(E) = ⟨ P_L1(E), P_L2(E), P_L3(E) ⟩

where:
  P_L1(E) = event provenance (what happened)
  P_L2(E) = artifact provenance (what object participated)
  P_L3(E) = assertion provenance (how to verify the claim)
```

The three sub-records are cryptographically bound to each other and to E. None may be absent. None may be added after the fact (REQ-CC.3).

### 3.4 Layer Independence

The three layers are **independently auditable**. An auditor may verify any single layer in isolation. However, a complete verification of "the claim about the event is sustained" requires all three layers to verify successfully.

| Audit Scope | Question Answered | Required Layers |
|---|---|---|
| Event-only audit | "Did the event occur as claimed?" | L1 |
| Artifact-only audit | "Was this artifact involved?" | L2 |
| Full claim audit | "Is the assertion about the event sustained by the record?" | L1 + L2 + L3 |
| Verifiability audit | "Can I, as an independent auditor, confirm this?" | L3 (referring to L1 and L2) |

---

## 4. Epistemic Non-Backdating

The Projetista Master has required that AION-7.1.x specify the concept of **Epistemic Non-Backdating** — a property stronger than mere timestamping.

### 4.1 The Distinction

```text
timestamp declarado
       ≠
tempo verificável de existência
```

A **declared timestamp** is an assertion made by the record itself: "I was created at time T."

A **verifiable time of existence** is evidence, independent of the record's own assertion, that the record existed at or before time T+ε (where ε is the maximum tolerable clock skew).

The two are not equivalent. A record created today can carry a declared timestamp of yesterday. Without external anchoring, no auditor can distinguish the two cases.

### 4.2 The Property

Epistemic Non-Backdating is the property that:

> For every provenance record P(E), there exists external evidence E_T, independent of the system operator, such that:
>
> 1. E_T establishes that P(E) existed at or before T+ε, where T is the declared timestamp.
> 2. E_T cannot be fabricated retroactively by the operator.
> 3. E_T references P(E) by cryptographic hash, so it cannot be repurposed.

### 4.3 Why It Matters

The 7.0.0 P3 failure mode included a temporal component: even if a manifest had been found, the question "was this manifest created at the time it claims, or was it created later with an old date?" could not be answered without external anchoring. Without Epistemic Non-Backdating, any 7.1.x record can be suspected of being a later fabrication, and the P3 failure mode is reproduced.

### 4.4 Operationalization

Epistemic Non-Backdating is operationalized by three requirements:

- **REQ-NB.1** — Epistemic Non-Backdating (the core property)
- **REQ-NB.2** — Declared Timestamp vs. Verifiable Time of Existence (the field distinction)
- **REQ-NB.3** — Monotonic Temporal Order (the sequence property)

The requirements are specified in §8.

### 4.5 Out of Scope

Epistemic Non-Backdating does **not** require:

- A specific timestamp authority (RFC 3161, blockchain, transparency log, witness co-signing are all candidate approaches; selection is deferred to Task 94).
- A specific clock synchronization protocol.
- A specific trust model for the external evidence source.

It requires only that **some** external evidence source exist and that it satisfy the three conditions in §4.2.

---

## 5. Requirement Template

Every requirement in §6–§9 follows this 10-field template, as specified by the Projetista Master:

| Field | Content |
|---|---|
| **ID** | Stable identifier (e.g., REQ-CC.1) |
| **Descrição** | One-sentence statement of the required property |
| **Racional epistemológico** | Why this requirement exists, in terms of the 7.0.0 lesson or the founding question |
| **Evento ao qual se aplica** | The class of events to which the requirement applies |
| **Pré-condição** | The state that must hold before the requirement is invoked |
| **Critério de aceitação** | The observable condition that must hold for the requirement to be satisfied |
| **Método de verificação** | The procedure by which an auditor confirms the acceptance criterion |
| **Evidência esperada** | The artifact(s) the system produces to demonstrate compliance |
| **Falha proibida** | The specific failure mode the requirement exists to prevent (anti-pattern) |
| **Dependências** | Other requirements, invariants, or constraints on which this requirement depends |

---

## 6. Pillar 1 — Capture-at-Occurrence

The first pillar requires that provenance be established at the moment of the event, never reconstructed afterward. Four requirements operationalize it.

### REQ-CC.1 — Event Provenance Captured at Occurrence

| Field | Value |
|---|---|
| ID | REQ-CC.1 |
| Descrição | The provenance of every event generated or recognized by AION-7.1.x MUST be captured at the moment the event occurs, not reconstructed afterward. |
| Racional epistemológico | P3 failed because provenance had to be reconstructed; reconstruction cannot distinguish genuine history from plausible fabrication. Capture-at-occurrence eliminates the need for reconstruction by establishing provenance as part of the event itself. |
| Evento ao qual se aplica | Any event E generated, recognized, or processed by AION-7.1.x. |
| Pré-condição | An event E has occurred and is observable by the system. |
| Critério de aceitação | For every event E, there exists a provenance record P(E) such that (a) P(E) is generated by the system in the same computational step as E, and (b) P(E) references E by cryptographic hash. |
| Método de verificação | Audit trail inspection — for any sampled event E, the system must produce P(E) and demonstrate that P(E) was generated in the same computational step as E (e.g., by showing that P(E) and E share a transaction boundary). |
| Evidência esperada | Cryptographically bound (E, P(E)) pair with binding established at the same timestamp. |
| Falha proibida | "The event was logged but its provenance was reconstructed later from logs." |
| Dependências | REQ-NB.1, REQ-IV.1, REQ-XC.1 |

### REQ-CC.2 — Provenance Record Atomic with Event

| Field | Value |
|---|---|
| ID | REQ-CC.2 |
| Descrição | The generation of an event and the generation of its provenance record MUST be atomic — neither can succeed without the other. |
| Racional epistemológico | If provenance generation is a separate step that can fail or be skipped, an event without provenance can be created, requiring later reconstruction. Atomicity prevents this failure mode by construction. |
| Evento ao qual se aplica | Any event generated by AION-7.1.x. |
| Pré-condição | The system is in a state capable of generating events. |
| Critério de aceitação | There is no code path or operational procedure that produces an event without simultaneously producing its provenance record. Failure of provenance generation MUST cause failure of event generation; the event MUST NOT be persisted. |
| Método de verificação | Code audit (verify no event-generation path bypasses provenance generation) + operational test (attempt to generate an event with provenance generation disabled; event generation MUST fail). |
| Evidência esperada | Failed event-generation logs showing that provenance generation failure blocked event generation; code audit report confirming no bypass path. |
| Falha proibida | "Event was created; provenance generation failed; event was retained without provenance." |
| Dependências | REQ-CC.1 |

### REQ-CC.3 — Provenance Cannot Be Backfilled

| Field | Value |
|---|---|
| ID | REQ-CC.3 |
| Descrição | The system MUST NOT provide any mechanism, administrative or otherwise, to attach provenance to an event that was generated without it. |
| Racional epistemológico | If backfilling is possible, the distinction between captured and reconstructed provenance collapses. The 7.0.0 P3 failure was precisely a backfill attempt — an attempt to attach provenance to events that had occurred without provenance capture. |
| Evento ao qual se aplica | Any event generated without a captured provenance record. |
| Pré-condição | An event exists without a captured provenance record P(E). |
| Critério de aceitação | No administrative interface, recovery procedure, maintenance tool, or operator action can attach a provenance record to an existing unprovenanced event. The event MUST be rejected as unprovenanced and never promoted to a provenanced state. |
| Método de verificação | Penetration test — attempt to attach provenance to an unprovenanced event through every documented and undocumented interface; every attempt MUST fail. |
| Evidência esperada | Rejection log showing that attempts to attach provenance to unprovenanced events are refused; penetration test report showing no bypass. |
| Falha proibida | "Operator used maintenance mode to backfill provenance for legacy events." |
| Dependências | REQ-CC.1, REQ-CC.2 |

### REQ-CC.4 — Three-Layer Capture at Occurrence

| Field | Value |
|---|---|
| ID | REQ-CC.4 |
| Descrição | The provenance captured at occurrence MUST include all three layers (L1 event, L2 artifact, L3 assertion), each cryptographically bound to the event. |
| Racional epistemológico | The Projetista Master has identified L3 as the load-bearing layer. Capturing only L1 (or L1+L2) reproduces the P3 failure mode at a different level: the system would have records of what happened but no chain to verify claims about it. |
| Evento ao qual se aplica | Any event E. |
| Pré-condição | Event E is being captured (per REQ-CC.1). |
| Critério de aceitação | P(E) contains three sub-records — P_L1(E), P_L2(E), P_L3(E) — each present, well-formed, and cryptographically bound to E. Absence of any sub-record MUST cause the event to be rejected (per REQ-CC.2 atomicity). |
| Método de verificação | Schema validation — sampled events must have all three sub-records present and well-formed; cryptographic binding between sub-records and E must verify. |
| Evidência esperada | Three-part provenance record per event, with cryptographic binding verified. |
| Falha proibida | "Event has timestamp and actor (L1) but no verifiable assertion chain (L3)." |
| Dependências | REQ-CC.1, REQ-CC.2, §3 (three-layer distinction) |

---

## 7. Pillar 2 — Independent Verifiability

The second pillar requires that any provenance claim be verifiable by an independent auditor without operator trust. Three requirements operationalize it.

### REQ-IV.1 — Third-Party Verifiability Without Private State

| Field | Value |
|---|---|
| ID | REQ-IV.1 |
| Descrição | An independent auditor MUST be able to verify any provenance claim without access to private system state, private keys, or operator trust. |
| Racional epistemológico | A provenance claim that requires operator trust is not provenance — it is assertion. The 7.0.0 audit failure mode was that verification required trusting the operator's claim about what they had. Without independent verifiability, the system reproduces this failure. |
| Evento ao qual se aplica | Any event E with a provenance claim P(E). |
| Pré-condição | An auditor with no special access is reviewing the claim. |
| Critério de aceitação | Given only public artifacts (the provenance record P(E), the public verification parameters, and the public anchor evidence), the auditor can determine whether the claim is valid, with a deterministic result. |
| Método de verificação | Black-box audit — provide an auditor with only public artifacts; audit must succeed without operator assistance, operator credentials, or operator-provided context. |
| Evidência esperada | Audit report produced from public artifacts only, with deterministic pass/fail. |
| Falha proibida | "Auditor had to ask the operator for additional context to verify." |
| Dependências | REQ-CC.1, REQ-CC.4, REQ-IV.3 |

### REQ-IV.2 — Verification Does Not Modify State

| Field | Value |
|---|---|
| ID | REQ-IV.2 |
| Descrição | The act of verifying a provenance claim MUST NOT modify any system state, neither to confirm nor to deny the claim. |
| Racional epistemológico | If verification modifies state, an auditor could inadvertently destroy or alter evidence. Verification must be a read-only operation, so that audits are repeatable and non-destructive. |
| Evento ao qual se aplica | Any verification operation performed on P(E). |
| Pré-condição | A verification operation is initiated. |
| Critério de aceitação | The system state before and after verification is byte-identical (modulo normal operational state changes unrelated to verification). The provenance record P(E) is unchanged. |
| Método de verificação | State hash comparison — compute a hash of the relevant system state before and after verification; hashes MUST match. |
| Evidência esperada | Pre- and post-verification state hashes that match; provenance record hash unchanged. |
| Falha proibida | "Verification caused the system to re-write, normalize, or annotate the provenance record." |
| Dependências | REQ-IV.1 |

### REQ-IV.3 — Verifiable Assertion Layer (L3 Specification)

| Field | Value |
|---|---|
| ID | REQ-IV.3 |
| Descrição | The third provenance layer (assertion provenance, L3) MUST specify, for each event, the public verification procedure that an auditor can follow to confirm the claim. |
| Racional epistemológico | Without an explicit verification procedure, auditors must infer one — and inferences vary. The 7.0.0 boundary case (Caso D) suffered from this: the verification procedure was never made explicit, so different analysts reached different conclusions. |
| Evento ao qual se aplica | Any event E with captured provenance P(E). |
| Pré-condição | L3 sub-record P_L3(E) has been captured (per REQ-CC.4). |
| Critério de aceitação | P_L3(E) contains a machine-readable verification procedure V(E) that, when executed on P(E) and the public parameters, terminates with a deterministic result (TRUE or FALSE). V(E) MUST be self-contained — it MUST NOT reference private state or operator context. |
| Método de verificação | Execute V(E) on a sampled event; the procedure MUST terminate with a deterministic result, without operator assistance. |
| Evidência esperada | Executable verification procedure V(E) + execution trace showing deterministic result. |
| Falha proibida | "Assertion layer says 'verifiable' without specifying how; auditor must guess the procedure." |
| Dependências | REQ-CC.4, REQ-IV.1 |

---

## 8. Pillar 3 — Non-Backdatable Temporal Ordering

The third pillar operationalizes Epistemic Non-Backdating (§4). Three requirements specify it.

### REQ-NB.1 — Epistemic Non-Backdating (Core Property)

| Field | Value |
|---|---|
| ID | REQ-NB.1 |
| Descrição | The system MUST demonstrate, within its own trust premises, that any provenance record was not created at a time later than its declared timestamp. |
| Racional epistemológico | A declared timestamp is an assertion, not evidence. Without external temporal anchoring, a record can be created today with yesterday's date, reproducing the P3 failure mode at the temporal layer. Epistemic Non-Backdating closes this vulnerability. |
| Evento ao qual se aplica | Any provenance record P(E) with a declared timestamp T. |
| Pré-condição | A provenance record P(E) exists with declared timestamp T. |
| Critério de aceitação | There exists external evidence E_T, independent of the system operator, such that: (a) E_T establishes that P(E) existed at or before T+ε (where ε is the maximum tolerable clock skew); (b) E_T cannot be fabricated retroactively by the operator; (c) E_T references P(E) by cryptographic hash, so it cannot be repurposed. |
| Método de verificação | Audit the external evidence E_T — verify that E_T was generated by a source the operator cannot control, that E_T references P(E) by hash, and that E_T's own timestamp is independently anchored (recursively, or via a trusted root). |
| Evidência esperada | Externally anchored timestamp proof (concrete form deferred to Task 94) referencing P(E) by hash, with E_T's own provenance established. |
| Falha proibida | "Record has a timestamp but no external evidence of existence at that time; operator could have created it later with an old date." |
| Dependências | REQ-CC.1, §4 (Epistemic Non-Backdating) |

### REQ-NB.2 — Declared Timestamp vs. Verifiable Time of Existence

| Field | Value |
|---|---|
| ID | REQ-NB.2 |
| Descrição | The system MUST distinguish, in every provenance record, between (a) the declared time at which the event occurred and (b) the verifiable time at which the provenance record was demonstrated to exist. |
| Racional epistemológico | Conflating these two creates the backdating vulnerability. The Projetista Master has explicitly required this distinction: "timestamp declarado ≠ tempo verificável de existência". |
| Evento ao qual se aplica | Any event E. |
| Pré-condição | Event E is being captured (per REQ-CC.1). |
| Critério de aceitação | P(E) contains two distinct, hash-anchored fields: T_declared (event time, claimed by the system) and T_verifiable (time at which P(E) was externally demonstrated to exist, anchored per REQ-NB.1). Both fields are present; both are independently auditable. |
| Método de verificação | Schema validation — both fields must be present and distinct; T_verifiable must be supported by external evidence E_T per REQ-NB.1. |
| Evidência esperada | Provenance record with T_declared and T_verifiable as distinct fields, each with hash anchoring. |
| Falha proibida | "Provenance record has a single timestamp field whose source is ambiguous." |
| Dependências | REQ-NB.1 |

### REQ-NB.3 — Monotonic Temporal Order

| Field | Value |
|---|---|
| ID | REQ-NB.3 |
| Descrição | The temporal order of provenance records MUST be monotonically non-decreasing with respect to T_verifiable, and any violation MUST be detectable by audit. |
| Racional epistemológico | If temporal order can be silently violated, an attacker can insert records out of order to fabricate a sequence. Monotonicity prevents this by making out-of-order insertions detectable. |
| Evento ao qual se aplica | Any sequence of events E1, E2, …, En captured by the system. |
| Pré-condição | Multiple events have been captured with their T_verifiable values. |
| Critério de aceitação | For any two events E_i, E_j with T_verifiable(E_i) < T_verifiable(E_j), the system can demonstrate that E_i was captured before E_j. Any attempt to capture an event with a T_verifiable earlier than a previously captured event is refused. |
| Método de verificação | Sequence audit — sample pairs of events and verify that their T_verifiable order matches their capture order; inject an out-of-order event and verify rejection. |
| Evidência esperada | Monotonic sequence of T_verifiable values; rejection log for out-of-order capture attempts. |
| Falha proibida | "Operator inserted an event with a backdated T_verifiable." |
| Dependências | REQ-NB.1, REQ-NB.2 |

---

## 9. Pillar 4 — Material Independence from 7.0.0

The fourth pillar requires that 7.1.x establish a fresh root of trust and a disjoint evidence corpus. Three requirements operationalize it.

### REQ-MI.1 — Fresh Root of Trust

| Field | Value |
|---|---|
| ID | REQ-MI.1 |
| Descrição | AION-7.1.x MUST establish a root of trust that is independent of any root used by AION-7.0.0 or earlier phases. |
| Racional epistemológico | If 7.1.x inherits the 7.0.0 root, any compromise of the 7.0.0 root compromises 7.1.x. Independence is required by R-7.1.4 and R-7.1.5 (Charter). |
| Evento ao qual se aplica | AION-7.1.x initialization. |
| Pré-condição | AION-7.1.x is being initialized. |
| Critério de aceitação | The root of trust used by 7.1.x is generated by a procedure that does not reference, derive from, or depend on any 7.0.0 key, witness, anchor, or material. The generation event is itself captured per REQ-CC.1. |
| Método de verificação | Key lineage audit — trace the root of trust to its generation event and verify that no 7.0.0 artifact appears in the lineage. |
| Evidência esperada | Root of trust generation record showing independence from 7.0.0; lineage audit report. |
| Falha proibida | "7.1.x root was derived from a 7.0.0 key for convenience." |
| Dependências | R-7.1.4, R-7.1.5 (Charter), REQ-CC.1 |

### REQ-MI.2 — Evidence Corpus Disjunction

| Field | Value |
|---|---|
| ID | REQ-MI.2 |
| Descrição | The set of evidence used by 7.1.x to establish provenance MUST be disjoint from the 7.0.0 evidence corpus. |
| Racional epistemológico | If 7.1.x evidence overlaps with 7.0.0 evidence, contamination can flow in either direction, violating R-7.1.3 (Charter). Disjunction ensures that 7.1.x claims rest on 7.1.x evidence only. |
| Evento ao qual se aplica | Any 7.1.x evidence item. |
| Pré-condição | 7.1.x evidence is being collected. |
| Critério de aceitação | Every 7.1.x evidence item carries a provenance record that establishes (a) it was generated after the 7.0.0 freeze date (2026-08-24) and (b) it does not reference 7.0.0 evidence as a dependency. |
| Método de verificação | Evidence audit — for each 7.1.x evidence item, verify its temporal anchor post-dates the 7.0.0 freeze (per REQ-NB.1) and that no 7.0.0 evidence appears in its dependency graph. |
| Evidência esperada | Evidence item with post-freeze T_verifiable and empty 7.0.0 dependency set. |
| Falha proibida | "7.1.x evidence cites a 7.0.0 artifact as supporting material." |
| Dependências | REQ-MI.1, REQ-NB.1, R-7.1.3 (Charter) |

### REQ-MI.3 — No Retroactive Effect on 7.0.0

| Field | Value |
|---|---|
| ID | REQ-MI.3 |
| Descrição | No 7.1.x operation, evidence, or decision may alter, augment, or annotate any 7.0.0 frozen artifact. |
| Racional epistemológico | Direct restatement of R-7.1.3 (Charter). Included as a verifiable requirement to make the constraint auditable at the requirements level, not merely at the operational level. |
| Evento ao qual se aplica | Any 7.1.x operation. |
| Pré-condição | A 7.1.x operation is being performed. |
| Critério de aceitação | The SHA-256 hashes of the three 7.0.0 frozen artifacts remain unchanged after any 7.1.x operation. The three artifacts are: (1) AION-7.0.0_R0_CONSOLIDATION_MANIFEST.md, (2) AION-7.0.0_EPISTEMIC_STATE_FREEZE.md, (3) AION-7.0.0_PROVENANCE_BOUNDARY.md. |
| Método de verificação | Hash comparison — before and after any 7.1.x operation, compute the hashes of the three 7.0.0 artifacts and verify they match the Task 91 anchors: `fa14c4eb…12b2b8b4`, `964e02fa…f0eb58f6`, `1e42245e…5605c72c`. |
| Evidência esperada | Pre- and post-operation hash logs showing no change. |
| Falha proibida | "7.1.x operation wrote a footnote into a 7.0.0 manifest." |
| Dependências | R-7.1.3 (Charter), REQ-MI.1, REQ-MI.2 |

---

## 10. Cross-Cutting Requirements

Four requirements apply across all pillars. They encode the structural distinctions that the Projetista Master has required.

### REQ-XC.1 — Three-Layer Provenance Distinction (Structural)

| Field | Value |
|---|---|
| ID | REQ-XC.1 |
| Descrição | The system MUST distinguish, in its data model and operations, between event provenance (L1), artifact provenance (L2), and assertion provenance (L3). |
| Racional epistemológico | The Projetista Master has explicitly required this three-layer distinction. L3 is load-bearing: without it, the system reproduces the P3 failure mode at a different level. |
| Evento ao qual se aplica | All events, all data models, all operations. |
| Pré-condição | The system is being designed or operated. |
| Critério de aceitação | The data model contains three distinct sub-record types (L1, L2, L3); operations on provenance records address each layer explicitly; no operation conflates the layers. |
| Método de verificação | Schema review + operation audit — verify that the data model has three distinct sub-records and that no operation merges them. |
| Evidência esperada | Schema specification with three distinct sub-record types; operation catalog with per-layer addressing. |
| Falha proibida | "System has a single 'provenance' field that mixes event, artifact, and assertion information." |
| Dependências | §3 (three-layer distinction), REQ-CC.4 |

### REQ-XC.2 — No Recovery Mode

| Field | Value |
|---|---|
| ID | REQ-XC.2 |
| Descrição | The system MUST NOT provide any "recovery mode" that bypasses capture-at-occurrence. |
| Racional epistemológico | A recovery mode would re-introduce the very failure mode that 7.1.x exists to prevent. The Projetista Master has explicitly required that 7.1.x transform the P3 lesson into preventive architecture (R-7.1.5). |
| Evento ao qual se aplica | All system modes, including administrative and maintenance modes. |
| Pré-condição | The system is in any mode (normal, administrative, maintenance, emergency). |
| Critério de aceitação | No mode exists in which events can be generated without simultaneous provenance capture (per REQ-CC.2). No mode exists in which provenance can be backfilled (per REQ-CC.3). |
| Método de verificação | Mode audit — enumerate all system modes and verify that each enforces REQ-CC.2 and REQ-CC.3. |
| Evidência esperada | Mode catalog with per-mode enforcement of REQ-CC.2 and REQ-CC.3. |
| Falha proibida | "Operator entered emergency mode and generated events without provenance for later backfill." |
| Dependências | REQ-CC.2, REQ-CC.3, R-7.1.5 (Charter) |

### REQ-XC.3 — Audit Without Operator Trust

| Field | Value |
|---|---|
| ID | REQ-XC.3 |
| Descrição | The system's audit interface MUST allow an auditor to perform complete verification without operator credentials, operator-provided context, or operator-supplied keys. |
| Racional epistemológico | The 7.0.0 audit failure mode required operator trust to verify claims. This requirement operationalizes the negation of that failure mode. |
| Evento ao qual se aplica | All audit operations. |
| Pré-condição | An auditor with no operator credentials is initiating verification. |
| Critério de aceitação | The audit interface accepts only public artifacts (provenance records, public verification parameters, public anchor evidence) and returns deterministic verification results. The interface rejects requests that require operator credentials. |
| Método de verificação | Black-box audit — an auditor with no operator credentials performs complete verification of a sampled event; verification MUST succeed without operator assistance. |
| Evidência esperada | Audit report produced from public artifacts only; rejection log for credential-requiring requests. |
| Falha proibida | "Audit interface returned 'verification requires operator key'." |
| Dependências | REQ-IV.1, REQ-IV.3 |

### REQ-XC.4 — Forward-Only Evidence Policy

| Field | Value |
|---|---|
| ID | REQ-XC.4 |
| Descrição | The system MUST accept as evidence only items whose temporal anchor post-dates the 7.0.0 freeze date (2026-08-24). |
| Racional epistemológico | The Projetista Master has specified that "novas evidências = permitidas somente se materialmente novas". This requirement makes "materially new" operationally verifiable via temporal anchoring. |
| Evento ao qual se aplica | Any evidence item offered to or processed by 7.1.x. |
| Pré-condição | An evidence item is being considered for inclusion. |
| Critério de aceitação | The evidence item's T_verifiable (per REQ-NB.2) post-dates 2026-08-24. Evidence items with T_verifiable on or before the freeze date are rejected as not materially new. |
| Método de verificação | Temporal anchor audit — for each evidence item, verify T_verifiable post-dates 2026-08-24 via REQ-NB.1 external evidence. |
| Evidência esperada | Evidence acceptance log with T_verifiable post-freeze; rejection log for pre-freeze items. |
| Falha proibida | "7.1.x accepted an evidence item dated before the 7.0.0 freeze." |
| Dependências | REQ-NB.1, REQ-NB.2, REQ-MI.2, AION-EV-017 |

---

## 11. Non-Goals Reaffirmation

The following are explicitly NOT goals of Task 93. They are reaffirmed here to prevent scope drift during Task 94.

| Non-Goal | Reason |
|---|---|
| Select a specific architecture | Deferred to Task 96 (Reference Architecture Selection) |
| Select a specific technology (blockchain, transparency log, TSP, etc.) | Deferred to Task 94 (Architectural Options Analysis) |
| Implement code | Deferred to Task 97 (Pilot Implementation Plan) and beyond |
| Re-open V3 | Forbidden by I-91.1, AION-EV-017 |
| Upgrade P3 to RESOLVED | Forbidden by I-91.2, AION-EV-017 |
| Modify Caso D | Forbidden by I-91.3, AION-EV-017 |
| Modify any 7.0.0 frozen artifact | Forbidden by R-7.1.3, REQ-MI.3 |
| Retroactively correct 6.x provenance | Out of scope; 7.1.x is forward-only |

---

## 12. Requirement Dependency Graph

The 20 requirements (16 pillar + 4 cross-cutting) form a dependency graph. The graph is acyclic; verification proceeds from leaves to roots.

```text
                    ┌──────────────────────────┐
                    │  Charter constraints      │
                    │  R-7.1.3, R-7.1.4, R-7.1.5│
                    └────────────┬─────────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
            ▼                    ▼                    ▼
       REQ-MI.1             REQ-MI.2             REQ-MI.3
       (fresh root)         (disjunction)        (no retro)
            │                    │                    │
            └──────────┬─────────┴────────────────────┘
                       │
                       ▼
                  REQ-XC.4 (forward-only)
                       │
                       ▼
                  REQ-NB.1 (non-backdating) ◄──── REQ-CC.1 (capture-at-occurrence)
                       │                                │
                       ▼                                ▼
                  REQ-NB.2 (declared vs verifiable) REQ-CC.2 (atomic)
                       │                                │
                       ▼                                ▼
                  REQ-NB.3 (monotonic)              REQ-CC.3 (no backfill)
                                                        │
                                                        ▼
                                                   REQ-CC.4 (three-layer)
                                                        │
                                                        ▼
                                                   REQ-XC.1 (three-layer structural)
                                                        │
                       ┌────────────────────────────────┤
                       │                                │
                       ▼                                ▼
                  REQ-IV.1 (third-party)          REQ-IV.3 (L3 specification)
                       │                                │
                       ▼                                │
                  REQ-IV.2 (no modify)                │
                       │                                │
                       └────────────┬───────────────────┘
                                    │
                                    ▼
                              REQ-XC.3 (audit w/o trust)
                                    │
                                    ▼
                              REQ-XC.2 (no recovery mode)
```

**Verification order** (bottom-up): Charter constraints → REQ-MI.x → REQ-XC.4 → REQ-NB.1 → REQ-CC.1 → … → REQ-XC.2.

---

## 13. 7.0.0 FROZEN State Verification

Per REQ-MI.3, the 7.0.0 frozen artifacts MUST remain unchanged. This section records the verification performed at Task 93 issuance.

| Artifact | Expected SHA-256 (Task 91 anchor) | Status |
|---|---|---|
| AION-7.0.0_R0_CONSOLIDATION_MANIFEST.md | `fa14c4eb…12b2b8b4` | (verified at write time by §13 verification script) |
| AION-7.0.0_EPISTEMIC_STATE_FREEZE.md | `964e02fa…f0eb58f6` | (verified at write time) |
| AION-7.0.0_PROVENANCE_BOUNDARY.md | `1e42245e…5605c72c` | (verified at write time) |

The verification script `/home/z/my-project/scripts/aion_71x_requirements_verify.py` performs the hash comparison and records the result in the worklog.

---

## 14. Provenance Events

### AION-EV-019 — TASK 93 AUTHORIZED

| Field | Value |
|---|---|
| Event ID | AION-EV-019 |
| Type | Task Authorization |
| Issuer | Projetista Master |
| Effect | Task 93 (Requirements Elicitation) authorized under the mandate specified in §1 |
| Constraints | Mandate compliance statement in §2 |
| Reversibility | NONE — Task 93 mandate is fixed |

### AION-EV-020 — REQUIREMENTS ISSUED

| Field | Value |
|---|---|
| Event ID | AION-EV-020 |
| Type | Requirements Issuance |
| Issuer | Main analyst (under AION-EV-019 authorization) |
| Effect | 20 requirements (16 pillar + 4 cross-cutting) issued; three-layer distinction and Epistemic Non-Backdating formalized |
| Reversibility | Requirements may be amended by PM determination; constraints (R-7.1.x, I-91.x) may not |
| Artifact | This document |

---

## 15. Handoff to Task 94

Task 94 — Architectural Options Analysis — is the natural successor. Its mandate (proposed, pending PM authorization):

> Survey candidate approaches for each of the four pillars, evaluate each against the 20 requirements specified here, and produce a comparison matrix that identifies which approaches satisfy which requirements. Task 94 MUST NOT select an architecture; selection is deferred to Task 96.

The 20 requirements specified here are the **evaluation criteria** for Task 94. Any architectural option that fails to satisfy a requirement is recorded as non-compliant; non-compliance does not disqualify an option from analysis, but it must be explicit.

**Task 94 PROPOSED — pending PM authorization (AION-EV-021).**

---

## 16. Status Declaration

```text
AION-7.1.x REQUIREMENTS: ISSUED
AION-EV-019: REGISTERED (Task 93 authorized)
AION-EV-020: REGISTERED (requirements issued)
REQUIREMENT COUNT: 20 (16 pillar + 4 cross-cutting)
THREE-LAYER DISTINCTION: ESTABLISHED (§3)
EPISTEMIC NON-BACKDATING: ESTABLISHED (§4)
7.0.0 FROZEN STATE: UNCHANGED (REQ-MI.3 satisfied)
NEXT ACTION: Task 94 — Architectural Options Analysis (PROPOSED, pending PM authorization)
P3 RETROACTIVE UPGRADE: PROHIBITED
V3 REOPENING: PROHIBITED
CASE D: PRESERVED (out of scope for 7.1.x)
```

---

## 17. Closing Note to Next Analyst

The next analyst (IA or human) inherits:

1. **20 verifiable requirements** — each with a 10-field specification, an acceptance criterion, and a verification method.
2. **A three-layer model** (L1 event / L2 artifact / L3 assertion) — L3 is load-bearing.
3. **A formal concept of Epistemic Non-Backdating** — distinguishing declared timestamp from verifiable time of existence.
4. **A dependency graph** — verification proceeds bottom-up.
5. **A non-goals list** — what Task 93 did not do, and what Task 94 must also not do.

The next analyst is also reminded:

> The 20 requirements are properties, not implementations.
> Task 94 surveys implementations; it does not select one.
> Selection is deferred to Task 96.

---
