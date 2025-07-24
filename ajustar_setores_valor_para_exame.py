import pandas as pd
import os

def padronizar_setores_para_exame(arquivo_entrada, arquivo_saida, coluna_a_padronizar='Setor primário'):
    """
    Lê um arquivo CSV, identifica setores no formato Valor Econômico na coluna especificada,
    mapeia-os para o formato da Revista Exame e salva o resultado (com a coluna padronizada)
    em um novo arquivo CSV. Setores já no formato Exame ou desconhecidos são mantidos.

    Args:
        arquivo_entrada (str): Caminho para o arquivo CSV de entrada (ex: 'tabela_principal.csv').
        arquivo_saida (str): Caminho para o arquivo CSV de saída com a coluna de setores padronizada.
        coluna_a_padronizar (str): Nome da coluna no arquivo de entrada que contém os setores misturados
                                    (Valor e Exame) a serem padronizados para o formato Exame.
                                    *** IMPORTANTE: Verifique e ajuste este nome de coluna! ***
    """

    # --- Dicionário de Mapeamento (Valor Econômico -> Exame) ---
    # Usado para converter APENAS os setores que forem identificados como sendo da Valor.
    mapa_valor_para_exame = {
        "Veículos e Peças": "Bens de Capital e Eletroeletrônicos",
        "Agronegócio": "Agronegócio",
        "Bioenergia": "Energia",
        "Petróleo e Gás": "Petróleo e Químico",
        "TI & Telecom": "Tecnologia e Telecomunicações",
        "Comércio Varejista": "Atacado e Varejo",
        "Transportes e Logística": "Transporte, Logística e Serviços Logísticos",
        "Química e Petroquímica": "Petróleo e Químico",
        "Eletroeletrônica": "Bens de Capital e Eletroeletrônicos",
        "Alimentos e Bebidas": "Alimentos e Bebidas",
        "Comércio Atacadista e Exterior": "Atacado e Varejo",
        "Energia Elétrica": "Energia",
        "Serviços Médicos": "Saúde e Serviços de Saúde",
        "Serviços Especializados": "Participações e Mídia", # Mapeamento forçado da análise anterior
        "Mineração": "Siderurgia, Mineração e Metalurgia",
        "Serviços Financeiros": "Serviços Financeiros",
        "Farmacêutica e Cosméticos": "Farmacêutico e Beleza",
        "Metalurgia e Siderurgia": "Siderurgia, Mineração e Metalurgia",
        "Mat. de Constr. e de Acabamento": "Imobiliário e Construção Civil",
        "Plásticos e Borracha": "Petróleo e Químico",
        "Água, Saneamento e Serviços Ambientais": "Saneamento e Meio Ambiente"
    }

    # Cria um conjunto com os nomes dos setores da Valor para verificação rápida
    setores_valor_conhecidos = set(mapa_valor_para_exame.keys())

    # --- Leitura do Arquivo de Entrada ---
    try:
        df = pd.read_csv(arquivo_entrada)
        print(f"Arquivo '{arquivo_entrada}' lido com sucesso ({len(df)} linhas).")
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada não encontrado em '{arquivo_entrada}'")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV '{arquivo_entrada}': {e}")
        return

    # --- Verificação da Coluna a ser Padronizada ---
    if coluna_a_padronizar not in df.columns:
        print(f"Erro: A coluna '{coluna_a_padronizar}' (que deveria conter os setores misturados) não foi encontrada.")
        print(f"Colunas disponíveis: {list(df.columns)}")
        print(f"*** Por favor, ajuste o parâmetro 'coluna_a_padronizar' na chamada da função ou no código para o nome correto da coluna de setores. ***")
        return

    # --- Função Auxiliar para Padronização ---
    def get_setor_exame(setor_atual):
        # Converte para string para segurança, remove espaços extras
        setor_str = str(setor_atual).strip()
        # Verifica se o setor atual está na lista de setores conhecidos da Valor
        if setor_str in setores_valor_conhecidos:
            # Se for da Valor, retorna o correspondente da Exame
            # .get() é usado para segurança, caso um setor_str esteja no set mas não no dict (improvável)
            return mapa_valor_para_exame.get(setor_str, setor_str)
        else:
            # Se não for um setor conhecido da Valor (pode ser Exame ou outro), retorna o valor original
            return setor_atual # Mantém o valor como está

    # --- Aplicação da Padronização na Coluna ---
    # Aplica a função 'get_setor_exame' a cada célula da coluna especificada,
    # modificando a coluna original (in-place).
    print(f"Padronizando a coluna '{coluna_a_padronizar}' para o padrão Exame...")
    # Garante que a coluna seja tratada como texto antes de aplicar
    df[coluna_a_padronizar] = df[coluna_a_padronizar].astype(str).apply(get_setor_exame)
    print("Padronização concluída.")

    # --- Salvamento do Arquivo de Saída ---
    try:
        # Garante que a pasta de destino exista, se o caminho incluir pastas
        pasta_destino = os.path.dirname(arquivo_saida)
        if pasta_destino and not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        df.to_csv(arquivo_saida, index=False, encoding='utf-8')
        print(f"Arquivo com coluna de setores padronizada salvo com sucesso em: '{arquivo_saida}'")
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV '{arquivo_saida}': {e}")

# --- Configuração e Execução ---
# Defina o nome do seu arquivo de entrada que contém os setores MISTURADOS (Valor e Exame)
arquivo_entrada_csv = 'tabelas_divididas_corrigido/tabela_principal.csv' # Ou o nome correto do seu arquivo

# Defina o nome desejado para o arquivo de saída (padronizado)
arquivo_saida_csv = 'tabela_principal_padronizada_exame.csv'

# *** ATENÇÃO: Defina o nome EXATO da coluna no seu CSV que contém os setores MISTURADOS ***
# Este é o nome da coluna que será lida e modificada.
coluna_com_setores_misturados = 'Setor primário'

# Chama a função para realizar a padronização
padronizar_setores_para_exame(arquivo_entrada_csv, arquivo_saida_csv, coluna_com_setores_misturados)
