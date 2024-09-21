import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_upwork_saved_jobs(username, password):
    # Set up Selenium WebDriver (you'll need to download the appropriate driver for your browser)
    driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.

    # Navigate to Upwork login page
    driver.get("https://www.upwork.com/ab/account-security/login")

    # Wait for the login form to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login_username")))

    # Fill in login credentials
    driver.find_element(By.ID, "login_username").send_keys(username)
    driver.find_element(By.ID, "login_password").send_keys(password)
    driver.find_element(By.ID, "login_submit").click()

    # Navigate to saved jobs page (you may need to adjust this URL)
    driver.get("https://www.upwork.com/nx/find-work/saved-jobs/")

    # Wait for the saved jobs to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "job-tile")))

    # Get the page source
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find and extract job information (adjust selectors as needed)
    job_tiles = soup.find_all('div', class_='job-tile')

    saved_jobs = []
    for job in job_tiles:
        title = job.find('h3', class_='job-title').text.strip()
        description = job.find('div', class_='job-description').text.strip()
        saved_jobs.append({'title': title, 'description': description})

    # Close the browser
    driver.quit()

    return saved_jobs

# Usage
username = "your_username"
password = "your_password"
jobs = scrape_upwork_saved_jobs(username, password)

for job in jobs:
    print(f"Title: {job['title']}")
    print(f"Description: {job['description']}")
    print("---")