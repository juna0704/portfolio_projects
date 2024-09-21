import ssl
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


def fetch_url(url):
    try:
        print(f'Getting response from {url}')
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.text
    except RequestException as e:
        print(f'Default request failed ERROR {e}' )
        print('Tring alternative method for request *******')

        try:
            resp = requests.get(url, verify=False)
            resp.raise_for_status()
            print('Warning: SSL verification was ignored ')
            return resp.text
        except RequestException as e:
            print(f'Ignoreing SSL verification did not work ERRoR {e}')

       




fetch_url('https://acordaos.economia.gov.br/solr/acordaos2/browse')


