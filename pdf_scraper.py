import requests
from bs4 import BeautifulSoup
from urllib.request import unquote


class PdfScraper:
    def fetch(self,url):
        print(f'Getting HTTP response from {url}',end=' ')
        resp = requests.get(url)
        print(f'| status code for url is {resp.status_code}')
        print('***********************')
        return resp
    
    def pdf_parser(self,html):
        soup = BeautifulSoup(html,'html.parser')
        all_links = soup.select('a[href]')
        pdf_url = ''
        for url in all_links:
            if 'pdf' in url['href']:
                if 'https' in url['href']:
                    pdf_url = url['href']
                else:
                    pdf_url = 'https://www.dyysg.org.uk'+ url['href']
                yield pdf_url
    
    def pdf_downloader(self, pdf_url):
        pdf_response = requests.get(pdf_url)
        file_name = unquote(pdf_url).split('/')[-1].replace(' ', '_')
        print(f'saving :-{file_name}')

        with open('./pdf/' + file_name, 'wb') as f:
            f.write(pdf_response.content)
            
        



scraper = PdfScraper()
html = scraper.fetch('https://dyysg.org.uk/docs.php')
pdf_url = scraper.pdf_parser(html.text)
for urls in pdf_url:

    scraper.pdf_downloader(urls)