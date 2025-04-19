import requests
from scrapers import *
import json
from dataclasses import asdict

if __name__ == "__main__":
    
    domain1 = "https://www.lockheedmartinjobs.com"
    domain2 = "https://careers.netapp.com"

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    scraper1 = CiscoJobScraper(session)
    scraper2 = TalentBrewScraper(session, domain1)
    scraper3 = TalentBrewScraper(session, domain2)

    list1 = scraper2.fetch_jobs()
    list2 = scraper3.fetch_jobs()
    list3 = scraper1.fetch_jobs()

    for job in list1:
        print(job)

    for job in list2:
        print(job)

    for job in list3:
        print(job)

    jobs_list = list1 + list2 + list3

    def job_to_dict(job):
        data = asdict(job)
        # Convert datetime to string
        data['date_recorded'] = job.date_scraped.strftime("%Y-%m-%d %H:%M:%S")
        return data

    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump([job_to_dict(job) for job in jobs_list], f, indent=4)