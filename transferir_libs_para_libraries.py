import pandas as pd
import os

# --- Configuração ---
arquivo_frameworks_origem = 'tabelas_divididas_corrigido/javascript_frameworks.csv'
arquivo_libraries_origem = 'tabelas_divididas_corrigido/javascript_libraries.csv'
arquivo_frameworks_destino = 'novos_arquivos_csv_refatorados/javascript_frameworks_new.csv'
arquivo_libraries_destino = 'novos_arquivos_csv_refatorados/javascript_libraries_new.csv'

# Lista das bibliotecas que estão incorretamente no arquivo de frameworks
bibliotecas_a_mover = {
    'styled-components',
    'React',
    'Emotion',
    'GSAP',
    'AlloyUI',
    'Zone.js',
    'Redux',
    'Socket.io',
    'Adobe Client Data Layer',
    'JSS',
    'RequireJS',
    'RxJS',
    'React Router',
    'toastr',
    'Stitches',
    'AlertifyJS',
    'Wink'
}

# Nomes das colunas esperadas
coluna_id = 'ID'
coluna_frameworks = 'JavaScript frameworks'
coluna_libraries = 'JavaScript libraries'

# --- Leitura dos Arquivos ---
try:
    df_frameworks = pd.read_csv(arquivo_frameworks_origem)
    print(f"Arquivo '{arquivo_frameworks_origem}' lido com sucesso ({len(df_frameworks)} linhas).")
except FileNotFoundError:
    print(f"Erro: Arquivo '{arquivo_frameworks_origem}' não encontrado.")
    exit() # Termina o script se o arquivo não for encontrado
except Exception as e:
    print(f"Erro ao ler '{arquivo_frameworks_origem}': {e}")
    exit()

try:
    df_libraries = pd.read_csv(arquivo_libraries_origem)
    print(f"Arquivo '{arquivo_libraries_origem}' lido com sucesso ({len(df_libraries)} linhas).")
except FileNotFoundError:
    print(f"Erro: Arquivo '{arquivo_libraries_origem}' não encontrado.")
    exit()
except Exception as e:
    print(f"Erro ao ler '{arquivo_libraries_origem}': {e}")
    exit()

# --- Verificação das Colunas ---
if coluna_frameworks not in df_frameworks.columns or coluna_id not in df_frameworks.columns:
     print(f"Erro: Colunas '{coluna_id}' ou '{coluna_frameworks}' não encontradas em '{arquivo_frameworks_origem}'.")
     print(f"Colunas encontradas: {list(df_frameworks.columns)}")
     exit()

if coluna_libraries not in df_libraries.columns or coluna_id not in df_libraries.columns:
     print(f"Erro: Colunas '{coluna_id}' ou '{coluna_libraries}' não encontradas em '{arquivo_libraries_origem}'.")
     print(f"Colunas encontradas: {list(df_libraries.columns)}")
     exit()


# --- Processamento ---

# 1. Identificar as linhas a serem movidas do DataFrame de frameworks
#    Verifica se o valor na coluna de frameworks está na nossa lista de bibliotecas a mover
linhas_para_mover = df_frameworks[df_frameworks[coluna_frameworks].isin(bibliotecas_a_mover)].copy()
print(f"Identificadas {len(linhas_para_mover)} linhas para mover de frameworks para libraries.")

# 2. Criar o novo DataFrame de frameworks (sem as linhas que foram movidas)
#    Usa o operador ~ (negação) para pegar todas as linhas EXCETO as que estão em 'linhas_para_mover'
df_frameworks_novo = df_frameworks[~df_frameworks[coluna_frameworks].isin(bibliotecas_a_mover)].copy()
print(f"Novo arquivo de frameworks terá {len(df_frameworks_novo)} linhas.")

# 3. Preparar as linhas movidas para serem adicionadas ao DataFrame de bibliotecas
if not linhas_para_mover.empty:
    # Renomear a coluna de 'JavaScript frameworks' para 'JavaScript libraries'
    linhas_para_mover.rename(columns={coluna_frameworks: coluna_libraries}, inplace=True)
    # Selecionar apenas as colunas 'ID' e a nova 'JavaScript libraries'
    linhas_para_mover = linhas_para_mover[[coluna_id, coluna_libraries]]

    # 4. Criar o novo DataFrame de bibliotecas (combinando o original com as linhas movidas)
    df_libraries_novo = pd.concat([df_libraries, linhas_para_mover], ignore_index=True)
    print(f"Novo arquivo de libraries terá {len(df_libraries_novo)} linhas.")
else:
    # Se nenhuma linha foi movida, o novo DataFrame de bibliotecas é igual ao original
    df_libraries_novo = df_libraries.copy()
    print("Nenhuma linha foi movida. O arquivo de libraries permanecerá o mesmo.")


# --- Salvamento dos Novos Arquivos ---
try:
    df_frameworks_novo.to_csv(arquivo_frameworks_destino, index=False, encoding='utf-8')
    print(f"Novo arquivo de frameworks salvo em: '{arquivo_frameworks_destino}'")
except Exception as e:
    print(f"Erro ao salvar '{arquivo_frameworks_destino}': {e}")

try:
    df_libraries_novo.to_csv(arquivo_libraries_destino, index=False, encoding='utf-8')
    print(f"Novo arquivo de libraries salvo em: '{arquivo_libraries_destino}'")
except Exception as e:
    print(f"Erro ao salvar '{arquivo_libraries_destino}': {e}")

print("\nProcesso concluído.")
