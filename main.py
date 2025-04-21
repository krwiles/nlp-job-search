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

    list1 = scraper2.fetch_jobs()
    list2 = scraper3.fetch_jobs()
    list3 = scraper1.fetch_jobs()

    for job in list1:
        print(job)

    for job in list2:
        print(job)

    for job in list3:
        print(job)
