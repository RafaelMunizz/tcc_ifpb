import pandas as pd
import numpy as np # Import numpy para lidar com NaN se necessário

def processar_csv(nome_arquivo, pasta_destino):
    """
    Processa um arquivo CSV, removendo duplicatas e convertendo colunas
    específicas para tipo booleano, lidando com diversos formatos de entrada.

    Args:
      nome_arquivo: O nome do arquivo CSV a ser processado.
      pasta_destino: A pasta onde o novo arquivo CSV será salvo.
    """
    # --- Leitura com tentativa de encoding ---
    try:
        # Tente UTF-8 primeiro, que é mais comum
        df = pd.read_csv(nome_arquivo, encoding='utf-8')
        print("Arquivo lido com encoding UTF-8.")
    except UnicodeDecodeError:
        try:
            # Se UTF-8 falhar, tente latin1 (comum em sistemas Windows antigos/Europa Ocidental)
            df = pd.read_csv(nome_arquivo, encoding='latin1')
            print("Arquivo lido com encoding latin1.")
        except Exception as e:
            print(f"Erro ao ler CSV com UTF-8 e latin1: {e}")
            return # Não continuar se não conseguir ler o arquivo

    print("\nTipos de dados ANTES do processamento:")
    print(df.dtypes)

    # Remover linhas duplicadas 
    try:
        df = df.drop_duplicates(subset=df.columns[2:], keep='first')
        print("\nDuplicatas removidas.")
    except IndexError:
         print("Erro: CSV não parece ter colunas suficientes para usar df.columns[2:]. Verifique o índice inicial.")
         return


    # --- Conversão para Booleano Aprimorada ---
    print("\nIniciando conversão para booleano...")
    for coluna in ['SSL/TLS enabled', 'Responsive']:
        if coluna in df.columns:
            print(f"Processando coluna: {coluna}")
            # Armazenar tipo original para comparação
            dtype_original = df[coluna].dtype

            # 1. (Opcional, mas recomendado) Padronizar strings para maiúsculas e sem espaços extras
            #    Isso simplifica o mapa. Só aplica se for string.
            if pd.api.types.is_string_dtype(df[coluna]):
                 df[coluna] = df[coluna].str.strip().str.upper()

            # 2. Criar o mapa abrangente para todos os casos vistos (e alguns extras por segurança)
            mapa_booleano = {
                '1': True, 'TRUE': True,  # Strings
                1: True, 1.0: True,      # Números (int, float)
                '0': False, 'FALSE': False, # Strings
                0: False, 0.0: False      # Números (int, float)
                # Valores como '', None, np.nan serão mapeados para NaN por padrão pelo .map
            }

            # 3. Aplicar o mapa. Valores não encontrados no mapa viram NaN.
            df[coluna] = df[coluna].map(mapa_booleano)

            # 4. Converter explicitamente para o tipo booleano anulável do Pandas ('boolean')
            #    Este tipo pode conter True, False, e <NA> (o indicador de ausente do Pandas)
            try:
                df[coluna] = df[coluna].astype('boolean')
                print(f" -> Coluna '{coluna}' convertida para tipo 'boolean'. Tipo anterior: {dtype_original}")
            except Exception as e:
                print(f" -> ERRO ao converter coluna '{coluna}' para 'boolean': {e}")
                print(f" -> Valores únicos após map em '{coluna}': {df[coluna].unique()}")


    print("\nTipos de dados DEPOIS da conversão booleana:")
    print(df.dtypes)
    # Opcional: Ver valores únicos depois
    if 'SSL/TLS enabled' in df.columns:
        print("\nValores únicos em 'SSL/TLS enabled' (DEPOIS):", df['SSL/TLS enabled'].unique())
    if 'Responsive' in df.columns:
        print("Valores únicos em 'Responsive' (DEPOIS):", df['Responsive'].unique())

    # --- Salvar o CSV ---
    try:
        # É uma boa prática especificar o encoding na escrita também, preferencialmente utf-8
        df.to_csv(pasta_destino, index=False, encoding='utf-8')
        print(f"\nArquivo processado salvo em: {pasta_destino}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")


# Exemplo de uso
nome_arquivo = 'PEC1_coleta_de_dados_Planilha_FINAL.csv'
pasta_destino = 'planilha_sem_duplicatas.csv'

processar_csv(nome_arquivo, pasta_destino)