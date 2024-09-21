import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def detect_website_technology(url):
    technologies = []

    # Make an initial request to get the static content
    response = requests.get(url)
    static_content = response.text

    # Set up Selenium WebDriver
    driver = webdriver.Chrome()  # Make sure to have chromedriver installed and in PATH
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)

    # Get the dynamic content
    dynamic_content = driver.page_source

    # Check if the content is static or dynamic
    if static_content == dynamic_content:
        technologies.append("Static Website")
    else:
        technologies.append("Dynamic Website")

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(dynamic_content, 'html.parser')

    # Check for common frameworks
    if soup.select('[ng-app]') or soup.select('[ng-controller]'):
        technologies.append("AngularJS")
    if soup.select('[data-reactroot]') or soup.select('[data-react-id]'):
        technologies.append("React")
    if soup.select('[data-v-]'):
        technologies.append("Vue.js")

    # Check for AJAX requests
    ajax_requests = driver.execute_script("""
        var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {};
        var network = performance.getEntriesByType("resource");
        return network.filter(function(entry) {
            return entry.initiatorType === "xmlhttprequest";
        }).length;
    """)
    if ajax_requests > 0:
        technologies.append("AJAX")

    # Check for Single Page Application (SPA)
    original_url = driver.current_url
    driver.find_element(By.TAG_NAME, 'body').click()  # Click somewhere to potentially trigger navigation
    time.sleep(2)
    if driver.current_url == original_url:
        technologies.append("Single Page Application (SPA)")

    # Check for server-side rendering
    if "server-side-render" in dynamic_content.lower():
        technologies.append("Server-side Rendering")

    # Check for common libraries
    if "jquery" in dynamic_content.lower():
        technologies.append("jQuery")
    if "bootstrap" in dynamic_content.lower():
        technologies.append("Bootstrap")

    # Close the browser
    driver.quit()

    return technologies

# Usage
url = "https://example.com"
detected_technologies = detect_website_technology(url)
print(f"Detected technologies for {url}:")
for tech in detected_technologies:
    print(f"- {tech}")