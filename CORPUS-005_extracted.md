# CORPUS-005 — Extração de Texto Estruturado

**Arquivo de origem:** `Cover_Letter_Paper_A_PRE_PT-BR.md` (conteúdo colado pelo autor no chat)
**ID do Corpus:** CORPUS-005
**Extração realizada em:** 2026-08-16T20:55:00+00:00
**Ferramenta:** Conversão direta de Markdown colado (texto fornecido pelo autor)
**Origem do material:** Conteúdo textual fornecido diretamente por Edson Carvalho do Nascimento na conversa.

---

## Metadados Declarados (do conteúdo)

| Campo | Valor | Proveniência |
|---|---|---|
| Para | Editor, *Physical Review E* (Statistical Physics) | `[E]` |
| De | Edson Carvalho do Nascimento (ORCID 0009-0003-5504-7439) | `[E]` ORCID confirmado pelo autor em mensagem separada |
| Data | 10 de agosto de 2026 | `[E]` — atualiza o `NÃO DECLARADO` do HTML canônico v1.2.0 |
| Assunto | Submissão do manuscrito "Coerência Relacional em Redes Biológicas..." | `[E]` |
| Idioma | Português (Brasil) | `[E]` |
| Versão referenciada | v6.1 REVTeX PT-BR (anexada) | `[E]` — verificação cruzada abaixo |

---

## Conteúdo Integral

### Carta de Apresentação — Paper A submetido à Physical Review E (PT-BR)

**Para:** Editor, *Physical Review E* (Statistical Physics)
**De:** Edson Carvalho do Nascimento (ORCID 0009-0003-5504-7439)
**Data:** 10 de agosto de 2026
**Assunto:** Submissão do manuscrito "Coerência Relacional em Redes Biológicas: Uma Estrutura Quantitativa de Conectomas a EEG"

---

Prezado Editor,

Encontra-se anexo nosso manuscrito intitulado "Coerência Relacional em Redes Biológicas: Uma Estrutura Quantitativa de Conectomas a EEG," submetido para consideração como Artigo Regular na *Physical Review E* (seção Statistical Physics).

#### Sumário da contribuição

O manuscrito introduz a camada biológica empírica do programa TCR/QDT: uma estrutura quantitativa — Teoria da Coerência Relacional (TCR) — propondo uma métrica unificada $\mathcal{C} = I \times S \times H^{\beta}$ para a coerência informacional de redes complexas. A métrica combina três componentes operacionalmente definidos: integração $I$ (informação mútua multivariada normalizada), simetria $S$ (índice de automorfismo de grafo), e entropia $H$ (entropia espectral normalizada). O expoente $\beta$ é calibrado via validação cruzada leave-one-out (LOOCV) sobre 12 fixtures sintéticas de conectomas, produzindo consistência de ranking perfeita ($\rho = 1.0$) para $\beta \in [0.1, 1.5]$; adotamos $\beta = 0.5$ como valor canônico.

A estrutura é validada em três regimes empíricos independentes:

- **P1 (Ranking de conectomas):** 12 conectomas de espécies de *C. elegans* a humanos HCP, ranking reproduzido com $p = 1.0$ (bootstrap, 3 réplicas).
- **P2 (Discriminação Drosophila):** 4 conectomas de *Drosophila* vs. 1.000 grafos aleatórios de grau pareado, $z = 28.4$, $p \approx 0$.
- **P3 (Classificação sono/vigília EEG):** banco de dados PhysioNet Sleep-EDF com reconstrução de fontes sLORETA, $91.2\% \pm 1.9\%$ acurácia, $F_1 = 0.912$, AUC $= 0.968$, $p < 10^{-4}$.

A métrica é adicionalmente submetida a análise de sensibilidade Sobol (confirmando $H$ como componente dominante) e ao teste de trivialidade computacional de Aaronson (produzindo $\mathcal{C} = 0$ para grafos expansores e matrizes de Vandermonde, como requerido).

#### Por que Physical Review E

*Physical Review E* é o veículo natural para este manuscrito por três razões:

- **Alinhamento de escopo:** a revista tem forte tradição de publicar trabalho quantitativo-métrico na interseção de física estatística de redes, teoria da informação, e biologia computacional.
- **Padrões metodológicos:** PRE exige rigor empírico e estatístico alto para métricas de sistemas complexos. Nosso manuscrito atende este padrão implementando calibração LOOCV, análise de sensibilidade Sobol, validação cruzada estratificada 10-fold com 10 repetições para P3, e intervalos de confiança explícitos via bootstrap.
- **Público:** o público da PRE é precisamente o público que pode avaliar criticamente tanto os pontos fortes quanto as limitações de uma métrica quantitativa de coerência.

#### Traços distintivos do manuscrito

1. **Transparência radical sobre limitações.** O manuscrito cataloga explicitamente seis inconsistências conhecidas, com três resolvidas nesta versão (circularidade de calibração via LOOCV; discrepância P3 sintético-vs-real via pipeline real-only; irrelevância do termo de recursão $R^\alpha$ via análise Sobol). As três restantes são diferidas para artigos complementares (B e C).

2. **Achado crítico da análise de ablação.** A métrica composta $\mathcal{C}$ atinge $91.2\%$ de acurácia em P3, mas o conjunto de features $\{I, S, H\}$ sem combinação multiplicativa atinge exatamente a mesma acurácia. Reportamos honestamente que $\mathcal{C}$ não adiciona poder discriminativo além de seus constituintes — reposicionando $\mathcal{C}$ como uma *assinatura estrutural interpretativa* para ranking e caracterização, em vez de uma feature discriminativa ótima.

3. **Escopo empírico.** Todas as validações atuais usam fixtures sintéticas de grafos (Watts-Strogatz, Barabási-Albert) calibradas para mimetizar propriedades estruturais do mundo real. O manuscrito compromete-se explicitamente à validação empírica v6.2 em WormWiring, Janelia Hemibrain, e Allen Mouse Brain Atlas antes da submissão final. A submissão atual é portanto posicionada como uma *contribuição metodológica* com suporte empírico preliminar, não como um achado empírico confirmado.

#### Status dos artigos complementares

Este manuscrito é o primeiro de uma trilogia:

- **Paper A** (esta submissão) — camada biológica empírica, alvo: *Physical Review E*.
- **Paper B** — camada quântico-dissipativa (power-law FMO com $R^2 = 0.988$, retração formal da hipótese cross-scale $\eta$), alvo: *Journal of Chemical Physics*. Em preparação.
- **Paper C** — camada categórico-tensorial-cosmológica (functor $\Phi_{\mathrm{cat}}$, tensor $Q_{\mu\nu}$, validações externas Chanyal/Sun/Pradhan, análise de falsificabilidade), **submetido à *Foundations of Physics* em 10 de agosto de 2026.**

O Paper A é auto-contido e legível independentemente, com referências explícitas aos Papers B e C onde resultados quântico-dinâmicos ou categóricos são invocados.

#### Nota de colaboração

Dr. B. C. Chanyal (Gargi Degree College, Índia) respondeu positivamente ao outreach e está avaliando a identificação algébrica entre sua equação de Einstein quaterniônica e o tensor $Q_{\mu\nu}$ apresentado no Paper C. Esta colaboração é reconhecida mas não afeta o conteúdo empírico do Paper A. A presente submissão reflete o trabalho independente do autor; Dr. Chanyal ainda não revisou este manuscrito e não tem responsabilidade por quaisquer erros que possa conter.

#### Falsificabilidade e limitações

Reconhecemos explicitamente:

- Todas as validações empíricas atuais baseiam-se em fixtures sintéticas de grafos; confirmação definitiva em conectomas reais está comprometida para v6.2.
- A métrica composta $\mathcal{C}$ não supera seus componentes como feature discriminativa (achado de ablação).
- O expoente de calibração $\beta = 0.5$ é robusto (consistência LOOCV $= 1.0$ sobre $[0.1, 1.5]$) mas não unicamente determinado; a estrutura permite qualquer $\beta$ nesta faixa sem mudança qualitativa nos resultados.

#### Conflitos de interesse e autoria

Sou o único autor. Declaro não haver conflitos de interesse, financeiros ou outros. O trabalho não recebeu financiamento externo. O manuscrito não foi publicado em outro local e não está sob consideração por outra revista.

#### Revisores sugeridos (opcional)

Para consideração do editor:

- **Prof. Olaf Sporns** (Indiana University) — ciência de redes de conectomas
- **Prof. Giulio Tononi** (University of Wisconsin) — teoria da informação integrada
- **Dr. Michele T. Young** (Allen Institute) — comparações empíricas de conectomas
- **Prof. Danielle Bassett** (University of Pennsylvania) — neurociência de redes

Não tenho relação pessoal ou profissional com nenhum dos revisores sugeridos.

Agradeço a consideração.

Atenciosamente,

Edson Carvalho do Nascimento
ORCID: 0009-0003-5504-7439
Lattes: http://lattes.cnpq.br/1695606186269515
Email: prof.edson.nascimento@protonmail.com
Curitiba, Brasil

---

#### Anexos (na submissão)

1. `Paper_A_v6.1_REVTeX_PT-BR.pdf` — Manuscrito principal (REVTeX 4.2, 128 KB)
2. `Paper_A_v6.1_REVTeX_PT-BR.tex` — Fonte LaTeX (suplementar)

**Nota:** Para submissão oficial à PRE, usar a versão em inglês (`Paper_A_v6.1_REVTeX_COMPLETE.pdf`) e a cover letter em inglês (`Cover_Letter_Paper_A_PRE.md`). Esta versão PT-BR é para referência do autor.

#### Status

⚠️ **AINDA NÃO PRONTO PARA SUBMISSÃO.** As Seções II, III, IV estão completas com fixtures sintéticos; validação definitiva requer processamento de dados empíricos (v6.2):

- WormWiring (conectoma C. elegans) — a ser baixado
- Janelia Hemibrain (Drosophila) — a ser baixado
- Allen Mouse Brain Atlas — a ser baixado
- PhysioNet Sleep-EDF (completo ~5 GB) — a ser baixado

Uma vez que os dados sejam processados (estimado 1-2 semanas), os placeholders serão substituídos por resultados empíricos, o manuscrito recompilado, e a submissão poderá prosseguir. Data estimada de submissão: final de agosto / início de setembro de 2026.

---

## Verificação Cruzada com Paper A (CORPUS-002)

Esta seção é a aplicação do Plano de Teste P4 (consistência entre documentos do corpus), antecipada manualmente.

### Contradições detectadas `[E]`

#### Contradição C1 — Versão do Paper A referenciada

| Fonte | Declaração |
|---|---|
| Cover Letter | "Anexo 1: `Paper_A_v6.1_REVTeX_PT-BR.pdf` — Manuscrito principal (REVTeX 4.2, 128 KB)" |
| Cover Letter | "Status: AINDA NÃO PRONTO PARA SUBMISSÃO" |
| Cover Letter | "Data estimada de submissão: final de agosto / início de setembro de 2026" |
| HTML canônico v1.2.0 | "Arquivo: Paper_A_v6.2_FINAL.pdf — Versão v6.2 — Estado: FINAL (submetido ao PRE)" |
| PDF extraído (CORPUS-002) | Metadados do PDF: creationDate 12 ago 2026, título "Relational Coherence in Biological Networks", autor "Edson C. do Nascimento" |
| Paper A (texto extraído) | "v6.2" declarado em múltiplas passagens; submetido ao PRE |

**Interpretação:** A Cover Letter em PT-BR é de uma versão **anterior** (v6.1) e está marcada como "ainda não pronto para submissão". A versão final v6.2 (que temos no corpus) foi compilada **2 dias depois** (12 ago 2026) e está marcada como FINAL/submetida. A Cover Letter PT-BR no corpus é portanto um **rascunho interno** que antecede a submissão real. A cover letter oficial enviada ao PRE é em inglês (`Cover_Letter_Paper_A_PRE.md`, sem sufixo PT-BR) e não está no corpus.

#### Contradição C2 — Resultados P3

| Fonte | P3 (EEG sono/vigília) |
|---|---|
| Cover Letter | "banco de dados PhysioNet Sleep-EDF com reconstrução de fontes sLORETA, **91.2% ± 1.9% acurácia, F1 = 0.912, AUC = 0.968, p < 10⁻⁴**" |
| Paper A (CORPUS-002) | "P3, **AUC = 0.793 ± 0.133** across 4 subjects, p < 0.05" |
| Paper A (CORPUS-002) | Dataset: "OpenNeuro ds003768" (NÃO PhysioNet Sleep-EDF) |
| Paper A (CORPUS-002) | "P3 uses real high-density EEG data but with a **preliminary sample of 4 subjects**; expansion to 10+ subjects is planned" |
| Paper A (CORPUS-002) | Seção V limitações: "expand P3 to 10+ subjects from ds003768" |

**Interpretação:** Esta é uma **contradição material severa**. A Cover Letter descreve P3 com métricas muito mais otimistas (AUC 0.968 vs 0.793; 91.2% acurácia não mencionada no paper) e atribui o resultado a um dataset diferente (PhysioNet Sleep-EDF vs OpenNeuro ds003768). A Cover Letter é **compatível com a versão v6.1 aspiracional** (que prometia o que seria feito em v6.2 com dados empíricos maiores); o Paper A v6.2 FINAL contém os resultados reais, mais modestos. A Cover Letter no corpus NÃO foi atualizada para refletir a v6.2.

#### Contradição C3 — Camada P1/P2

| Fonte | P1 (Ranking conectomas) | P2 (Discriminação Drosophila) |
|---|---|---|
| Cover Letter | "12 conectomas de espécies de *C. elegans* a humanos HCP" | "4 conectomas de *Drosophila* vs. 1.000 grafos aleatórios" |
| Paper A (CORPUS-002) | "12 synthetic connectome fixtures" | "Drosophila melanogaster connectomes vs degree-matched random graphs" — sem número explícito de grafos aleatórios |
| Paper A (CORPUS-002) | Seção V: "All results in this paper (P1, P2, Sobol, LOOCV) are based on synthetic connectome fixtures" | |

**Interpretação:** A Cover Letter descreve P1/P2 como validações em conectomas **empíricos** (C. elegans a humanos HCP, 4 conectomas Drosophila). O Paper A v6.2 FINAL declara que P1/P2 usam **fixtures sintéticos** (Watts-Strogatz, Barabási-Albert), com validação empírica prometida para v6.3 (não v6.2 — outra discrepância menor). Esta contradição reforça a interpretação de que a Cover Letter descreve o **plano aspiracional v6.1**, não o estado real v6.2.

#### Contradição C4 — Versão do Paper C

| Fonte | Status do Paper C |
|---|---|
| Cover Letter | "submetido à *Foundations of Physics* em 10 de agosto de 2026" |
| Paper A (CORPUS-002) | "reserved for a companion paper, Paper C" — sem menção a submissão |
| HTML canônico v1.2.0 | CORPUS-003 (Parte IV) descrito como "Documento teórico — difusão controlada", versão 1.0, 10 ago 2026 |

**Interpretação:** A Cover Letter afirma que o Paper C já foi submetido à Foundations of Physics em 10 de agosto de 2026. Como CORPUS-003 (Parte IV) tem a mesma data (10 ago 2026), é **plausível `[I]`** que a Parte IV seja a versão PT-BR do material submetido como Paper C. Isto confirma a hipótese H1 do relatório anterior (CORPUS-003 = rascunho do Paper C), mas adiciona um novo dado: **Paper C já foi submetido**. Isto é materialmente diferente do que Paper A v6.2 sugere ("reserved for a companion paper").

### Contradições NÃO detectadas (alinhamento confirmado)

Os seguintes pontos estão **consistentes** entre Cover Letter e Paper A:

- Métrica fundamental: $\mathcal{C} = I \times S \times H^\beta$ com $\beta = 0.5$
- Calibração LOOCV sobre 12 fixtures sintéticas
- Três componentes: I (integração), S (simetria/autormorfismos), H (entropia espectral)
- Análise Sobol confirma H como componente dominante
- Teste de Aaronson passa (C = 0 para expansores e Vandermonde)
- Achado de ablação: C não supera {I, S, H} como feature discriminativa
- Seis inconsistências catalogadas, três resolvidas, três diferidas
- Reconhecimento a B.C. Chanyal (quaternionic extensions)
- Compromisso com validação empírica em WormWiring, Janelia, Allen
- Trilogia: Paper A (biológico), Paper B (quântico), Paper C (cosmológico/categórico)

### Síntese da Verificação Cruzada

A Cover Letter PT-BR no corpus é um **rascunho interno de v6.1** que antecede a submissão real. Ela descreve o **plano aspiracional** do que seria feito em v6.2 (datasets empíricos, métricas otimistas), mas o Paper A v6.2 FINAL (que temos no corpus) contém os **resultados reais**, mais modestos. A Cover Letter em PT-BR NÃO foi atualizada para refletir a v6.2 — provavelmente porque a cover letter oficial enviada ao PRE é em inglês.

**Isto significa que T5 (a contradição que detectamos anteriormente) não é um caso de sobrevenda científica**, mas sim um **problema de versionamento documental**: o corpus contém uma Cover Letter de uma versão anterior do programa, não a Cover Letter que foi efetivamente enviada ao PRE.

### Implicação curatorial

A cover letter oficial enviada ao PRE (em inglês, `Cover_Letter_Paper_A_PRE.md` sem sufixo PT-BR) **não está no corpus**. Isto é uma **lacuna material** do corpus AION-001: ele não contém a versão final da carta de submissão. Recomenda-se:
- Adicionar `Cover_Letter_Paper_A_PRE.md` (versão EN) ao corpus em futura revisão do AION-CORPUS-001 (v1.3.0), ou
- Rebaixar a Cover Letter PT-BR no corpus atual de `[E]` para `[E-versiondraft]` — evidência textual de uma versão preliminar, não da submissão real.

Esta recomendação será incorporada à ontologia v1.0.0 como **T6** (lacuna documental identificada).
