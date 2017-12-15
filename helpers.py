from bs4 import BeautifulSoup
import requests


def process_request(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')


def download_pdf(url, link):
    name = link.contents[0]
    response = requests.get(url)
    with open(f'pdfs/{name}.pdf', 'wb') as f:
        f.write(response.content)

