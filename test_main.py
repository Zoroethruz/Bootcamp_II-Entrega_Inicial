import json
import sys
import os
from decimal import Decimal
from unittest.mock import patch, MagicMock

mock_supabase_client = MagicMock()
sys.modules.setdefault("supabase", MagicMock(create_client=lambda url, key: mock_supabase_client))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import main as app


# ── helpers ──────────────────────────────────────────────

def gasto(id, descricao, valor, categoria="outros", data="2024-01-01"):
    """Cria um dict de gasto no formato retornado pelo Supabase."""
    return {
        "id": id,
        "descricao": descricao,
        "valor": str(Decimal(str(valor)).quantize(Decimal("0.01"))),
        "categoria": categoria,
        "data": data,
    }


# ── validar_valor ─────────────────────────────────────────

def test_validar_valor_inteiro():
    valor, erro = app.validar_valor("50")
    assert erro is None
    assert valor == Decimal("50.00")


def test_validar_valor_decimal_ponto():
    valor, erro = app.validar_valor("19.90")
    assert erro is None
    assert valor == Decimal("19.90")


def test_validar_valor_decimal_virgula():
    """Vírgula simples como separador decimal deve ser aceita."""
    valor, erro = app.validar_valor("19,90")
    assert erro is None
    assert valor == Decimal("19.90")


def test_validar_valor_float_nativo():
    valor, erro = app.validar_valor(29.9)
    assert erro is None
    assert valor == Decimal("29.90")


def test_validar_valor_invalido():
    valor, erro = app.validar_valor("abc")
    assert valor is None
    assert erro is not None


def test_validar_valor_negativo():
    valor, erro = app.validar_valor("-10")
    assert valor is None
    assert erro is not None


def test_validar_valor_zero():
    valor, erro = app.validar_valor("0")
    assert valor is None
    assert erro is not None


def test_validar_valor_muito_alto():
    valor, erro = app.validar_valor("1e+45")
    assert valor is None
    assert erro is not None


# ── adicionar_gasto ───────────────────────────────────────

def test_adicionar_gasto_sucesso():
    gastos = []
    with patch("main.inserir_gasto") as mock_inserir:
        sucesso, erro = app.adicionar_gasto(gastos, "Mercado", "50.00", "alimentacao")

    assert sucesso is True
    assert erro is None
    assert len(gastos) == 1
    g = gastos[0]
    assert g["descricao"] == "Mercado"
    assert g["valor"] == "50.00"
    assert g["categoria"] == "alimentacao"
    assert "data" in g
    mock_inserir.assert_called_once()


def test_adicionar_gasto_valor_como_float():
    gastos = []
    with patch("main.inserir_gasto"):
        sucesso, _ = app.adicionar_gasto(gastos, "Uber", 29.9, "transporte")
    assert sucesso is True
    assert gastos[0]["valor"] == "29.90"


def test_adicionar_gasto_valor_invalido_nao_insere():
    gastos = []
    with patch("main.inserir_gasto") as mock_inserir:
        sucesso, erro = app.adicionar_gasto(gastos, "Erro", "abc", "outros")
    assert sucesso is False
    assert erro is not None
    assert len(gastos) == 0
    mock_inserir.assert_not_called()


def test_adicionar_gasto_valor_negativo_nao_insere():
    gastos = []
    with patch("main.inserir_gasto") as mock_inserir:
        sucesso, erro = app.adicionar_gasto(gastos, "Neg", "-5", "outros")
    assert sucesso is False
    assert erro is not None
    mock_inserir.assert_not_called()


def test_adicionar_gasto_valor_zero_nao_insere():
    gastos = []
    with patch("main.inserir_gasto") as mock_inserir:
        sucesso, erro = app.adicionar_gasto(gastos, "Zero", "0", "outros")
    assert sucesso is False
    assert erro is not None
    mock_inserir.assert_not_called()


def test_adicionar_gasto_valor_muito_alto_nao_insere():
    gastos = []
    with patch("main.inserir_gasto") as mock_inserir:
        sucesso, erro = app.adicionar_gasto(gastos, "Absurdo", "1e+45", "outros")
    assert sucesso is False
    assert erro is not None
    mock_inserir.assert_not_called()


# ── remover_gasto ─────────────────────────────────────────

def test_remover_gasto_existente():
    gastos = [gasto(1, "Teste", "10.00")]
    with patch("main.deletar_gasto") as mock_deletar:
        resultado = app.remover_gasto(gastos, 1)
    assert resultado is True
    assert len(gastos) == 0
    mock_deletar.assert_called_once_with(1)


def test_remover_gasto_id_inexistente():
    gastos = [gasto(1, "Teste", "10.00")]
    with patch("main.deletar_gasto") as mock_deletar:
        resultado = app.remover_gasto(gastos, 99)
    assert resultado is False
    assert len(gastos) == 1
    mock_deletar.assert_not_called()


def test_remover_gasto_lista_vazia():
    gastos = []
    with patch("main.deletar_gasto") as mock_deletar:
        resultado = app.remover_gasto(gastos, 1)
    assert resultado is False
    mock_deletar.assert_not_called()


# ── listar_gastos ─────────────────────────────────────────

def test_listar_gastos_vazia(capsys):
    app.listar_gastos([])
    saida = capsys.readouterr().out
    assert saida == ""


def test_listar_gastos_exibe_dados(capsys):
    gastos = [gasto(1, "Almoço", "35.50", "alimentacao", "2024-06-01")]
    app.listar_gastos(gastos)
    saida = capsys.readouterr().out
    assert "Almoço" in saida
    assert "35.50" in saida
    assert "alimentacao" in saida


# ── ver_resumo ────────────────────────────────────────────

def test_ver_resumo_lista_vazia(capsys):
    app.ver_resumo([])
    saida = capsys.readouterr().out
    assert "Nenhum" in saida


def test_ver_resumo_total_correto(capsys):
    gastos = [
        gasto(1, "A", "100.00", "alimentacao"),
        gasto(2, "B", "50.00", "transporte"),
    ]
    app.ver_resumo(gastos)
    saida = capsys.readouterr().out
    assert "150.00" in saida


def test_ver_resumo_precisao_decimal(capsys):
    """Garante que 0.10 + 0.20 resulta em 0.30, sem erro de ponto flutuante."""
    gastos = [gasto(1, "A", "0.10"), gasto(2, "B", "0.20")]
    app.ver_resumo(gastos)
    saida = capsys.readouterr().out
    assert "0.30" in saida


def test_ver_resumo_quantidade(capsys):
    gastos = [gasto(i, "X", "10.00") for i in range(1, 4)]
    app.ver_resumo(gastos)
    saida = capsys.readouterr().out
    assert "3" in saida


# ── buscar_cotacao_dolar ──────────────────────────────────

def test_buscar_cotacao_dolar_sucesso():
    resposta_fake = json.dumps({"USDBRL": {"bid": "5.25"}}).encode()
    mock_resp = MagicMock()
    mock_resp.read.return_value = resposta_fake
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)

    with patch("urllib.request.urlopen", return_value=mock_resp):
        cotacao = app.buscar_cotacao_dolar()

    assert cotacao == Decimal("5.25")


def test_buscar_cotacao_dolar_falha_conexao():
    with patch("urllib.request.urlopen", side_effect=Exception("sem conexao")):
        cotacao = app.buscar_cotacao_dolar()
    assert cotacao is None


# ── ver_resumo_em_dolar ───────────────────────────────────

def test_ver_resumo_em_dolar_com_cotacao(capsys):
    gastos = [gasto(1, "A", "525.00")]
    with patch("main.buscar_cotacao_dolar", return_value=Decimal("5.25")):
        app.ver_resumo_em_dolar(gastos)
    saida = capsys.readouterr().out
    assert "100.00" in saida  # 525 / 5.25 = 100.00


def test_ver_resumo_em_dolar_sem_conexao(capsys):
    gastos = [gasto(1, "A", "100.00")]
    with patch("main.buscar_cotacao_dolar", return_value=None):
        app.ver_resumo_em_dolar(gastos)
    saida = capsys.readouterr().out
    assert "conexao" in saida.lower() or "cotacao" in saida.lower()


def test_ver_resumo_em_dolar_lista_vazia(capsys):
    app.ver_resumo_em_dolar([])
    saida = capsys.readouterr().out
    assert "Nenhum" in saida


# ── carregar_gastos (integração com mock Supabase) ────────

def test_carregar_gastos_sucesso():
    dados_fake = [gasto(1, "X", "10.00")]
    mock_execute = MagicMock()
    mock_execute.data = dados_fake
    app.supabase.table.return_value.select.return_value.order.return_value.execute.return_value = mock_execute

    resultado = app.carregar_gastos()
    assert resultado == dados_fake


def test_carregar_gastos_erro_retorna_lista_vazia(capsys):
    app.supabase.table.return_value.select.return_value.order.return_value.execute.side_effect = Exception("falha")
    resultado = app.carregar_gastos()
    assert resultado == []
    # Restaura para não afetar outros testes
    app.supabase.table.return_value.select.return_value.order.return_value.execute.side_effect = None
