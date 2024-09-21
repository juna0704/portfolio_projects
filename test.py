import requests
import ssl
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re

def scrape_website(url):
    try:
        # Attempt 1: Default request
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        print(f"Default request failed. Error: {e}")
        print("Trying alternative methods...")
        
        try:
            # Attempt 2: Ignore SSL verification
            response = requests.get(url, verify=False)
            response.raise_for_status()
            print("Warning: SSL verification was ignored.")
            return response.text
        except RequestException as e:
            print(f"Ignoring SSL verification didn't work. Error: {e}")
            print("Trying with custom SSL context...")
            
            # try:
            #     # Attempt 3: Custom SSL context
            #     context = ssl.create_default_context()
            #     context.check_hostname = False
            #     context.verify_mode = ssl.CERT_NONE
                
            #     response = requests.get(url, verify=False)
            #     response.raise_for_status()
            #     print("Warning: Custom SSL context was used.")
            #     return response.text
            # except RequestException as e:
            #     print(f"All attempts failed. Error: {e}")
            #     return None

def extract_pdf_links(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    pdf_links = []

    # Look for links that end with .pdf
    for link in soup.find_all('a', href=re.compile(r'\.pdf$')):
        pdf_url = link.get('href')
        if pdf_url.startswith('/'):
            pdf_url = base_url + pdf_url
        elif not pdf_url.startswith('http'):
            pdf_url = base_url + '/' + pdf_url
        pdf_links.append(pdf_url)

    return pdf_links

# Usage
base_url = "https://acordaos.economia.gov.br"
url = f"{base_url}/solr/acordaos2/browse"
result = scrape_website(url)

if result:
    print("Successfully scraped the website.")
    pdf_links = extract_pdf_links(result, base_url)
    
    if pdf_links:
        print(f"Found {len(pdf_links)} PDF links:")
        for link in pdf_links: 
            print(link)
    else:
        print("No PDF links found on the first page.")
else:
    print("Failed to scrape the website.")



