import json
import os
import urllib.request
from datetime import date
from decimal import Decimal, InvalidOperation

ARQUIVO = "gastos.json"
VALOR_MAXIMO = Decimal("126000000000000.00")  # 126 trilhoes, mais que o PIB mundial... eu acho que n precisa que mais kkkk


def carregar_gastos():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r") as f:
        try:
            dados = json.load(f)
        except json.JSONDecodeError:
            print("Aviso: arquivo de gastos corrompido ou vazio. Iniciando com lista vazia.")
            return []

    gastos_validos = []
    ignorados = 0
    for g in dados:
        try:
            valor = Decimal(str(g["valor"]))
            if valor <= 0 or valor > VALOR_MAXIMO:
                raise InvalidOperation
            g["valor"] = str(valor.quantize(Decimal("0.01")))
            gastos_validos.append(g)
        except InvalidOperation:
            ignorados += 1

    if ignorados:
        print(f"Aviso: {ignorados} gasto(s) com valor invalido foram ignorados ao carregar o arquivo.")

    return gastos_validos


def salvar_gastos(gastos):
    with open(ARQUIVO, "w") as f:
        json.dump(gastos, f, indent=2)


def valor_para_decimal(gastos_entry):
    """Retorna o valor de um gasto como Decimal."""
    return Decimal(gastos_entry["valor"])


def validar_valor(valor_str):
    """
    Valida e converte uma string de valor monetário para Decimal.
    Retorna (Decimal, None) em sucesso ou (None, mensagem_de_erro) em falha.
    """
    try:
        valor = Decimal(str(valor_str).replace(",", "."))
    except InvalidOperation:
        return None, "Valor invalido. Digite apenas numeros (ex: 19.90)."

    if valor <= 0:
        return None, "O valor deve ser maior que zero."

    if valor > VALOR_MAXIMO:
        return None, f"Valor muito alto. O limite e R$ {VALOR_MAXIMO:,.2f}."

    return valor.quantize(Decimal("0.01")), None


def adicionar_gasto(gastos, descricao, valor, categoria):
    """
    Adiciona um gasto à lista.
    `valor` pode ser string, int, float ou Decimal, será validado internamente.
    Retorna (True, None) em sucesso ou (False, mensagem) em falha.
    """
    valor_decimal, erro = validar_valor(valor)
    if erro:
        return False, erro

    novo_id = max((g["id"] for g in gastos), default=0) + 1

    novo = {
        "id": novo_id,
        "descricao": descricao,
        "valor": str(valor_decimal),   # salvo como string para preservar precisão
        "categoria": categoria,
        "data": str(date.today()),
    }
    gastos.append(novo)
    salvar_gastos(gastos)
    return True, None


def listar_gastos(gastos):
    if not gastos:
        return
    print(f"\n{'ID':<5} {'Data':<12} {'Categoria':<15} {'Valor':>10}  Descricao")
    print("-" * 60)
    for g in gastos:
        valor = Decimal(g["valor"])
        print(f"{g['id']:<5} {g['data']:<12} {g['categoria']:<15} R${valor:>8.2f}  {g['descricao']}")


def remover_gasto(gastos, id_remover):
    for g in gastos:
        if g["id"] == id_remover:
            gastos.remove(g)
            salvar_gastos(gastos)
            return True
    return False


def ver_resumo(gastos):
    if not gastos:
        print("\nNenhum gasto registrado.")
        return
    total = sum(Decimal(g["valor"]) for g in gastos)
    print(f"\nTotal de gastos: R$ {total:.2f}")
    print(f"Quantidade: {len(gastos)}")


def buscar_cotacao_dolar():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    try:
        with urllib.request.urlopen(url, timeout=5) as resposta:
            dados = json.loads(resposta.read())
            cotacao = Decimal(str(dados["USDBRL"]["bid"]))
            return cotacao
    except Exception:
        return None


def ver_resumo_em_dolar(gastos):
    if not gastos:
        print("\nNenhum gasto registrado.")
        return
    total = sum(Decimal(g["valor"]) for g in gastos)
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
            descricao = input("Descricao: ").strip()
            if not descricao:
                print("Descricao nao pode ser vazia.")
                continue
            valor_str = input("Valor: R$ ").strip()
            categoria = input("Categoria: ").strip()
            if not categoria:
                print("Categoria nao pode ser vazia.")
                continue
            sucesso, erro = adicionar_gasto(gastos, descricao, valor_str, categoria)
            if sucesso:
                print("Gasto adicionado com sucesso!")
            else:
                print(f"Erro: {erro}")
        elif opcao == "2":
            listar_gastos(gastos)
        elif opcao == "3":
            listar_gastos(gastos)
            if not gastos:
                continue
            try:
                id_remover = int(input("ID para remover: "))
            except ValueError:
                print("ID invalido. Digite apenas numeros inteiros.")
                continue
            removido = remover_gasto(gastos, id_remover)
            if removido:
                print("Gasto removido com sucesso!")
            else:
                print(f"Nenhum gasto encontrado com ID {id_remover}.")
        elif opcao == "4":
            ver_resumo(gastos)
        elif opcao == "5":
            ver_resumo_em_dolar(gastos)
        elif opcao == "0":
            break
        else:
            print("Opcao invalida. Escolha um numero do menu.")


if __name__ == "__main__":
    main()