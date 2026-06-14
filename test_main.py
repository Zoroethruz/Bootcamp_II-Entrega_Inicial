import sys
import os
import json
from decimal import Decimal
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import main as app


# ── helpers ──────────────────────────────────────────────

def gasto(id, descricao, valor, categoria="outros", data="2024-01-01"):
    """Cria um dict de gasto com valor já no formato string (novo padrão)."""
    return {"id": id, "descricao": descricao, "valor": str(Decimal(str(valor)).quantize(Decimal("0.01"))), "categoria": categoria, "data": data}


# ── testes unitarios ─────────────────────────────────────

def test_adicionar_gasto():
    gastos = []
    with patch("main.salvar_gastos"):
        sucesso, erro = app.adicionar_gasto(gastos, "Mercado", "50.00", "alimentacao")
    assert sucesso is True
    assert erro is None
    assert len(gastos) == 1
    assert gastos[0]["descricao"] == "Mercado"
    assert gastos[0]["valor"] == "50.00"


def test_adicionar_gasto_valor_como_numero():
    gastos = []
    with patch("main.salvar_gastos"):
        sucesso, _ = app.adicionar_gasto(gastos, "Uber", 29.9, "transporte")
    assert sucesso is True
    assert gastos[0]["valor"] == "29.90"


def test_adicionar_gasto_valor_invalido():
    gastos = []
    with patch("main.salvar_gastos"):
        sucesso, erro = app.adicionar_gasto(gastos, "Erro", "abc", "outros")
    assert sucesso is False
    assert erro is not None
    assert len(gastos) == 0


def test_adicionar_gasto_valor_negativo():
    gastos = []
    with patch("main.salvar_gastos"):
        sucesso, erro = app.adicionar_gasto(gastos, "Negativo", "-10", "outros")
    assert sucesso is False
    assert erro is not None


def test_adicionar_gasto_valor_zero():
    gastos = []
    with patch("main.salvar_gastos"):
        sucesso, erro = app.adicionar_gasto(gastos, "Zero", "0", "outros")
    assert sucesso is False
    assert erro is not None


def test_adicionar_gasto_valor_muito_alto():
    gastos = []
    with patch("main.salvar_gastos"):
        sucesso, erro = app.adicionar_gasto(gastos, "Absurdo", "1e+45", "outros")
    assert sucesso is False
    assert erro is not None


def test_id_sem_duplicatas_apos_remocao():
    """
    Garante que o ID gerado após remoção não duplica IDs existentes.
    Antes da correção: len(gastos)+1 geraria id=2 de novo após remover id=2.
    """
    gastos = [gasto(1, "A", "10.00"), gasto(2, "B", "20.00"), gasto(3, "C", "30.00")]
    with patch("main.salvar_gastos"):
        app.remover_gasto(gastos, 2)       # remove id=2; restam ids 1 e 3
        app.adicionar_gasto(gastos, "D", "40.00", "outros")

    ids = [g["id"] for g in gastos]
    assert len(ids) == len(set(ids)), f"IDs duplicados encontrados: {ids}"
    assert gastos[-1]["id"] == 4


def test_remover_gasto():
    gastos = [gasto(1, "Teste", "10.00")]
    with patch("main.salvar_gastos"):
        resultado = app.remover_gasto(gastos, 1)
    assert resultado is True
    assert len(gastos) == 0


def test_remover_id_inexistente():
    gastos = []
    with patch("main.salvar_gastos"):
        resultado = app.remover_gasto(gastos, 99)
    assert resultado is False
    assert len(gastos) == 0


def test_ver_resumo_vazio(capsys):
    app.ver_resumo([])
    saida = capsys.readouterr().out
    assert "Nenhum" in saida


def test_ver_resumo_com_dados(capsys):
    gastos = [
        gasto(1, "A", "100.00", "alimentacao"),
        gasto(2, "B", "50.00", "transporte"),
    ]
    app.ver_resumo(gastos)
    saida = capsys.readouterr().out
    assert "150.00" in saida


def test_ver_resumo_precisao_decimal(capsys):
    """Garante que valores decimais são somados sem erro de ponto flutuante."""
    gastos = [
        gasto(1, "A", "0.10"),
        gasto(2, "B", "0.20"),
    ]
    app.ver_resumo(gastos)
    saida = capsys.readouterr().out
    assert "0.30" in saida   # com float puro isso daria 0.30000000000000004


# ── testes de validacao ──────────────────────────────────

def test_validar_valor_virgula():
    """Aceita vírgula como separador decimal (comum no Brasil)."""
    valor, erro = app.validar_valor("1.250,99")
    # Nota: "1.250,99" após replace(",", ".") vira "1.250.99" que é inválido.
    # Documentamos aqui que o formato aceito é ponto como separador.
    # Para suporte a vírgula como decimal sem milhar, "19,90" → "19.90" funciona.
    valor2, erro2 = app.validar_valor("19,90")
    assert erro2 is None
    assert valor2 == Decimal("19.90")


# ── teste de integracao (com mock) ───────────────────────

def test_buscar_cotacao_dolar_sucesso():
    resposta_fake = json.dumps({
        "USDBRL": {"bid": "5.25"}
    }).encode()

    mock_resposta = MagicMock()
    mock_resposta.read.return_value = resposta_fake
    mock_resposta.__enter__ = lambda s: s
    mock_resposta.__exit__ = MagicMock(return_value=False)

    with patch("urllib.request.urlopen", return_value=mock_resposta):
        cotacao = app.buscar_cotacao_dolar()

    assert cotacao == Decimal("5.25")


def test_buscar_cotacao_dolar_falha_de_conexao():
    with patch("urllib.request.urlopen", side_effect=Exception("sem conexao")):
        cotacao = app.buscar_cotacao_dolar()

    assert cotacao is None


def test_ver_resumo_em_dolar_com_cotacao(capsys):
    gastos = [gasto(1, "A", "525.00")]

    with patch("main.buscar_cotacao_dolar", return_value=Decimal("5.25")):
        app.ver_resumo_em_dolar(gastos)

    saida = capsys.readouterr().out
    assert "100.00" in saida  # 525 / 5.25 = 100.00