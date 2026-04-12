import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import main as app


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
    app.remover_gasto(gastos, 99)  # nao deve dar erro
    assert len(gastos) == 0


def test_ver_resumo_vazio(capsys):
    app.ver_resumo([])
    saida = capsys.readouterr().out
    assert "Nenhum" in saida


def test_ver_resumo_com_dados(capsys):
    gastos = [
        {"id": 1, "descricao": "A", "valor": 100.0, "categoria": "alimentacao", "data": "2024-01-01"},
        {"id": 2, "descricao": "B", "valor": 50.0,  "categoria": "transporte",  "data": "2024-01-02"},
    ]
    app.ver_resumo(gastos)
    saida = capsys.readouterr().out
    assert "150.00" in saida
