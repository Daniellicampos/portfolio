import json
from pathlib import Path

ARQUIVO_DADOS = Path("estoque.json")


def carregar_estoque():
    """Carrega os produtos salvos. Se o arquivo não existir, começa vazio."""
    if not ARQUIVO_DADOS.exists():
        return []

    try:
        with ARQUIVO_DADOS.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados if isinstance(dados, list) else []
    except (json.JSONDecodeError, OSError):
        print("Aviso: não foi possível ler estoque.json. Um estoque vazio será iniciado.")
        return []


def salvar_estoque(produtos):
    """Salva a lista de produtos em um arquivo JSON."""
    with ARQUIVO_DADOS.open("w", encoding="utf-8") as arquivo:
        json.dump(produtos, arquivo, ensure_ascii=False, indent=4)


def localizar_produto(produtos, codigo):
    for produto in produtos:
        if produto["codigo"].lower() == codigo.lower():
            return produto
    return None


def ler_inteiro(mensagem, minimo=0):
    while True:
        try:
            valor = int(input(mensagem))
            if valor < minimo:
                print(f"Digite um número igual ou maior que {minimo}.")
                continue
            return valor
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_preco(mensagem):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor < 0:
                print("O preço não pode ser negativo.")
                continue
            return valor
        except ValueError:
            print("Digite um preço válido. Exemplo: 19.90")


def cadastrar_produto(produtos):
    print("\n--- CADASTRAR PRODUTO ---")
    codigo = input("Código do produto: ").strip()
    if not codigo:
        print("O código não pode ficar vazio.")
        return
    if localizar_produto(produtos, codigo):
        print("Já existe um produto com esse código.")
        return

    nome = input("Nome do produto: ").strip()
    if not nome:
        print("O nome não pode ficar vazio.")
        return

    quantidade = ler_inteiro("Quantidade inicial: ")
    preco = ler_preco("Preço unitário (R$): ")

    produtos.append({
        "codigo": codigo,
        "nome": nome,
        "quantidade": quantidade,
        "preco": preco
    })
    salvar_estoque(produtos)
    print(f"Produto '{nome}' cadastrado com sucesso!")


def listar_produtos(produtos):
    print("\n--- ESTOQUE ATUAL ---")
    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    print(f"{'CÓDIGO':<12} {'PRODUTO':<25} {'QTD.':>8} {'PREÇO':>12} {'TOTAL':>12}")
    print("-" * 73)
    for produto in produtos:
        total = produto["quantidade"] * produto["preco"]
        print(
            f"{produto['codigo']:<12} "
            f"{produto['nome'][:24]:<25} "
            f"{produto['quantidade']:>8} "
            f"R$ {produto['preco']:>8.2f} "
            f"R$ {total:>8.2f}"
        )
    valor_total = sum(p["quantidade"] * p["preco"] for p in produtos)
    print("-" * 73)
    print(f"Valor total estimado do estoque: R$ {valor_total:.2f}")


def consultar_produto(produtos):
    print("\n--- CONSULTAR PRODUTO ---")
    termo = input("Digite o código ou parte do nome: ").strip().lower()
    encontrados = [
        p for p in produtos
        if termo in p["codigo"].lower() or termo in p["nome"].lower()
    ]
    if not encontrados:
        print("Nenhum produto encontrado.")
        return

    for p in encontrados:
        print(
            f"Código: {p['codigo']} | Nome: {p['nome']} | "
            f"Quantidade: {p['quantidade']} | Preço: R$ {p['preco']:.2f}"
        )


def adicionar_estoque(produtos):
    print("\n--- ENTRADA DE ESTOQUE ---")
    codigo = input("Código do produto: ").strip()
    produto = localizar_produto(produtos, codigo)
    if not produto:
        print("Produto não encontrado.")
        return

    quantidade = ler_inteiro("Quantidade a adicionar: ", minimo=1)
    produto["quantidade"] += quantidade
    salvar_estoque(produtos)
    print(f"Entrada registrada! Novo saldo: {produto['quantidade']} unidades.")


def retirar_estoque(produtos):
    print("\n--- SAÍDA DE ESTOQUE ---")
    codigo = input("Código do produto: ").strip()
    produto = localizar_produto(produtos, codigo)
    if not produto:
        print("Produto não encontrado.")
        return

    quantidade = ler_inteiro("Quantidade a retirar: ", minimo=1)
    if quantidade > produto["quantidade"]:
        print(f"Estoque insuficiente. Disponível: {produto['quantidade']}.")
        return

    produto["quantidade"] -= quantidade
    salvar_estoque(produtos)
    print(f"Saída registrada! Novo saldo: {produto['quantidade']} unidades.")


def excluir_produto(produtos):
    print("\n--- EXCLUIR PRODUTO ---")
    codigo = input("Código do produto: ").strip()
    produto = localizar_produto(produtos, codigo)
    if not produto:
        print("Produto não encontrado.")
        return

    confirmacao = input(f"Confirma excluir '{produto['nome']}'? (s/n): ").strip().lower()
    if confirmacao == "s":
        produtos.remove(produto)
        salvar_estoque(produtos)
        print("Produto excluído com sucesso.")
    else:
        print("Exclusão cancelada.")


def exibir_menu():
    print("\n" + "=" * 42)
    print("       SISTEMA DE CONTROLE DE ESTOQUE")
    print("=" * 42)
    print("1 - Cadastrar produto")
    print("2 - Listar produtos")
    print("3 - Consultar produto")
    print("4 - Adicionar estoque")
    print("5 - Retirar estoque")
    print("6 - Excluir produto")
    print("0 - Sair")
    print("=" * 42)


def main():
    produtos = carregar_estoque()
    print("Bem-vindo(a) ao Sistema de Controle de Estoque!")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_produto(produtos)
        elif opcao == "2":
            listar_produtos(produtos)
        elif opcao == "3":
            consultar_produto(produtos)
        elif opcao == "4":
            adicionar_estoque(produtos)
        elif opcao == "5":
            retirar_estoque(produtos)
        elif opcao == "6":
            excluir_produto(produtos)
        elif opcao == "0":
            salvar_estoque(produtos)
            print("Dados salvos. Obrigado por utilizar o sistema!")
            break
        else:
            print("Opção inválida. Escolha uma opção do menu.")


if __name__ == "__main__":
    main()
