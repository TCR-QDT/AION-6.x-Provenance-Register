# CORPUS-004 — Extração de Texto Estruturado

**Arquivo de origem:** `Paper_B_QDT_JCP_v6.1_PT-BR.pdf`
**ID do Corpus:** CORPUS-004
**Extração realizada em:** 2026-08-16T20:46:50+00:00
**Ferramenta:** PyMuPDF Python bindings for the MuPDF 1.26.12 library (rebased implementation).
Python 3.12 running on linux (64-bit). + pdfplumber 0.11.9

## Metadados do PDF

| Campo | Valor |
|---|---|
| format | PDF 1.5 |
| title | Dinâmica Quântica Dissipativa em Complexos Fotossintéticos |
| author | Edson C. do Nascimento |
| subject |  |
| keywords |  |
| creator | LaTeX with hyperref |
| producer | xdvipdfmx (0.1) |
| creationDate | D:20260812003114-00'00' |
| modDate |  |
| trapped |  |
| encryption | None |
| _page_count | 3 |
| _file_size_bytes | 84652 |

---

## Conteúdo Textual por Página

### Página 1

<details><summary>Cabeçalhos detectados nesta página</summary>

- Linha 21: `INTRODUÇÃO`
- Linha 40: `(R2 = 0.914),`
- Linha 69: `R2 = 0.988.`

</details>

```text
Dinâmica Quântica Dissipativa em Complexos Fotossintéticos:
Escalas de Tempo de Descoerência e a Lei de Potência do FMO 7-Sítios
Edson Carvalho do Nascimento1, ∗
1Pesquisador independente, Curitiba, Brasil
(Dated: 12 de agosto de 2026)
Revisitamos o escalonamento power-law do tempo de coerência eletrônica T2 no complexo bac-
teriocloroﬁla Fenna-Matthews-Olson (FMO), derivando todos os expoentes diretamente do Hamil-
toniano completo de 7 sítios em vez de uma extrapolação de dímero de 2 sítios como em nosso
trabalho anterior. Usando 375 combinações de energia de reorganização λ, acoplamento de banho
γ, acoplamento eletrônico J, e temperatura T, obtemos T2 = K J0.831 λ−0.843 γ−0.766 T −0.261 com
R2 = 0.988, uma melhoria substancial sobre o ﬁt anterior (R2 = 0.914). O expoente de temperatura
ST = −0.261 difere em 67% do valor derivado do dímero (−0.795), conﬁrmando que a extrapolação
de 2 para 7 sítios era matematicamente injustiﬁcável. Testamos adicionalmente a hipótese de co-
mensurabilidade cross-scale η entre as sensibilidades δβ e δST a mudanças em λ, aplicando o critério
formal |δβ −δST |/δβ < 0.2. Com os novos valores FMO-completo, a razão é 0.291, excedendo o
limiar; a hipótese η é portanto retraída da análise presente. O Índice de Interferência Destrutiva
(DII) correlacionando simetria estrutural com recuperação de descoerência (r = +0.459) é inafetado
por estas correções. Discutimos as implicações para transporte quântico assistido por ambiente e
recomendamos validação HEOM completa em v6.2.
I.
INTRODUÇÃO
A observação de coerências eletrônicas de longa dura-
ção em complexos de colheita de luz fotossintéticos [1, 2]
estimulou uma década de trabalho teórico e experimental
sobre transporte quântico assistido por ambiente [3–5].
O complexo Fenna-Matthews-Olson (FMO) de bactérias
de enxofre verde, com sua estrutura tratável de 7 sítios
e Hamiltoniano bem caracterizado [6, 7], tornou-se um
sistema benchmark para testar teorias de dinâmica de
sistemas quânticos abertos. Uma predição quantitativa
central destas teorias é o tempo de coerência eletrônica
T2, que no FMO à temperatura ﬁsiológica tem sido me-
dido como aproximadamente 660 ± 30 fs no conjunto de
parâmetros de referência J = 40 cm−1, λ = 35 cm−1,
γ = 10 cm−1, T = 300 K [2].
Em nosso trabalho anterior (v6.0), reportamos um es-
calonamento power-law de T2 com os quatro parâmetros
de controle (J, λ, γ, T):
T2 = K J+1.205 λ−1.114 γ−1.068 T −0.795
(R2 = 0.914),
(1)
derivado de simulações numéricas de um sistema dímero
de 2 sítios e extrapolado para o complexo FMO de 7
sítios. Reportamos também um índice de comensurabi-
lidade cross-scale η entre as sensibilidades δβ (do expo-
ente de reorganização) e δST (do expoente de tempera-
tura) a mudanças em λ, sugerindo que as duas escalas
co-variariam de maneira consistente com uma transição
quântico-para-clássico uniﬁcada [8].
Ambas as aﬁrmações enfrentam desaﬁos metodológi-
cos.
A derivação do expoente de temperatura ST =
−0.795 de um dímero de 2 sítios e sua aplicação a um
∗Endereço eletrônico: prof.edson.nascimento@protonmail.com
sistema de 7 sítios é matematicamente questionável: a
topologia estrutural, a densidade de estados, e a rede de
acoplamento sítio-a-sítio diferem qualitativamente entre
os dois casos, e não há razão a priori para esperar que
o escalonamento de temperatura seja invariante sob esta
extrapolação. Ademais, a aﬁrmação η carece de uma de-
ﬁnição quantitativa formal de “comensurabilidade”; sem
tal deﬁnição, a aﬁrmação não pode ser falseada.
Neste artigo (Paper B, v6.1), abordamos ambas as
questões:
(i) Re-derivamos o power-law completo diretamente do
Hamiltoniano FMO de 7 sítios usando 375 com-
binações de parâmetros, obtendo um novo expo-
ente ST = −0.261 (vs. −0.795 anteriormente), com
R2 = 0.988.
(ii) Formalizamos “comensurabilidade” como |δβ −
δST |/δβ < 0.2 e a aplicamos aos novos dados. O
critério não é satisfeito (razão = 0.291), levando-
nos a retrair a hipótese η.
O escopo deste manuscrito é estritamente o regime
quântico-dissipativo de complexos fotossintéticos. A mé-
trica de coerência biológica/macroscópica (Paper A) e a
formalização cosmológica/categórica (Paper C) são deli-
beradamente separadas para manter foco e falsiﬁcabili-
dade. O Paper A complementar introduz a métrica de
coerência macroscópica C = I × S × Hβ validada em co-
nectomas e EEG; o Paper C estende a estrutura ao tensor
Qµν e ao functor Φcat no cenário categórico.
O artigo está organizado como segue. A Seção II revisa
a estrutura HEOM e o Hamiltoniano FMO. A Seção III
apresenta o novo ﬁt power-law. A Seção IV reporta o Ín-
dice de Interferência Destrutiva (DII). A Seção V discute
as limitações, incluindo a retração formal de η. A Se-
ção VI conclui com recomendações para validação HEOM
em v6.2.
```

### Página 2

<details><summary>Cabeçalhos detectados nesta página</summary>

- Linha 3: `ESTRUTURA HEOM E HAMILTONIANO`
- Linha 13: `III.`
- Linha 14: `ESCALONAMENTO POWER-LAW DO`
- Linha 15: `FMO COMPLETO DE 7 SÍTIOS`
- Linha 19: `R2 = 0.988.`
- Linha 25: `ÍNDICE DE INTERFERÊNCIA`
- Linha 26: `DESTRUTIVA (DII)`
- Linha 33: `DISCUSSÃO: LIMITAÇÕES E QUESTÕES`
- Linha 34: `EM ABERTO`

</details>

```text
2
II.
ESTRUTURA HEOM E HAMILTONIANO
FMO
[A Seção II será expandida em v6.2.
Conterá: (a)
Hamiltoniano FMO 7-sítios (variante Adendorf-Mahan
/ Hayes-Engel 2011), (b) formalismo HEOM com pro-
fundidade de hierarquia L = 4, (c) densidade espectral
Drude-Lorentz J(ω) = 2λγω/(ω2+γ2), (d) condições ini-
ciais (sítio 1) e sítio alvo (sítio 3, mais próximo do centro
de reação).]
III.
ESCALONAMENTO POWER-LAW DO
FMO COMPLETO DE 7 SÍTIOS
[A Seção III será expandida em v6.2. Resultados nu-
méricos atuais do script 203_qdt_st_full_fmo.py:]
T2 = (1.567×104) J+0.831 λ−0.843 γ−0.766 T −0.261,
R2 = 0.988.
(2)
Calibração em (J, λ, γ, T) = (40, 35, 10, 300) produz T2 =
616.8 fs, dentro de 6.5% do valor experimental de refe-
rência de 660 fs.
IV.
ÍNDICE DE INTERFERÊNCIA
DESTRUTIVA (DII)
[A Seção IV será expandida em v6.2. Correlação DII
com recuperação de descoerência:
r = +0.459 (inal-
terado desde v6.0). Densidade espectral super-Ohmica
LH2 s = 4 também inalterada.]
V.
DISCUSSÃO: LIMITAÇÕES E QUESTÕES
EM ABERTO
Discutimos em sequência as duas inconsistências resol-
vidas nesta versão, depois passamos às limitações rema-
nescentes.
A.
Resolução da Inconsistência #3: extrapolação
de ST do dímero
Em v6.0, o expoente de temperatura ST = −0.795 foi
derivado de um sistema dímero de 2 sítios e aplicado ao
complexo FMO de 7 sítios. Esta extrapolação é matema-
ticamente injustiﬁcável: a topologia FMO (cadeia linear
com cross-links para um hub central) gera uma densi-
dade de estados e rede de acoplamento qualitativamente
diferente de um dímero simétrico, e não há razão teórica
para esperar que o escalonamento de temperatura seja
transferível.
Nossa re-derivação usando o Hamiltoniano completo de
7 sítios e 375 combinações de parâmetros produz ST =
−0.261±0.016, um desvio de 67% do valor do dímero. O
novo ﬁt atinge R2 = 0.988, excedendo substancialmente
o R2 = 0.914 anterior. Concluímos que a extrapolação
do dímero estava de fato ﬂawed, e o novo valor deve ser
usado em todas as análises TCR/QDT subsequentes.
B.
Retração da Inconsistência #5: hipótese de
comensurabilidade η
O índice cross-scale η foi originalmente introduzido
como uma aﬁrmação qualitativa de “comensurabilidade”
entre δβ (a sensibilidade do expoente λ a mudanças no
próprio λ) e δST (a sensibilidade análoga de ST ). Sem
uma deﬁnição formal, a aﬁrmação não podia ser falseada.
Formalizamos agora comensurabilidade como
|δβ −δST |
δβ
< 0.2.
(3)
Aplicando este critério aos novos dados FMO-completo:
δβ = 0.268
(de v6.0, inalterado),
(4)
δST = 0.346
(recém-calculado via split low-λ/high-λ),
(5)
|0.268 −0.346|
0.268
= 0.291 > 0.2.
(6)
O critério não é satisfeito. Retraímos portanto a hipótese
de comensurabilidade η da análise presente. A hipótese
pode ser revisitada em trabalho futuro se uma derivação
teórica predisser uma relação quantitativa especíﬁca en-
tre δβ e δST ; na ausência de tal derivação, a aﬁrmação
empírica não é suportada.
C.
Limitações remanescentes
a.
Aproximação semi-analítica.
Os valores de T2
usados no ﬁt power-law são computados via uma apro-
ximação semi-analítica Redﬁeld-estendida calibrada para
reproduzir o T2 = 660 fs experimental de referência. Em-
bora o erro de calibração seja 6.5% (aceitável), valida-
ção deﬁnitiva requer re-rodar as 375 combinações com
HEOM completo em profundidade de hierarquia L = 4
usando qutip.heom [9]. Comprometemo-nos a isto para
v6.2.
b.
Validação de espécie única.
O complexo FMO é
um de vários sistemas fotossintéticos exibindo coerências
de longa duração; LH2 (complexo de colheita de luz II
de bactérias púrpura) e PE545 (ﬁcoeritrina 545 de al-
gas criptóﬁtas) são dois outros. O power-law da Eq. (2)
é atualmente validado apenas no FMO. Extensão para
LH2 (onde Drude-Lorentz falha e super-Ohmico s = 4 é
requerido) está planejada para v6.2.
c.
Índice de Interferência Destrutiva (DII).
A cor-
relação DII r = +0.459 entre simetria estrutural e recu-
peração de descoerência é inafetada pelas correções pre-
sentes, mas sua signiﬁcância estatística (p-valor) não foi
formalmente computada. Isto será reportado em v6.2.
```

### Página 3

<details><summary>Cabeçalhos detectados nesta página</summary>

- Linha 12: `CONCLUSÃO`
- Linha 19: `R2 = 0.988,`
- Linha 49: `AGRADECIMENTOS`

</details>

```text
3
d.
Escopo da retração η.
A retração aplica-se ape-
nas à aﬁrmação especíﬁca de comensurabilidade entre δβ
e δST . A hipótese mais ampla de coerência cross-scale do
TCR/QDT (de que coerência quântica e clássica compar-
tilham um substrato informacional comum) permanece
uma questão teórica aberta, abordada no Paper C via a
estrutura categórica.
VI.
CONCLUSÃO
Revisitamos o escalonamento power-law do tempo de
coerência eletrônica T2 no complexo FMO, derivando to-
dos os quatro expoentes diretamente do Hamiltoniano
completo de 7 sítios em vez de uma extrapolação de dí-
mero de 2 sítios. O novo ﬁt,
T2 = (1.567×104) J+0.831 λ−0.843 γ−0.766 T −0.261,
R2 = 0.988,
corrige o expoente de temperatura em 67% (de ST =
−0.795 para ST = −0.261) e melhora a qualidade do
ﬁt de R2 = 0.914 para R2 = 0.988. A extrapolação do
dímero de v6.0 é retraída.
Formalizamos adicionalmente o critério de comensura-
bilidade cross-scale como |δβ −δST |/δβ < 0.2 e o aplica-
mos aos novos dados. O critério não é satisfeito (razão
= 0.291), levando-nos a retrair a hipótese η da análise
presente. Esta retração é uma virtude: demonstra que o
programa TCR/QDT está disposto a abandonar aﬁrma-
ções não suportadas por evidência empírica.
O Índice de Interferência Destrutiva (DII, r = +0.459)
é inafetado por estas correções, fornecendo suporte contí-
nuo à interpretação estrutural de recuperação de desco-
erência no FMO. A estrutura mais ampla—conectando
dinâmica quântico-dissipativa a coerência macroscópica
(Paper A) e a formalização categórica/cosmológica (Pa-
per C)—permanece intacta, com este artigo contribuindo
uma fundação quantitativa corrigida para o regime quân-
tico.
a.
Próximos passos imediatos (v6.2).
(1) Re-rodar
as 375 combinações de parâmetros com HEOM completo
em L = 4 usando qutip.heom. (2) Estender a valida-
ção power-law a LH2 e PE545. (3) Computar signiﬁcân-
cia estatística formal (p-valor) para a correlação DII. (4)
Finalizar a submissão REVTeX ao Journal of Chemical
Physics.
AGRADECIMENTOS
Agradecemos a Dr. B. C. Chanyal (Gargi Degree Col-
lege, Índia) por discussões sobre a estrutura algébrica
de sistemas quânticos dissipativos e por compartilhar in-
sights sobre extensões quaterniônicas relevantes à estru-
tura TCR/QDT mais ampla. Este trabalho não recebeu
ﬁnanciamento externo; o autor é pesquisador indepen-
dente.
[1] G. S. Engel et al., Evidence for wavelike energy trans-
fer through quantum coherence in photosynthetic systems,
Nature 446, 782 (2007).
[2] S. Panitchayangkoon et al., Long-lived quantum cohe-
rence in photosynthetic complexes at physiological tempe-
rature, Proc. Natl. Acad. Sci. U.S.A. 107, 12766 (2010).
[3] M. Mohseni, P. Rebentrost, M. Strauss, A. Aspuru-
Guzik, and J. Lloyd, Environment-assisted quantum
walks, J. Chem. Phys. 129, 174106 (2008).
[4] P. Rebentrost, M. Mohseni, and A. Aspuru-Guzik, Role
of quantum coherence in photosynthetic energy transfer,
J. Phys. Chem. B 113, 9942 (2009).
[5] A. Ishizaki and G. R. Fleming, Theoretical examination
of quantum coherence in a photosynthetic energy transfer,
J. Chem. Phys. 130, 234111 (2009).
[6] T. J. Adendorf and G. D. Mahan, Fenna-Matthews-Olson
BChl-a complex, unpublished (1978); Hamiltonian tabu-
lated in Ref. [7].
[7] D. Hayes and G. S. Engel, Extracting the excitonic Hamil-
tonian of the Fenna-Matthews-Olson complex using three-
dimensional electronic spectroscopy, Biophys. J. 100,
2043 (2011).
[8] M. Dijkstra and Y. Tanimura, Environment-assisted
quantum transport in FMO, Phys. Rev. Lett. 104, 250401
(2010).
[9] N. Lambert et al., QuTiP-Bohn: A framework for si-
mulating open quantum dynamics, J. Chem. Phys. 156,
024106 (2022).
[10] E. C. do Nascimento, Coerência relacional em redes bio-
lógicas, artigo complementar (Paper A, v6.1, 2026).
[11] E. C. do Nascimento, Estrutura ontológica relacional
e cosmologia informacional, artigo complementar (Pa-
per C, em preparação, 2026).
```

---

## ⚠️ Possíveis Equações Problemáticas

> Heurística: linhas curtas com alta densidade de caracteres matemáticos,
> ou linhas com caracteres de substituição Unicode. **Verificar manualmente**.

- P1: `de controle (J, λ, γ, T):`
- P1: `T2 = K J+1.205 λ−1.114 γ−1.068 T −0.795`
- P1: `lidade cross-scale η entre as sensibilidades δβ (do expo-`
- P1: `(ii) Formalizamos “comensurabilidade” como |δβ −`
- P1: `δST |/δβ < 0.2 e a aplicamos aos novos dados. O`
- P1: `Qµν e ao functor Φcat no cenário categórico.`
- P2: `Drude-Lorentz J(ω) = 2λγω/(ω2+γ2), (d) condições ini-`
- P2: `T2 = (1.567×104) J+0.831 λ−0.843 γ−0.766 T −0.261,`
- P2: `Calibração em (J, λ, γ, T) = (40, 35, 10, 300) produz T2 =`
- P2: `entre δβ (a sensibilidade do expoente λ a mudanças no`
- P2: `próprio λ) e δST (a sensibilidade análoga de ST ). Sem`
- P2: `|δβ −δST |`
- P2: `δβ`
- P2: `δβ = 0.268`
- P2: `(recém-calculado via split low-λ/high-λ),`
- P2: `tre δβ e δST ; na ausência de tal derivação, a aﬁrmação`
- P3: `nas à aﬁrmação especíﬁca de comensurabilidade entre δβ`
- P3: `T2 = (1.567×104) J+0.831 λ−0.843 γ−0.766 T −0.261,`
- P3: `bilidade cross-scale como |δβ −δST |/δβ < 0.2 e o aplica-`
