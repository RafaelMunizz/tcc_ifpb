import os
import pandas as pd

def unificar_arquivos_tecnologia(pasta_entrada, arquivo_saida="novos_arquivos_csv_refatorados/Tecnologias_Unificadas.csv"):
    """
    Unifica arquivos CSV de tecnologias de uma pasta em um único arquivo CSV.

    Args:
        pasta_entrada (str): O caminho para a pasta contendo os arquivos CSV.
        arquivo_saida (str): O nome do arquivo CSV unificado a ser gerado.
    """
    lista_dataframes = []
    arquivo_principal_ignorar = "tabela_principal.csv"

    print(f"Procurando arquivos na pasta: {pasta_entrada}")

    # Listar todos os arquivos na pasta de entrada
    try:
        arquivos_na_pasta = os.listdir(pasta_entrada)
    except FileNotFoundError:
        print(f"Erro: A pasta '{pasta_entrada}' não foi encontrada.")
        return
    except Exception as e:
        print(f"Erro ao listar arquivos na pasta: {e}")
        return

    arquivos_csv_processados = 0

    for nome_arquivo in arquivos_na_pasta:
        if nome_arquivo.endswith(".csv") and nome_arquivo.lower() != arquivo_principal_ignorar.lower():
            caminho_completo_arquivo = os.path.join(pasta_entrada, nome_arquivo)
            print(f"Processando arquivo: {nome_arquivo}...")

            try:
                # Ler o CSV
                df_temp = pd.read_csv(caminho_completo_arquivo)

                # Verificar se o DataFrame tem pelo menos duas colunas
                if df_temp.shape[1] < 2:
                    print(f"  Aviso: O arquivo {nome_arquivo} não possui as duas colunas esperadas e será ignorado.")
                    continue

                # A primeira coluna é 'ID'
                coluna_id = df_temp.columns[0]

                # A segunda coluna contém as ferramentas/tecnologias específicas
                # O nome desta segunda coluna também é a categoria (antes de adicionar .csv)
                nome_coluna_ferramentas = df_temp.columns[1]

                # Criar o DataFrame processado
                df_processado = pd.DataFrame()
                df_processado['ID'] = df_temp[coluna_id]
                df_processado['Nome_Ferramenta_Tecnologia'] = df_temp[nome_coluna_ferramentas]

                # A categoria da tecnologia é o nome do arquivo sem a extensão .csv
                # Ou, neste caso, o nome da segunda coluna original
                categoria_tecnologia = nome_coluna_ferramentas
                # Se preferir usar o nome do arquivo:
                # categoria_tecnologia = nome_arquivo.replace(".csv", "")

                df_processado['Categoria_Tecnologia'] = categoria_tecnologia

                lista_dataframes.append(df_processado)
                arquivos_csv_processados += 1
                print(f"  Arquivo {nome_arquivo} processado com sucesso. Categoria: {categoria_tecnologia}")

            except pd.errors.EmptyDataError:
                print(f"  Aviso: O arquivo {nome_arquivo} está vazio e será ignorado.")
            except Exception as e:
                print(f"  Erro ao processar o arquivo {nome_arquivo}: {e}")

    if not lista_dataframes:
        print("\nNenhum arquivo de tecnologia encontrado ou processado para unificar.")
        return

    # Concatenar todos os DataFrames da lista em um único DataFrame
    df_unificado = pd.concat(lista_dataframes, ignore_index=True)

    # Salvar o DataFrame unificado em um novo arquivo CSV
    try:
        df_unificado.to_csv(arquivo_saida, index=False)
        print(f"\nArquivo unificado '{arquivo_saida}' criado com sucesso em '{pasta_entrada}'.")
        print(f"Total de arquivos CSV de tecnologia processados: {arquivos_csv_processados}")
        print(f"Total de registros no arquivo unificado: {len(df_unificado)}")
    except Exception as e:
        print(f"\nErro ao salvar o arquivo unificado: {e}")

# --- COMO USAR ---
# Especifique o caminho para a sua pasta
pasta_dos_arquivos = "tabelas_divididas_corrigido"

# Chame a função
unificar_arquivos_tecnologia(pasta_dos_arquivos)