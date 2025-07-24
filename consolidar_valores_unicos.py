import pandas as pd
import os
import sys # Para sair do script em caso de erro grave

def consolidar_valores_unicos_de_pasta(pasta_entrada, arquivo_saida):
    """
    Lê todos os arquivos CSV em uma pasta de entrada, extrai os valores únicos
    da segunda coluna de cada arquivo, e consolida tudo em um único CSV de saída
    com as colunas 'Categoria' e 'Valor_Unico'.

    Args:
        pasta_entrada (str): O caminho para a pasta contendo os arquivos CSV.
        arquivo_saida (str): O caminho para o arquivo CSV de saída consolidado.
    """
    lista_resultados = [] # Lista para armazenar dicionários {'Categoria': ..., 'Valor_Unico': ...}

    # Verifica se a pasta de entrada existe
    if not os.path.isdir(pasta_entrada):
        print(f"Erro: Pasta de entrada não encontrada em '{pasta_entrada}'")
        return

    print(f"Iniciando varredura na pasta: '{pasta_entrada}'")

    # Itera sobre todos os arquivos na pasta de entrada
    for nome_arquivo in os.listdir(pasta_entrada):
        # Verifica se é um arquivo CSV
        if nome_arquivo.lower().endswith('.csv'):
            caminho_completo = os.path.join(pasta_entrada, nome_arquivo)
            print(f"\nProcessando arquivo: '{nome_arquivo}'...")

            try:
                # Tenta ler o arquivo CSV
                df = pd.read_csv(caminho_completo)

                # Verifica se o DataFrame tem pelo menos duas colunas
                if df.shape[1] < 2:
                    print(f"  Aviso: O arquivo '{nome_arquivo}' não possui pelo menos duas colunas. Pulando.")
                    continue # Pula para o próximo arquivo

                # Pega o nome da segunda coluna (índice 1) - esta será a 'Categoria'
                nome_segunda_coluna = df.columns[1]
                print(f"  Analisando coluna de categoria: '{nome_segunda_coluna}'")

                # Extrai os valores únicos da segunda coluna
                # .dropna() remove valores ausentes (NaN, None)
                # .astype(str) converte para string para garantir consistência
                # .str.strip() remove espaços em branco no início e fim
                # .unique() pega apenas os valores distintos
                # Filtra strings vazias explicitamente após o strip
                valores_unicos = df[nome_segunda_coluna].dropna().astype(str).str.strip().unique()
                valores_unicos_filtrados = [valor for valor in valores_unicos if valor] # Remove strings vazias

                if valores_unicos_filtrados:
                    print(f"  Encontrados {len(valores_unicos_filtrados)} valores únicos.")
                    # Adiciona cada valor único à lista de resultados
                    for valor in valores_unicos_filtrados:
                        lista_resultados.append({
                            'Categoria': nome_segunda_coluna,
                            'Valor_Unico': valor
                        })
                else:
                    print("  Nenhum valor único (não nulo/vazio) encontrado nesta coluna.")

            except pd.errors.EmptyDataError:
                print(f"  Aviso: O arquivo '{nome_arquivo}' está vazio. Pulando.")
            except Exception as e:
                print(f"  Erro inesperado ao processar o arquivo '{nome_arquivo}':")
                print(f"  {e}")
                print("  Pulando este arquivo.")

    # --- Consolidação e Salvamento ---
    if lista_resultados:
        print(f"\nConsolidando {len(lista_resultados)} valores únicos de todas as categorias...")
        # Cria um DataFrame a partir da lista de resultados
        df_consolidado = pd.DataFrame(lista_resultados)

        # Opcional: Ordenar o DataFrame final para melhor visualização
        df_consolidado = df_consolidado.sort_values(by=['Categoria', 'Valor_Unico']).reset_index(drop=True)

        try:
            # Garante que a pasta de destino exista, se o caminho incluir pastas
            pasta_destino_saida = os.path.dirname(arquivo_saida)
            if pasta_destino_saida and not os.path.exists(pasta_destino_saida):
                os.makedirs(pasta_destino_saida)

            # Salva o DataFrame consolidado no arquivo de saída
            df_consolidado.to_csv(arquivo_saida, index=False, encoding='utf-8')
            print(f"\nArquivo consolidado salvo com sucesso em: '{arquivo_saida}'")
        except Exception as e:
            print(f"\nErro ao salvar o arquivo consolidado '{arquivo_saida}':")
            print(e)
    else:
        print("\nNenhum valor único foi extraído de nenhum arquivo CSV na pasta especificada.")
        print("Nenhum arquivo de saída foi gerado.")

# --- Como usar ---
# 1. Defina o nome da pasta que contém os arquivos CSV:
nome_da_pasta_entrada = 'tabelas_divididas_corrigido' # <--- CONFIRME O NOME DA PASTA

# 2. Defina o nome desejado para o arquivo CSV de saída consolidado:
nome_do_arquivo_saida_consolidado = 'consolidado_valores_unicos.csv'

# 3. Chama a função para processar a pasta e gerar o arquivo consolidado
consolidar_valores_unicos_de_pasta(nome_da_pasta_entrada, nome_do_arquivo_saida_consolidado)
