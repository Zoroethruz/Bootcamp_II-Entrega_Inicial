import json
import os
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
        print("Nenhum gasto")
        return
    
    total = sum(gasto["valor"] for gasto in gastos)
    print(f"Total de gastos: {total:.2f}")
    print(f"Quantidade: {len(gastos)}")

def main():
    gastos = carregar_gastos()

    while True:
        print("\n Gerenciador de Gastos")
        print("1 - Adicionar gasto")
        print("2 - Listar gastos")
        print("3 - Remover gasto")
        print("4 - Ver total")
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

        elif opcao == "0":
            break

if __name__ == "__main__":
    main()
