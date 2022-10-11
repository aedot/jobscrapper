import cloudscraper
from email import header
import urllib
from urllib import request
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os


def find_jobs_from(website, job_title, location, desired_characs, filename="results.xls"):

    if website == 'Indeed':
        job_soup = load_indeed_jobs_div(job_title, location)
        jobs_list, num_listings = extract_job_information_indeed(job_soup, desired_characs)

    save_jobs_to_excel(jobs_list, filename)

    print('{} new job postings retrieved from {}. Stored in {}.'.format(num_listings, website, filename))

    

## ====================== SAVED TO EXECL ===================== ##

def save_jobs_to_excel(jobs_list, filename):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel(filename)


## ===================== FUNCTIONS FOR INDEED.COM ===================== ##



def load_indeed_jobs_div(job_title, location):
    getVars = {'q': job_title, 'l': location, 'fromage' : 'last', 'sort' : 'date'}
    url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(getVars))
    # headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'}
    scraper = cloudscraper.create_scraper()
    x = scraper.get(url)
    print(x.status_code)
    page = scraper.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="resultsCol")
    return job_soup

def extract_job_information_indeed(job_soup, desired_characs):
    job_elems = job_soup.find_all('div', class_='jobsearch-ResultsList')

    cols = []
    extracted_info = []


    if 'titles' in desired_characs:
        titles = []
        cols.append('tittles')
        for job_elem in job_elems:
            titles.append(extract_job_title_indeed(job_elem))
        extracted_info.append(titles)

    if 'companies' in desired_characs:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_indeed(job_elem))
        extracted_info.append(companies)

    if 'links' in desired_characs:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_indeed(job_elem))
        extracted_info.append(links)

    if 'date_listed'in desired_characs:
        dates = []
        cols.append('date_listed')
        for job_elem in job_elems:
            dates.append(extract_date_indeed(job_elem))
        extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    num_listings = len(extracted_info[0])

    return jobs_list, num_listings

def extract_job_title_indeed(job_elem):
    title_elem = job_elem.find('h2', class_='jobTitle')
    title = title_elem.text.strip()
    return title

def extract_company_indeed(job_elem):
    company_elem = job_elem.find('span', class_='companyName')
    company = company_elem.text.strip()
    return company

def extract_link_indeed(job_elem):
    link = job_elem.find('a')['heref']
    link = 'www,Indeed.com/' + link
    return link

def extract_date_indeed(job_elem):
    date_elem = job_elem.find('span', class_='date')
    date = date_elem.text.strip()
    return date

### ================ FUNCTIONS FOR ZIPRECRUITER.COM ============= ###