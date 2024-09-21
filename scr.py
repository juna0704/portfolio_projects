import requests
from bs4 import BeautifulSoup
from urllib.request import unquote


class PdfScraper:
    def fetch(self,url):
        print(f'Send HTTP request to {url}')
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                print(f'Response successful {resp.status_code}')
            else:
                print(f'Response failde trying another response ...')

        except Exception as e:
            print('Error occured during request ', e )

        return resp
    
    def parse_pdf(self, html):
        content = BeautifulSoup(html, 'html.parser')
        all_urls = content.select('a[href]')
        pdf_url = ''    
        for url in all_urls:
            if 'pdf' in url['href']:
                if 'https:' in  url['href']:
                    pdf_url = url['href']

                else:
                    pdf_url ='https://www.dyysg.org.uk' + url['href']
                    
                file_name = unquote(pdf_url).split('/')[-1].replace(' ','_')
                print(f'saving :-{file_name} ')
                pdf_response = requests.get(pdf_url)
                # print(type(pdf_response.content))
                with open('./pdf/' + file_name, 'wb') as f:
                    f.write(pdf_response.content)
                





scraper = PdfScraper()

url = 'https://dyysg.org.uk/docs.php'
response = scraper.fetch(url)
html = scraper.parse_pdf(response.text)
