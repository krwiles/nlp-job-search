from bs4 import BeautifulSoup

from data import *
from .link_scraper import LinkScraper


class TalentBrewScraper(LinkScraper):
    """Scraper for sites using Radancy TalentBrew for hosting job listings."""

    search_directory = "/search-jobs/results"

    params = {
        "RecordsPerPage": 3000,  # Arbitrary large number
        "SearchResultsModuleName": "Search Results",  # Tells backend to send results
    }

    def __init__(self, domain: str):
        super().__init__(domain)

    def fetch_jobs(self) -> None:
        """Fetch job listings from a TalentBrew site."""
        self.job_links = []  # Make sure the list is empty so not to duplicate data

        print(f"Fetching jobs from {self.domain}")
        response = self.session.get(
            self.domain + self.search_directory,
            params=self.params
        )
        response.raise_for_status()  # Checks for error codes in response

        data = response.json()  # Backend sends a Json containing HTML
        soup = BeautifulSoup(data["results"], "html.parser")
        jobs = soup.select("li")  # All jobs are in a list

        for job in jobs:
            a_tag = job.find("a", href=True)
            if not a_tag:
                continue

            href = self.domain + a_tag["href"]
            raw_text = job.get_text()

            # Instantiate JobLink with info and append
            self.job_links.append(JobLink(
                url=href,
                raw_text=raw_text
            ))
