from typing import List

from bs4 import BeautifulSoup
from requests import Session

from data import *
from .scraper import Scraper


# Radancy TalentBrew Scraper
class TalentBrewScraper(Scraper):

    search_directory = "/search-jobs/results"

    params = {
        "RecordsPerPage": 3000,
        "SearchResultsModuleName": "Search Results",  # Tells backend to send results
    }

    def __init__(self, session: Session, domain: str):
        super().__init__(session, domain)

    def fetch_jobs(self) -> List[JobLink]:
        print(f"Fetching jobs from {self.domain}")
        response = self.session.get(
            self.domain + self.search_directory,
            params=self.params
        )
        response.raise_for_status()  # Checks for error codes in response

        data = response.json()  # Backend sends a Json containing HTML
        soup = BeautifulSoup(data["results"], "html.parser")
        jobs = soup.select("li")  # All jobs are in a list

        jobs_list = []
        for job in jobs:
            a_tag = job.find("a", href=True)
            if not a_tag:
                continue

            href = self.domain + a_tag["href"]
            raw_text = job.get_text()

            # Instantiate JobLink with info and append
            jobs_list.append(JobLink(
                url=href,
                raw_text=raw_text
            ))

        return jobs_list
