import numpy as np

# ==============================================================================
# ETAPA 1: DIAGNÓSTICO E MODELAGEM DA SITUAÇÃO ATUAL
# ==============================================================================

regioes = ["Norte", "Sul", "Leste", "Oeste"]

# Matriz dos coeficientes (A) baseada no Relatório I
A = np.array([
    [1, 1, 1, 1],  # N + S + L + O = 72 (Frota total)
    [1, 2, 0, 1],  # N + 2S + O = 76
    [0, 1, 2, 0],  # S + 2L = 52
    [1, 0, 1, 2]   # N + L + 2O = 76
], dtype=float)

# Vetor dos termos independentes (b)
b = np.array([72, 76, 52, 76], dtype=float)

# Análise de Álgebra Linear (Unicidade da solução)
det_A = np.linalg.det(A)
posto_A = np.linalg.matrix_rank(A)
posto_Ab = np.linalg.matrix_rank(np.column_stack((A, b)))

print("=" * 65)
print("ETAPA 1: DIAGNÓSTICO DA FROTA ATUAL")
print("=" * 65)
print(f"Determinante de A: {det_A:.2f}")
print(f"Posto(A) = {posto_A} | Posto([A|b]) = {posto_Ab}")

if not np.isclose(det_A, 0) and posto_A == posto_Ab == 4:
    print("Classificação: Sistema Possível e Determinado (SPD) -> Solução Única.\n")
    x_atual = np.linalg.solve(A, b)
    for reg, qtd in zip(regioes, x_atual):
        print(f"  - Região {reg:<6}: {int(round(qtd))} ônibus")
else:
    raise ValueError("O sistema não possui solução única.")

# Verificação dos registros operacionais (A * x_atual == b)
verificacao = A @ x_atual
print("\nVerificação dos registros operacionais (A * x_atual == b):", np.allclose(verificacao, b))
print(f"Valores calculados: {verificacao.astype(int)} | Esperados: {b.astype(int)}")

# ==============================================================================
# ETAPA 2: POLÍTICA DE REDISTRIBUIÇÃO VIA TRANSFORMAÇÃO LINEAR
# ==============================================================================

print("\n" + "=" * 65)
print("ETAPA 2: ANÁLISE DE DEMANDA E REDISTRIBUIÇÃO (TRANSFORMAÇÃO LINEAR)")
print("=" * 65)

# Dados do Relatório II
passageiros_pico = np.array([560, 760, 720, 840], dtype=float)
capacidade_onibus = 40.0

# Estimativa da frota necessária por região
x_necessario = np.ceil(passageiros_pico / capacidade_onibus)
desequilibrio = x_atual - x_necessario

print("\nDiagnóstico de Desequilíbrios (Atual vs. Necessário):")
for i, reg in enumerate(regioes):
    status = "Déficit" if desequilibrio[i] < 0 else ("Superávit" if desequilibrio[i] > 0 else "Equilibrado")
    print(f"  - {reg:<6}: Atual = {int(x_atual[i]):2d} | Necessário = {int(x_necessario[i]):2d} | Saldo = {int(desequilibrio[i]):+d} ({status})")

# Matriz de Transformação Linear M (4x4)
# Coluna j = origem | Linha i = destino | Soma de cada coluna = 1
M = np.array([
    [1.0,  0.00, 0.0, 2/24],   # Norte: retém 100% de N + recebe 2/24 de O
    [0.0,  0.95, 0.0, 0.00],   # Sul  : retém 95% de S (19 ônibus)
    [0.0,  0.05, 1.0, 1/24],   # Leste: recebe 5% de S + retém 100% de L + recebe 1/24 de O
    [0.0,  0.00, 0.0, 21/24]   # Oeste: retém 21/24 de O (21 ônibus)
], dtype=float)

# Aplicação do operador linear T(x) = M * x_atual
x_redistribuido = M @ x_atual

print("\nNova Distribuição Após Transformação Linear T(x) = M * x:")
for reg, qtd in zip(regioes, x_redistribuido):
    print(f"  - Região {reg:<6}: {int(round(qtd))} ônibus")

# Demonstração computacional das propriedades
soma_colunas = np.sum(M, axis=0)
preserva_total = np.isclose(np.sum(x_redistribuido), np.sum(x_atual))
nao_negativo = np.all(M >= 0) and np.all(x_redistribuido >= 0)

print("\nValidação das Propriedades da Transformação:")
print(f"  - Soma das colunas de M: {soma_colunas}")
print(f"  - Preserva frota total ({int(np.sum(x_atual))} -> {int(np.sum(x_redistribuido))}): {preserva_total}")
print(f"  - Alocações não-negativas: {nao_negativo}")