
from xml.etree.ElementTree import indent
import json
import requests
from bs4 import BeautifulSoup


def get_html(url):
    headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'}
    response = requests.get(url, headers=headers)
    return response.text


def get_currency(html):
    soup=BeautifulSoup(html, 'html.parser')
    currency = {}
    table = soup.find('table', class_='js_sortable')
    rows = table.find_all('tr')
    for row in rows[1:]:
        try:
            currency_number = row.find('td', class_='t-center').find('span').text
            currency_name = row.find('td', class_='t-left').text.split('\n')[0]
            currency_price = row.find('td', class_='t-right').text.split('\n')[0]
            currency_abbr = row.find('td', class_='t-center').find('span', class_='gray').text
        except AttributeError:
            continue
        try:
            currency_number = int(currency_number)  # Convert currency_number to int
        except (ValueError, TypeError):
            continue
        currency[currency_abbr]={
                'currency_number': currency_number,
                'currency_name': currency_name,
                'currency_price': currency_price

        }

    return currency



def write_currency_json(currency, filename='currency.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(currency, file, indent=2, ensure_ascii=False)




url='https://www.alta.ru/currency/'
html=get_html(url)
currency=get_currency(html)
write_currency_json(currency)

