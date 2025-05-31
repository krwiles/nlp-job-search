import random
import time

from bs4 import BeautifulSoup

from data import *
from .link_scraper import LinkScraper


# Cisco Job Site Scraper
class CiscoJobScraper(LinkScraper):
    """Scraper for Cisco Jobs."""

    job_num_directory = "https://jobs.cisco.com/jobs/SearchJobsResultsAJAX"

    params = {
        "21178": "%5B169482%5D",  # Filter by US jobs
        "21178_format": "6020",
        "listFilterMode": 1,
        "projectOffset": 0  # For pagination
    }

    pageSize = 25

    def __init__(self) -> None:
        domain = "https://jobs.cisco.com/jobs/SearchJobs"
        super().__init__(domain)

    # This function uses a URL on Cisco's website that will return the number of jobs with the filer applied
    def fetch_job_count(self) -> int:
        """
        Fetches the number of job listings at Cisco.

        Utilizes an endpoint on Cisco's site to get the number of job listings with the filters applied.
        """
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

    def fetch_jobs(self) -> None:
        """
        Fetch job links from Cisco's job site.

        Scrapes all job postings from the site looping through pagination using the total number of jobs and page size.
        """
        self.job_links = []  # Make sure the list is empty so not to duplicate data

        print(f"Fetching jobs from {self.domain}")
        job_count = self.fetch_job_count()

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
                self.job_links.append(JobLink(
                    url=href,
                    raw_text=raw_text
                ))

            # Add a delay after each page to mimic human behavior
            delay = random.uniform(1, 4)  # Wait between 1 and 4 seconds
            print(f"Sleeping for {delay:.2f} seconds...")
            time.sleep(delay)
