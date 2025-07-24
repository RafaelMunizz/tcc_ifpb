import pandas as pd
import sys # Para sair do script em caso de erro grave

def listar_valores_unicos_segunda_coluna(nome_arquivo):
    """
    Lê um arquivo CSV, extrai todos os valores únicos da segunda coluna
    (ignorando valores nulos/vazios) e os imprime.

    Args:
        nome_arquivo (str): O caminho para o arquivo CSV a ser processado.
    """
    try:
        # Tenta ler o arquivo CSV
        df = pd.read_csv(nome_arquivo)
        print(f"Arquivo '{nome_arquivo}' lido com sucesso.")

        # Verifica se o DataFrame tem pelo menos duas colunas
        if df.shape[1] < 2:
            print(f"Erro: O arquivo '{nome_arquivo}' não possui pelo menos duas colunas.")
            return # Sai da função

        # Pega o nome da segunda coluna (índice 1)
        nome_segunda_coluna = df.columns[1]
        print(f"Analisando a segunda coluna: '{nome_segunda_coluna}'")

        # Extrai os valores únicos da segunda coluna
        # .dropna() remove valores ausentes (NaN, None)
        # .astype(str) converte para string para garantir consistência e remover espaços
        # .str.strip() remove espaços em branco no início e fim
        # .unique() pega apenas os valores distintos
        # Filtra strings vazias explicitamente após o strip
        valores_unicos = df[nome_segunda_coluna].dropna().astype(str).str.strip().unique()
        valores_unicos_filtrados = [valor for valor in valores_unicos if valor] # Remove strings vazias

        # Ordena os valores para facilitar a leitura (opcional)
        valores_unicos_filtrados.sort()

        # Imprime os resultados
        if valores_unicos_filtrados:
            print("\nValores únicos encontrados na segunda coluna:")

            print(f"\nO Wappalyzer classifica essas ferramentas abaixo como {nome_segunda_coluna}. Confira se eles realmente se classificam nessa categoria. Caso não se classifique, coloque uma classificação que ele melhor se encaixe.':")
            
            # Imprime um valor por linha para melhor visualização
            for valor in valores_unicos_filtrados:
                print(f"- {valor}")
            print(f"\nTotal de valores únicos: {len(valores_unicos_filtrados)}")
        else:
            print("Nenhum valor único (não nulo/vazio) encontrado na segunda coluna.")

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{nome_arquivo}'")
    except pd.errors.EmptyDataError:
         print(f"Erro: O arquivo '{nome_arquivo}' está vazio.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao processar o arquivo '{nome_arquivo}':")
        print(e)

# --- Como usar ---
# 1. Defina o nome do arquivo CSV que você quer analisar:
#    Substitua 'seu_arquivo.csv' pelo nome real do seu arquivo.
#    Certifique-se de que ele esteja na mesma pasta do script Python,
#    ou forneça o caminho completo (ex: 'C:/pasta/seu_arquivo.csv').
nome_do_arquivo_csv = 'tabelas_divididas_corrigido/cdn.csv'


# 2. Chama a função para processar o arquivo definido acima
listar_valores_unicos_segunda_coluna(nome_do_arquivo_csv)

# Exemplo para outro arquivo (descomente para usar):
# print("\n--- Analisando outro arquivo ---")
# listar_valores_unicos_segunda_coluna('javascript_frameworks_new.csv')
