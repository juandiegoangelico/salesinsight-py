"""
modulo_vendas.py
Módulo com as funções do pipeline SalesInsight PY.
Usa apenas a biblioteca padrão do Python (csv, json, os, random, datetime).
"""

import csv
import json
import os
import random
from datetime import datetime

CAMPOS_OBRIGATORIOS = ["id_venda", "data_venda", "cliente", "produto",
                       "categoria", "regiao", "quantidade", "preco_unitario"]


# ---------------------------------------------------------------------------
# RF01 - Criar o dataset de vendas
# ---------------------------------------------------------------------------
def gerar_dataset_sintetico(caminho_arquivo="vendas.csv", n_registros=100, seed=42):
    """Gera um CSV sintético de vendas com alguns nulos e espaços extras propositais."""
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse"]
    categorias = {"Notebook": "Eletrônicos", "Smartphone": "Celulares", "Tablet": "Celulares",
                  "Monitor": "Eletrônicos", "Teclado": "Acessórios", "Mouse": "Acessórios"}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

    cabecalho = CAMPOS_OBRIGATORIOS
    dados = []

    for i in range(1, n_registros + 1):
        prod = random.choice(produtos)
        qtd = str(random.randint(1, 8)) if random.random() > 0.05 else ""        # nulos
        preco = str(round(random.uniform(100, 3500), 2)) if random.random() > 0.05 else ""
        prod_nome = f"  {prod} " if random.random() < 0.1 else prod             # espaços extras

        dados.append([
            i,
            f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            f"Cliente_{random.randint(1, 30):03d}",
            prod_nome,
            categorias.get(prod, "Outros"),
            random.choice(regioes),
            qtd,
            preco,
        ])

    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(cabecalho)
        writer.writerows(dados)   # (o exemplo do enunciado gravava a 1ª linha duas vezes)
    print(f"[OK] Dataset gerado em: {caminho_arquivo} ({n_registros} registros)")


# ---------------------------------------------------------------------------
# RF07 - Leitura do CSV com csv.DictReader
# ---------------------------------------------------------------------------
def carregar_csv(caminho_arquivo):
    """Lê o CSV e devolve uma lista de dicionários."""
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    dados = []
    with open(caminho_arquivo, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            dados.append(linha)
    print(f"[OK] {len(dados)} registros lidos de: {caminho_arquivo}")
    return dados


# ---------------------------------------------------------------------------
# RF02 - Inspeção dos dados
# ---------------------------------------------------------------------------
def inspecionar_dados(dados):
    """Mostra total de registros, campos e mapeia linhas com valores nulos/vazios."""
    print("\n=== INSPEÇÃO INICIAL DOS DADOS ===")
    print(f"Total de registros carregados: {len(dados)}")

    if not dados:
        print("Nenhum registro encontrado.")
        return {"total_registros": 0, "linhas_incompletas": 0, "nulos_por_campo": {}}

    print(f"Campos disponíveis: {list(dados[0].keys())}")
    print(f"Exemplo do primeiro registro: {dados[0]}")

    nulos_por_campo = {campo: 0 for campo in dados[0].keys()}
    ids_incompletos = []

    for linha in dados:
        incompleta = False
        for campo, valor in linha.items():
            if valor is None or str(valor).strip() == "":
                nulos_por_campo[campo] += 1
                incompleta = True
        if incompleta:
            ids_incompletos.append(linha.get("id_venda", "?"))

    print(f"Linhas com dados incompletos/nulos: {len(ids_incompletos)}")
    print("Valores nulos por campo:")
    for campo, qtd in nulos_por_campo.items():
        if qtd > 0:
            print(f"  - {campo}: {qtd}")
    if ids_incompletos:
        print(f"IDs das linhas incompletas: {', '.join(ids_incompletos)}")

    return {
        "total_registros": len(dados),
        "linhas_incompletas": len(ids_incompletos),
        "nulos_por_campo": nulos_por_campo,
    }


# ---------------------------------------------------------------------------
# RF03 - Limpeza e tratamento
# ---------------------------------------------------------------------------
def data_valida(texto):
    """Retorna True se a data estiver no formato AAAA-MM-DD e for uma data real."""
    try:
        datetime.strptime(texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def limpar_dados(dados_brutos):
    """Remove espaços, descarta registros vazios/inválidos e converte tipos."""
    dados_limpos = []
    removidos = 0

    for lin in dados_brutos:
        # Remove espaços extras de todos os campos de texto
        lin = {campo: (valor or "").strip() for campo, valor in lin.items()}

        # Registros com quantidade ou preço vazios são descartados
        if not lin["quantidade"] or not lin["preco_unitario"]:
            removidos += 1
            continue

        # Data inválida também invalida o registro
        if not data_valida(lin["data_venda"]):
            removidos += 1
            continue

        try:
            qtd = int(lin["quantidade"])
            preco = float(lin["preco_unitario"])
        except ValueError:
            removidos += 1
            continue

        # Valores negativos ou zero não fazem sentido em uma venda
        if qtd <= 0 or preco <= 0:
            removidos += 1
            continue

        dados_limpos.append({
            "id_venda": int(lin["id_venda"]),
            "data_venda": lin["data_venda"],
            "cliente": lin["cliente"],
            "produto": lin["produto"],
            "categoria": lin["categoria"],
            "regiao": lin["regiao"],
            "quantidade": qtd,
            "preco_unitario": preco,
        })

    print("\n=== RELATÓRIO DE LIMPEZA ===")
    print(f"Registros Válidos: {len(dados_limpos)} | Registros Removidos: {removidos}")
    return dados_limpos


# ---------------------------------------------------------------------------
# RF04 - Campos derivados
# ---------------------------------------------------------------------------
def classificar_faixa_preco(preco):
    """Baixo (< 500), Médio (500 a 2000), Alto (> 2000)."""
    if preco < 500:
        return "Baixo"
    elif preco <= 2000:
        return "Médio"
    return "Alto"


def criar_campos_derivados(dados):
    """Adiciona receita_total e faixa_preco a cada registro."""
    for item in dados:
        item["receita_total"] = round(item["quantidade"] * item["preco_unitario"], 2)
        item["faixa_preco"] = classificar_faixa_preco(item["preco_unitario"])
    return dados


# ---------------------------------------------------------------------------
# Função de ordem superior (usada no main com lambda)
# ---------------------------------------------------------------------------
def processar_transformacao(dados, funcao):
    """Aplica uma função (ex.: lambda) a cada registro e devolve uma nova lista."""
    return [funcao(item) for item in dados]


# ---------------------------------------------------------------------------
# RF05 - Métricas agregadas
# ---------------------------------------------------------------------------
def calcular_metricas(dados):
    """Receita por categoria, por região e total geral."""
    receita_categoria = {}
    receita_regiao = {}
    total_geral = 0.0

    for item in dados:
        cat = item["categoria"]
        reg = item["regiao"]
        rec = item["receita_total"]

        receita_categoria[cat] = receita_categoria.get(cat, 0.0) + rec
        receita_regiao[reg] = receita_regiao.get(reg, 0.0) + rec
        total_geral += rec

    # Arredonda só no final para não acumular erro de arredondamento
    receita_categoria = {k: round(v, 2) for k, v in receita_categoria.items()}
    receita_regiao = {k: round(v, 2) for k, v in receita_regiao.items()}

    return {
        "total_geral": round(total_geral, 2),
        "total_registros": len(dados),
        "por_categoria": receita_categoria,
        "por_regiao": receita_regiao,
    }


# ---------------------------------------------------------------------------
# RF06 - Segmentação de clientes
# ---------------------------------------------------------------------------
def classificar_segmento(total):
    """Bronze (< 3000), Prata (3000 a 8000), Ouro (> 8000)."""
    if total > 8000:
        return "Ouro"
    elif total >= 3000:
        return "Prata"
    return "Bronze"


def segmentar_clientes(dados):
    """Soma o gasto de cada cliente e classifica em Bronze/Prata/Ouro."""
    gastos_cliente = {}
    for item in dados:
        cli = item["cliente"]
        gastos_cliente[cli] = gastos_cliente.get(cli, 0.0) + item["receita_total"]

    segmentos = {}
    for cli, total in gastos_cliente.items():
        segmentos[cli] = {"total_gasto": round(total, 2), "segmento": classificar_segmento(total)}
    return segmentos


def contar_segmentos(segmentos):
    """Quantos clientes há em cada segmento."""
    contagem = {"Ouro": 0, "Prata": 0, "Bronze": 0}
    for info in segmentos.values():
        contagem[info["segmento"]] += 1
    return contagem


def obter_top_clientes(segmentos, top_n=5):
    """Top N clientes Ouro/Prata, ordenados pelo gasto (maior primeiro)."""
    elegiveis = [(cli, info) for cli, info in segmentos.items()
                 if info["segmento"] in ("Ouro", "Prata")]
    elegiveis.sort(key=lambda par: par[1]["total_gasto"], reverse=True)
    return elegiveis[:top_n]


# ---------------------------------------------------------------------------
# RF07 - Exportação CSV e JSON
# ---------------------------------------------------------------------------
def exportar_resultados(metricas, clientes, pasta_saida="outputs"):
    """Gera outputs/estatisticas.json e outputs/metricas_resumo.csv."""
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_json = os.path.join(pasta_saida, "estatisticas.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump({
            "metricas_gerais": metricas,
            "resumo_segmentos": contar_segmentos(clientes),
            "clientes": clientes,
        }, f, indent=4, ensure_ascii=False)
    print(f"[OK] Arquivo JSON exportado em: {caminho_json}")

    caminho_csv = os.path.join(pasta_saida, "metricas_resumo.csv")
    with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Tipo", "Nome", "Receita Total"])
        for cat, rec in sorted(metricas["por_categoria"].items()):
            escritor.writerow(["Categoria", cat, f"{rec:.2f}"])
        for reg, rec in sorted(metricas["por_regiao"].items()):
            escritor.writerow(["Regiao", reg, f"{rec:.2f}"])
        escritor.writerow(["Total", "Geral", f"{metricas['total_geral']:.2f}"])
    print(f"[OK] Arquivo CSV exportado em: {caminho_csv}")
