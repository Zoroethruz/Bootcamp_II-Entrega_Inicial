import json
import os
import urllib.request
from datetime import date

ARQUIVO = "gastos.json"


def carregar_gastos():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r") as f:
        return json.load(f)


def salvar_gastos(gastos):
    with open(ARQUIVO, "w") as f:
        json.dump(gastos, f, indent=2)


def adicionar_gasto(gastos, descricao, valor, categoria):
    novo = {
        "id": len(gastos) + 1,
        "descricao": descricao,
        "valor": float(valor),
        "categoria": categoria,
        "data": str(date.today())
    }
    gastos.append(novo)
    salvar_gastos(gastos)


def listar_gastos(gastos):
    if not gastos:
        return
    print(f"\n{'ID':<5} {'Data':<12} {'Categoria':<15} {'Valor':>8}  Descricao")
    print("-" * 55)
    for g in gastos:
        print(f"{g['id']:<5} {g['data']:<12} {g['categoria']:<15} R${g['valor']:>6.2f}  {g['descricao']}")


def remover_gasto(gastos, id_remover):
    for g in gastos:
        if g["id"] == id_remover:
            gastos.remove(g)
            salvar_gastos(gastos)
            return


def ver_resumo(gastos):
    if not gastos:
        print("\nNenhum gasto registrado.")
        return
    total = sum(g["valor"] for g in gastos)
    print(f"\nTotal de gastos: R$ {total:.2f}")
    print(f"Quantidade: {len(gastos)}")


def buscar_cotacao_dolar():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    try:
        with urllib.request.urlopen(url, timeout=5) as resposta:
            dados = json.loads(resposta.read())
            cotacao = float(dados["USDBRL"]["bid"])
            return cotacao
    except Exception:
        return None


def ver_resumo_em_dolar(gastos):
    if not gastos:
        print("\nNenhum gasto registrado.")
        return
    total = sum(g["valor"] for g in gastos)
    print(f"\nTotal de gastos: R$ {total:.2f}")

    print("Buscando cotacao do dolar...")
    cotacao = buscar_cotacao_dolar()
    if cotacao:
        total_usd = total / cotacao
        print(f"Cotacao atual:   US$ 1 = R$ {cotacao:.2f}")
        print(f"Total em dolar:  US$ {total_usd:.2f}")
    else:
        print("Nao foi possivel buscar a cotacao. Verifique sua conexao.")


def main():
    gastos = carregar_gastos()

    while True:
        print("\n Gerenciador de Gastos")
        print("1 - Adicionar gasto")
        print("2 - Listar gastos")
        print("3 - Remover gasto")
        print("4 - Ver total")
        print("5 - Ver total em dolar")
        print("0 - Sair")

        opcao = input("\nEscolha: ")

        if opcao == "1":
            descricao = input("Descricao: ")
            valor = input("Valor: R$ ")
            categoria = input("Categoria: ")
            adicionar_gasto(gastos, descricao, valor, categoria)

        elif opcao == "2":
            listar_gastos(gastos)

        elif opcao == "3":
            listar_gastos(gastos)
            id_remover = int(input("ID para remover: "))
            remover_gasto(gastos, id_remover)

        elif opcao == "4":
            ver_resumo(gastos)

        elif opcao == "5":
            ver_resumo_em_dolar(gastos)

        elif opcao == "0":
            break


if __name__ == "__main__":
    main()
