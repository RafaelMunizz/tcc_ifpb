import requests
import os
from bs4 import BeautifulSoup

def find_website(company_name):
    query = f"{company_name} site oficial"
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for div in soup.find_all("div", class_="yuRUbf"):
        a_tag = div.find("a", class_="LCaQh")
        if a_tag and a_tag.has_attr("href"):
            links.append(a_tag["href"])

    filtered_links = [
        link.split("&")[0].replace("/url?q=", "")
        for link in links if "/url?q=" in link
    ]

    return filtered_links[0] if filtered_links else "Website não encontrado"

def process_links(input_file, output_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, input_file)
    output_path = os.path.join(script_dir, output_file)

    with open(input_path, "r", encoding='utf-8') as file:
        companies = file.read().splitlines()

    with open(output_path, "w") as outfile:
        for company in companies:
            website = find_website(company)
            outfile.write(f"{website}\n")
            print(f"{company}: {website}")

input_file = "empresas.txt"
output_file = "sites.txt"

process_links(input_file, output_file)