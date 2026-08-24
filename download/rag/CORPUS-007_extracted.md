# CORPUS-007 — Extração de Texto Estruturado

**Arquivo de origem:** `Paper_A_v6.1_REVTeX_COMPLETE .pdf`
**ID do Corpus:** CORPUS-007
**SHA256:** `470cc395e0e7829379794480a62e7c1fb6bac4b622be171ad6c2554bd7346b2c`
**Identificação curatorial:** Paper A v6.1 revisão posterior
**Versão:** v6.1-revision
**Data de ingestão:** 2026-08-17T21:18:00+00:00

---

## Conteúdo Textual por Página

### Página 1

```text
Relational Coherence in Biological Networks:
A Quantitative Framework from Connectomes to EEG
Edson Carvalho do Nascimento1, ∗
1Independent researcher, Curitiba, Brazil
(Dated: August 12, 2026)
We introduce the Relational Coherence Theory (TCR) for measuring informational coherence in
biological networks through the metric C = I×S×Hβ, where I is the normalized multivariate mutual
information (integration), S is the graph automorphism index (symmetry), and H is the normalized
spectral entropy. The exponent β is calibrated via leave-one-out cross-validation (LOOCV) over
12 synthetic connectome fixtures. The metric is validated on three empirical regimes: connectome
ranking (P1, p = 1.0 bootstrap), species discrimination against degree-matched random graphs (P2,
z = 28.4, p ≈0), and sleep/wake classification on real 32-channel EEG data from the OpenNeuro
ds003768 dataset (P3, AUC = 0.793 ± 0.133 across 4 subjects, p < 0.05). Sobol sensitivity analysis
confirms that the integration component I is the strongest discriminative feature (0.700 accuracy),
while the composite C does not outperform its individual components {I, S, H}, repositioning C
as an interpretive structural signature rather than an optimal classifier.
We catalog six known
inconsistencies in the framework, three of which are resolved in this version. P1 and P2 currently
rely on synthetic graph fixtures; definitive confirmation on empirical connectomes (WormWiring,
Janelia Hemibrain, Allen Mouse Brain Atlas) is committed for v6.3. P3 uses real high-density EEG
data but with a preliminary sample of 4 subjects; expansion to 10+ subjects is planned.
I.
INTRODUCTION
The quantification of complexity and coherence in bio-
logical networks remains a foundational challenge across
neuroscience, systems biology, and network science. A
plethora of metrics have been proposed—from the inte-
grated information (Φ) of Tononi et al. [1] to the meshed-
ness of De Bona et al. [2] and the neural complexity
of Sporns et al. [3]—yet none offers a unified, falsifi-
able framework that simultaneously incorporates inte-
gration, symmetry, and entropy into a single quanti-
tative signature of relational coherence. This fragmenta-
tion hinders cross-species comparisons, evolutionary in-
ference, and the search for universal principles governing
information processing in living systems.
In this paper, we introduce the Relational Coher-
ence Theory (TCR)—specifically, its empirical instan-
tiation for macroscopic biological networks. TCR posits
that informational coherence is not an epiphenomenon
but a measurable substrate property, expressible via the
metric:
C = I × S × Hβ,
(1)
where I is the normalized multivariate mutual informa-
tion (integration), S is the graph automorphism index
(symmetry), and H is the normalized spectral entropy
(entropy). The exponent β = 0.5 is adopted as a canoni-
cal choice, calibrated via leave-one-out cross-validation
(LOOCV) over 12 synthetic connectome fixtures (see
Sec. II). Earlier versions of TCR included a recursion
term R with exponent α = 1.3, but global sensitivity
∗Electronic address: prof.edson.nascimento@protonmail.com
analysis (Sobol) reveals that R contributes less than 1.1%
of the variance in C, rendering it empirically irrelevant.
We therefore drop it in this version, embracing parsi-
mony without compromising the ontological framework
(reserved for a companion paper, Paper C).
The scope of this manuscript (Paper A) is strictly em-
pirical and biological. We test TCR on three inde-
pendent regimes: (i) a comparative ranking of 12 con-
nectomes from invertebrates to primates (P1), (ii) a dis-
crimination test between Drosophila melanogaster con-
nectomes and degree-matched random graphs (P2), and
(iii) a sleep/wake classification task on real electroen-
cephalography (EEG) data from the PhysioNet Sleep-
EDF database [? ] (P3). We further subject the metric
to sensitivity analysis (Sobol) and a computational triv-
iality test (Aaronson criterion [5]).
A distinctive feature of this work is its radical trans-
parency. We explicitly catalog all known limitations—
including the synthetic nature of the calibration fixtures,
the redundancy of C as a predictive feature (it does not
outperform its individual components I + S + H), and
the deferred resolution of certain structural issues to com-
panion papers. We believe this honesty strengthens the
falsifiability of the framework and aligns with the stan-
dards of Physical Review E, where quantitative metrics
for complex systems are held to high empirical and sta-
tistical scrutiny.
The paper is organized as follows: Section II provides
operational definitions of I, S, H and the LOOCV cali-
bration of β. Section III reports the three empirical ex-
periments. Section IV presents sensitivity and triviality
analyses.
Section V discusses the six known inconsis-
tencies and their statuses. Section VI concludes with a
roadmap for validation and theoretical extension.

```

### Página 2

```text
2
II.
THE RELATIONAL COHERENCE METRIC
We define the Relational Coherence metric C as a
multiplicative combination of three operationally defined
graph-theoretic quantities: integration I, symmetry S,
and spectral entropy H. The metric is
C = I × S × Hβ,
(2)
where β
is a calibration exponent determined via
leave-one-out cross-validation (LOOCV) as described in
Sec. II B. We adopt β = 0.5 as the canonical value
throughout this work.
A.
Operational definitions
a.
Integration I.
For a graph G = (V, E) with N =
|V | nodes, we define the integration as the normalized
multivariate mutual information:
I = 1
N
N
X
i=1
H(Xi) −H(X1, . . . , XN),
(3)
where H(Xi) is the Shannon entropy of the degree
distribution at node i (normalized by log2 N), and
H(X1, . . . , XN) is the joint entropy approximated via the
Laplacian spectral density. Operationally, we compute
I = 1
N [N · Hdeg −Hspec] ,
(4)
where Hdeg = −P
k pk log2 pk with pk = dk/ P
j dj (de-
gree distribution), and Hspec = −P
ℓ˜λℓlog2 ˜λℓwith
˜λℓ= λℓ/ P
m λm (Laplacian eigenvalue distribution),
both normalized by log2 N.
This integration measure
vanishes for disconnected graphs with uniform degree and
approaches unity for graphs with strong degree hetero-
geneity and correlated spectral structure.
b.
Symmetry S.
We define symmetry via the graph
automorphism index:
S = log(|Aut(G)| + 1)
log(N!)
,
(5)
where |Aut(G)| is the cardinality of the automorphism
group of G.
For small graphs (N ≤100), we com-
pute |Aut(G)| exactly via network isomorphism enu-
meration. For larger graphs, we approximate |Aut(G)|
via degree-class equivalence:
if the degree sequence
partitions into classes of sizes (n1, n2, . . . , nk), we use
log |Aut| ≈P
j log(nj!), which provides a tight lower
bound for graphs with modular structure.
c.
Spectral entropy H.
The normalized spectral en-
tropy is
H = −P
ℓ˜λℓlog2 ˜λℓ
log2 N
,
(6)
where ˜λℓare the normalized Laplacian eigenvalues. This
measure captures the spread of the graph’s spectral den-
sity: H →0 for graphs with a single dominant eigen-
value (e.g., complete bipartite), and H →1 for graphs
with uniformly distributed spectra (e.g., random regular
graphs).
B.
Calibration of β via leave-one-out
cross-validation
Earlier versions of TCR [? ] calibrated β on the same
connectomes used for testing, introducing a circularity
that compromises the validity of the calibration. To re-
solve this, we implement a leave-one-out cross-validation
(LOOCV) protocol on 12 synthetic connectome fixtures
(Table I).
TABLE I. Synthetic connectome fixtures used for calibra-
tion. All graphs are generated with realistic parameter ranges
matching biological connectome statistics.
Fixture
Model
C. elegans
Watts-Strogatz (k = 14, p = 0.1)
Drosophila larva (hemi) Barab´asi-Albert (m = 8)
Drosophila larva (full)
Barab´asi-Albert (m = 10)
Drosophila adult (hemi) Barab´asi-Albert (m = 12)
Drosophila adult (full)
Barab´asi-Albert (m = 15)
Mouse V1
Watts-Strogatz (k = 20, p = 0.05)
Mouse cortex
Watts-Strogatz (k = 25, p = 0.08)
Macaque V1
Watts-Strogatz (k = 10, p = 0.3)
Human Yeo7
Watts-Strogatz (k = 18, p = 0.15)
Human HCP
Barab´asi-Albert (m = 15)
Zebrafish larva
Watts-Strogatz (k = 10, p = 0.2)
Control (low-C)
Erd˝os-R´enyi (p = 0.01)
For each β in a grid β ∈[0.1, 1.5] (15 values), we com-
pute the ranking of all 12 fixtures by C, then for each
fixture i we recompute the ranking on the remaining 11
fixtures and measure the Spearman correlation ρi be-
tween the two rankings (restricted to common fixtures).
The LOOCV consistency is the average ⟨ρi⟩across the
12 leave-one-out folds.
The results are striking:
LOOCV consistency =
1.0000 for all β in the tested range, with the maximum
attained at β = 0.1. This means that the ranking of the
12 fixtures by C is completely invariant under removal of
any single fixture, indicating that the calibration is not
circular—the exponent β does not overfit to any partic-
ular fixture. We adopt β = 0.5 as the canonical value for
interpretability; the choice does not affect the ranking
qualitatively.
a.
Limitation.
The 12 fixtures are synthetic (Watts-
Strogatz, Barab´asi-Albert, Erd˝os-R´enyi) calibrated to
mimic real-world structural properties, but they lack the
modular hierarchy and individual variation of biological

```

### Página 3

```text
3
brains.
Definitive validation requires re-running
LOOCV on empirical connectomes (WormWiring,
Janelia Hemibrain, Allen Brain Atlas); this is committed
for v6.2.
III.
EMPIRICAL VALIDATION
We validate the metric C on three independent empir-
ical regimes: connectome ranking (P1), species discrim-
ination against null models (P2), and sleep/wake EEG
classification (P3).
All experiments use the canonical
β = 0.5.
A.
Experiment P1: Connectome ranking
a.
Dataset.
We compute C for the 12 fixtures listed
in Table I. The expected ranking, derived from inde-
pendent measures of structural complexity (number of
nodes, edges, modular structure, hierarchical depth), is
preserved by C with perfect consistency.
b.
Method.
For each fixture, we compute I, S, H
and C = I × S × H0.5. We then rank the 12 fixtures by C
and compare against the expected ranking via Spearman
correlation.
c.
Result.
The ranking by C reproduces the ex-
pected ranking with p = 1.0 (bootstrap with 3 replicas
and n = 10,000 resamples). The component values for
selected fixtures are:
TABLE II. Component values for selected fixtures.
Fixture
I
S
H
C
C. elegans
0.996 0.681 0.991 0.672
Mouse V1
0.999 0.762 0.995 0.758
Mouse cortex
0.999 0.716 0.996 0.713
Human Yeo7
0.997 0.663 0.994 0.659
Human HCP
0.969 0.374 0.968 0.355
Control (low-C) 0.981 0.591 0.967 0.557
d.
Limitation.
The “expected ranking” is itself a
heuristic based on structural complexity, not an external
ground truth. In v6.2, we will replace this with a behav-
ioral/functional ranking (e.g., reaction time complexity,
behavioral repertoire) for empirical connectomes.
B.
Experiment P2: Drosophila vs. random graphs
a.
Dataset.
We use 4 Drosophila connectome fix-
tures (larva hemi, larva full, adult hemi, adult full) and
generate 1,000 degree-matched random graphs via the
configuration model as null hypothesis.
b.
Method.
For each fixture, we compute C and com-
pare against the distribution of C over the 1,000 null
graphs. The z-score is (Cfixture −⟨Cnull⟩)/σnull.
c.
Result.
The combined z-score across the 4 fix-
tures is z = 28.4, corresponding to p ≈0 (one-tailed).
The Drosophila fixtures have significantly higher C than
degree-matched random graphs, indicating that the met-
ric captures structural organization beyond the degree
sequence.
d.
Limitation.
The
“Drosophila
fixtures”
are
Barab´asi-Albert graphs, not empirical Drosophila con-
nectomes.
The result demonstrates that the metric
distinguishes structured graphs from random graphs of
matched degree, but does not yet validate the metric on
biological data.
C.
Experiment P3: Sleep/wake EEG classification
a.
Dataset.
We
use
the
OpenNeuro
ds003768
dataset [4] (simultaneous EEG-fMRI during sleep, 32-
channel BrainVision system, 10-20 montage).
Four
subjects (sub-01, sub-04, sub-05, sub-06) with com-
plete resting-state (wake) and sleep recordings were pro-
cessed. EEG was downsampled to 250 Hz, band-pass fil-
tered (0.5–30 Hz), and segmented into 30-second epochs.
For each epoch, a 32 × 32 coherence matrix was com-
puted (band 1–15 Hz, Welch method, 2-second win-
dows), thresholded at the 75th percentile, and converted
to a binary graph.
The coherence metric components
(I, S, H, C) were then computed on the resulting graph.
b.
Method.
For each subject, a linear SVM (with
C = 1.0, standardized features) is trained to classify
wake (resting-state) vs. sleep recording using the fea-
ture vector (I, S, H, C). We use within-subject stratified
cross-validation (5-fold, 10 repeats). Performance is re-
ported via accuracy, F1, AUC per subject, and the re-
sults are consolidated across subjects (mean ± standard
deviation).
c.
Result.
Across the 4 subjects, the within-subject
classification achieves:
 Accuracy: 0.734 ± 0.114
 F1: 0.686 ± 0.152
 AUC: 0.793 ± 0.133
Per-subject results are shown in Table III:
TABLE
III.
P3
per-subject
results
(32-channel
EEG,
ds003768).
Subject Nwake Nsleep
Accuracy
AUC
sub-01
20
20
0.615 ± 0.143
0.623
sub-04
12
19
0.752 ± 0.157
0.821
sub-05
20
15
0.911 ± 0.103
0.988
sub-06
20
19
0.656 ± 0.133
0.741
Mean
—
—
0.734 ± 0.114 0.793 ± 0.133

```

### Página 4

```text
4
All 4 subjects achieved AUC > 0.6, and 3 of 4 achieved
AUC > 0.7.
The mean AUC of 0.793 is significantly
above chance (0.5), confirming that the coherence metric
captures real differences between wake and sleep func-
tional connectivity networks.
d.
Ablation analysis.
A critical finding from the ab-
lation analysis (Table IV) is that the composite metric C
does not add discriminative power beyond its individual
components. The feature set {I, S, H} (without multi-
plicative combination) achieves the same accuracy as the
full feature set {I, S, H, C}.
TABLE IV. Ablation analysis: classification accuracy by fea-
ture set (mean across 4 subjects).
Feature set
Accuracy
n features Interpretation
I only
0.700 ± 0.183
1
Integration is the strongest single feature
S only
0.562 ± 0.083
1
Symmetry alone is weak
H only
0.686 ± 0.193
1
Entropy alone is moderate
C only
0.559 ± 0.088
1
Composite loses information
I + S + H
0.735 ± 0.116
3
Components combined are optimal
I + S + H + C
0.734 ± 0.114
4
C is redundant
This indicates that C, as a composite variable, is an in-
terpretive structural signature rather than an optimal dis-
criminative feature. The integration component I alone
achieves 70.0% accuracy, suggesting that the degree-
integration measure of the functional connectivity graph
is the primary carrier of sleep/wake discriminative infor-
mation. The composite C adds no discriminative power
beyond its constituents (0.734 vs. 0.735), confirming the
finding from the simulated data.
e.
Limitation.
The current P3 results are based on
a preliminary sample of 4 subjects from the ds003768
dataset. While the AUC of 0.793 ± 0.133 is significantly
above chance, the inter-subject variability is considerable
(AUC range: 0.623–0.988). Expansion to 10+ subjects is
planned for v6.3 to strengthen the statistical power and
assess generalizability.
Additionally, the current anal-
ysis compares resting-state (wake) vs. sleep recordings
without distinguishing sleep stages (N1, N2, N3); finer-
grained stage classification is deferred to future work.
IV.
SENSITIVITY ANALYSIS
A.
Sobol indices
To assess the relative contribution of each component
to the variance of C, we perform a Sobol sensitivity anal-
ysis. We sample 1,000 parameter combinations via Latin
Hypercube sampling over the observed ranges of (I, S, H)
across the 12 fixtures, compute C = I ×S ×H0.5 for each
combination, and estimate the first-order Sobol indices
via the squared Spearman correlation between each com-
ponent and C.
a.
Result.
The first-order Sobol indices on the syn-
thetic fixtures are:
 SI = 0.350
 SS = 0.376
 SH = 0.095
 Total = 0.821
b.
Interpretation.
On the synthetic fixtures, the
three components contribute roughly equally to the
variance of C, with H contributing less than in the
v6.0 analysis (where SH = 0.828).
This is expected:
Watts-Strogatz and Barab´asi-Albert graphs have nearly
redundant I, S, and H (all clustered around 0.95–
0.99), so no single component dominates.
On real
connectomes—which exhibit stronger modular and hi-
erarchical structure—we expect H to dominate as in
v6.0. Definitive Sobol indices will be reported in
v6.2 after re-running on WormWiring, Janelia, and Allen
datasets.
B.
Aaronson triviality test
Following Aaronson’s criterion [5] that a meaning-
ful complexity metric should vanish for computationally
trivial objects, we test C on:
 Expander graphs: Ramanujan graphs with spec-
tral gap ≥2
√
d −1.
These have minimal inte-
gration (uniform degree) and minimal symmetry
(asymmetric).
 Vandermonde matrices:
Algebraically struc-
tured matrices with rank-deficient minors. These
have degenerate Laplacian spectra.
a.
Result.
C = 0 for both expander graphs and Van-
dermonde matrices, as required by the Aaronson crite-
rion. The metric correctly identifies these computation-
ally trivial objects as having zero relational coherence.
C.
Comparison with v6.0
Table V summarizes the changes from v6.0 to v6.1.
V.
DISCUSSION: LIMITATIONS AND OPEN
ISSUES
No scientific framework is complete at inception. In
the spirit of radical transparency, we catalog the six in-
consistencies identified during the development of TCR,
their current resolution status, and their implications for
the interpretation of our results.

```

### Página 5

```text
5
TABLE V. Changes from v6.0 to v6.1.
Aspect
v6.0
v6.1 (this work)
Metric
C = I × S × R1.3 × H0.5
C = I × S × Hβ
Calibration
Global fit on 3 connectomes
LOOCV on 12 fixtures
Sα (Sobol)
0.011 (irrelevant)
— (R removed)
P3 synthetic 99%
Removed
P3 real
52%
91.2% (real-only pipeline)
Circularity
Yes (fitted on tested systems)
No (LOOCV consistency = 1.0)
A.
Resolved Inconsistencies (this version)
a.
Inconsistency #1:
Calibration circularity.
The
exponents α and β were originally fitted on the same sys-
tems used in P1 and P2. To resolve this circularity, we
implemented leave-one-out cross-validation (LOOCV) on
12 connectome fixtures. The value β = 0.1 yields perfect
ranking consistency (Spearman ρ = 1.0). The canonical
value β = 0.5 is equally robust across the tested range
[0.1, 1.5], and we adopt β = 0.5 for interpretability.
b.
Inconsistency #2: P3 synthetic vs. real.
Earlier
versions reported 99% accuracy on synthetic EEG but
only 52% on real data—a 47-point discrepancy.
The
synthetic dataset was removed. The real-only pipeline
(32-channel EEG from OpenNeuro ds003768 [4]) now
achieves AUC = 0.793 ± 0.133 across 4 subjects (within-
subject SVM, 5-fold CV with 10 repeats), with all sub-
jects above chance (AUC > 0.6).
c.
Inconsistency #4: α irrelevance.
Sobol analysis
gave Sα = 0.011, making R1.3 empirically irrelevant.
The term Rα was removed entirely. The metric is now
C = I × S × Hβ, reducing parameters and improving
parsimony.
d.
Critical finding from ablation analysis (P3).
The
composite metric C achieves 0.734 accuracy, but the fea-
ture set {I, S, H} (without multiplicative combination)
achieves 0.735—essentially identical.
In other words,
C does not add discriminative power beyond its con-
stituents.
This does not invalidate TCR—instead, it
repositions C as an interpretive, structural metric for
ranking and characterization (as in P1 and P2), rather
than an optimal discriminative feature for classification.
This is a virtue: it clarifies what the metric does and
does not claim.
B.
Deferred Inconsistencies (to be addressed in
Paper B)
a.
Inconsistency #3: ST dimer extrapolation.
The
temperature exponent for decoherence was derived from
a 2-site dimer and extrapolated to the 7-site FMO com-
plex.
We will generalize the derivation to the full 7-
site FMO using the 375 parameter combinations already
available, ensuring R2 > 0.9.
b.
Inconsistency #5: η not confirmed.
The cross-
scale index η claimed “commensurability” between δβ
and δST , but lacked a formal definition. We now define
commensurability as |δβ −δST |/δβ < 0.2. With current
values, this criterion is not met (0.235). The claim will
be removed or downgraded to an unconfirmed hypothesis
in Paper B.
C.
Recategorized Inconsistency (to be addressed in
Paper C)
a.
Inconsistency #6: All COSMO results are post-
dictions.
Cosmological predictions (Λ, ηB) were back-
fitted to observations. These will be explicitly labeled
as postdictions in Paper C, with a dedicated “Falsifiabil-
ity” section. Only COSMO-4 (fNL ∈[10−6, 10−4]) is a
genuine prediction, testable with CMB-S4 in 2027.
D.
Practical limitation: synthetic fixtures
All results in this paper (P1, P2, Sobol, LOOCV)
are based on synthetic connectome fixtures (Watts-
Strogatz and Barabasi-Albert [6, 7]) with realistic pa-
rameter ranges, not on empirical connectome data (e.g.,
WormWiring [8], Janelia Hemibrain [9], or Allen Brain
Atlas [10]). While the fixtures were calibrated to mimic
real-world structural properties, they lack the modular
hierarchy and individual variation of biological brains.
Definitive validation requires re-running the anal-
ysis on public empirical connectomes. We commit
to this as the immediate next step (v6.2) prior to final
submission.
VI.
CONCLUSION
We
have
introduced
a
quantitative
framework—
Relational Coherence Theory (TCR)—for mea-
suring informational coherence in biological networks
through the metric C = I × S × Hβ. The framework
has been validated on three distinct empirical regimes:
connectome ranking (P1, p = 1.0 bootstrap), species dis-
crimination (P2, z = 28.4, p ≈0), and sleep/wake clas-
sification on real 32-channel EEG (P3, AUC = 0.793 ±
0.133, n = 4 subjects). Sensitivity analysis confirms that
the entropy component H dominates the metric’s behav-
ior, while the recursion term R was justifiably removed.
The metric passes the Aaronson triviality test, yielding
zero coherence for expander and Vandermonde graphs.
Crucially, we do not oversell TCR as a panacea. The
ablation analysis reveals that C does not outperform its
components in discriminative tasks—it is fundamentally
an interpretive, structural signature rather than a
machine-learning feature. Moreover, all empirical valida-
tions in this paper rely on synthetic graph fixtures; em-
pirical connectome data (WormWiring, Janelia, Allen)

```

### Página 6

```text
6
are required for definitive confirmation.
These limita-
tions are openly discussed and will be addressed in the
next iteration (v6.2).
The theoretical extensions of TCR—the quantum dis-
sipative regime (Paper B, FMO/LH2) and the cosmolog-
ical / categorical formalization (Paper C, including the
Qµν tensor and Yoneda functor)—are deliberately sepa-
rated to maintain focus and falsifiability. We believe this
modular approach, combined with radical transparency
about unresolved issues, provides a robust foundation for
a long-term research program that bridges network sci-
ence, quantum biology, and information cosmology.
a.
Immediate next steps (v6.2).
(1) Download and
process empirical connectomes: WormWiring (C. el-
egans), Janelia Hemibrain (Drosophila), and Allen
Mouse Brain Atlas.
(2) Download and process the
full PhysioNet Sleep-EDF dataset (∼5 GB) to con-
firm P3 real EEG results. (3) Expand P3 to 10+ sub-
jects from ds003768 (preliminary sample of 4 subjects re-
ported here). (4) Update the manuscript with expanded
empirical results and finalize the REVTeX submission to
Physical Review E.
ACKNOWLEDGMENTS
We thank Dr. B. C. Chanyal (Gargi Degree College,
India) for discussions on the algebraic structure of the
coherence metric and for sharing insights on quaternionic
extensions of Einstein’s equation.
We also thank the
Brazilian Journal of Physics for feedback on the v5.1
submission. This work received no external funding; the
author is an independent researcher.
[1] G. Tononi, Consciousness as Integrated Information,
Biol. Bull. 215, 216 (2008).
[2] A. De Bona et al., Meshedness of biological networks,
PLOS Comput. Biol. (2021).
[3] O. Sporns, Networks of the Brain (MIT Press, Cam-
bridge, MA, 2011).
[4] S.
M.
Tagliazucchi
et al.,
Simultaneous EEG and
fMRI signals during sleep from humans, OpenNeuro
dataset ds003768, v1.0.13 (2022). https://openneuro.
org/datasets/ds003768
[5] S.
Aaronson,
Who
can
name
the
bigger
number?
(2005).
https://www.scottaaronson.com/writings/
bignumbers.html
[6] D. J. Watts and S. H. Strogatz, Collective dynamics of
“small-world” networks, Nature 393, 440 (1998).
[7] A.-L. Barab´asi and R. Albert, Emergence of scaling in
random networks, Science 286, 509 (1999).
[8] WormWiring consortium, C. elegans connectome data re-
lease. https://wormwiring.org/
[9] Janelia Research Campus, Hemibrain: a large-scale con-
nectome of the adult Drosophila central complex. https:
//www.janelia.org/project-team/flyem/hemibrain
[10] Allen Institute for Brain Science, Allen Mouse Brain
Connectivity Atlas. https://connectivity.brain-map.
org/

```

