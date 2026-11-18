# CitizenTech — Mobilidade Urbana Inteligente (Modelagem Matemática)

**Global Solution 2026.2 — FIAP**  
Disciplina: Modelagem Matemática e Computacional

## Integrantes da Equipe

* **Enzo Yudi de Oliveira Hino** — RM: 570173
* **Inaldo Pereira Freitas** — RM: 569672
* **Arthur Micarelli** — RM: 571476

> **Documentação Completa:** Para visualizar todas as demonstrações algébricas passo a passo (cálculo do determinante, Teorema de Rouché-Capelli e provas formais com somatórios), acesse o [Relatório Técnico em PDF](./relatorio_modelagem_matematica.pdf).

---

## 1. Contextualização e Objetivo

Após uma falha no sistema de gerenciamento da empresa municipal de transporte público, os registros individuais da frota de ônibus distribuída entre quatro centros operacionais (**Norte**, **Sul**, **Leste** e **Oeste**) ficaram indisponíveis, restando apenas indicadores consolidados e uma pesquisa de demanda no horário de pico.

O objetivo deste projeto é aplicar conceitos de **Sistemas Lineares**, **Matrizes** e **Transformações Lineares** em Python para:

1. Recuperar a distribuição atual dos **72 ônibus** e provar matematicamente a unicidade da solução.
2. Diagnosticar gargalos de superlotação no horário de pico (capacidade de **40 passageiros/ônibus**).
3. Propor e validar uma política de redistribuição da frota sem ampliar o número total de veículos.

---

## 2. Etapa 1: Diagnóstico da Frota Atual

### Variáveis e Sistema Linear

Definindo $N, S, L, O \in \mathbb{Z}_+$ como a quantidade de ônibus nas regiões Norte, Sul, Leste e Oeste, respectivamente:

$$
\begin{cases}
N + S + L + O = 72 \\
N + 2S + O = 76 \\
S + 2L = 52 \\
N + L + 2O = 76
\end{cases}
$$

### Representação Matricial ($A\mathbf{x} = \mathbf{b}$)

$$
\begin{bmatrix}
1 & 1 & 1 & 1 \\
1 & 2 & 0 & 1 \\
0 & 1 & 2 & 0 \\
1 & 0 & 1 & 2
\end{bmatrix}
\begin{bmatrix}
N \\ S \\ L \\ O
\end{bmatrix}
=
\begin{bmatrix}
72 \\ 76 \\ 52 \\ 76
\end{bmatrix}
$$

### Unicidade e Solução Encontrada

* **Determinante:** $\det(A) = 3 \neq 0$, garantindo que $A$ é invertível.
* **Posto:** $\text{posto}(A) = \text{posto}([A \mid \mathbf{b}]) = 4$ (Sistema Possível e Determinado — solução única).
* **Distribuição Atual:**
  * **Norte:** `12` ônibus
  * **Sul:** `20` ônibus
  * **Leste:** `16` ônibus
  * **Oeste:** `24` ônibus

---

## 3. Etapa 2: Política de Redistribuição (Transformação Linear)

### Diagnóstico de Demanda (Horário de Pico — 40 pass./ônibus)

| Região | Passageiros | Frota Necessária | Frota Atual | Saldo | Diagnóstico |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Norte** | 560 | 14 | 12 | **-2** | Déficit (superlotação) |
| **Sul** | 760 | 19 | 20 | **+1** | Superávit (1 ocioso) |
| **Leste** | 720 | 18 | 16 | **-2** | Déficit (superlotação) |
| **Oeste** | 840 | 21 | 24 | **+3** | Superávit (3 ociosos) |
| **Total** | **2.880** | **72** | **72** | **0** | **Equilíbrio viável** |

### Matriz de Transformação Linear ($T(\mathbf{x}) = M\mathbf{x}$)

Para realocar os 4 ônibus excedentes de Sul e Oeste para Norte e Leste, define-se o operador linear $T: \mathbb{R}^4 \to \mathbb{R}^4$ associado à matriz estocástica por colunas $M$:

$$
M = \begin{bmatrix}
1 & 0 & 0 & \frac{1}{12} \\
0 & \frac{19}{20} & 0 & 0 \\
0 & \frac{1}{20} & 1 & \frac{1}{24} \\
0 & 0 & 0 & \frac{7}{8}
\end{bmatrix}
$$

* **Conservação da frota:** A soma de cada coluna de $M$ é igual a $1$, assegurando $\sum_{i=1}^{4} y_i = \sum_{j=1}^{4} x_j = 72$.
* **Não negatividade:** Todos os coeficientes $m_{ij} \ge 0$, garantindo alocações fisicamente válidas.
* **Nova Distribuição ($M \cdot \mathbf{x}_{\text{atual}}$):** Norte = **14**, Sul = **19**, Leste = **18**, Oeste = **21**.

---

## 4. Estrutura do Repositório e Execução

* `main.py`: Script em Python com a resolução matricial e simulação da transformação linear.
* `relatorio_modelagem_matematica.pdf`: Relatório técnico completo com todas as deduções algébricas.
* `README.md`: Documentação geral do projeto.

### Como Executar

1. Instale a biblioteca `numpy`:

   ```bash
   pip install numpy
   ```

2. Execute o script principal:

   ```bash
   python main.py
   ```