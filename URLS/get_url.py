import requests
import os
from bs4 import BeautifulSoup

def find_website(company_name):
    query = f"{company_name} site oficial"
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/"
    }
    response = requests.get(url, headers=headers, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    # Captura todos os links (atributo href) da página
    links = []
    for a_tag in soup.find_all("a", href=True):
        links.append(a_tag["href"])

    # Filtra apenas links relevantes (removendo parâmetros do Google como "/url?q=")
    filtered_links = [
        link.split("&")[0].replace("/url?q=", "")
        for link in links if "/url?q=" in link
    ]

    # Retorna o primeiro link relevante encontrado ou uma mensagem
    return filtered_links[0] if filtered_links else "Website não encontrado"


def process_links(input_file, output_file):
    # Obter o diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir os caminhos absolutos dos arquivos
    input_path = os.path.join(script_dir, input_file)
    output_path = os.path.join(script_dir, output_file)

    with open(input_path, "r", encoding='utf-8') as file:
        companies = file.read().splitlines()  # Lê cada linha do arquivo como uma empresa

    with open(output_path, "w") as outfile:
        for company in companies:
            website = find_website(company)
            outfile.write(f"{website}\n")
            print(f"{company}: {website}")
            break

input_file = "empresas.txt"  # Nomes das empresas
output_file = "sites.txt"  # Resultados salvos

process_links(input_file, output_file)