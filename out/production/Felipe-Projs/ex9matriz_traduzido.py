# Exercício 9 - Matriz de Estoque
# Traduzido de Visualg para Python

# Inicialização das listas
produto = [""] * 6  # vetor de 6 caracteres
estoque = [[0, 0] for _ in range(6)]  # matriz 6x2 de inteiros
status = [""] * 6  # vetor de 6 caracteres
prodalerta = 0
dif = 0

# Leitura dos nomes dos produtos
print("=" * 50)
print("CADASTRO DE PRODUTOS")
print("=" * 50)
for i in range(6):
    produto[i] = input(f"Insira o nome do {i+1}º produto: ")

# Leitura das quantidades atual e mínima
print("\n" + "=" * 50)
print("CADASTRO DE QUANTIDADES")
print("=" * 50)
for i in range(6):
    estoque[i][0] = int(input(f"Insira a quantidade atual de {produto[i]}: "))
    estoque[i][1] = int(input(f"Agora, insira a quantidade mínima requerida no estoque: "))

# Verificação do status de cada produto
print("\n" + "=" * 50)
print("VERIFICANDO STATUS DOS PRODUTOS")
print("=" * 50)
for i in range(6):
    dif = estoque[i][0] - estoque[i][1]
    if dif < 0:
        status[i] = "ALERTA!"
    else:
        status[i] = "Ok!"

# Contagem de produtos em alerta
for i in range(6):
    if status[i] == "ALERTA!":
        prodalerta += 1

# Exibição do relatório
print("\n" + "=" * 50)
print("RELATÓRIO FINAL")
print("=" * 50)
print(f"{prodalerta} produtos estão abaixo do estoque mínimo\n")

for i in range(6):
    print(f"{produto[i]}: - {status[i]}")

print("=" * 50)
