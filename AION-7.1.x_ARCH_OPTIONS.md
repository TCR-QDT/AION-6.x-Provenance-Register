# AION-7.1.x — ARCHITECTURAL OPTIONS ANALYSIS
## Task 94 — Survey of Candidate Mechanism Classes Against the 20 Requirements

| Field | Value |
|---|---|
| Task ID | 94 |
| Phase | AION-7.1.x (Forward Investigation) |
| Origin | Projetista Master determination AION-EV-021 |
| Predecessor | Task 93 — Requirements Elicitation (AION-EV-020) |
| Successor | Task 95 — Threat Model (PROPOSED) |
| Status | ISSUED — analysis complete, no selection made |
| Date (UTC-3) | 2026-08-24 |
| Provenance Event | AION-EV-021 (authorization) → AION-EV-022 (analysis issued) |
| Reversibility | Analysis may be amended; constraints may not |

---

## 1. Authorization Received (AION-EV-021)

```text
AION-EV-021

TASK: 94
TITLE: AION-7.1.x ARCHITECTURAL OPTIONS ANALYSIS

STATUS: AUTHORIZED

INPUT:
    AION-7.1.x_CHARTER
    AION-7.1.x_REQUIREMENTS

SCOPE:
    4 pilares
    20 requisitos
    L1 / L2 / L3
    Epistemic Non-Backdating

OUTPUT:
    Architectural Options Matrix
    Compliance Assessment
    Trust Model
    Strengths / Weaknesses
    Failure Modes
    Trade-offs
    Open Questions

MUST NOT:
    selecionar arquitetura
    implementar solução
    reabrir V3
    alterar P3
    alterar Caso D
    modificar AION-7.0.0

SELECTION:
    DEFERRED TO TASK 96
```

This document executes that mandate. It surveys 8 classes of candidate mechanisms, evaluates each against the 20 requirements of Task 93, and produces a compliance matrix. It does **not** select an architecture.

---

## 2. The Central Methodological Distinction

The Projetista Master has required that the analysis maintain a strict distinction:

```text
PROPRIEDADE TECNOLÓGICA        ≠        GARANTIA EPISTÊMICA
```

| Technological Property | (Does NOT imply) | Epistemic Guarantee |
|---| ≠ | ---|
| Has a timestamp | ≠ | Prevents backdating |
| Has a hash | ≠ | Proves prior existence |
| Is append-only | ≠ | Is independently verifiable |
| Is on a blockchain | ≠ | Has sufficient provenance |
| Uses hardware attestation | ≠ | Resolves the L1/L2/L3 chain |

This distinction governs the entire analysis. A class of mechanisms is **compliant** with a requirement only if it provides the epistemic guarantee the requirement demands — not merely the technological property that superficially resembles it.

### 2.1 The Compliance Test

For each (class, requirement) pair, the analysis asks:

> Does this class provide the **epistemic guarantee** required, or merely the **technological property** that resembles it?

Three outcomes are possible:

| Outcome | Symbol | Meaning |
|---|---|---|
| Compliant | `✓` | The class provides the epistemic guarantee under its stated trust model. |
| Conditional | `≈` | The class provides the guarantee only under additional assumptions (which must be stated). |
| Non-Compliant | `✗` | The class provides the technological property but not the epistemic guarantee; or does not address the requirement. |

The `≈` outcome is the most dangerous: it is where the technological-property / epistemic-guarantee confusion lives. Every `≈` in the matrix is accompanied by a statement of the additional assumption required to promote it to `✓`.

---

## 3. Classes of Candidate Mechanisms

Eight classes are surveyed. They are not endorsed; they are analyzed.

| Class ID | Name | One-line description |
|---|---|---|
| C1 | Append-only log + hash chaining | Local append-only sequence where each entry hashes the previous |
| C2 | RFC 3161 / Trusted Timestamping | External timestamp authority signs a hash, anchoring it in time |
| C3 | Witness co-signing | Multiple independent parties co-sign each event at occurrence |
| C4 | Transparency logs | Public append-only log with merkle proofs and third-party monitoring |
| C5 | Blockchain anchoring | Anchoring event hashes in a public/consensus blockchain |
| C6 | Hardware-rooted attestation | Hardware TPM/TEE attests to event capture at occurrence |
| C7 | Zero-knowledge attestation | Cryptographic proofs that verification succeeds without revealing private state |
| C8 | Quorum / multi-witness | A quorum of independent witnesses must agree an event occurred |

Classes may be combined in actual architectures; this analysis treats them in isolation to expose their individual guarantees and limits. Combination analysis is deferred to Task 96 (Reference Architecture Selection).

---

## 4. Trust Model Summary per Class

Each class operates under a distinct trust model. The trust model determines what an auditor must assume to accept the class's claims.

| Class | Trust Root | What Auditor Must Trust | Failure if Trust Root Compromised |
|---|---|---|---|
| C1 | Local operator | Operator did not rewrite the log | Entire sequence forgeable |
| C2 | Timestamp Authority (TSA) | TSA's clock and signature | Backdating possible |
| C3 | Set of witnesses | Each witness is independent and honest at signing time | Colluding witnesses can fabricate events |
| C4 | Log operator + monitors | Log operator cannot forge without a monitor detecting | Forgeable if all monitors are absent |
| C5 | Consensus protocol | Consensus protocol's liveness and safety | Reorg/backdating if consensus fails |
| C6 | Hardware manufacturer | Hardware attestation key is unextractable | Attestations forgeable if key extracted |
| C7 | Cryptographic assumptions + setup | Setup parameters were generated honestly | Soundness fails if setup compromised |
| C8 | Quorum threshold | No coalition ≥ threshold is malicious | False events accepted if coalition forms |

The trust model is **not** a property of the class alone — it depends on deployment context. Where the deployment context materially affects the trust model, the analysis notes the dependency.

---

## 5. Detailed Class Analyses

Each class is analyzed against the 20 requirements of Task 93. The 10-field template of Task 93 is not repeated per requirement here (it would multiply to 160 entries); instead, each class is given a structured analysis covering:

- Mechanism summary
- Trust model
- Compliance against each pillar (with the `✓`/`≈`/`✗` outcomes and rationale)
- Failure modes
- Strengths
- Weaknesses
- Open questions

---

### 5.1 Class C1 — Append-only Log + Hash Chaining

**Mechanism summary**: Events are written to a log where each entry contains the hash of the previous entry. The log is stored on durable media. Reads return entries with their predecessor hashes.

**Trust model**: Trust root is the local operator. Auditor must trust the operator did not rewrite the log. No external anchoring.

**Pillar 1 — Capture-at-Occurrence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-CC.1 | `✓` | Capture at occurrence is achievable if the log is the system of record. |
| REQ-CC.2 | `✓` | Atomicity is achievable if event generation and log append are in the same transaction. |
| REQ-CC.3 | `✗` | **No technical barrier prevents the operator from rewriting the log from a chosen point.** "Append-only" is a property the operator claims, not a guarantee the mechanism enforces against the operator. |
| REQ-CC.4 | `✓` | Three-layer capture is achievable if the log entry schema includes L1/L2/L3 sub-records. |

**Pillar 2 — Independent Verifiability**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-IV.1 | `✗` | An auditor with only public artifacts cannot verify: the log is held by the operator, and the operator controls what is shown. The property "append-only" cannot be verified from a single snapshot. |
| REQ-IV.2 | `✓` | Verification (hash chain check) does not modify state. |
| REQ-IV.3 | `≈` | L3 specification is achievable, but the verification procedure includes the step "trust that the operator showed the full log", which is not a deterministic step. |

**Pillar 3 — Non-Backdatable Temporal Ordering**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-NB.1 | `✗` | **No external evidence of existence.** The hash chain proves sequence but not time. An operator can rewrite the entire log today and the chain is internally consistent. |
| REQ-NB.2 | `✗` | No verifiable time of existence distinct from declared time. |
| REQ-NB.3 | `≈` | Monotonicity holds *within* the log as currently presented, but cannot be verified against historical snapshots. |

**Pillar 4 — Material Independence from 7.0.0**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-MI.1 | `✓` | Fresh root of trust is achievable (new log, new keys). |
| REQ-MI.2 | `✓` | Evidence corpus disjunction is achievable (no 7.0.0 references required). |
| REQ-MI.3 | `✓` | No modification of 7.0.0 artifacts. |

**Cross-cutting**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-XC.1 | `✓` | Three-layer distinction is achievable in the schema. |
| REQ-XC.2 | `✗` | "Recovery mode" is trivially implementable (rewrite the log); the class provides no barrier. |
| REQ-XC.3 | `✗` | Audit requires operator-provided log; fails the no-trust audit test. |
| REQ-XC.4 | `✓` | Forward-only evidence policy is achievable at the policy level. |

**Failure modes**:
- Operator rewrites log from a chosen point (silent).
- Operator presents a subset of the log to an auditor (selective disclosure).
- Log is lost; no recovery is possible without reconstruction (which is forbidden).

**Strengths**: Simple; cheap; well-understood; good for internal accountability.

**Weaknesses**: Provides no guarantees against the operator; reproduces the P3 failure mode if the operator is the only source.

**Open questions**:
- Can C1 be combined with an external anchor (C2, C4, C5) to close REQ-NB.1 and REQ-IV.1? (Yes — but combination analysis is deferred to Task 96.)

---

### 5.2 Class C2 — RFC 3161 / Trusted Timestamping

**Mechanism summary**: For each event, the system sends the event's hash to a Trusted Timestamp Authority (TSA). The TSA returns a signed timestamp token asserting that it received the hash at time T. The token is stored with the event.

**Trust model**: Trust root is the TSA. Auditor must trust the TSA's clock, the TSA's signature, and the TSA's non-collusion with the operator.

**Pillar 1 — Capture-at-Occurrence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-CC.1 | `≈` | Capture-at-occurrence is achievable, but requires the TSA round-trip to complete before the event is considered captured. If the TSA is offline, capture fails. |
| REQ-CC.2 | `≈` | Atomicity is achievable but bounded by TSA availability. |
| REQ-CC.3 | `✓` | Backfilling is detectable: a backfilled event would need a TSA token dated after the claimed event time, which is visible to the auditor. |
| REQ-CC.4 | `✓` | Three-layer capture is achievable. |

**Pillar 2 — Independent Verifiability**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-IV.1 | `✓` | An auditor with the TSA's public key and the timestamp token can verify the token signature and timestamp without operator assistance. |
| REQ-IV.2 | `✓` | Verification is read-only. |
| REQ-IV.3 | `✓` | L3 specification is well-defined: verify token signature, verify token timestamp ≥ declared timestamp, verify token hash matches event hash. |

**Pillar 3 — Non-Backdatable Temporal Ordering**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-NB.1 | `✓` | The TSA token is external evidence of existence at time T. The operator cannot fabricate it without TSA collusion. |
| REQ-NB.2 | `✓` | Distinct fields: T_declared (event time) and T_verifiable (TSA token time). |
| REQ-NB.3 | `≈` | Monotonicity holds per event but is not enforced across events by the TSA. A separate sequence mechanism is needed. |

**Pillar 4 — Material Independence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-MI.1 | `≈` | Fresh root achievable, but the TSA itself is a shared root. If 7.0.0 also used the same TSA, independence is partial. |
| REQ-MI.2 | `✓` | Evidence corpus disjunction achievable. |
| REQ-MI.3 | `✓` | No modification of 7.0.0. |

**Cross-cutting**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-XC.1 | `✓` | Three-layer distinction achievable. |
| REQ-XC.2 | `≈` | No recovery mode *via timestamp*, but events without timestamps can still be created if capture fails. |
| REQ-XC.3 | `✓` | Audit possible with only public TSA key and the token. |
| REQ-XC.4 | `✓` | Forward-only policy achievable. |

**Failure modes**:
- TSA is offline at capture time → event cannot be captured (liveness).
- TSA colludes with operator → backdating possible (trust).
- TSA key compromise → all tokens issued by that key become untrustworthy (key management).

**Strengths**: Provides genuine external temporal anchoring; well-standardized (RFC 3161); lightweight.

**Weaknesses**: Single point of trust in the TSA; liveness depends on TSA availability; does not address sequence/monotonicity by itself.

**Open questions**:
- Can multiple TSAs be used in parallel to reduce single-TSA trust? (Yes — combination with C8 quorum.)
- What happens to old tokens when a TSA key is rotated or compromised? (Requires a key-management policy, deferred to Task 96.)

---

### 5.3 Class C3 — Witness Co-Signing

**Mechanism summary**: For each event, the system sends the event hash to a set of independent witnesses. Each witness signs the hash with its own key. The set of signatures is stored with the event.

**Trust model**: Trust root is the set of witnesses. Auditor must trust that (a) the witnesses are independent, (b) they were honest at signing time, and (c) the threshold of signatures required is met.

**Pillar 1 — Capture-at-Occurrence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-CC.1 | `≈` | Capture-at-occurrence achievable but requires witness quorum to respond synchronously. |
| REQ-CC.2 | `≈` | Atomicity bounded by witness availability. |
| REQ-CC.3 | `✓` | Backfilling detectable: a backfilled event would need fresh witness signatures, which are time-stamped (or otherwise anchored). |
| REQ-CC.4 | `✓` | Three-layer capture achievable. |

**Pillar 2 — Independent Verifiability**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-IV.1 | `✓` | Auditor with witness public keys can verify signatures independently. |
| REQ-IV.2 | `✓` | Verification is read-only. |
| REQ-IV.3 | `✓` | L3 specification: verify each witness signature, verify threshold met, verify witness set is the canonical set. |

**Pillar 3 — Non-Backdatable Temporal Ordering**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-NB.1 | `≈` | External evidence of existence is provided *if* the witnesses also timestamp their signatures (otherwise they only attest to the hash, not to when). Without timestamps, signatures prove "existed at some point" but not "existed at T". |
| REQ-NB.2 | `≈` | Distinct fields achievable if witnesses timestamp; otherwise conflated. |
| REQ-NB.3 | `✗` | No sequence guarantee across events. |

**Pillar 4 — Material Independence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-MI.1 | `✓` | Fresh witness set achievable. |
| REQ-MI.2 | `✓` | Disjunction achievable. |
| REQ-MI.3 | `✓` | No modification of 7.0.0. |

**Cross-cutting**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-XC.1 | `✓` | Three-layer distinction achievable. |
| REQ-XC.2 | `≈` | Recovery mode not blocked unless witnesses refuse to sign backfilled events. |
| REQ-XC.3 | `✓` | Audit possible with witness public keys only. |
| REQ-XC.4 | `✓` | Forward-only achievable. |

**Failure modes**:
- Witness coalition ≥ threshold → false events accepted.
- Witness set is not actually independent (e.g., all controlled by same party) → trust model collapses to single-operator.
- Witnesses refuse to sign → capture fails (liveness).

**Strengths**: Distributes trust across multiple parties; supports threshold policies.

**Weaknesses**: Requires witness availability at capture time; independence must be verified externally; does not by itself provide temporal anchoring.

**Open questions**:
- How is witness independence established and verified? (Requires an external registry, possibly itself a transparency log.)
- Can witness signatures be combined with C2 timestamps to close REQ-NB.1? (Yes.)

---

### 5.4 Class C4 — Transparency Logs

**Mechanism summary**: A public append-only log (e.g., Certificate Transparency) where entries are visible to anyone. Monitors watch the log and detect inconsistencies. Clients request merkle inclusion proofs.

**Trust model**: Trust root is the log operator + a non-colluding monitor. Auditor must trust that (a) the log operator cannot forge without detection and (b) at least one honest monitor is watching.

**Pillar 1 — Capture-at-Occurrence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-CC.1 | `✓` | Capture at occurrence achievable if event submission to the log is part of the event-generation step. |
| REQ-CC.2 | `≈` | Atomicity bounded by log submission latency. |
| REQ-CC.3 | `✓` | Backfilling is detectable: a backfilled entry would appear in the log at a position inconsistent with other entries' timestamps. |
| REQ-CC.4 | `✓` | Three-layer capture achievable. |

**Pillar 2 — Independent Verifiability**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-IV.1 | `✓` | Auditor can request inclusion proofs from the log and verify them with public parameters. |
| REQ-IV.2 | `✓` | Verification is read-only. |
| REQ-IV.3 | `✓` | L3 specification: verify inclusion proof, verify merkle root is published, verify monitor did not flag inconsistency. |

**Pillar 3 — Non-Backdatable Temporal Ordering**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-NB.1 | `✓` | The published merkle root is external evidence of existence. The operator cannot fabricate a merkle root without a monitor detecting. |
| REQ-NB.2 | `✓` | Distinct fields achievable: T_declared (event) vs. T_verifiable (merkle root publication time). |
| REQ-NB.3 | `✓` | Monotonicity enforced by the log's append-only structure with merkle roots. |

**Pillar 4 — Material Independence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-MI.1 | `✓` | Fresh log achievable. |
| REQ-MI.2 | `✓` | Disjunction achievable. |
| REQ-MI.3 | `✓` | No modification of 7.0.0. |

**Cross-cutting**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-XC.1 | `✓` | Three-layer distinction achievable. |
| REQ-XC.2 | `≈` | Recovery mode partially mitigated: backfilled entries would be detected, but the log operator could refuse to log certain events. |
| REQ-XC.3 | `✓` | Audit possible with public log access. |
| REQ-XC.4 | `✓` | Forward-only achievable. |

**Failure modes**:
- Log operator and all monitors collude → forgeable.
- Log operator withholds entries (selective disclosure) → audit may not detect missing events.
- Split-view attack: log operator presents different views to different monitors.

**Strengths**: Strong external anchoring; supports public verifiability; mature technology (Certificate Transparency).

**Weaknesses**: Requires active monitors; depends on gossip between monitors; liveness bounded by log submission.

**Open questions**:
- Who operates the monitor(s) for AION-7.1.x? (Operational question, deferred to Task 96/97.)
- What is the maximum tolerable delay between event capture and log inclusion? (Performance question.)

---

### 5.5 Class C5 — Blockchain Anchoring

**Mechanism summary**: Event hashes are anchored in a public blockchain (e.g., by submitting a transaction whose data field contains the hash). The blockchain's consensus protocol provides temporal ordering and immutability.

**Trust model**: Trust root is the blockchain's consensus protocol. Auditor must trust (a) the consensus protocol's safety and liveness and (b) the absence of chain reorganizations deeper than the confirmation threshold.

**Pillar 1 — Capture-at-Occurrence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-CC.1 | `≈` | Capture achievable, but the blockchain's block interval (e.g., 10 minutes for Bitcoin) means "occurrence" is rounded to block boundaries. |
| REQ-CC.2 | `≈` | Atomicity bounded by block inclusion latency. |
| REQ-CC.3 | `✓` | Backfilling detectable: a backfilled anchor would appear in a later block. |
| REQ-CC.4 | `✓` | Three-layer capture achievable. |

**Pillar 2 — Independent Verifiability**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-IV.1 | `✓` | Auditor can verify the on-chain transaction and the inclusion of the event hash. |
| REQ-IV.2 | `✓` | Verification is read-only. |
| REQ-IV.3 | `✓` | L3 specification: verify transaction inclusion, verify block confirmation depth, verify hash match. |

**Pillar 3 — Non-Backdatable Temporal Ordering**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-NB.1 | `✓` | The blockchain's block timestamp is external evidence of existence (within the block interval). |
| REQ-NB.2 | `✓` | Distinct fields achievable. |
| REQ-NB.3 | `✓` | Monotonicity enforced by the chain's block sequence. |

**Pillar 4 — Material Independence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-MI.1 | `✓` | Fresh root achievable. |
| REQ-MI.2 | `✓` | Disjunction achievable. |
| REQ-MI.3 | `✓` | No modification of 7.0.0. |

**Cross-cutting**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-XC.1 | `✓` | Three-layer distinction achievable. |
| REQ-XC.2 | `≈` | Recovery mode partially mitigated (backfilled anchors detected), but if capture fails (chain congestion), events may be queued without provenance. |
| REQ-XC.3 | `✓` | Audit possible with public chain access. |
| REQ-XC.4 | `✓` | Forward-only achievable. |

**Failure modes**:
- Chain reorganization deeper than confirmation threshold → anchored events may be reversed.
- Chain congestion → capture latency increases; events may be queued (violating REQ-CC.1).
- 51% attack (or equivalent for the chosen chain) → entire history forgeable.
- Cost: anchoring every event on-chain may be prohibitively expensive.

**Strengths**: Strong external anchoring; no single operator to trust; publicly verifiable.

**Weaknesses**: Latency (block interval); cost; dependence on chain liveness; not suitable for high-frequency events.

**Open questions**:
- Should anchoring be per-event or per-batch (e.g., merkle root of many events per block)? (Trade-off: per-batch reduces cost but increases capture latency.)
- Which chain? (Selection deferred to Task 96.)

**Critical distinction**: "Is on a blockchain" ≠ "has sufficient provenance". A blockchain anchor proves the hash existed at block time; it does NOT prove the event itself occurred, nor that the artifact (L2) was correctly identified, nor that the assertion layer (L3) is sound. Blockchain anchoring addresses Pillar 3 well but does not, by itself, satisfy Pillars 1 and 2.

---

### 5.6 Class C6 — Hardware-Rooted Attestation

**Mechanism summary**: A hardware Trusted Execution Environment (TEE) or TPM attests that an event was captured within the secure enclave at a particular time. The attestation is signed by a hardware-derived key.

**Trust model**: Trust root is the hardware manufacturer. Auditor must trust (a) the hardware attestation key is unextractable, (b) the TEE's measurement is correct, and (c) the manufacturer's key provisioning is sound.

**Pillar 1 — Capture-at-Occurrence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-CC.1 | `✓` | Capture-at-occurrence is the TEE's native mode: the attestation is generated inside the enclave at the moment of the event. |
| REQ-CC.2 | `✓` | Atomicity is enforceable by the TEE: no attestation, no event. |
| REQ-CC.3 | `≈` | Backfilling is blocked at the TEE level, but the operator could potentially use a different (compromised) TEE to generate attestations for backfilled events. The class itself does not prevent TEE substitution. |
| REQ-CC.4 | `✓` | Three-layer capture achievable inside the TEE. |

**Pillar 2 — Independent Verifiability**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-IV.1 | `✓` | Auditor with the manufacturer's public key and the attestation can verify independently. |
| REQ-IV.2 | `✓` | Verification is read-only. |
| REQ-IV.3 | `✓` | L3 specification: verify attestation signature, verify TEE measurement, verify timestamp. |

**Pillar 3 — Non-Backdatable Temporal Ordering**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-NB.1 | `≈` | The attestation includes a timestamp, but the timestamp source is the TEE's internal clock. If the TEE clock can be manipulated (e.g., by the operator controlling the host), backdating is possible within the TEE's trust boundary. |
| REQ-NB.2 | `≈` | Distinct fields achievable, but T_verifiable is anchored to the TEE clock, not to an external authority. |
| REQ-NB.3 | `✗` | No sequence guarantee across TEEs. |

**Pillar 4 — Material Independence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-MI.1 | `✓` | Fresh TEE/key achievable. |
| REQ-MI.2 | `✓` | Disjunction achievable. |
| REQ-MI.3 | `✓` | No modification of 7.0.0. |

**Cross-cutting**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-XC.1 | `✓` | Three-layer distinction achievable. |
| REQ-XC.2 | `≈` | Recovery mode blocked at the TEE level, but TEE substitution remains a risk. |
| REQ-XC.3 | `✓` | Audit possible with manufacturer's public key. |
| REQ-XC.4 | `✓` | Forward-only achievable. |

**Failure modes**:
- TEE key extraction (if the hardware is compromised) → attestations forgeable.
- TEE clock manipulation by the host → backdating possible.
- TEE substitution (operator uses a different, compromised TEE) → backfilling possible.
- Manufacturer key compromise → all attestations by that manufacturer's keys untrustworthy.

**Strengths**: Provides strong guarantees at the moment of capture; well-suited to REQ-CC.1 and REQ-CC.2.

**Weaknesses**: Trust concentration in the hardware manufacturer; TEE clock is not externally anchored; TEE substitution is a real risk.

**Open questions**:
- Can C6 be combined with C2 (TSA) or C4 (transparency log) to externally anchor the TEE clock? (Yes.)
- How is TEE identity verified and pinned? (Operational question.)

**Critical distinction**: "Uses hardware attestation" ≠ "resolves the L1/L2/L3 chain". Hardware attestation addresses Pillar 1 (capture) strongly but does not, by itself, satisfy Pillars 2, 3, or 4. In particular, the TEE clock issue means REQ-NB.1 is only `≈`, not `✓`.

---

### 5.7 Class C7 — Zero-Knowledge Attestation

**Mechanism summary**: The system produces a zero-knowledge proof that an event was captured correctly, without revealing the event contents. The proof can be verified by anyone with the public verification key.

**Trust model**: Trust root is the cryptographic assumptions of the proof system + the setup parameters. Auditor must trust (a) the proof system's soundness and (b) the setup was generated honestly (for SNARKs with trusted setup).

**Pillar 1 — Capture-at-Occurrence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-CC.1 | `≈` | Capture achievable, but ZK proof generation is computationally expensive; may not be feasible at event rate. |
| REQ-CC.2 | `≈` | Atomicity achievable if proof generation is part of event generation, but failure modes (proof generation too slow) complicate atomicity. |
| REQ-CC.3 | `✓` | Backfilling is detectable: a backfilled event would need a proof with the wrong generation time, which is not possible if the proof binds to capture time. |
| REQ-CC.4 | `✓` | Three-layer capture achievable in principle. |

**Pillar 2 — Independent Verifiability**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-IV.1 | `✓` | ZK proofs are independently verifiable with the public verification key — this is their defining property. |
| REQ-IV.2 | `✓` | Verification is read-only. |
| REQ-IV.3 | `✓` | L3 specification is the proof itself; the verification procedure is the proof system's verifier. |

**Pillar 3 — Non-Backdatable Temporal Ordering**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-NB.1 | `≈` | The proof can include a timestamp, but the timestamp source is the prover. External anchoring (per REQ-NB.1) requires combining C7 with C2/C4/C5. |
| REQ-NB.2 | `≈` | Distinct fields achievable if the proof binds to both declared and externally-anchored times; otherwise conflated. |
| REQ-NB.3 | `✗` | No sequence guarantee by the proof system alone. |

**Pillar 4 — Material Independence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-MI.1 | `✓` | Fresh setup achievable. |
| REQ-MI.2 | `✓` | Disjunction achievable. |
| REQ-MI.3 | `✓` | No modification of 7.0.0. |

**Cross-cutting**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-XC.1 | `✓` | Three-layer distinction achievable. |
| REQ-XC.2 | `≈` | Recovery mode partially blocked (proofs cannot be backfilled), but performance pressure may push the system to skip proof generation. |
| REQ-XC.3 | `✓` | Audit possible with public verification key only. |
| REQ-XC.4 | `✓` | Forward-only achievable. |

**Failure modes**:
- Trusted setup compromise (for SNARKs) → false proofs possible.
- Proof system soundness failure (cryptographic break) → false proofs possible.
- Performance: proof generation too slow for the event rate → capture fails or is bypassed.

**Strengths**: Strongest independent verifiability (this is ZK's defining property); privacy-preserving.

**Weaknesses**: Computational cost; trusted setup (for some systems); does not by itself anchor in time.

**Open questions**:
- Which proof system? (Selection deferred to Task 96.)
- Is the proof generation cost tolerable at the expected event rate? (Performance question, deferred to Task 97.)

---

### 5.8 Class C8 — Quorum / Multi-Witness

**Mechanism summary**: A quorum of N independent witnesses must agree that an event occurred. The event is considered captured only when ≥ threshold signatures are collected.

**Trust model**: Trust root is the quorum threshold. Auditor must trust (a) the witnesses are independent, (b) the threshold is set correctly, and (c) no coalition ≥ threshold is malicious.

**Pillar 1 — Capture-at-Occurrence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-CC.1 | `≈` | Capture achievable but requires quorum assembly at capture time. |
| REQ-CC.2 | `≈` | Atomicity bounded by quorum assembly. |
| REQ-CC.3 | `✓` | Backfilling requires fresh quorum signatures, which are visible. |
| REQ-CC.4 | `✓` | Three-layer capture achievable. |

**Pillar 2 — Independent Verifiability**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-IV.1 | `✓` | Auditor with witness public keys can verify quorum signatures. |
| REQ-IV.2 | `✓` | Verification is read-only. |
| REQ-IV.3 | `✓` | L3 specification: verify each signature, verify threshold, verify witness set. |

**Pillar 3 — Non-Backdatable Temporal Ordering**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-NB.1 | `≈` | External evidence provided *if* witnesses also timestamp their signatures; otherwise only attests to "existed at some point". |
| REQ-NB.2 | `≈` | Distinct fields achievable if witnesses timestamp. |
| REQ-NB.3 | `✗` | No sequence guarantee across events. |

**Pillar 4 — Material Independence**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-MI.1 | `✓` | Fresh witness set achievable. |
| REQ-MI.2 | `✓` | Disjunction achievable. |
| REQ-MI.3 | `✓` | No modification of 7.0.0. |

**Cross-cutting**:

| Req | Outcome | Rationale |
|---|---|---|
| REQ-XC.1 | `✓` | Three-layer distinction achievable. |
| REQ-XC.2 | `≈` | Recovery mode partially blocked (quorum refuses backfill), but capture failures may queue events. |
| REQ-XC.3 | `✓` | Audit possible with witness public keys only. |
| REQ-XC.4 | `✓` | Forward-only achievable. |

**Failure modes**:
- Coalition ≥ threshold → false events accepted.
- Witness set is not actually independent → trust model collapses.
- Quorum assembly fails (witnesses offline) → capture fails (liveness).

**Strengths**: Distributes trust; supports configurable thresholds; aligns with BFT tradition.

**Weaknesses**: Requires witness coordination at capture time; independence must be externally verified; does not by itself anchor in time.

**Open questions**:
- How is witness independence verified? (Same as C3.)
- What is the right threshold? (Trade-off: higher = safer but slower; deferred to Task 96.)

**Relation to C3**: C8 is a generalization of C3 (witness co-signing) with explicit threshold semantics. The two are analyzed separately because C3 emphasizes individual witnesses while C8 emphasizes the quorum property.

---

## 6. Compliance Matrix

The matrix below summarizes the 8 classes against the 20 requirements. Symbols: `✓` compliant, `≈` conditional (additional assumption required), `✗` non-compliant.

| Requirement | C1 Log | C2 TSA | C3 Witness | C4 Transp. | C5 Block. | C6 HW | C7 ZK | C8 Quorum |
|---|---|---|---|---|---|---|---|---|
| **Pillar 1 — Capture-at-Occurrence** | | | | | | | | |
| REQ-CC.1 capture at occurrence | ✓ | ≈ | ≈ | ✓ | ≈ | ✓ | ≈ | ≈ |
| REQ-CC.2 atomic with event | ✓ | ≈ | ≈ | ≈ | ≈ | ✓ | ≈ | ≈ |
| REQ-CC.3 no backfill | ✗ | ✓ | ✓ | ✓ | ✓ | ≈ | ✓ | ✓ |
| REQ-CC.4 three-layer capture | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Pillar 2 — Independent Verifiability** | | | | | | | | |
| REQ-IV.1 third-party verifiability | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| REQ-IV.2 verification no modify | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| REQ-IV.3 L3 specification | ≈ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Pillar 3 — Non-Backdatable Temporal Ordering** | | | | | | | | |
| REQ-NB.1 Epistemic Non-Backdating | ✗ | ✓ | ≈ | ✓ | ✓ | ≈ | ≈ | ≈ |
| REQ-NB.2 declared vs verifiable time | ✗ | ✓ | ≈ | ✓ | ✓ | ≈ | ≈ | ≈ |
| REQ-NB.3 monotonic temporal order | ≈ | ≈ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| **Pillar 4 — Material Independence** | | | | | | | | |
| REQ-MI.1 fresh root of trust | ✓ | ≈ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| REQ-MI.2 evidence corpus disjunction | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| REQ-MI.3 no retroactive mod of 7.0.0 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Cross-cutting** | | | | | | | | |
| REQ-XC.1 three-layer structural | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| REQ-XC.2 no recovery mode | ✗ | ≈ | ≈ | ≈ | ≈ | ≈ | ≈ | ≈ |
| REQ-XC.3 audit w/o operator trust | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| REQ-XC.4 forward-only evidence | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

### 6.1 Compliance Score per Class

| Class | ✓ | ≈ | ✗ | Total | Score (✓/20) |
|---|---|---|---|---|---|
| C1 — Append-only log + hash chaining | 11 | 3 | 6 | 20 | 55% |
| C2 — RFC 3161 / Trusted Timestamping | 16 | 4 | 0 | 20 | 80% |
| C3 — Witness co-signing | 14 | 6 | 0 | 20 | 70% |
| C4 — Transparency logs | 19 | 1 | 0 | 20 | 95% |
| C5 — Blockchain anchoring | 16 | 4 | 0 | 20 | 80% |
| C6 — Hardware-rooted attestation | 15 | 5 | 0 | 20 | 75% |
| C7 — Zero-knowledge attestation | 15 | 5 | 0 | 20 | 75% |
| C8 — Quorum / multi-witness | 14 | 6 | 0 | 20 | 70% |

### 6.2 Critical Observations from the Matrix

**No single class satisfies all 20 requirements.** This is the most important finding of the analysis. Every class has at least one `≈` or `✗`. A compliant AION-7.1.x architecture will require **combination** of classes.

**C1 (append-only log) is the weakest in isolation.** It fails 6 requirements, all related to external anchoring and operator trust. C1 alone reproduces the P3 failure mode. C1 may still be useful as a *component* of a combined architecture (it provides cheap local capture), but it cannot be the sole mechanism.

**C4 (transparency logs) has the highest standalone score (95%)** but still has one `≈` (REQ-XC.2 — recovery mode partially mitigated). C4 also depends on active monitors, which is an operational requirement outside the class itself.

**Pillar 3 (Non-Backdatable Temporal Ordering) is the hardest pillar.** Only C2 (TSA), C4 (transparency log), and C5 (blockchain) achieve `✓` on REQ-NB.1. Classes that lack external temporal anchoring (C1, C3, C6, C7, C8) cannot satisfy REQ-NB.1 in isolation.

**REQ-NB.3 (monotonic temporal order) is the hardest single requirement.** Only C4 and C5 satisfy it with `✓`. All other classes are `≈` or `✗`. This suggests that any compliant architecture must include a C4-like or C5-like sequence mechanism.

**REQ-XC.2 (no recovery mode) is universally `≈` or `✗`.** No class provides a strong guarantee against recovery mode by itself. This requirement must be satisfied at the architectural level (combination of classes + operational policy), not at the class level.

---

## 7. Trade-off Analysis

### 7.1 Trust Distribution vs. Liveness

Classes that distribute trust (C3, C8) require witness availability at capture time. Classes that concentrate trust (C2, C6) have higher liveness but lower trust distribution. The trade-off:

| Trust Distribution | Liveness Impact | Example Classes |
|---|---|---|
| Concentrated (single trust root) | High (always available if trust root is up) | C2, C6 |
| Distributed (multi-party) | Lower (requires quorum assembly) | C3, C8 |
| Public (anyone can verify) | Highest (no operator coordination needed for verification) | C4, C5, C7 |

### 7.2 Capture Latency vs. Verifiability Strength

Classes with strong external anchoring (C4, C5) impose latency on capture (log submission, block inclusion). Classes with internal anchoring (C1, C6) have low latency but weak verifiability.

| Capture Latency | Verifiability Strength | Example Classes |
|---|---|---|
| Low (synchronous) | Weak (operator trust) | C1, C6 |
| Medium (TSA round-trip, witness assembly) | Medium (third-party trust) | C2, C3, C8 |
| High (block inclusion, log submission) | Strong (public verifiability) | C4, C5, C7 |

### 7.3 Cost vs. Granularity

C5 (blockchain) is expensive per event but provides strong guarantees. C1 (local log) is cheap but provides weak guarantees. The trade-off suggests per-batch anchoring (e.g., merkle root of many events anchored once) as a middle ground — but this increases capture latency.

### 7.4 Privacy vs. Auditability

C7 (ZK attestation) provides privacy (event contents not revealed) but at high computational cost. Other classes either reveal event contents (C1, C4, C5) or rely on witness trust (C3, C8). The trade-off:

| Privacy | Auditability | Example Classes |
|---|---|---|
| Full (contents hidden) | Strong (ZK proofs) | C7 |
| Partial (hash only) | Strong (public verifiability) | C4, C5 |
| None (full contents) | Strong (public verifiability) | C1 (if public) |
| Partial (witnesses see) | Medium (witness trust) | C3, C8 |

---

## 8. Failure Modes That Cross Classes

Some failure modes are not specific to a single class but affect multiple classes or combinations. These are recorded here because they will need to be addressed at the architectural level (Task 96) or threat model level (Task 95).

| Failure Mode | Affected Classes | Mitigation Direction |
|---|---|---|
| Operator withholds events from capture | All | Architectural: no event-generation path bypasses capture (REQ-CC.2) |
| Trust root compromise (TSA key, hardware key, witness coalition) | C2, C3, C5, C6, C8 | Multi-root combination; key rotation policy |
| Capture failure due to liveness (TSA offline, witness offline, chain congested) | C2, C3, C5, C8 | Combination with synchronous mechanism (C1, C6) for liveness |
| Selective disclosure (operator shows subset to auditor) | C1, C3, C6, C8 | Public verifiability mechanism (C4, C5, C7) |
| TEE substitution / hardware swap | C6 | Multi-witness cross-check (C3, C8) |
| Trusted setup compromise | C7 (SNARKs) | Use transparent-setup systems (STARKs, bulletproofs) |
| Monitor absence | C4 | Multiple independent monitors; monitor registry |

---

## 9. Open Questions for Task 95 (Threat Model)

The analysis identifies the following open questions that the Threat Model (Task 95) should address:

1. **What is the adversary model?** Is the operator adversarial? Are witnesses? Are external parties? The threat model must specify which parties can be malicious and what they can do.
2. **What is the coalition bound?** For C3, C8, and any multi-party mechanism, the threat model must specify the maximum coalition size the system must resist.
3. **What is the temporal adversary?** Can the adversary backdate events? By how much? (Drives REQ-NB.1 ε parameter.)
4. **What is the liveness adversary?** Can the adversary cause capture to fail? What is the acceptable capture failure rate?
5. **What is the key-compromise scenario?** If a trust root key is compromised, how much history is affected? Can the system recover (forward-secure key rotation)?
6. **What is the operational adversary?** Can the operator substitute hardware (C6), replace the witness set (C3, C8), or rotate the TSA (C2)?
7. **What is the combination adversary?** If multiple classes are combined (as expected), how do adversaries against each class compose?

These questions are not answered here. They are inputs to Task 95.

---

## 10. Non-Goals Reaffirmation

| Non-Goal | Status |
|---|---|
| Select an architecture | NOT DONE — deferred to Task 96 |
| Select specific technologies within a class | NOT DONE — deferred to Task 96 |
| Implement code | NOT DONE — deferred to Task 97 and beyond |
| Re-open V3 | NOT DONE — forbidden by I-91.1, AION-EV-017 |
| Upgrade P3 | NOT DONE — forbidden by I-91.2, AION-EV-017 |
| Modify Caso D | NOT DONE — forbidden by I-91.3, AION-EV-017 |
| Modify 7.0.0 frozen artifacts | NOT DONE — REQ-MI.3 verified (§11) |
| Take credit for "resolving P3" | NOT DONE — forbidden by AION-EV-021 |

---

## 11. 7.0.0 FROZEN State Verification

Per REQ-MI.3, the 7.0.0 frozen artifacts MUST remain unchanged. Verified at Task 94 issuance by the verification script.

| Artifact | Expected SHA-256 | Status |
|---|---|---|
| AION-7.0.0_R0_CONSOLIDATION_MANIFEST.md | `fa14c4eb…12b2b8b4` | (verified by script) |
| AION-7.0.0_EPISTEMIC_STATE_FREEZE.md | `964e02fa…f0eb58f6` | (verified by script) |
| AION-7.0.0_PROVENANCE_BOUNDARY.md | `1e42245e…5605c72c` | (verified by script) |

---

## 12. Provenance Events

### AION-EV-021 — TASK 94 AUTHORIZED

| Field | Value |
|---|---|
| Event ID | AION-EV-021 |
| Type | Task Authorization |
| Issuer | Projetista Master |
| Effect | Task 94 (Architectural Options Analysis) authorized |
| Constraints | Mandate in §1; distinction PROPERTY ≠ GUARANTEE in §2; no P3-resolution credit |
| Reversibility | NONE |

### AION-EV-022 — ANALYSIS ISSUED

| Field | Value |
|---|---|
| Event ID | AION-EV-022 |
| Type | Analysis Issuance |
| Issuer | Main analyst (under AION-EV-021 authorization) |
| Effect | 8 classes surveyed; compliance matrix produced; no selection made |
| Reversibility | Analysis may be amended by PM determination; constraints may not |
| Artifact | This document |

---

## 13. Handoff to Task 95

Task 95 — Threat Model — is the natural successor. Its proposed mandate:

> Specify the adversary model, coalition bounds, temporal adversary, liveness adversary, key-compromise scenarios, operational adversary, and combination adversary. Identify threats to each of the 20 requirements. Identify which threats are mitigated by which classes (and combinations) from Task 94. Produce a threat matrix that maps threats to mitigations.

The 7 open questions in §9 are the inputs to Task 95.

**Task 95 PROPOSED — pending PM authorization (AION-EV-023).**

---

## 14. Status Declaration

```text
AION-7.1.x ARCHITECTURAL OPTIONS ANALYSIS: ISSUED
AION-EV-021: REGISTERED (Task 94 authorized)
AION-EV-022: REGISTERED (analysis issued)
CLASSES SURVEYED: 8 (C1–C8)
REQUIREMENTS EVALUATED: 20
COMPLIANCE MATRIX: PRODUCED
KEY FINDING: NO SINGLE CLASS SATISFIES ALL 20 REQUIREMENTS
KEY FINDING: PILLAR 3 (NON-BACKDATING) IS THE HARDEST PILLAR
KEY FINDING: REQ-NB.3 (MONOTONIC ORDER) REQUIRES C4- OR C5-LIKE MECHANISM
KEY FINDING: REQ-XC.2 (NO RECOVERY MODE) REQUIRES ARCHITECTURAL-LEVEL MITIGATION
7.0.0 FROZEN STATE: UNCHANGED (REQ-MI.3 satisfied)
NEXT ACTION: Task 95 — Threat Model (PROPOSED, pending PM authorization)
NO ARCHITECTURE SELECTED (per mandate)
P3 RETROACTIVE UPGRADE: PROHIBITED
V3 REOPENING: PROHIBITED
CASE D: PRESERVED (out of scope)
```

---

## 15. Closing Note to Next Analyst

The next analyst inherits:

1. **A compliance matrix** — 8 classes × 20 requirements, with `✓`/`≈`/`✗` outcomes and rationale.
2. **A key finding** — no single class satisfies all 20 requirements; combination is necessary.
3. **A trade-off analysis** — trust distribution, latency, cost, privacy.
4. **A list of cross-class failure modes** — for the threat model to address.
5. **7 open questions** — inputs to Task 95.

The next analyst is also reminded:

> Property is not guarantee.
> A class that "has a timestamp" does not "prevent backdating".
> A class that "is on a blockchain" does not "have sufficient provenance".
> Every `≈` in the matrix is a place where property was confused with guarantee.
> Task 95 (Threat Model) must address each `≈` by specifying the additional assumption required to promote it to `✓`.

---
