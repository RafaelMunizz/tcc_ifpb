import pandas as pd
import os
import numpy as np # Para lidar com NaN de forma mais explícita

def processar_csv_split(nome_arquivo, pasta_destino):
    """
    Processa um arquivo CSV, separando colunas com múltiplos dados (delimitados por ';')
    em arquivos CSV individuais (tabelas de relacionamento n:n com ID).

    Args:
      nome_arquivo: O nome do arquivo CSV de entrada.
      pasta_destino: A pasta onde os novos arquivos CSV serão salvos.
    """

    # --- 0. Garantir que a pasta de destino existe ---
    if not os.path.exists(pasta_destino):
        try:
            os.makedirs(pasta_destino)
            print(f"Pasta de destino criada: {pasta_destino}")
        except OSError as e:
            print(f"Erro ao criar pasta de destino '{pasta_destino}': {e}")
            return

    # --- 1. Ler o arquivo CSV ---
    try:
        # É mais seguro ler como está e converter ID depois, caso haja valores não numéricos.
        df = pd.read_csv(nome_arquivo)
        print(f"Arquivo '{nome_arquivo}' lido com sucesso ({len(df)} linhas).")
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{nome_arquivo}'")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV '{nome_arquivo}': {e}")
        return

    # --- Garantir que a coluna 'ID' existe ---
    if 'ID' not in df.columns:
        print("Erro Crítico: Coluna 'ID' não encontrada no arquivo CSV.")
        return

    # --- 2. Identificar colunas para dividir e colunas para a tabela principal ---
    colunas_sem_multiplos_dados = []
    colunas_com_multiplos_dados = []
    print("\nAnalisando colunas:")
    for coluna in df.columns:
        # Pular a coluna ID da verificação de múltiplos dados
        if coluna == 'ID':
            colunas_sem_multiplos_dados.append(coluna)
            continue

        # Verificar se a coluna tem dados e se contém ';'
        # Usar .astype(str) para tratar números/booleanos que podem não ter .str
        # E .any() para verificar se *alguma* linha contém ';'
        contem_ponto_virgula = False
        if df[coluna].notna().any(): # Só verifica se houver algum dado não-nulo
             # fillna('') evita erro em .str.contains com NaN
             if df[coluna].astype(str).str.contains(';', na=False).any():
                 contem_ponto_virgula = True

        if contem_ponto_virgula:
            colunas_com_multiplos_dados.append(coluna)
            print(f"  - '{coluna}': Contém múltiplos valores (será dividida).")
        else:
            colunas_sem_multiplos_dados.append(coluna)
            # print(f"  - '{coluna}': Não contém múltiplos valores.") # Opcional: Descomentar para verbosidade

    # --- 3. Criar e salvar a tabela principal (se houver colunas para ela) ---
    if colunas_sem_multiplos_dados:
        df_sem_multiplos_dados = df[colunas_sem_multiplos_dados].copy()
        # Remover linhas onde o ID é nulo na tabela principal também
        df_sem_multiplos_dados = df_sem_multiplos_dados.dropna(subset=['ID'])
        # Opcional: Converter ID para int na tabela principal
        try:
             df_sem_multiplos_dados['ID'] = df_sem_multiplos_dados['ID'].astype(int)
        except ValueError:
             print("Aviso: IDs não inteiros encontrados na tabela principal. Mantendo como float/object.")


        caminho_principal = os.path.join(pasta_destino, 'tabela_principal.csv')
        try:
            df_sem_multiplos_dados.to_csv(caminho_principal, index=False, encoding='utf-8')
            print(f"\nTabela principal salva em: {caminho_principal} ({len(df_sem_multiplos_dados)} linhas).")
        except Exception as e:
            print(f"Erro ao salvar a tabela principal: {e}")
    else:
        print("\nNenhuma coluna identificada para a tabela principal (exceto talvez ID se existir).")


    # --- 4. Iterar e criar tabelas N:N ---
    print("\nProcessando colunas com múltiplos valores para criar tabelas N:N:")
    if not colunas_com_multiplos_dados:
        print("Nenhuma coluna com ';' encontrada para dividir.")

    for coluna in colunas_com_multiplos_dados:
        print(f"  - Processando coluna: '{coluna}'...")

        # Criar um novo DataFrame apenas com 'ID' e a coluna atual
        # Remover linhas onde a coluna de DADOS é nula ANTES de processar
        # Manter linhas com ID nulo por enquanto, serão tratadas depois
        novo_df = df[['ID', coluna]].dropna(subset=[coluna]).copy()

        # Verificar se restou algum dado após dropar NaNs da coluna de dados
        if novo_df.empty:
            print(f"    * Coluna '{coluna}' vazia ou contém apenas NaNs. Pulando.")
            continue

        # ** LINHA PROBLEMÁTICA REMOVIDA **
        # A lógica de drop_duplicates aqui estava incorreta e causava perda de dados.

        # Garantir que IDs nulos sejam tratados antes da conversão para int
        novo_df = novo_df.dropna(subset=['ID'])
        if novo_df.empty:
            print(f"    * Coluna '{coluna}' não possui IDs válidos após remover NaNs de ID. Pulando.")
            continue

        # Tentar converter ID para Int ANTES do explode
        try:
             novo_df['ID'] = novo_df['ID'].astype(int)
        except ValueError:
             print(f"    * Aviso: IDs não inteiros encontrados ao processar '{coluna}'. Tentando converter para numérico e removendo falhas.")
             novo_df['ID'] = pd.to_numeric(novo_df['ID'], errors='coerce') # Erros viram NaN
             novo_df = novo_df.dropna(subset=['ID']) # Remove IDs que falharam na conversão
             if novo_df.empty:
                  print(f"    * Pulando coluna '{coluna}' pois não restaram IDs numéricos válidos.")
                  continue
             novo_df['ID'] = novo_df['ID'].astype(int) # Tenta de novo após coerção e dropna
        except Exception as e:
             print(f"    * Erro inesperado ao converter ID para int na coluna '{coluna}': {e}. Pulando coluna.")
             continue


        # Expandir os dados da coluna (split e explode)
        # .astype(str) antes de .str.split é importante se a coluna tiver números/outros tipos
        novo_df[coluna] = novo_df[coluna].astype(str).str.split(';')
        novo_df = novo_df.explode(coluna)

        # Limpar espaços em branco dos dados explodidos
        # Verificar se a coluna ainda é string/object antes de usar .str
        if pd.api.types.is_string_dtype(novo_df[coluna]):
            novo_df[coluna] = novo_df[coluna].str.strip()
        # else: # Se virou outro tipo após explode (improvável com split de string), não aplicar strip
        #    pass

        # Descartar dados que se tornaram vazios ('') ou nulos (None/NaN) APÓS split/strip
        novo_df[coluna] = novo_df[coluna].replace('', np.nan) # Substitui '' por NaN
        novo_df = novo_df.dropna(subset=[coluna])       # Remove linhas com NaN na coluna de dados

        # Verificar se ainda há dados válidos após a limpeza
        if novo_df.empty:
             print(f"    * Coluna '{coluna}' não gerou dados válidos após split e limpeza. Pulando.")
             continue

        # Garantir que ID ainda é inteiro (pode não ser necessário, mas seguro)
        novo_df['ID'] = novo_df['ID'].astype(int)

        # Criar nome do arquivo em snake_case seguro para sistemas de arquivos
        nome_base = coluna.lower().replace(' ', '_')
        # Remover caracteres que podem ser problemáticos em nomes de arquivo
        nome_arquivo_saida = "".join(c for c in nome_base if c.isalnum() or c == '_')
        # Evitar nomes vazios se a coluna só tiver caracteres inválidos
        if not nome_arquivo_saida:
             nome_arquivo_saida = f"coluna_{df.columns.get_loc(coluna)}" # Usa índice como fallback

        caminho_saida = os.path.join(pasta_destino, f"{nome_arquivo_saida}.csv")

        # Salvar o novo DataFrame
        try:
            # Ordenar pelo ID pode ser útil para visualização
            novo_df = novo_df.sort_values(by='ID')
            novo_df.to_csv(caminho_saida, index=False, encoding='utf-8')
            print(f"    -> Tabela N:N salva em: '{caminho_saida}' ({len(novo_df)} linhas).")
        except Exception as e:
            print(f"    -> Erro ao salvar o arquivo '{caminho_saida}': {e}")

    print("\nProcessamento concluído.")


# --- Exemplo de Uso ---
# Certifique-se de que o nome do arquivo de entrada está correto
# nome_arquivo_entrada = 'planilha_TESTE.csv'
nome_arquivo_entrada = 'planilha_sem_duplicatas.csv' # Usando o nome do seu exemplo original

# Defina onde os arquivos gerados serão salvos
pasta_destino_saida = 'tabelas_divididas_corrigido' # Sugestão de novo nome para a pasta

processar_csv_split(nome_arquivo_entrada, pasta_destino_saida)