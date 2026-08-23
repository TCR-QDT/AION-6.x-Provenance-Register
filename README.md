# AION-6.x Provenance Register

> **Registro material de proveniência para a genealogia documental do AION-6.x.**
> **Material provenance register for the AION-6.x documental genealogy.**

---

## Repository identity

| Field | Value |
|---|---|
| Repository name | AION-6.x-Provenance-Register |
| Organization | TCR-QDT |
| URL | https://github.com/TCR-QDT/AION-6.x-Provenance-Register |
| Visibility | Public |
| Initial state (at first commit) | EMPTY REPOSITORY |
| First commit date | 2026-08-23 |
| Authority | Projetista Master (Edson Carvalho do Nascimento, ORCID 0009-0003-5504-7439) |
| Operator | IA Curadora (Escriba / Arquiteto de Metadados) |
| Session | web-73c75281-201c-4716-b85c-97833d25f9b3 |
| Authorizing task | AION-7.0.0-R0.3.3.A.2.4.A.2 — PROVENANCE REGISTER INITIALIZATION |

---

## Purpose

Este repositório estabelece um **registro material de proveniência** para o contexto histórico do AION-6.x. **Não autentica retroativamente** o passado do AION-6.x. Estabelece apenas uma cadeia de custódia explícita a partir do ponto de recuperação atual.

This repository establishes a **material provenance register** for the historical context of AION-6.x. **It does not retroactively authenticate** the AION-6.x past. It only establishes an explicit chain of custody from the current recovery point onward.

---

## Critical epistemic distinction

```
DATA DE INCORPORAÇÃO AO REPOSITÓRIO    ≠    DATA DOS EVENTOS HISTÓRICOS DESCRITOS
(date of repository incorporation)         (date of historical events described)
```

O Git registra **quando** a documentação foi incorporada ao repositório. Os documentos descrevem **quando** os eventos históricos ocorreram. Estas duas datas **não devem ser confundidas**.

Git records **when** documentation was incorporated into the repository. Documents describe **when** historical events occurred. These two dates **must not be conflated**.

---

## Repository structure

```
AION-6.x-Provenance-Register/
│
├── README.md                                  # This document — repository identity and purpose
│
├── provenance/                                 # Provenance documentation
│   ├── README.md                              # Provenance documentation overview
│   ├── TCR_QDT_BRIDGE.md                      # Bridge between TCR/QDT and AION-6.x (status: not authenticated)
│   ├── CORPUS_PROVENANCE.md                   # Per-CORPUS-ID provenance status
│   └── HISTORICAL_STATUS.md                   # Historical status of AION-6.x components
│
├── manifests/                                  # Machine-readable provenance manifests
│   └── AION-6.x_CORPUS_PROVENANCE.yaml         # YAML manifest of corpus provenance
│
├── evidence/                                   # Evidence material
│   └── historical/                             # Historical documentation
│       └── MEMORIAS_DE_UMA_CONSTRUCAO.md       # PR-001 — recovered historical narrative
│
└── ledger/                                     # Provenance ledger
    └── PROVENANCE_LEDGER.md                    # Central provenance ledger
```

---

## Three-level distinction preserved

```
TCR/QDT                       →    AION-6.x                    →    AION-7.0.0
(materially exists,                (architectural context           (specification phase
 captured; PDFs C-01, C-02          investigated in 6.x;           of the epistemic gate
 have content-compatible V4 PASS,    corpus source not              for the 7.0.0 baseline;
 but V3 INSUFFICIENT)               materially accessible)          this register)
       │                                   │                              │
       └────── not authenticated ──────────┘                              │
                                          │                              │
                                          └────── evidence recovery ─────┘
                                                  (this repository)
                                                  (records current state,
                                                   NOT past existence)
```

**This register does NOT collapse the three levels.** It establishes material record of the current recovery effort, not retroactive authentication of historical AION-6.x content.

---

## Initial state declaration

This repository was initialized as an **EMPTY REPOSITORY** on GitHub prior to the first commit on 2026-08-23.

The first commit (`AION-6.x Provenance Register — Initial Historical Recovery`) establishes:

- Material record of repository initialization date
- Material record of the historical document `MEMORIAS_DE_UMA_CONSTRUCAO.md` (PR-001, SHA-256 `7549597b065e784c7baae3baca42049e23cc57937c610cfd2c4f23b242d2d9df`)
- Explicit declaration that no retroactive authentication is intended
- Explicit declaration that AION-6.x historical content is NOT yet deposited or authenticated
- Status of C-01 and C-02 (PDF candidates from TCR/QDT) as `V3 = INSUFFICIENT`
- Acknowledgment that the historical AION-6.x environment is not materially accessible from this repository

---

## What this repository IS

- A material provenance register for documentation recovery
- A chain-of-custody record from the current recovery point onward
- An infrastructure for future evidence incorporation
- A formal record of what is known, what is candidate, and what is unknown

## What this repository is NOT

- An authentication of the AION-6.x past
- A reconstruction of the AION-6.x corpus
- A substitute for missing material evidence
- A retroactive declaration that TCR/QDT PDFs are the same files as AION-6.x corpus source

---

## License

This repository's documentation is licensed under MIT + CC-BY-4.0 (consistent with TCR-QDT organization policy as observed in `Coerencia_Relacional` repository).

---

## Contact

- **Author / Curador:** Edson Carvalho do Nascimento (Projetista Master)
- **ORCID:** 0009-0003-5504-7439
- **Operator (this initialization):** IA Curadora (Ecriba / Arquiteto de Metadados)
- **Session:** web-73c75281-201c-4716-b85c-97833d25f9b3

---

*"Este repositório registra materialmente a recuperação de documentação histórica do AION-6.x. Não autentica retroativamente o passado. Estabelece uma cadeia de custódia explícita a partir do ponto de recuperação atual. A distinção entre data de incorporação e data dos eventos históricos é fundamental para a integridade epistêmica do registro."*
