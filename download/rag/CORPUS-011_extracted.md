# CORPUS-011 — Extração de Texto Estruturado

**Arquivo de origem:** `Paper_B_QDT_v6.1_PT.pdf`
**ID do Corpus:** CORPUS-011
**SHA256:** `30476135b03b182d8d38c74fc2b276119a356c5ced293797fdf9ccc7f70ba916`
**Identificação curatorial:** Paper B v6.1 PT (novo, 5 págs)
**Versão:** v6.1
**Data de ingestão:** 2026-08-17T21:18:00+00:00

---

## Conteúdo Textual por Página

### Página 1

```text
Escalonamento Quântico Dissipativo no Complexo Fenna-Matthews-Olson:
Um Expoente de Temperatura em Lei de Potência a partir da Topologia de 7 Sítios
Edson Carvalho do Nascimento1, ∗
1Pesquisador independente, Curitiba, Brasil
(Dated: August 17, 2026)
Reportamos uma análise de escalonamento abrangente do tempo de coerência eletrônica T2 no
complexo pigmento-proteico Fenna-Matthews-Olson (FMO) de Chlorobium tepidum, tratando os
sete sítios cromofóricos de bacterioclorofila em pé de igualdade. Usando uma propagação HEOM
(Hierarchical Equations of Motion) numericamente exata validada no nível de truncamento L = 2,
complementada por um ajuste de escalonamento semi-analítico sobre 375 combinações de parâmetros
cobrindo as faixas biologicamente plausíveis do acoplamento inter-sítios J, energia de reorganização
λ, corte do banho γ, e temperatura T, obtemos a relação em lei de potência
T2 = K · J0.831 · λ−0.843 · γ−0.766 · T −0.261,
R2 = 0.988.
O expoente de temperatura ST = −0.261 generaliza a extrapolação do dímero de 2 sítios previa-
mente reportada e é consistente, dentro dos limites do modelo de banho Drude–Lorentz, com um
regime crítico no campo de coerência subjacente. Retraímos formalmente o índice de comensurabil-
idade inter-escala η anteriormente alegado, sob o argumento de que o critério de comensurabilidade
|δβ −δST |/δβ < 0.2 não é satisfeito (razão medida: 0.291). A correlação DII (Índice de Inversão
Dinâmica) entre simetria estrutural e recuperação de coerência é r = +0.459. Discutimos a conexão
destes resultados com a camada de criticalidade do programa TCR/QDT (subnível 0.2) e identifi-
camos a tarefa teórica em aberto de derivar ST dos expoentes críticos de uma ação efetiva do tipo
ϕ4.
I.
INTRODUÇÃO
A observação de coerências eletrônicas de longa du-
ração em complexos pigmento-proteicos fotossintéticos
— primeiro reportada por Engel et al. [1] para o complexo
Fenna-Matthews-Olson (FMO) e subsequentemente con-
firmada em centros de reação [2], algas criptófitas [3],
e na antena LHCII de plantas superiores [4] — mo-
tivou uma década de trabalho teórico sobre os mecan-
ismos pelos quais ambientes ruidosos, quentes e úmi-
dos podem sustentar, em vez de destruir, coerência
quântica.
Os mecanismos propostos cobrem o espec-
tro desde transporte quântico assistido por ambiente
(ENAQT) [5, 6], passando por modelos de ressonância
quântico-clássica [7], até argumentos de densidade espec-
tral estruturada [8]. Apesar desta atividade, não emergiu
uma lei de escalonamento consensual que capture a de-
pendência conjunta do tempo de coerência T2 nos quatro
parâmetros físicos primários — acoplamento inter-sítios
J, energia de reorganização λ, corte do banho γ, e tem-
peratura T — ao longo do regime paramétrico biologica-
mente plausível.
Este artigo apresenta tal lei de escalonamento para o
complexo FMO de sete sítios. O resultado central é a
relação em lei de potência dada no resumo, com o ex-
poente de temperatura ST = −0.261 sendo o principal
diagnóstico do regime dinâmico subjacente. O resultado
substitui a extrapolação do dímero de 2 sítios reportada
em versões anteriores do programa TCR/QDT [15]; a
∗Endereço eletrônico: prof.edson.nascimento@protonmail.com
extrapolação do dímero foi identificada como uma gener-
alização não controlada, e o presente trabalho endereça
diretamente esta questão (Inconsistência #3 da auditoria
v6.0) computando ST a partir do Hamiltoniano completo
de 7 sítios com propagação HEOM.
Um segundo resultado deste artigo é a retração for-
mal do índice de comensurabilidade inter-escala η.
O
índice η foi anteriormente alegado como indicador de uma
comensurabilidade quantitativa entre o expoente de tem-
peratura ST e o expoente métrico β do arcabouço de co-
erência relacional; na presente análise, a razão medida
|δβ −δST |/δβ = 0.291 excede o limiar de comensurabili-
dade de 0.2, e a alegação é portanto formalmente retraída
(Inconsistência #5 da auditoria v6.0).
O restante do artigo está organizado como segue. A
Seção II especifica o Hamiltoniano do sistema e o modelo
de banho Drude–Lorentz. A Seção III descreve a propa-
gação HEOM e sua validação.
A Seção IV reporta o
ajuste de escalonamento e os expoentes principais.
A
Seção V reporta a correlação DII. A Seção VI discute a
conexão com criticalidade. A Seção VII retrata formal-
mente η. A Seção VIII discute limitações e a Seção IX
conclui.
II.
MODELO DE SISTEMA E BANHO
A.
Hamiltoniano do sistema
O complexo FMO de Chlorobium tepidum é modelado
como sete sítios cromofóricos acoplados de bacteriocloro-

```

### Página 2

```text
2
fila a (BChl a), com o Hamiltoniano padrão
ˆHS =
7
∑
n=1
ϵn |n⟩⟨n| +
∑
m̸=n
Jmn |m⟩⟨n|,
(1)
onde ϵn são as energias de sítio e Jmn são os acoplamen-
tos inter-sítios. Usamos a parametrização de Adolphs–
Renger [9] para as energias e acoplamentos a T = 77 K
e T = 300 K. Para cobrir a faixa biológica, adicional-
mente reescalamos J →αJJ com αJ ∈[0.5, 2.0], co-
brindo regimes de acoplamento fraco a forte.
B.
Modelo de banho
Cada sítio é acoplado a um banho Drude–Lorentz in-
dependente,
Jn(ω) = 2λ
ωγ
ω2 + γ2 ,
(2)
onde λ é a energia de reorganização e γ é a frequência
de corte do banho.
Amostramos λ ∈[10, 200] cm−1 e
γ ∈[30, 200] cm−1, cobrindo as faixas experimentalmente
constrangidas reportadas na literatura de espectroscopia
FMO [9, 10]. A temperatura do banho T é amostrada
em [77, 300] K, cobrindo a faixa criogênica a fisiológica.
O acoplamento sistema-banho é tratado na base de
sítios, com banhos independentes para cada sítio (a
hipótese de acoplamento “local” ou “independente de sí-
tio”). O Hamiltoniano total é
H = ˆHS +
∑
n
[ 1
2p2
n + 1
2ω2
nx2
n −cnxn|n⟩⟨n|
]
,
(3)
com cn = √2λnωn/(2π).
III.
PROPAGAÇÃO HEOM
A.
Equações de movimento
A abordagem HEOM [11–13] propaga a matriz de den-
sidade reduzida ˆρ(t) juntamente com uma hierarquia de
matrizes de densidade auxiliares (ADMs) que codificam
a memória do banho. As equações de movimento são
˙ρn = −

i ˆHS +
∑
m,k
nmkνk

ρn−i
∑
m,k
[Qm, ρn+emk]−i
∑
m,k
nmk(cmkQmρn−emk−c∗
mkρn−emkQm),
(4)
onde Qm = |m⟩⟨m| são os operadores de acoplamento
sistema-banho, νk são as frequências de Matsubara, e cmk
são os coeficientes de correlação do banho. A hierarquia
é truncada no nível L via o terminador padrão [13].
B.
Validação
Validamos a propagação HEOM no nível de trunca-
mento L = 2 contra o resultado analítico exato para
um dímero de 2 sítios a T = 300 K, λ = 35 cm−1,
γ = 106 cm−1, J = 40 cm−1. A concordância é melhor
que 0.5% no tempo de coerência T2 extraído de |ρ12(t)|
via o critério de decaimento 1/e.
Para o complexo FMO de 7 sítios, a propagação com
L = 2 é numericamente tratável em uma estação de tra-
balho única (tempos de execução de aproximadamente
4 horas por combinação de parâmetros em um AMD
Threadripper 3970X). O truncamento em L ≥3 exige
recursos de cluster e fica para uma validação completa
futura; os resultados com L = 2 são reportados aqui
como estimativa semi-analítica, com a ressalva de que a
convergência quantitativa em L = 3 pode deslocar val-
ores individuais de T2 em até 5–10%. Os expoentes de
escalonamento reportados na Seção IV são, no entanto,
robustos a este nível de incerteza, conforme confirmado
por uma análise perturbativa do erro de truncamento.
C.
Nota de API
A implementação HEOM usa o pacote qutip 5.x [14]
via o módulo qutip.nonmarkov.heom.
A API foi val-
idada contra a suíte de testes publicada por Chen
et al. [13], com todos os casos de referência reproduzindo
os tempos de coerência publicados dentro das tolerân-
cias declaradas. Um pequeno número de mudanças de
API entre qutip 4.x e 5.x exigiu migração das definições
dos coeficientes de correlação do banho; a migração está
documentada no repositório de código suplementar.
IV.
ANÁLISE DE ESCALONAMENTO
A.
Varredura de parâmetros
Amostramos N = 375 combinações de parâmetros co-
brindo:
• Escala
de
acoplamento
inter-sítios
αJ
∈
{0.5, 0.75, 1.0, 1.25, 1.5, 2.0} (6 valores),
• Energia
de
reorganização
λ
∈
{10, 35, 50, 80, 100, 150, 200} cm−1 (7 valores),
• Corte do banho γ ∈{30, 60, 106, 150, 200} cm−1 (5
valores),
• Temperatura T ∈{77, 150, 200, 250, 300} K (5 val-
ores),
fornecendo 6 × 7 × 5 × 5 = 1050 combinações brutas, das
quais 375 convergiram dentro do orçamento de tempo
L = 2 e são reportadas aqui.

```

### Página 3

```text
3
B.
Ajuste de escalonamento
Para cada combinação de parâmetros, o tempo de co-
erência T2 é extraído do elemento fora-da-diagonal da
matriz de densidade |ρ12(t)| via o critério de decaimento
1/e. O ajuste de escalonamento assume a forma multi-
plicativa
T2 = K · JaJ · λaλ · γaγ · T aT ,
(5)
e os expoentes (aJ, aλ, aγ, aT ) são obtidos por regressão
linear de log T2 contra log J, log λ, log γ, log T.
C.
Resultado
Os expoentes ajustados são:
aJ = 0.831,
aλ = −0.843,
aγ = −0.766,
ST ≡aT = −0.261,
(6)
com o coeficiente de regressão R2 = 0.988 sobre as
375 combinações.
O pré-fator é K = 1.42 × 10−3 ps ·
cm−1/KST .
Os sinais são fisicamente interpretáveis:
maior acoplamento inter-sítios J estende coerência (ex-
poente positivo), enquanto maior energia de reorganiza-
ção, corte do banho, e temperatura encurtam coerência
(expoentes negativos), consistente com a imagem conven-
cional de decoerência induzida por ambiente.
O expoente de temperatura ST = −0.261 é o resul-
tado principal deste artigo. É significativamente menor
em magnitude que o escalonamento linear em T ST = −1
predito pela teoria de Lindblad simples e o escalonamento
ST = −2 predito por modelos de defasagem pura. O ex-
poente fracionário indica um regime dinâmico mais sutil,
que discutimos na Seção VI.
TABLE I. Expoentes de escalonamento ajustados para o com-
plexo FMO de 7 sítios. Intervalos de confiança são 95% boot-
strap sobre 1.000 reamostragens.
Expoente Significado físico
Valor
IC 95%
aJ
Acoplamento inter-sítios
+0.831
[0.812, 0.851]
aλ
Energia de reorganização
−0.843
[−0.866, −0.819]
aγ
Corte do banho
−0.766
[−0.788, −0.743]
ST
Temperatura
−0.261
[−0.275, −0.248]
K
Pré-fator
1.42 × 10−3 [1.31 × 10−3, 1.55 × 10−3]
V.
ÍNDICE DE INVERSÃO DINÂMICA
A.
Definição
O Índice de Inversão Dinâmica (DII) mede o grau em
que a simetria estrutural do grafo de sítios FMO prediz
a recuperação de coerência após uma perturbação ini-
cial. Para cada par de sítios (m, n), computamos a am-
plitude máxima de coerência |ρmn(t)|max alcançada após
o decaimento inicial, normalizada pela amplitude inicial
|ρmn(0)|.
O DII é a correlação de Pearson entre esta
razão de recuperação e o índice de automorfismo teórico-
grafos Smn do par de sítios.
B.
Resultado
Sobre os 21 pares de sítios únicos do complexo FMO
de 7 sítios, a correlação DII é
rDII = +0.459,
p < 0.05
(t-test, gl = 19).
(7)
Isso indica uma correlação moderada, porém estatistica-
mente significativa, entre simetria estrutural e recuper-
ação de coerência. O resultado é consistente com a com-
ponente de simetria S da métrica de coerência relacional
C = I·S·Hβ reportada no Paper A [15], onde S captura a
estrutura de automorfismo do grafo de sítios subjacente.
VI.
CONEXÃO COM CRITICALIDADE
O expoente de temperatura fracionário ST = −0.261
é uma assinatura de um sistema próximo a um ponto
crítico. Em um modelo de defasagem de Lindblad sim-
ples, o tempo de coerência escala como T2 ∝1/(γϕ)
onde γϕ é a taxa de defasagem, que é ela própria pro-
porcional a T no limite de alta temperatura, fornecendo
ST = −1. No limite de defasagem pura com densidade
espectral estruturada, o escalonamento pode ser mais
íngreme, ST = −2.
O expoente fracionário observado
ST = −0.261 é significativamente mais raso que qualquer
das predições, sugerindo que o complexo FMO opera em
um regime onde a decoerência é parcialmente suprimida
por flutuações estruturadas do banho — um regime con-
sistente com a proximidade a um ponto crítico.
Dentro do arcabouço TCR/QDT, conjectura-se que
o campo de coerência C situa-se em um ponto crítico
de uma ação efetiva ϕ4 [16].
Os expoentes críticos
(ν, βcrit, γ, δ) desta ação estão, em princípio, relacionados
aos expoentes de escalonamento dinâmico de observáveis
físicos. A derivação de ST a partir destes expoentes críti-
cos é a principal tarefa teórica em aberto do programa;
ainda não somos capazes de fornecer esta derivação, e ro-
tulamos explicitamente a conexão entre ST e criticalidade
como uma hipótese (Hipótese H0.2.b da formalização do
Nível 0) em vez de uma consequência derivada.
Duas assinaturas empíricas consistentes com a hipótese
de criticalidade são notadas. Primeiro, o escalonamento
em lei de potência de T2 com T vale uniformemente so-
bre as 375 combinações de parâmetros, sem mudança
de regime observada entre os extremos criogênico (T =
77 K) e fisiológico (T = 300 K). Esta invariância de es-
cala é uma assinatura de regimes críticos. Segundo, a
pequena magnitude de ST (comparado a ST = −1 para
Lindblad e ST = −2 para defasagem pura) indica um
regime onde a decoerência é parcialmente compensada

```

### Página 4

```text
4
por dinâmica coerente — uma compensação que surge
naturalmente em sistemas críticos.
VII.
RETRAÇÃO DO ÍNDICE η
Versões anteriores do programa TCR/QDT [15] intro-
duziram um índice de comensurabilidade inter-escala η
alegado como medida da correspondência quantitativa
entre o expoente métrico β = 0.5 e o expoente de tem-
peratura ST . Retraímos esta alegação.
O critério de comensurabilidade adotado na presente
versão é:
η é satisfeito se
|δβ −δST |
δβ
< 0.2,
(8)
onde δβ = 0.5 −0.1 = 0.4 (a variação de β ao longo da
faixa LOOCV testada no Paper A) e δST = |Scriognico
T
−
Sﬁsiolgico
T
| = 0.117 (a variação observada de ST ao longo
da faixa de temperatura). A razão medida é
|0.4 −0.117|
0.4
= 0.708,
(9)
que está bem acima do limiar de comensurabilidade. (Um
cálculo anterior, menos conservador, reportou razão de
0.291; ambos os valores excedem o limiar.) Retraímos
portanto a alegação η e a rebaixamos a uma hipótese
não confirmada no Paper B.
Esta retração endereça a Inconsistência #5 da audi-
toria v6.0.
A retração não afeta o resultado central
(ST = −0.261) ou a conexão com criticalidade, ambos
independentes de η.
VIII.
DISCUSSÃO: LIMITAÇÕES
A.
Truncamento HEOM
A propagação HEOM reportada aqui usa nível de trun-
camento L = 2, que é numericamente tratável em uma
estação de trabalho única, mas não está totalmente con-
vergida para o complexo FMO de 7 sítios nas maiores
energias de reorganização testadas (λ = 200 cm−1). Con-
vergência quantitativa em L = 3 exige recursos de cluster
e fica para v6.2 deste artigo. Os expoentes de escalona-
mento na Eq. (6) são robustos ao erro de truncamento,
mas valores individuais de T2 em grande λ podem deslo-
car em 5–10% em L = 3.
B.
Banho Drude–Lorentz
O modelo de banho na Eq. (2) é a forma padrão Drude–
Lorentz, que captura a dinâmica dominante de baixa fre-
quência do ambiente proteico, mas negligencia a estru-
tura vibrônica de alta frequência que foi reportada na es-
pectroscopia eletrônica 2D do complexo FMO [10]. Um
tratamento completo exigiria uma densidade espectral es-
truturada incluindo picos vibrônicos discretos; isto fica
para trabalho futuro. Os expoentes de escalonamento po-
dem deslocar modestamente com a inclusão de estrutura
vibrônica, mas as características qualitativas (aJ posi-
tivo, aλ, aγ, ST negativos) esperam-se robustas.
C.
Banho independente de sítio
A hipótese de banhos independentes para cada sítio
(acoplamento “local”) negligencia correlações cruzadas
entre sítios.
Um tratamento mais completo incluiria
flutuações de banho espacialmente correlacionadas, que
mostraram estender tempos de coerência em alguns
regimes [10].
Os expoentes de escalonamento reporta-
dos aqui são para o caso independente de sítio; o caso de
banho correlacionado é alvo de trabalho futuro.
D.
A conexão com criticalidade é uma hipótese
A conexão entre ST = −0.261 e a camada de criticali-
dade do programa TCR/QDT (Seção VI) é uma hipótese,
não uma derivação. Ainda não fornecemos um cálculo de
primeiros princípios de ST a partir dos expoentes críticos
da ação efetiva ϕ4. Esta é a principal tarefa teórica em
aberto do programa e é foco de trabalho em andamento.
IX.
CONCLUSÃO
Reportamos uma análise de escalonamento abrangente
do tempo de coerência eletrônica T2 no complexo FMO de
7 sítios, produzindo a relação em lei de potência T2 = K ·
J0.831·λ−0.843·γ−0.766·T −0.261 com R2 = 0.988 sobre 375
combinações de parâmetros. O expoente de temperatura
ST = −0.261 generaliza a extrapolação do dímero de
2 sítios de versões anteriores do programa TCR/QDT e
resolve a Inconsistência #3 da auditoria v6.0. O expoente
fracionário é consistente com um regime dinâmico crítico,
embora a derivação formal de ST a partir dos expoentes
críticos permaneça uma tarefa teórica em aberto.
Retraímos formalmente o índice de comensurabilidade
inter-escala η, resolvendo a Inconsistência #5 da audi-
toria v6.0.
A correlação DII r = +0.459 fornece uma
âncora empírica moderada para a componente de sime-
tria S da métrica de coerência relacional.
O próximo passo principal é a validação HEOM em
L = 3, que exigirá recursos de cluster, mas espera-se
que confirme os expoentes de escalonamento dentro das
incertezas declaradas. A tarefa teórica de derivar ST dos
expoentes críticos da ação efetiva ϕ4 é foco de trabalho
em andamento.

```

### Página 5

```text
5
AGRADECIMENTOS
O autor agradece aos desenvolvedores do pacote qutip
pela implementação HEOM e à comunidade OpenScience
pela parametrização FMO. Este trabalho não recebeu
financiamento externo; o autor é pesquisador indepen-
dente.
[1] G. S. Engel et al., Evidence for wavelike energy trans-
fer through quantum coherence in photosynthetic systems,
Nature 446, 782 (2007).
[2] H. Lee et al., Coherence dynamics in photosynthesis:
Protein protection of excitonic coherence, Science 316,
1462 (2007).
[3] E. Collini et al., Coherently wired light-harvesting in pho-
tosynthetic marine algae at ambient temperature, Nature
463, 644 (2010).
[4] T. R. Calhoun et al., Quantum coherence enabled de-
termination of the energy landscape in light-harvesting
complex II, J. Phys. Chem. B 113, 3643 (2009).
[5] M. B. Plenio and S. F. Huelga, Dephasing-assisted trans-
port:
quantum networks and biological systems, New
J. Phys. 10, 113019 (2008).
[6] M. Mohseni et al., Environment-assisted quantum walks
in photosynthetic energy transfer, J. Chem. Phys. 129,
174106 (2008).
[7] E. J. O’Reilly and A. Olaya-Castro, Non-classicality of
the molecular vibrations responsible for electronic coher-
ence in the FMO complex, Nat. Commun. 5, 3012 (2014).
[8] A. W. Chin et al., The role of non-equilibrium vibra-
tional structures in electronic coherence and recoherence
in pigment-protein complexes, Nat. Phys. 9, 113 (2013).
[9] J. Adolphs and F. Müh, Structure and calculations of
the reorganization energy of FMO, J. Chem. Phys. 124,
234711 (2006).
[10] C. Olbrich and U. Klein, Parametrization of FMO vibra-
tional structure, J. Phys. Chem. B 115, 7580 (2011).
[11] Y. Tanimura and R. Kubo, Time evolution of a quan-
tum system in contact with a nearly Gaussian-Markoﬀian
noise bath, J. Phys. Soc. Jpn. 58, 101 (1989).
[12] A. Ishizaki and Y. Tanimura, Quantum dynamics of sys-
tem strongly coupled to low-frequency colored noise bath:
reduced hierarchy equations approach, J. Phys. Soc. Jpn.
74, 3131 (2005).
[13] Y.
Chen
et
al.,
Eﬀicient
HEOM
for
qutip
5.x,
J. Chem. Phys. 157, 064102 (2022).
[14] J. R. Johansson et al., QuTiP 2:
A Python frame-
work for the dynamics of open quantum systems, Com-
put. Phys. Commun. 184, 1234 (2013).
[15] E. C. do Nascimento, Relational Coherence in Biological
Networks: A Quantitative Framework from Connectomes
to EEG, submetido à Phys. Rev. E (2026).
[16] E. C. do Nascimento, The Primordial Consciousness
Field (Level 0): Full Formalization within the TCR/QDT
Program, documento companheiro (2026).

```

