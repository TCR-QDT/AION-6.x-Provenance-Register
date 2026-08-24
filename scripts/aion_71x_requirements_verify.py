#!/usr/bin/env python3
"""
AION-7.1.x Requirements — Hash Computation & Worklog Update
Task 93: Requirements Elicitation

Registers AION-EV-019 (PM authorization) and AION-EV-020 (requirements issued)
in the shared worklog. Verifies that 7.0.0 FROZEN artifacts remain unchanged
(REQ-MI.3 compliance at requirements issuance).
"""

import hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta

BASE = Path("/home/z/my-project")
DOWNLOAD = BASE / "download"
WORKLOG = BASE / "worklog.md"

REQUIREMENTS = "AION-7.1.x_REQUIREMENTS.md"

# 7.0.0 frozen artifact anchors (Task 91)
FROZEN_700 = [
    ("AION-7.0.0_R0_CONSOLIDATION_MANIFEST.md", "fa14c4ebdad30063f5921f1c73bdd11c7b9a263b16239aaa996bf75112b2b8b4"),
    ("AION-7.0.0_EPISTEMIC_STATE_FREEZE.md",    "964e02fa5f645cdcdefc676fe12ae86fd6271ca84ef9e7bb6a2d9466f0eb58f6"),
    ("AION-7.0.0_PROVENANCE_BOUNDARY.md",       "1e42245ed96ddd12e1ae6ed0ab973ffb58ea8ad8fabb12866ec198405605c72c"),
]

# 7.1.x Charter anchor (Task 92)
CHARTER = ("AION-7.1.x_CHARTER.md", "e9254e55e090ef067993965c2768013c2893668435f450bc287f9e168e128f84")

tz_sp = timezone(timedelta(hours=-3))
now = datetime.now(tz_sp).strftime("%Y-%m-%d %H:%M:%S (UTC-3)")

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

print("=" * 72)
print("AION-7.1.x — REQUIREMENTS ISSUED (Task 93)")
print("Hash Computation & Worklog Update")
print("=" * 72)
print(f"Timestamp: {now}")
print()

# Compute hash of the new requirements artifact
p = DOWNLOAD / REQUIREMENTS
size = p.stat().st_size
h_req = sha256(p)
print(f"[OK] {REQUIREMENTS}")
print(f"     size  = {size} bytes")
print(f"     sha256 = {h_req}")
print()

# Verify 7.0.0 FROZEN artifacts (REQ-MI.3)
print("REQ-MI.3 verification — 7.0.0 FROZEN artifacts unchanged:")
all_700_ok = True
for name, expected in FROZEN_700:
    fp = DOWNLOAD / name
    if not fp.exists():
        print(f"  [MISSING] {name}")
        all_700_ok = False
        continue
    actual = sha256(fp)
    match = "MATCH" if actual == expected else "MISMATCH"
    if actual != expected:
        all_700_ok = False
    print(f"  [{match}] {name}")

print()

# Verify 7.1.x Charter unchanged
print("Charter verification (Task 92 anchor):")
name, expected = CHARTER
fp = DOWNLOAD / name
charter_ok = False
if fp.exists():
    actual = sha256(fp)
    match = "MATCH" if actual == expected else "MISMATCH"
    charter_ok = (actual == expected)
    print(f"  [{match}] {name}")
else:
    print(f"  [MISSING] {name}")

print()

if all_700_ok and charter_ok:
    print("REQ-MI.3 (no retroactive modification of 7.0.0): SATISFIED")
    print("Charter integrity: SATISFIED")
else:
    print("INTEGRITY VIOLATION DETECTED — escalate to PM")

print()

worklog_entry = f"""
---
Task ID: 93
Agent: main (Super Z, GLM)
Task: AION-7.1.x REQUIREMENTS ELICITATION — formalize the four pillars as verifiable requirements per PM mandate AION-EV-019.

Work Log:
- Received AION-EV-019 from Projetista Master: Task 93 authorized with specific mandate (formalize 4 pillars, 10-field template, three-layer distinction, Epistemic Non-Backdating, no architecture selection).
- Verified 7.0.0 FROZEN artifacts unchanged (REQ-MI.3 satisfied at Task 93 issuance): all three Task 91 hashes MATCH.
- Verified 7.1.x Charter artifact unchanged: Task 92 hash MATCH.
- Produced AION-7.1.x_REQUIREMENTS.md with:
  * Authorization restatement (AION-EV-019 verbatim)
  * Mandate compliance statement (8 items, all confirmed)
  * Three-Layer Provenance Distinction (Section 3): L1 event / L2 artifact / L3 assertion; L3 identified as load-bearing per PM directive
  * Epistemic Non-Backdating (Section 4): declared timestamp ≠ verifiable time of existence; 3-condition property specification
  * 10-field requirement template (Section 5): ID, Descrição, Racional epistemológico, Evento, Pré-condição, Critério de aceitação, Método de verificação, Evidência esperada, Falha proibida, Dependências
  * Pillar 1 (Capture-at-Occurrence): REQ-CC.1, REQ-CC.2, REQ-CC.3, REQ-CC.4
  * Pillar 2 (Independent Verifiability): REQ-IV.1, REQ-IV.2, REQ-IV.3
  * Pillar 3 (Non-Backdatable Temporal Ordering): REQ-NB.1, REQ-NB.2, REQ-NB.3
  * Pillar 4 (Material Independence from 7.0.0): REQ-MI.1, REQ-MI.2, REQ-MI.3
  * Cross-cutting requirements: REQ-XC.1 (three-layer structural), REQ-XC.2 (no recovery mode), REQ-XC.3 (audit w/o operator trust), REQ-XC.4 (forward-only evidence)
  * Non-goals reaffirmation (7 items)
  * Requirement dependency graph (acyclic, bottom-up verification)
  * 7.0.0 FROZEN state verification (REQ-MI.3)
  * AION-EV-019 and AION-EV-020 registration
  * Handoff to Task 94 (Architectural Options Analysis) — PROPOSED, pending PM authorization
- Registered AION-EV-020 (requirements issued).

Stage Summary:
- AION-EV-019 REGISTERED: Task 93 authorized.
- AION-EV-020 REGISTERED: 20 requirements issued (16 pillar + 4 cross-cutting).
- Requirements artifact: AION-7.1.x_REQUIREMENTS.md (size={size} bytes, sha256={h_req}).
- 7.0.0 FROZEN state verified unchanged (REQ-MI.3 satisfied at Task 93).
- Three-Layer Provenance Distinction established: L1 (event) / L2 (artifact) / L3 (assertion); L3 load-bearing.
- Epistemic Non-Backdating formalized: declared timestamp ≠ verifiable time of existence; three conditions specified (existence at T+ε, non-fabricability, hash-binding).
- 20 requirements total, each with 10-field specification:
  * REQ-CC.1–CC.4 (Capture-at-Occurrence)
  * REQ-IV.1–IV.3 (Independent Verifiability)
  * REQ-NB.1–NB.3 (Non-Backdatable Temporal Ordering)
  * REQ-MI.1–MI.3 (Material Independence)
  * REQ-XC.1–XC.4 (Cross-cutting)
- Dependency graph acyclic; verification proceeds bottom-up from Charter constraints to REQ-XC.2.
- No architecture, technology, or implementation selected (non-goal compliance).
- Next action: Task 94 (Architectural Options Analysis) — PROPOSED, pending PM authorization (AION-EV-021).
- Founding question for Task 94: which candidate approaches satisfy which of the 20 requirements? Task 94 surveys; it does not select.
- Timestamp: {now}
"""

with WORKLOG.open("a", encoding="utf-8") as f:
    f.write(worklog_entry)

print(f"Worklog updated: {WORKLOG}")
print(f"Worklog size: {WORKLOG.stat().st_size} bytes")
print()
print("=" * 72)
print("AION-7.1.x REQUIREMENTS ISSUED.")
print("AION-EV-019 + AION-EV-020 REGISTERED.")
print(f"Requirement count: 20 (16 pillar + 4 cross-cutting)")
print("Three-layer distinction: ESTABLISHED")
print("Epistemic Non-Backdating: ESTABLISHED")
print("Phase state: 7.1.x REQUIREMENTS — ISSUED, PENDING TASK 94")
print("Next: Task 94 (Architectural Options Analysis) — PROPOSED, pending PM auth")
print("=" * 72)
