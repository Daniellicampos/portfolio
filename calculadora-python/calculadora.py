
while True:
    print("\n============================")
    print("    CALCULADORA EM PYTHON")
    print("============================")
    print("1 - Somar")
    print("2 - Subtrair")
    print("3 - Multiplicar")
    print("4 - Dividir")
    print("0 - Sair")
    print("============================")

    opcao = input("Escolha uma operação: ")

    if opcao == "0":
        print("Obrigado por usar a calculadora!")
        break

    elif opcao in ("1", "2", "3", "4"):
        numero1 = float(input("Digite o primeiro número: "))
        numero2 = float(input("Digite o segundo número: "))

        if opcao == "1":
            resultado = numero1 + numero2
            print("Resultado da soma:", resultado)

        elif opcao == "2":
            resultado = numero1 - numero2
            print("Resultado da subtração:", resultado)

        elif opcao == "3":
            resultado = numero1 * numero2
            print("Resultado da multiplicação:", resultado)

        elif opcao == "4":
            if numero2 == 0:
                print("Erro: não é possível dividir por zero!")
            else:
                resultado = numero1 / numero2
                print("Resultado da divisão:", resultado)

    else:
        print("Opção inválida! Tente novamente.")
