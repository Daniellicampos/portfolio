
import json
import os
import math

ARQUIVO = "gastos.json"


def carregar_gastos():
    if not os.path.exists(ARQUIVO):
        return []

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if isinstance(dados, list):
            return dados

        print("Aviso: o arquivo não contém uma lista de gastos.")
        return []

    except (json.JSONDecodeError, OSError):
        print("Aviso: não foi possível ler os gastos salvos.")
        return []


def salvar_gastos():
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump(gastos, arquivo, ensure_ascii=False, indent=4)
        return True

    except OSError:
        print("Erro: não foi possível salvar os gastos.")
        return False


def cadastrar_gasto():
    print("\n--- CADASTRAR GASTO ---")

    descricao = input("O que você comprou ou pagou? ").strip()
    if not descricao:
        print("Erro: a descrição não pode ficar vazia!")
        return

    categoria = input("Qual é a categoria? ").strip()
    if not categoria:
        print("Erro: a categoria não pode ficar vazia!")
        return

    try:
        valor = float(input("Qual foi o valor? R$ ").replace(",", "."))
        if not math.isfinite(valor) or valor <= 0:
            print("Erro: digite um valor positivo e válido!")
            return
    except ValueError:
        print("Erro: digite um valor numérico válido!")
        return

    gasto = {
        "descricao": descricao,
        "categoria": categoria,
        "valor": valor
    }

    gastos.append(gasto)

    if salvar_gastos():
        print("Gasto cadastrado e salvo com sucesso!")
    else:
        gastos.pop()


def listar_gastos():
    print("\n--- GASTOS CADASTRADOS ---")

    if not gastos:
        print("Nenhum gasto cadastrado.")
        return

    for indice, gasto in enumerate(gastos, start=1):
        print(f"\nGasto {indice}")
        print("Descrição:", gasto["descricao"])
        print("Categoria:", gasto["categoria"])
        print(f"Valor: R$ {gasto['valor']:.2f}")


def calcular_total():
    print("\n--- TOTAL DE GASTOS ---")
    total = sum(gasto["valor"] for gasto in gastos)
    print(f"Total gasto: R$ {total:.2f}")


def total_por_categoria():
    print("\n--- TOTAL POR CATEGORIA ---")

    if not gastos:
        print("Nenhum gasto cadastrado.")
        return

    totais = {}

    for gasto in gastos:
        categoria = gasto["categoria"].strip().title()
        valor = gasto["valor"]

        if categoria in totais:
            totais[categoria] += valor
        else:
            totais[categoria] = valor

    for categoria, total in sorted(totais.items()):
        print(f"{categoria}: R$ {total:.2f}")


def exibir_menu():
    print("\n================================")
    print("   CONTROLE DE GASTOS PESSOAIS")
    print("================================")
    print("1 - Cadastrar gasto")
    print("2 - Listar gastos")
    print("3 - Calcular total gasto")
    print("4 - Ver total por categoria")
    print("0 - Sair")
    print("================================")


gastos = carregar_gastos()
print(f"{len(gastos)} gasto(s) carregado(s).")

while True:
    exibir_menu()
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        cadastrar_gasto()
    elif opcao == "2":
        listar_gastos()
    elif opcao == "3":
        calcular_total()
    elif opcao == "4":
        total_por_categoria()
    elif opcao == "0":
        print("Obrigado por usar o Controle de Gastos!")
        break
    else:
        print("Opção inválida! Tente novamente.")
