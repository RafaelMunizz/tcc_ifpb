# Análise de Tecnologias Web nas Maiores Empresas do Brasil

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este repositório contém todos os dados, scripts e artefatos desenvolvidos para o Trabalho de Conclusão de Curso (TCC) intitulado **"TECNOLOGIAS WEB UTILIZADAS NAS MAIORES EMPRESAS DO BRASIL"**, do curso de Bacharelado em Engenharia de Computação do IFPB - Campus Campina Grande.

## 📖 Sobre o Projeto

Este estudo teve como objetivo mapear e analisar o panorama tecnológico do setor corporativo brasileiro. Através da coleta de dados de mais de 1000 websites das maiores empresas do país, a pesquisa identifica as linguagens de programação, frameworks, bibliotecas e serviços mais prevalentes, oferecendo um retrato quantitativo do ecossistema de desenvolvimento web nacional.

Os dados foram coletados, tratados e analisados para gerar insights que possam orientar decisões estratégicas de empresas, guiar a formação de novos profissionais e contribuir para a compreensão das tendências tecnológicas no Brasil.

## ⚙️ Pipeline Metodológico

O processo de pesquisa foi executado em uma série de etapas automatizadas e manuais, refletidas na estrutura deste repositório. O fluxo de trabalho pode ser resumido da seguinte forma:

1.  **📂 Obtenção da Amostra e Coleta de URLs:** Definição da amostra a partir dos rankings "Valor 1000" e "Melhores e Maiores" e extração automatizada das URLs institucionais via script Python.
2.  **🔍 Coleta de Dados Tecnológicos:** Identificação das tecnologias de cada website utilizando a plataforma online **Wappalyzer**.
3.  **🧹 Tratamento e Limpeza dos Dados:** Execução de múltiplos scripts para padronizar setores, remover versões de tecnologias, corrigir categorizações e eliminar duplicatas.
4.  **📊 Estruturação Final para Análise:** Reestruturação dos dados limpos para um formato longo ("tidy"), ideal para a análise e importação em ferramentas de Business Intelligence.

## 📁 Estrutura do Repositório

```
.
├── Power BI/                         # Arquivos do dashboard interativo
│   └── Dashboard_PEC1.pbix
├── URLS/                             # Scripts e listas para coleta de URLs
│   ├── empresas.txt
│   └── get_url.py
├── tabelas_divididas_corrigido/      # CSVs finais, separados por categoria de tecnologia
│   ├── tabela_principal.csv          # Dados principais das empresas (ID, Nome, Setor)
│   └── ...                           # (analytics.csv, databases.csv, etc.)
├── novos_arquivos_csv_refatorados/   # Arquivos gerados durante o processo de refatoração
│   └── Tecnologias_Unificadas.csv    # O dataset final e unificado, pronto para o Power BI
├── ajustar_setores_valor_para_exame.py
├── transferir_libs_para_libraries.py
├── unificar_tecnologias_csv.py
├── PEC1_coleta_de_dados_Planilha_FINAL.csv # O principal arquivo de dados brutos pós-Wappalyzer
└── README.md
```

## 🚀 Como Utilizar

Para executar os scripts de análise, é necessário ter o Python 3.9 (ou superior) instalado, juntamente com as bibliotecas listadas no arquivo `requirements.txt`.

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/RafaelMunizz/tcc_ifpb.git](https://github.com/RafaelMunizz/tcc_ifpb.git)
    cd nome-do-repositorio
    ```

2.  Crie um ambiente virtual e instale as dependências:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  Execute os scripts na ordem descrita no pipeline metodológico.

## 📈 Visualização dos Dados

A análise final e a visualização dos dados foram realizadas na plataforma Microsoft Power BI. O dashboard interativo, cujo arquivo (`.pbix`) se encontra na pasta `/Power BI`, permite a exploração dos dados por setor, tecnologia e outras dimensões.

## ✍️ Como Citar

Se você utilizar os dados ou a metodologia deste trabalho, por favor, cite da seguinte forma:

ARAÚJO, Maria Eduarda Cunha Silva; MUNIZ, Rafael Victor Cordeiro. **TECNOLOGIAS WEB UTILIZADAS NAS MAIORES EMPRESAS DO BRASIL**. 2025. Trabalho de Conclusão de Curso (Bacharelado em Engenharia de Computação) – Instituto Federal de Educação, Ciência e Tecnologia da Paraíba, Campus Campina Grande, Campina Grande, 2025.

## 👥 Autores

-   **Maria Eduarda Cunha Silva Araújo**
    -   `eduardaaraujo492@gmail.com`
    -   `eduarda.cunha@academico.ifpb.edu.br`

-   **Rafael Victor Cordeiro Muniz**
    -   `rafaelvictormuniz@gmail.com`
    -   `rafael.muniz@academico.ifpb.edu.br`

### Orientador

-   **Prof. Dr. Elmano Ramalho Cavalcanti**

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.