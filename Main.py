from datetime import datetime
import json
import os


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

ARQUIVO_PEDIDOS = "pedidos.json"


# ==========================================================
# VALIDAÇÕES
# ==========================================================

def ler_numero_positivo(mensagem, inteiro=False):
    while True:
        try:
            valor = float(input(mensagem))

            if valor <= 0:
                print("Digite um valor maior que zero.")
                continue

            if inteiro:
                if not valor.is_integer():
                    print("Digite um número inteiro.")
                    continue

                return int(valor)

            return valor

        except ValueError:
            print("Digite um valor numérico válido.")


# ==========================================================
# PAGAMENTO
# ==========================================================

def escolher_pagamento(total):
    while True:
        print("\n===================================")
        print("        FORMA DE PAGAMENTO")
        print("===================================")
        print("1 - PIX")
        print("2 - Cartão")
        print("3 - Dinheiro")
        print("===================================")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\nPagamento selecionado: PIX")
            print("Você recebeu mais 5% de desconto no PIX!")

            return "PIX", 0

        elif opcao == "2":
            print("\nDados do cartão:")

            numero_cartao = input("Número do cartão: ")
            validade = input("Data de validade: ")
            cvv = input("CVV: ")

            if not numero_cartao or not validade or not cvv:
                print("Preencha todos os dados do cartão.")
                continue

            print("Pagamento selecionado: Cartão")

            return "Cartão", 0

        elif opcao == "3":
            valor_pago = ler_numero_positivo(
                "Valor recebido: R$ "
            )

            while valor_pago < total:
                print("Valor insuficiente.")

                valor_pago = ler_numero_positivo(
                    "Digite outro valor recebido: R$ "
                )

            return "Dinheiro", valor_pago

        else:
            print("Opção inválida. Escolha 1, 2 ou 3.")


# ==========================================================
# CARDÁPIO
# ==========================================================

PIZZAS = {
    1: {
        "nome": "Pizza Calabresa",
        "preco": 49.90,
        "especificacoes": "Molho, mussarela, calabresa e cebola."
    },
    2: {
        "nome": "Pizza Portuguesa",
        "preco": 54.90,
        "especificacoes": "Molho, mussarela, presunto, ovo, cebola e azeitona."
    },
    3: {
        "nome": "Pizza Quatro Queijos",
        "preco": 59.90,
        "especificacoes": "Mussarela, provolone, parmesão e catupiry."
    },
    4: {
        "nome": "Pizza Frango com Catupiry",
        "preco": 57.90,
        "especificacoes": "Molho, mussarela, frango desfiado e catupiry."
    },
    5: {
        "nome": "Pizza Margherita",
        "preco": 52.90,
        "especificacoes": "Molho, mussarela, tomate e manjericão."
    }
}


HAMBURGUERES = {
    1: {
        "nome": "X-Burger Clássico",
        "preco": 24.90,
        "especificacoes": "Pão, hambúrguer, mussarela e molho da casa."
    },
    2: {
        "nome": "X-Salada Especial",
        "preco": 27.90,
        "especificacoes": "Pão, hambúrguer, queijo, alface, tomate e molho."
    },
    3: {
        "nome": "Bacon Burger",
        "preco": 31.90,
        "especificacoes": "Pão, hambúrguer, bacon crocante, queijo e molho."
    },
    4: {
        "nome": "Cheddar Burger",
        "preco": 29.90,
        "especificacoes": "Pão, hambúrguer, cheddar cremoso e cebola."
    },
    5: {
        "nome": "Duplo Burger",
        "preco": 36.90,
        "especificacoes": "Pão, dois hambúrgueres, queijo e molho da casa."
    }
}


REFRIGERANTES = {
    1: {
        "nome": "Coca-Cola Lata 350ml",
        "preco": 6.00,
        "especificacoes": "Refrigerante em lata de 350 ml."
    },
    2: {
        "nome": "Guaraná Lata 350ml",
        "preco": 6.00,
        "especificacoes": "Refrigerante em lata de 350 ml."
    },
    3: {
        "nome": "Coca-Cola 2L",
        "preco": 12.00,
        "especificacoes": "Garrafa de refrigerante de 2 litros."
    },
    4: {
        "nome": "Guaraná 2L",
        "preco": 11.00,
        "especificacoes": "Garrafa de refrigerante de 2 litros."
    },
    5: {
        "nome": "Água Mineral 500ml",
        "preco": 4.00,
        "especificacoes": "Água mineral sem gás, garrafa de 500 ml."
    }
}


SOBREMESAS = {
    1: {
        "nome": "Pudim de Leite",
        "preco": 9.90,
        "especificacoes": "Pudim de leite condensado com calda de caramelo."
    },
    2: {
        "nome": "Brownie com Chocolate",
        "preco": 12.90,
        "especificacoes": "Brownie de chocolate servido em porção individual."
    },
    3: {
        "nome": "Sorvete de Creme",
        "preco": 8.90,
        "especificacoes": "Duas bolas de sorvete de creme."
    },
    4: {
        "nome": "Mousse de Chocolate",
        "preco": 10.90,
        "especificacoes": "Mousse cremoso de chocolate em porção individual."
    },
    5: {
        "nome": "Cheesecake de Morango",
        "preco": 14.90,
        "especificacoes": "Cheesecake com cobertura de morango."
    }
}


CARDAPIOS = {
    1: ("Pizzas", PIZZAS),
    2: ("Hambúrgueres", HAMBURGUERES),
    3: ("Refrigerantes", REFRIGERANTES),
    4: ("Sobremesas", SOBREMESAS)
}


# ==========================================================
# CLIENTE
# ==========================================================

def calcular_idade(nascimento):
    hoje = datetime.now().date()

    idade = hoje.year - nascimento.year

    if (hoje.month, hoje.day) < (
        nascimento.month,
        nascimento.day
    ):
        idade -= 1

    return idade


def cadastrar_cliente():
    print("\n===================================")
    print("        CADASTRO DO CLIENTE")
    print("===================================")

    while True:
        nome = " ".join(
            input("Nome completo: ").split()
        )

        if len(nome.split()) >= 2:
            break

        print("Digite nome e sobrenome.")

    while True:
        try:
            nascimento = datetime.strptime(
                input(
                    "Data de nascimento (dd/mm/aaaa): "
                ).strip(),
                "%d/%m/%Y"
            ).date()

            if nascimento > datetime.now().date():
                print(
                    "A data de nascimento não pode "
                    "estar no futuro."
                )
                continue

            idade = calcular_idade(nascimento)

            if idade < 18:
                print(
                    "Acesso não permitido: "
                    "é necessário ter 18 anos ou mais."
                )
                return None

            print(
                f"\nCadastro confirmado. "
                f"Idade: {idade} anos."
            )

            return {
                "nome": nome,
                "data_nascimento": (
                    nascimento.strftime("%d/%m/%Y")
                ),
                "idade": idade
            }

        except ValueError:
            print(
                "Digite a data no formato dd/mm/aaaa."
            )


# ==========================================================
# ARQUIVO JSON
# ==========================================================

def carregar_pedidos():
    if not os.path.exists(ARQUIVO_PEDIDOS):
        return []

    try:
        with open(
            ARQUIVO_PEDIDOS,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)

    except (json.JSONDecodeError, OSError):
        print("Não foi possível ler os pedidos.")
        return []


def salvar_pedidos(pedidos):
    with open(
        ARQUIVO_PEDIDOS,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            pedidos,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


# ==========================================================
# EXIBIÇÃO DO CARDÁPIO
# ==========================================================

def mostrar_cardapio_principal():
    print("\n===================================")
    print("          CARDÁPIO PRINCIPAL")
    print("===================================")

    for numero, (nome, _) in CARDAPIOS.items():
        print(f"{numero} - {nome}")

    print("0 - Finalizar escolha")
    print("===================================")


def mostrar_subcardapio(nome, cardapio):
    print("\n===================================")
    print(f"           {nome.upper()}")
    print("===================================")

    for numero, item in cardapio.items():
        print(
            f"{numero} - {item['nome']} "
            f"- R$ {item['preco']:.2f}"
        )

    print("0 - Voltar")
    print("===================================")


# ==========================================================
# ESCOLHER PRODUTOS
# ==========================================================

def escolher_produtos():
    produtos = []

    while True:
        mostrar_cardapio_principal()

        categoria = input(
            "Escolha uma categoria: "
        ).strip()

        if categoria == "0":
            if produtos:
                return produtos

            print("Escolha pelo menos um produto.")
            continue

        try:
            categoria = int(categoria)

        except ValueError:
            print("Digite um número válido.")
            continue

        if categoria not in CARDAPIOS:
            print("Categoria não encontrada.")
            continue

        nome_categoria, cardapio = CARDAPIOS[
            categoria
        ]

        while True:
            mostrar_subcardapio(
                nome_categoria,
                cardapio
            )

            opcao = input(
                "Escolha um produto: "
            ).strip()

            if opcao == "0":
                break

            try:
                opcao = int(opcao)

            except ValueError:
                print("Digite um número válido.")
                continue

            if opcao not in cardapio:
                print("Produto não encontrado.")
                continue

            produto = cardapio[opcao]

            print("\n===================================")
            print("        PRODUTO SELECIONADO")
            print("===================================")

            print(f"Produto: {produto['nome']}")

            print(
                f"Especificações: "
                f"{produto['especificacoes']}"
            )

            print(
                f"Preço unitário: "
                f"R$ {produto['preco']:.2f}"
            )

            quantidade = ler_numero_positivo(
                "Quantidade: ",
                inteiro=True
            )

            subtotal = round(
                produto["preco"] * quantidade,
                2
            )

            produtos.append({
                "categoria": nome_categoria,
                "produto": produto["nome"],
                "especificacoes": (
                    produto["especificacoes"]
                ),
                "preco": produto["preco"],
                "quantidade": quantidade,
                "subtotal": subtotal
            })

            print(
                f"\nAdicionado: "
                f"{quantidade}x {produto['nome']}"
            )

            print(
                f"Subtotal: R$ {subtotal:.2f}"
            )

            continuar = input(
                "\nDeseja adicionar outro produto? (s/n): "
            ).lower().strip()

            if continuar != "s":
                return produtos


# ==========================================================
# REALIZAR PEDIDO
# ==========================================================

def realizar_pedido(pedidos):
    print("\n===================================")
    print("            NOVO PEDIDO")
    print("===================================")

    cliente = cadastrar_cliente()

    if cliente is None:
        print("Pedido cancelado.")
        return

    produtos = escolher_produtos()

    total = round(
        sum(
            item["subtotal"]
            for item in produtos
        ),
        2
    )

    print("\n===================================")
    print("        RESUMO DOS PRODUTOS")
    print("===================================")

    for item in produtos:
        print(
            f"{item['quantidade']}x "
            f"{item['produto']} "
            f"- R$ {item['subtotal']:.2f}"
        )

    print(f"\nTotal: R$ {total:.2f}")

    # ======================================================
    # DESCONTO AUTOMÁTICO DA LOJA
    # ======================================================

    desconto_loja = round(
        total * 0.05,
        2
    )

    total_com_desconto = round(
        total - desconto_loja,
        2
    )

    print("\n===================================")
    print("             DESCONTO")
    print("===================================")
    print("A loja oferece 5% de desconto")
    print("para todos os clientes!")

    print(
        f"Desconto da loja: "
        f"R$ {desconto_loja:.2f}"
    )

    print(
        f"Total com desconto: "
        f"R$ {total_com_desconto:.2f}"
    )

    # ======================================================
    # PAGAMENTO
    # ======================================================

    pagamento, valor_recebido = escolher_pagamento(
        total_com_desconto
    )

    # ======================================================
    # DESCONTO PIX
    # ======================================================

    desconto_pix = 0

    if pagamento == "PIX":
        desconto_pix = round(
            total_com_desconto * 0.05,
            2
        )

        print("\n===================================")
        print("          DESCONTO PIX")
        print("===================================")
        print("Pagamento via PIX garante")
        print("mais 5% de desconto!")

    preco_final = round(
        total_com_desconto - desconto_pix,
        2
    )

    # ======================================================
    # TROCO
    # ======================================================

    troco = 0

    if pagamento == "Dinheiro":
        troco = round(
            valor_recebido - preco_final,
            2
        )

    # ======================================================
    # NÚMERO DO PEDIDO
    # ======================================================

    if not pedidos:
        numero_pedido = 1

    else:
        numero_pedido = max(
            pedido["numero"]
            for pedido in pedidos
        ) + 1

    # ======================================================
    # DATA
    # ======================================================

    data_hora = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    # ======================================================
    # PEDIDO
    # ======================================================

    pedido = {
        "numero": numero_pedido,
        "status": "CONFIRMADO",
        "data": data_hora,
        "cliente": cliente,
        "produtos": produtos,
        "total": total,
        "desconto": desconto_loja,
        "desconto_pix": desconto_pix,
        "preco_final": preco_final,
        "pagamento": pagamento,
        "valor_recebido": round(
            valor_recebido,
            2
        ),
        "troco": troco
    }

    # ======================================================
    # RESUMO FINAL
    # ======================================================

    print("\n===================================")
    print("          RESUMO DO PEDIDO")
    print("===================================")

    print(
        f"Pedido: #{numero_pedido:04d}"
    )

    print(
        f"Cliente: {cliente['nome']}"
    )

    print(
        f"Data de nascimento: "
        f"{cliente['data_nascimento']}"
    )

    print(
        f"Idade: {cliente['idade']} anos"
    )

    print(
        f"Data do pedido: {data_hora}"
    )

    print("\nProdutos:")

    for item in produtos:
        print(
            f"{item['quantidade']}x "
            f"{item['produto']} "
            f"- R$ {item['subtotal']:.2f}"
        )

    print(
        f"\nTotal original: "
        f"R$ {total:.2f}"
    )

    print(
        f"Desconto da loja (5%): "
        f"R$ {desconto_loja:.2f}"
    )

    print(
        f"Desconto PIX (5%): "
        f"R$ {desconto_pix:.2f}"
    )

    print(
        f"Preço final: "
        f"R$ {preco_final:.2f}"
    )

    print(
        f"Pagamento: {pagamento}"
    )

    if pagamento == "Dinheiro":
        print(
            f"Valor recebido: "
            f"R$ {valor_recebido:.2f}"
        )

        print(
            f"Troco: "
            f"R$ {troco:.2f}"
        )

    print("===================================")

    # ======================================================
    # CONFIRMAÇÃO
    # ======================================================

    confirmar = input(
        "\nConfirmar pedido? (s/n): "
    ).lower().strip()

    if confirmar == "s":
        pedidos.append(pedido)

        salvar_pedidos(pedidos)

        print(
            f"\nPedido #{numero_pedido:04d} "
            "salvo com sucesso!"
        )

    else:
        print("\nPedido cancelado.")


# ==========================================================
# LISTAR PEDIDOS
# ==========================================================

def listar_pedidos(pedidos):
    print("\n===================================")
    print("          LISTAR PEDIDOS")
    print("===================================")

    if not pedidos:
        print("Nenhum pedido encontrado.")
        return

    for pedido in pedidos:
        print(
            f"\nPedido #{pedido['numero']:04d}"
        )

        print(
            f"Cliente: "
            f"{pedido['cliente']['nome']}"
        )

        print(
            f"Data: {pedido['data']}"
        )

        print(
            f"Valor: "
            f"R$ {pedido['preco_final']:.2f}"
        )

        print(
            f"Status: "
            f"{pedido['status']}"
        )


# ==========================================================
# BUSCAR PEDIDO
# ==========================================================

def buscar_pedido(pedidos):
    print("\n===================================")
    print("           BUSCAR PEDIDO")
    print("===================================")

    if not pedidos:
        print("Nenhum pedido encontrado.")
        return

    numero = ler_numero_positivo(
        "Digite o número do pedido: ",
        inteiro=True
    )

    for pedido in pedidos:

        if pedido["numero"] == numero:

            print(
                f"\nPedido #{pedido['numero']:04d}"
            )

            print(
                f"Status: {pedido['status']}"
            )

            print(
                f"Cliente: "
                f"{pedido['cliente']['nome']}"
            )

            print(
                f"Data de nascimento: "
                f"{pedido['cliente']['data_nascimento']}"
            )

            print(
                f"Idade: "
                f"{pedido['cliente']['idade']} anos"
            )

            print(
                f"Data: {pedido['data']}"
            )

            print("\nProdutos:")

            for item in pedido["produtos"]:
                print(
                    f"{item['quantidade']}x "
                    f"{item['produto']} "
                    f"- R$ {item['subtotal']:.2f}"
                )

                print(
                    f"   {item['especificacoes']}"
                )

            print(
                f"\nTotal: "
                f"R$ {pedido['total']:.2f}"
            )

            print(
                f"Desconto da loja: "
                f"R$ {pedido['desconto']:.2f}"
            )

            print(
                f"Desconto PIX: "
                f"R$ {pedido['desconto_pix']:.2f}"
            )

            print(
                f"Preço final: "
                f"R$ {pedido['preco_final']:.2f}"
            )

            print(
                f"Pagamento: "
                f"{pedido['pagamento']}"
            )

            if pedido["pagamento"] == "Dinheiro":
                print(
                    f"Valor recebido: "
                    f"R$ {pedido['valor_recebido']:.2f}"
                )

                print(
                    f"Troco: "
                    f"R$ {pedido['troco']:.2f}"
                )

            return

    print("Pedido não encontrado.")


# ==========================================================
# CANCELAR PEDIDO
# ==========================================================

def cancelar_pedido(pedidos):
    print("\n===================================")
    print("          CANCELAR PEDIDO")
    print("===================================")

    if not pedidos:
        print("Nenhum pedido encontrado.")
        return

    numero = ler_numero_positivo(
        "Digite o número do pedido: ",
        inteiro=True
    )

    for pedido in pedidos:

        if pedido["numero"] == numero:

            if pedido["status"] == "CANCELADO":
                print(
                    "Esse pedido já está cancelado."
                )
                return

            print(
                f"\nPedido #{pedido['numero']:04d}"
            )

            print(
                f"Cliente: "
                f"{pedido['cliente']['nome']}"
            )

            print(
                f"Valor: "
                f"R$ {pedido['preco_final']:.2f}"
            )

            print(
                f"Status: {pedido['status']}"
            )

            confirmar = input(
                "\nTem certeza que deseja "
                "cancelar este pedido? (s/n): "
            ).lower().strip()

            if confirmar == "s":

                pedido["status"] = "CANCELADO"

                pedido["data_cancelamento"] = (
                    datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    )
                )

                salvar_pedidos(pedidos)

                print(
                    f"\nPedido #{numero:04d} "
                    "cancelado com sucesso!"
                )

                print(
                    "O pedido permanece no histórico "
                    "com o status CANCELADO."
                )

            else:
                print(
                    "\nCancelamento interrompido."
                )

            return

    print("Pedido não encontrado.")


# ==========================================================
# SISTEMA PRINCIPAL
# ==========================================================

def sistema():
    pedidos = carregar_pedidos()

    while True:

        print("\n===================================")
        print("         SISTEMA DE PEDIDOS")
        print("===================================")
        print("1 - Novo pedido")
        print("2 - Listar pedidos")
        print("3 - Buscar pedido")
        print("4 - Cancelar pedido")
        print("5 - Sair")
        print("===================================")

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":
            realizar_pedido(pedidos)

        elif opcao == "2":
            listar_pedidos(pedidos)

        elif opcao == "3":
            buscar_pedido(pedidos)

        elif opcao == "4":
            cancelar_pedido(pedidos)

        elif opcao == "5":
            print("Programa encerrado.")
            break

        else:
            print("Opção inválida.")


# ==========================================================
# INICIAR PROGRAMA
# ==========================================================

if __name__ == "__main__":
    sistema()
