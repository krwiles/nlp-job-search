import requests
from scrapers import *
import json
from dataclasses import asdict

if __name__ == "__main__":

    domain1 = "https://www.lockheedmartinjobs.com"
    domain2 = "https://careers.netapp.com"

    scraper1 = CiscoJobScraper()
    scraper2 = TalentBrewScraper(domain1)
    scraper3 = TalentBrewScraper(domain2)

    scraper2.fetch_jobs()
    scraper3.fetch_jobs()
    scraper1.fetch_jobs()

    for job in scraper1.job_links:
        print(job)

    for job in scraper2.job_links:
        print(job)

    for job in scraper3.job_links:
        print(job)
