# AION-6.5.0 — B2 Provenance Failure Characterization & Experimental Boundary

**ID do Documento:** AION-6.5.0
**Versão:** 1.0.0 (Frozen)
**Estado:** Characterization & Boundary Document
**Data:** 21 de agosto de 2026
**Autor da estrutura:** Edson C. Nascimento (Projetista Master)
**Implementação técnica:** IA Curadora
**Base experimental:** AION-6.2 → 6.4 (Tasks 33-56)

---

## 1. ESTADO EXPERIMENTAL CONGELADO

```
Corpus: v1.3.0 (9 registros documentais + 2 inexistentes)
Oracle: v3 (7 chunks interversionais)
GraphRAG: v1.0.0 (22 nós, 187 arestas)
P-RESP-001: v0.3 (validator determinístico)
AION-EVAL-002: v0.2 (multicamada, FAIL-SYSTEM vs FAIL-EVALUATOR)
B1 Configuration: 6.2.11 (cross-lingual PT-BR→EN + Oracle v3)
```

Nenhum componente deve ser alterado.

---

## 2. FORMALIZAÇÃO DAS MÉTRICAS

### 2.1 PER — Provenance Emission Rate

$$PER = \frac{N_{\text{runs com provenance}}}{N_{\text{runs}}}$$

Mede: probabilidade de o LLM decidir emitir provenance documental em uma run.

### 2.2 CFR-ID — Conditional Fabrication Rate (por referência)

$$CFR_{ID} = \frac{N_{\text{IDs inválidos}}}{N_{\text{IDs produzidos}}}$$

Mede: probabilidade de um ID individual ser inválido, condicionada à emissão.

### 2.3 CFR-RUN — Conditional Fabrication Rate (por run)

$$CFR_{RUN} = \frac{N_{\text{runs com fabricação}}}{N_{\text{runs com provenance}}}$$

Mede: probabilidade de uma run com provenance conter pelo menos 1 ID inválido.

### 2.4 EBA — Evidence-Bound Accuracy

$$EBA = \frac{N_{\text{IDs válidos e correspondentes à evidência}}}{N_{\text{IDs produzidos}}}$$

Mede: probabilidade de um ID ser válido E corresponder ao chunk efetivamente recuperado como evidência.

### 2.5 FR — Fabrication Rate (clássico)

$$FR = \frac{N_{\text{runs com fabricação}}}{N_{\text{runs}}}$$

Mede: probabilidade observada de fabricação no conjunto total de runs.

### 2.6 VR — Validation Rate

$$VR = \frac{N_{\text{IDs inválidos interceptados}}}{N_{\text{IDs inválidos}}}$$

Mede: probabilidade de o validator P-RESP-001 v0.3 interceptar um ID inválido.

### 2.7 F3R — F3 Rate

$$F3R = \frac{N_{\text{runs com F3}}}{N_{\text{runs}}}$$

Mede: probabilidade de uma run conter pelo menos 1 caso de F3 (Provenance Transduction Error).

### 2.8 Decomposição fundamental

$$\boxed{FR = PER \times CFR_{RUN}}$$

**Confirmada empiricamente** no baseline 6.4.0: FR = 0.30 × 0.47 = 0.14 = FR observado.

---

## 3. F3 — PROVENANCE TRANSDUCTION ERROR

### 3.1 Definição formal

> **F3 — Provenance Transduction Error:** geração de identificador documental que preserva a identidade semântica do documento, mas não preserva sua identidade formal de chunk, em consequência de inferência ou transferência indevida de schema.

### 3.2 Exemplo canônico

```
Documento correto:   CORPUS-002 (Paper A v6.2)
Schema real:         CORPUS-002#p1_01  (formato pN_NN)
Schema fabricado:    CORPUS-002#chunk_001  (formato chunk_NNN)

Causa: contexto continha CORPUS-005#chunk_001 (schema chunk_NNN)
       e CORPUS-003#p3_02 (schema pN_NN)
       LLM aplicou schema chunk_NNN ao CORPUS-002 por inferência.
```

### 3.3 Diferenciação de "alucinação genérica"

F3 NÃO é alucinação aleatória de documento. É **inferência de schema**:
- O documento citado está correto (CORPUS-002 existe e é relevante)
- O formato do chunk está incorreto (chunk_001 não existe em CORPUS-002)
- O LLM raciocina: "este documento deve ter um chunk_001 porque outros documentos têm"

### 3.4 Estabilidade observacional

| Experimento | N | F3 / total fabricações | % F3 |
|---|---|---|---|
| 6.3.0 (baseline) | 100 | 14/15 | 93.3% |
| A.1 (reprodução) | 30 | 16/17 | 94.1% |
| 6.4.0 (conditional) | 100 | 14/14 | 100% |
| 6.4.2 (N=5) | 5 | 2/2 | 100% |

F3 é **estável como mecanismo dominante** em todas as sessões com fabricação observável.

---

## 4. CADEIA CAUSAL DOCUMENTADA

```
EVIDÊNCIA RECUPERADA
        ↓
REPRESENTAÇÃO CONTEXTUAL
  (múltiplos schemas de chunk visíveis:
   chunk_001 de CORPUS-001/005
   pN_NN de CORPUS-002/003/004/006/007)
        ↓
IDENTIFICAÇÃO SEMÂNTICA DO DOCUMENTO
  (LLM sabe qual documento citar)
        ↓
TRANSDUÇÃO PARA IDENTIFICADOR FORMAL
  (LLM precisa produzir chunk_id)
        ↓
┌─────────────────────────────────┐
│ ID do documento-alvo está       │
│ literalmente disponível no      │
│ contexto?                       │
└──────────────┬──────────────────┘
               │
        NÃO (documento-alvo não está
        nos top-5 recuperados para B2)
               ↓
       INFERÊNCIA DE SCHEMA
  (LLM aplica formato observado
   em outros documentos)
               ↓
              F3
  (documento correto + chunk incorreto)
               ↓
     VALIDATOR INTERCEPTA
  (P-RESP-001 v0.3 detecta e marca
   [PROVENANCE_INVALID])
```

**Expressão arquitetural central:** "erro de transdução evidência→identificador"

---

## 5. LIMITE EXPERIMENTAL H-TEMP

### 5.1 Definição

> **H-TEMP caracteriza uma não-estacionariedade observada no comportamento de geração do ambiente experimental utilizado.**

### 5.2 Evidência

| Sessão | N | PER | SR | FR | Observável? |
|---|---|---|---|---|---|
| 6.3.0 | 100 | — | 29% | 15% | ✅ |
| A.1 | 30 | — | 90% | 57% | ✅ |
| 6.3.1-B P0 | 20 | — | 20% | 5% | ✅ |
| 6.3.1-C C0 | 10 | 0% | 0% | 0% | ❌ |
| 6.4.0 | 100 | 30% | 29% | 14% | ✅ |
| 6.4.1-B A0 | 25 | 60% | 60% | 28% | ✅ |
| 6.4.2-B M0 | 10 | 0% | 0% | 0% | ❌ |

PER observado: **[0%, 80%]** entre sessões comparáveis.

### 5.3 Regra epistemológica de interpretação

> **Ausência de fabricação não pode ser interpretada como ausência de risco quando PER = 0.**

Quando PER=0:
- Nenhuma provenance foi emitida
- CFR não é observável
- FR=0 é trivialmente verdadeiro mas não informativo
- O experimento é classificado como CENÁRIO D (não observável)

### 5.4 Consequência para validação de intervenções

H-TEMP impede validação estatística de intervenções (M1/M2) porque:
1. Timeout impede N grande em uma única sessão
2. PER varia extremamente entre sessões
3. Sessões com PER=0 são inúteis para estimar CFR
4. Não é possível acumular lotes de sessões diferentes (taxa base não é estacionária)

---

## 6. CLASSIFICAÇÃO DEFINITIVA DAS INTERVENÇÕES

| Intervenção | Mecanismo | CFR | PER | SR | EBA | Classificação |
|---|---|---|---|---|---|---|
| **A1** (evidence-bound proibitiva) | "Não infira" (proibição cognitiva) | ↓ marginal | ↓ 40% | ↓ 47% | ≈ | **PARTIAL / NEGATIVE TRADE-OFF** |
| **M1** (literal-copy) | "Copie o que está presente" (ancoragem observacional) | → 0 | ↓ 25% | ↓ 25% | → 100% | **CANDIDATE / UNVALIDATED** |
| **M2** (context-presence) | "Verifique presença antes de emitir" (validação local) | → 0 | ↓ 25% | ↓ 25% | → 100% | **CANDIDATE / UNVALIDATED** |
| **P1** (remoção de provenance) | Remove exigência de provenance | → 0 | → 0 | → 0 | — | **FALSE SOLUTION** |
| **P2** (schema unificado) | Unifica formato de chunk no contexto | → 0 | → 0 | → 0 | — | **FALSE SOLUTION** |

### 6.1 Distinção fundamental

| Abordagem | Mecanismo | Efeito sobre PER/SR |
|---|---|---|
| **Proibição cognitiva** (A1) | "Não infira" | Suprime cognição → PER/SR ↓↓ |
| **Ancoragem observacional** (M1/M2) | "Copie o que está presente" | Ancora observação → PER/SR ↓ (menor) |
| **Supressão de provenance** (P1/P2) | Remove exigência | Elimina provenance → PER/SR → 0 |

### 6.2 M1/M2 NÃO promovidas

P-RESP-001 v0.3 permanece congelado. M1/M2 são hipóteses experimentais não validadas.

---

## 7. MATRIZ DE EVIDÊNCIA

| Afirmação | Fonte experimental | Status |
|---|---|---|
| B1 é determinístico (Top-1=3/3) | 6.2.11 (N=3), 6.3.0 (N=100) | **DEMONSTRADO** |
| B1 retrieval é cross-lingual (PT-BR→EN) | 6.2.9, 6.2.11 | **DEMONSTRADO** |
| Oracle v3 é metodologicamente correto | 6.2.8, 6.2.10 | **DEMONSTRADO** |
| F3 domina fabricação (93-100%) | 6.3.0, A.1, 6.4.0, 6.4.2 | **FORTEMENTE SUPORTADO** |
| Competição de schemas contribui para F3 | 6.3.1.1-2 (14/14 F3 sob múltiplos schemas) | **CONFIRMADO NO CONTEXTO TESTADO** |
| FR = PER × CFR_RUN | 6.4.0 (0.30 × 0.47 = 0.14 = FR) | **DEMONSTRADO** |
| PER é não-estacionário | 6.3.0–6.4.2 (PER ∈ [0%, 80%]) | **OBSERVADO** |
| CFR ≈ 47% (quando observável) | 6.4.0 (N=100, CFR-RUN=0.4667) | **BASELINE CONDICIONAL** |
| EBA ≈ 68% | 6.4.0 (N=100, EBA=0.6818) | **BASELINE CONDICIONAL** |
| VR = 100% | 6.3.0, A.1, 6.4.0, 6.4.1, 6.4.2 (todos) | **ROBUSTAMENTE OBSERVADO** |
| F3 = Provenance Transduction Error | 6.3.1.1-2, 6.3.1-B.0 (auditoria causal) | **CARACTERIZADO** |
| A1 resolve B2 | 6.4.1-B (N=25: CFR↓marginal, PER↓40%, SR↓47%) | **REFUTADO** |
| M1/M2 resolvem B2 | 6.4.2 (N=5: CFR=0) — não reproduzido em N=10 | **NÃO DEMONSTRADO** |
| M1/M2 são promissores | 6.4.2 (N=5: CFR=0, EBA=100%, PER=75%, SR=75%) | **HIPÓTESE SUPORTADA** |
| H-TEMP impede validação | 6.4.2-B (PER=0 em N=10) | **DEMONSTRADO** |
| Ancoragem > proibição | 6.4.1-A (A1: PER↓40%) vs 6.4.2 (M1/M2: PER↓25%) | **SUPORTADO (preliminar)** |

---

## 8. VEREDITO EPISTEMOLÓGICO FINAL

### 8.1 B2 não está resolvido

B2 permanece como **CONTROLLED LIMITATION**. Nenhuma intervenção foi validada estatisticamente.

### 8.2 B2 não é uma falha indeterminada

O AION caracterizou uma classe específica de falha de proveniência — F3 — com:
- Mecanismo identificado (transdução evidência→identificador sob competição de schemas)
- Detecção determinística (validator P-RESP-001 v0.3, VR=100%)
- Decomposição matemática (FR = PER × CFR_RUN)
- Separacão de emissão (PER) e confiabilidade (CFR)

### 8.3 Limite de inferência

A principal limitação remanescente é a **não-estacionariedade de PER** (H-TEMP), que impede:
- Estimar FR de maneira confiável por agregação de sessões heterogêneas
- Validar intervenções (M1/M2) com poder estatístico adequado
- Distinguir variabilidade temporal de efeito de intervenção

### 8.4 O que NÃO pode ser afirmado

- "B2 foi resolvido" — não há validação estatística
- "M1/M2 eliminam fabricação" — N=5 insuficiente, não reproduzido em N=10
- "O LLM é temporalmente instável" — H-TEMP é observação do ambiente específico
- "A causa raiz é o schema" — schema é causa contribuinte confirmada, mas não única (prompt também contribui)
- "B2 é permanente" — a limitação é do ambiente experimental, não necessariamente do sistema

### 8.5 O que PODE ser afirmado

- F3 é o mecanismo dominante de fabricação (93-100% em todas as sessões observáveis)
- F3 é um erro de transdução evidência→identificador (não alucinação aleatória)
- Validator intercepta 100% dos casos de F3 (VR=1.000 robustamente)
- FR = PER × CFR_RUN (decomposição confirmada)
- PER é não-estacionário no ambiente atual
- Ancoragem observacional (M1/M2) é preliminarmente superior a proibição cognitiva (A1)
- A1, M1, M2 são intervenções sobre a camada de geração, não sobre retrieval

---

## 9. ESTADO FINAL DO AION-MVP-001

```
AION-MVP-001
│
├── B1 ............... RESOLVED
│   ├── Retrieval: Top-1=3/3, determinístico
│   ├── Cross-lingual: PT-BR → EN tradução
│   └── Oracle v3: 7 chunks interversionais
│
├── B2 ............... CHARACTERIZED / CONTROLLED LIMITATION
│   ├── F3 ........... CHARACTERIZED (Provenance Transduction Error)
│   ├── Mechanism .... SUPPORTED (competição de schemas + transdução)
│   ├── PER ........... NON-STATIONARY (0%-80%)
│   ├── CFR ........... CONDITIONAL (≈47% quando observável)
│   ├── EBA ........... ≈68%
│   ├── VR ............ 100% (robustamente observado)
│   ├── A1 ............ PARTIAL / NEGATIVE TRADE-OFF
│   ├── M1 ............ CANDIDATE / UNVALIDATED
│   └── M2 ............ CANDIDATE / UNVALIDATED
│
├── B3 ............... FAIL-SYSTEM
├── B4 ............... PARTIAL
├── B5 ............... PASS-SEMANTIC
├── B6 ............... PARTIAL / TEMPORALLY BOUNDED
└── B7 ............... PASS-SEMANTIC
```

---

## 10. TRAJETÓRIA COMPLETA DA INVESTIGAÇÃO B2

| Fase | Resultado |
|---|---|
| 6.2.0-6.2.2 | Baseline: B1=FAIL-SYSTEM, diagnóstico inicial |
| 6.2.3-6.2.5 | Experimentos B/C/D (normalização, chunking, tokenização) — todos rejeitados |
| 6.2.6 | Top-k + E/F/G/H — apenas E (stopwords) parcial |
| 6.2.7 | E+B — pior que E isolado |
| 6.2.8 | Auditoria gabarito + lexical — classificação D (ambos problemas) |
| 6.2.9 | Oracle v2 + Cross-lingual J — Resultado B (evidência de mecanismo) |
| 6.2.10 | Equivalência interversional — CORPUS-006/007 EQUIVALENT |
| 6.2.11 | Oracle v3 + J — Top-1=3/3, determinístico → B1 RESOLVED |
| 6.2.12 | B2 isolation — falha não determinística (stochastic) |
| 6.3.0 | Baseline N=100: FR=15%, F3=93.3%, VR=100% |
| 6.3.1.1-2 | H-F3 confirmada: 14/14 F3 sob múltiplos schemas |
| 6.3.1-A | Piloto C0-C3 — INVALIDADO (prompt drift) |
| 6.3.1-A.1 | Reprodução com prompt correto — F3 reproduzido (FR=57%) |
| 6.3.1-B | P0/P1/P2 — P1/P2 = FALSAS SOLUÇÕES (supressão de provenance) |
| 6.3.1-C | C0/C1/C2 — INCONCLUSIVO (H-TEMP, PER=0) |
| 6.4.0 | Baseline N=100: PER=30%, CFR=47%, EBA=68%, FR=PER×CFR confirmado |
| 6.4.1-A | A1 evidence-bound — CANDIDATO FORTE (N=8, CFR=0) |
| 6.4.1-B | Validação N=25 — efeito real mas pequeno (CFR↓marginal, PER↓40%) |
| 6.4.1-C | ENCERRADO — A1 não promovida |
| 6.4.2 | M1/M2 minimal anchoring — CANDIDATO FORTE (N=5, CFR=0, EBA=100%) |
| 6.4.2-B | Validação N=10 — INCONCLUSIVO (PER=0, H-TEMP dominante) |
| **6.5.0** | **CARACTERIZAÇÃO E DELIMITAÇÃO EPISTEMOLÓGICA** |

---

*"Nenhuma afirmação de resolução sem validação. Nenhuma inferência além da evidência. Nenhuma limitação experimental transformada em propriedade permanente do sistema."*
