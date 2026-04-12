# Bootcamp_II-Entrega_Inicial

# Gerenciador de Gastos

## Descrição do Problema

Muitas pessoas têm dificuldade de controlar os próprios gastos no dia a dia. Sem um registro simples e acessível, é fácil perder a noção de quanto foi gasto e em quê, o que pode levar a problemas financeiros no fim do mês.

## Proposta da Solução

Uma aplicação de linha de comando (CLI) que permite registrar, visualizar e remover gastos pessoais de forma rápida e simples, sem precisar de internet ou criar conta em nenhum serviço. Os dados ficam salvos localmente em um arquivo JSON.

## Público-alvo

Pessoas que querem começar a controlar suas finanças pessoais de forma simples, sem depender de aplicativos complexos ou pagos.

## Funcionalidades Principais

- Adicionar um gasto informando descrição, valor e categoria
- Listar todos os gastos cadastrados
- Remover um gasto pelo ID
- Ver o total gasto

## Tecnologias Utilizadas

- Python 3.10+
- Módulos nativos: `json`, `os`, `datetime`
- pytest (testes)
- Ruff (lint)
- GitHub Actions (CI)

## Instruções de Instalação

Certifique-se de ter o Python 3.10 ou superior instalado. Depois, clone o repositório:

```bash
git clone https://github.com/Zoroethruz/Bootcamp_II-Entrega_Inicial.git
cd Bootcamp_II-Entrega_Inicial

```

Instale as dependências de desenvolvimento:

```bash
pip install pytest ruff
```

## Instruções de Execução

```bash
python main.py
```

## Instruções para Rodar os Testes

```bash
pytest
```

## Instruções para Rodar o Lint

```bash
ruff check .
```

## Versão Atual

1.0.0

## Autor

João Guilherme Rangel do Nascimento

## Repositório

https://github.com/Zoroethruz/Bootcamp_II-Entrega_Inicial
