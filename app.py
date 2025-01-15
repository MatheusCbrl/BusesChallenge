import requests
from bs4 import BeautifulSoup
import json
import re

def extract_bus_data(url):
    # Enviar a requisição e obter o conteúdo da página
    response = requests.get(url)
    html_content = response.content

    # Parsear o HTML usando BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Localizar os elementos de listagem de ônibus
    bus_listings = soup.find_all('table', border="0")

    # Lista para armazenar os dados extraídos
    bus_data = []

    # Iterar pelas listagens e extrair informações relevantes
    for listing in bus_listings:
        bus_info = {}

        # Extrair título
        title_element = listing.find('a')
        bus_info['title'] = title_element.text.strip() if title_element else ''

        # Extrair ano
        year_element = listing.find(text=re.compile(r'Year:\s*'))
        if year_element:
            year_match = re.search(r'Year:\s*(\d{4})', year_element)
            bus_info['year'] = int(year_match.group(1)) if year_match else None

        # Extrair preço, verificando se está em tags `<strong>` ou aninhado
        price_element = listing.find(text=re.compile(r'Price:\s*'))
        if not price_element:
            price_element = listing.find('strong', text=re.compile(r'\$[\d,]+'))
        
        if price_element:
            price_match = re.search(r'\$([\d,]+)', price_element)
            bus_info['price'] = float(price_match.group(1).replace(',', '')) if price_match else None

        # Extrair fabricante e modelo
        make_model_text = listing.find(text=re.compile(r'Bus Builder:\s*'))
        bus_info['make'] = make_model_text.split(":")[1].strip() if make_model_text else ''
        
        # Extrair motor
        engine_text = listing.find(text=re.compile(r'Engine:\s*'))
        bus_info['engine'] = engine_text.split(":")[1].strip() if engine_text else ''

        # Extrair número de estoque
        stock_number_text = listing.find(text=re.compile(r'Stock Number:\s*'))
        if stock_number_text:
            stock_number_match = re.search(r'Stock Number:\s*(\d+)', stock_number_text)
            bus_info['stock_number'] = int(stock_number_match.group(1)) if stock_number_match else None

        # Extrair URL da imagem
        image_element = listing.find('img')
        bus_info['image_url'] = image_element['src'] if image_element else ''

        # Adicionar dados do ônibus à lista
        bus_data.append(bus_info)

    return bus_data

# URL da página para coleta de dados
bus_listings_url = 'http://absolutebus.com/listings/'
bus_data = extract_bus_data(bus_listings_url)

# Salvar dados extraídos em um arquivo JSON
with open('bus_data.json', 'w') as f:
    json.dump(bus_data, f, indent=4)

print("Dados extraídos e salvos com sucesso!")
