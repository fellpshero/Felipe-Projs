#area do retangulo
print("Área do retângulo")
a = float(input("Insira a altura: "))
l = float(input("Insira a largura: "))
areaRet = a * l
print("A área do retângulo é de: ", areaRet)

#area de um quadrado
print("Área do quadrado")
l = float(input("Insira a valor do lado: "))
areaQuad = l * l
print("A área do quadrado é de: ", areaQuad)

#desconto
print("Cálculo de desconto")
p = float(input("Qual valor do seu produto: "))
d = float(input('Quantos % de desconto será aplicado (sem o %): '))
prodComDsct = (float(p)-(float(p) * float(d)/100))
print("O valor do produto com desconto é de R$", prodComDsct)
