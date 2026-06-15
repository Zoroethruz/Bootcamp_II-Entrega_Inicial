# Gerenciador de Gastos

## Descrição do Problema

Muitas pessoas têm dificuldade de controlar os próprios gastos no dia a dia. Sem um registro simples e acessível, é fácil acabar gastando mais do que o necessário, o que pode levar a problemas financeiros no fim do mês.

## Proposta da Solução

Uma aplicação de linha de comando (CLI) que permite registrar, visualizar e remover gastos pessoais de forma simples, sem precisar de internet ou criar conta em nenhum serviço. A aplicação também se conecta à internet para buscar a cotação atual do dólar e exibir o total de gastos convertido em tempo real.

## Público-alvo

Pessoas que querem começar a controlar suas finanças pessoais de forma simples, pessoas que possuem problemas de compra impulsiva e pessoas que se esquecem facilmente das próprias despesas

## Funcionalidades Principais

- Adicionar um gasto informando descrição, valor e categoria
- Listar todos os gastos cadastrados
- Remover um gasto pelo ID
- Ver o total gasto em reais
- Ver o total gasto convertido em dólar (cotação em tempo real)

## Tecnologias Utilizadas

- Python 3.11
- Módulos nativos: `json`, `os`, `datetime`, `urllib`
- AwesomeAPI (cotação do dólar, gratuita e sem chave)
- pytest (testes)
- Ruff (lint)
- GitHub Actions (CI)
- Supabase (banco de dados em nuvem)

## Instruções de Instalação

Certifique-se de ter o Python 3.11 ou superior instalado. Depois, clone o repositório:

```
git clone https://github.com/Zoroethruz/Bootcamp_II-Entrega_Inicial.git
cd Bootcamp_II-Entrega_Inicial
```

Instale o Supabase

```
pip install Supabase

```

Instale as dependências de desenvolvimento:

```
pip install pytest ruff
```

## Instruções de Execução

```
python main.py
```

## Instruções para Rodar os Testes

```
pytest
```

## Instruções para Rodar o Lint

```
ruff check .
```

## Deploy

Por se tratar de uma aplicação CLI, não há uma URL de acesso web. Para executá-la, siga as instruções de instalação e execução acima.

## Versão Atual

1.2.1

## Autor

- João Guilherme Rangel do Nascimento
-  Guilherme Ribeiro da Paula

## Repositório

<https://github.com/Zoroethruz/Bootcamp_II-Entrega_Inicial>
