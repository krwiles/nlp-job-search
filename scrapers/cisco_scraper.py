import random
import time
from typing import List

from bs4 import BeautifulSoup
from requests import Session

from data import *
from .scraper import Scraper


# Cisco Job Site Scraper
class CiscoJobScraper(Scraper):

    job_num_directory = "https://jobs.cisco.com/jobs/SearchJobsResultsAJAX"

    params = {
        "21178": "%5B169482%5D",  # Filter by US jobs
        "21178_format": "6020",
        "listFilterMode": 1,
        "projectOffset": 0  # For pagination
    }

    pageSize = 25

    def __init__(self, session: Session) -> None:
        domain = "https://jobs.cisco.com/jobs/SearchJobs"
        super().__init__(session, domain)

    # This function uses a URL on Cisco's website that will return the number of jobs with the filer applied
    def fetch_job_count(self) -> int:
        print("Fetching Cisco job count...")
        job_count_response = self.session.get(
            self.job_num_directory,
            params=self.params
        )
        job_count_response.raise_for_status()

        soup = BeautifulSoup(job_count_response.text, "html.parser")
        text = soup.get_text(strip=True)

        # The response should only contain a number
        job_count = 0
        try:
            job_count = int(text)
        except ValueError:
            print(f"CiscoJobScraper Error: {ValueError}")

        print("Cisco job count acquired.")
        return job_count

    def fetch_jobs(self) -> List[JobLink]:
        print(f"Fetching jobs from {self.domain}")
        job_count = self.fetch_job_count()
        jobs_list = []

        # Loop through the pagination on Cisco's site
        for offset in range(0, job_count, self.pageSize):
            print(f"Requesting jobs: offset {offset}")

            # Set params in request
            self.params["projectOffset"] = offset
            response = self.session.get(self.domain, params=self.params)
            response.raise_for_status()  # Checks for error codes in response

            soup = BeautifulSoup(response.text, "html.parser")
            jobs = soup.select("tr")  # All jobs are in table rows

            for job in jobs:
                a_tag = job.find("a", href=True)
                if not a_tag:
                    continue

                href = a_tag["href"]
                raw_text = job.get_text()

                # Instantiate JobLink with info and append
                jobs_list.append(JobLink(
                    url=href,
                    raw_text=raw_text
                ))

            # Add a delay after each page to mimic human behavior
            delay = random.uniform(1, 4)  # Wait between 1 and 4 seconds
            print(f"Sleeping for {delay:.2f} seconds...")
            time.sleep(delay)

        return jobs_list
