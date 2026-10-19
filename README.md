# SalesInsight PY - Pipeline de Análise de Dados de Vendas

Pipeline simples e modularizado para tratamento, transformação e agregação de dados de vendas utilizando **apenas recursos nativos do Python** (`csv`, `json`, `os`, `random`, `datetime`).

## 📁 Estrutura do Projeto

```
salesinsight-py/
├── modulo_vendas.py       # Funções de leitura, limpeza, transformação, agregação e exportação
├── main.py                # Ponto de entrada: importa o módulo e executa o pipeline
├── vendas.csv             # Dataset sintético de vendas (150 registros, seed=42)
├── README.md
└── outputs/
    ├── metricas_resumo.csv   # Receita por categoria, por região e total geral
    └── estatisticas.json     # Métricas gerais, resumo de segmentos e dados por cliente
```

## 🚀 Como Executar

1. Certifique-se de ter o Python 3 instalado (`python --version`).
2. Clone ou descompacte o repositório.
3. No terminal, dentro da pasta do projeto, execute:

```bash
python main.py
```

Se o arquivo `vendas.csv` não existir, ele é gerado automaticamente. Os relatórios são gravados na pasta `outputs/`. Nenhuma biblioteca externa é necessária.

## 🔄 Etapas do Pipeline

| Etapa | Requisito | Função(ões) |
|---|---|---|
| Geração do dataset | RF01 | `gerar_dataset_sintetico()` |
| Leitura com `csv.DictReader` | RF07 | `carregar_csv()` |
| Inspeção (total de registros e nulos por campo) | RF02 | `inspecionar_dados()` |
| Limpeza (`.strip()`, remoção de nulos, validação de data, conversão para `int`/`float`) | RF03 | `limpar_dados()`, `data_valida()` |
| Campos derivados `receita_total` e `faixa_preco` | RF04 | `criar_campos_derivados()` |
| Função de ordem superior com `lambda` | — | `processar_transformacao()` |
| Receita por categoria, por região e total geral | RF05 | `calcular_metricas()` |
| Segmentação Bronze / Prata / Ouro | RF06 | `segmentar_clientes()`, `obter_top_clientes()` |
| Exportação CSV e JSON | RF07 | `exportar_resultados()` |
| Orquestração | RF08 | `main.py` |

## 📏 Regras de Negócio

**Faixa de preço** (baseada no `preco_unitario`): Baixo (< R$ 500), Médio (R$ 500 a R$ 2.000), Alto (> R$ 2.000).

**Segmento de cliente** (gasto acumulado): Bronze (< R$ 3.000), Prata (R$ 3.000 a R$ 8.000), Ouro (> R$ 8.000).

**Limpeza:** registros com quantidade ou preço vazios, não numéricos, menores ou iguais a zero, ou com data inválida são descartados.

## 🧠 Conceitos Aplicados

Listas e dicionários, laços `for`, condicionais, funções e modularização, função de ordem superior com `lambda`, tratamento de exceções (`try/except`), leitura e escrita de arquivos CSV e JSON, e versionamento com Git.

## 👥 Autoria

- Nome do(a) estudante / integrantes da squad
