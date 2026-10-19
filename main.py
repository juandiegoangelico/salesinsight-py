"""
main.py
Ponto de entrada do SalesInsight PY: executa o pipeline de ponta a ponta.
"""

import os
import modulo_vendas as mv

# Caminhos relativos à pasta do projeto (funciona de qualquer diretório)
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_DADOS = os.path.join(PASTA_PROJETO, "vendas.csv")
PASTA_SAIDA = os.path.join(PASTA_PROJETO, "outputs")


def main():
    print("=" * 60)
    print(" SALESINSIGHT PY - Pipeline de Processamento com Python Nativo")
    print("=" * 60)

    # 1. Gerar dataset sintético se não existir
    if not os.path.exists(ARQUIVO_DADOS):
        mv.gerar_dataset_sintetico(ARQUIVO_DADOS, n_registros=150)

    # 2. Leitura e inspeção
    dados_brutos = mv.carregar_csv(ARQUIVO_DADOS)
    mv.inspecionar_dados(dados_brutos)

    # 3. Limpeza e transformação
    dados_limpos = mv.limpar_dados(dados_brutos)
    dados_transformados = mv.criar_campos_derivados(dados_limpos)

    # 4. Função de ordem superior com lambda
    dados_com_tag = mv.processar_transformacao(
        dados_transformados,
        lambda x: {**x, "processado": True}
    )

    # 5. Métricas e segmentação
    metricas = mv.calcular_metricas(dados_com_tag)
    segmentos = mv.segmentar_clientes(dados_com_tag)
    top_clientes = mv.obter_top_clientes(segmentos, top_n=5)

    # 6. Exibição dos resultados
    print("\n=== RESUMO EXECUTIVO ===")
    print(f"Receita Total da Empresa: R$ {metricas['total_geral']:,.2f}")

    print("\nReceita por Categoria:")
    for cat, rec in sorted(metricas["por_categoria"].items(), key=lambda p: p[1], reverse=True):
        print(f"  - {cat:<12} R$ {rec:>12,.2f}")

    print("\nReceita por Região:")
    for reg, rec in sorted(metricas["por_regiao"].items(), key=lambda p: p[1], reverse=True):
        print(f"  - {reg:<12} R$ {rec:>12,.2f}")

    print("\nClientes por segmento:")
    for seg, qtd in mv.contar_segmentos(segmentos).items():
        print(f"  - {seg}: {qtd}")

    print("\nTop 5 Clientes Ouro/Prata:")
    for cli, info in top_clientes:
        print(f"  - {cli}: R$ {info['total_gasto']:,.2f} ({info['segmento']})")

    # 7. Exportação
    print()
    mv.exportar_resultados(metricas, segmentos, PASTA_SAIDA)

    print("\n[CONCLUÍDO] Pipeline executado com sucesso!")


if __name__ == "__main__":
    main()
