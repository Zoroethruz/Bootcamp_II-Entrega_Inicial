import sys
import os
import json
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import main as app


# ── testes unitarios ─────────────────────────────────────

def test_adicionar_gasto():
    gastos = []
    app.adicionar_gasto(gastos, "Mercado", 50.0, "alimentacao")
    assert len(gastos) == 1
    assert gastos[0]["descricao"] == "Mercado"
    assert gastos[0]["valor"] == 50.0


def test_remover_gasto():
    gastos = [{"id": 1, "descricao": "Teste", "valor": 10.0, "categoria": "outros", "data": "2024-01-01"}]
    app.remover_gasto(gastos, 1)
    assert len(gastos) == 0


def test_remover_id_inexistente():
    gastos = []
    app.remover_gasto(gastos, 99)
    assert len(gastos) == 0


def test_ver_resumo_vazio(capsys):
    app.ver_resumo([])
    saida = capsys.readouterr().out
    assert "Nenhum" in saida


def test_ver_resumo_com_dados(capsys):
    gastos = [
        {"id": 1, "descricao": "A", "valor": 100.0, "categoria": "alimentacao", "data": "2024-01-01"},
        {"id": 2, "descricao": "B", "valor": 50.0, "categoria": "transporte", "data": "2024-01-02"},
    ]
    app.ver_resumo(gastos)
    saida = capsys.readouterr().out
    assert "150.00" in saida


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

    assert cotacao == 5.25


def test_buscar_cotacao_dolar_falha_de_conexao():
    with patch("urllib.request.urlopen", side_effect=Exception("sem conexao")):
        cotacao = app.buscar_cotacao_dolar()

    assert cotacao is None


def test_ver_resumo_em_dolar_com_cotacao(capsys):
    gastos = [
        {"id": 1, "descricao": "A", "valor": 525.0, "categoria": "outros", "data": "2024-01-01"},
    ]

    with patch("main.buscar_cotacao_dolar", return_value=5.25):
        app.ver_resumo_em_dolar(gastos)

    saida = capsys.readouterr().out
    assert "100.00" in saida  # 525 / 5.25 = 100.00
