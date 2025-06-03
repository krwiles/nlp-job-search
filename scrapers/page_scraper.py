import json
from pathlib import Path
from typing import List

from data import JobLink, JobPageEntry
from utils import create_session, random_delay, clean_url


class PageScraper:
    """
    Class for scraping HTML from a list of web pages on a single website.

    This class handles scraping multiple pages and tracking which ones have already been scraped
    using an index.

    Attributes:
        domain (str): The base domain of the website being scraped.
        job_links (List[JobLink]): A list of pages to be scraped.
        job_pages (List[Tuple[JobPageEntry, str]]): The scraped job pages as tuples of
            JobPageEntry and raw HTML content.
        output_dir (Path): The output directory where results are saved.
        index_page_entries (List[JobPageEntry]): Entries already present in the index.
        index_urls (Set[str]): The set of URLs already indexed.
        session (requests.Session): A configured session with default headers.
    """
    def __init__(self, domain: str, job_links: List[JobLink]) -> None:
        self.domain = domain
        self.job_links: List[JobLink] = job_links  # Links to check
        self.job_pages: List[(JobPageEntry, str)] = []  # List to store fetched web pages

        # Find or create output directory
        base_dir = Path(__file__).resolve().parent
        self.output_dir = base_dir / ".." / "resources" / "job_pages" / clean_url(self.domain)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load index file if it exists
        # This file keeps track of the pages that are already saved
        self.index_page_entries = []
        self.index_urls = set()
        self.refresh_index()

        self.session = create_session()

    def refresh_index(self) -> None:
        """Refreshes the instance variables with the latest information from the index."""
        index = self.output_dir / "index.json"
        if index.exists():
            try:
                with open(index, "r") as f:
                    self.index_page_entries = json.load(f)
                    self.index_urls = {page["url"] for page in self.index_page_entries}
            except Exception as e:
                print(f"Could not load index for {self.domain}: {e}")

    def fetch_pages(self) -> None:
        """
        Fetch the html from each job link.

        This method checks the index for each job link, then requests any page that hasn't already been saved.
        """
        self.job_pages: List[(JobPageEntry, str)] = []  # Make sure the list is empty so not to duplicate data

        for link in self.job_links:
            if link.url in self.index_urls:
                continue

            # Get the page HTML
            print(f"Fetching web page from {link.url}")
            response = self.session.get(link.url)
            response.raise_for_status()  # Checks for error codes in response

            file_name = f"{clean_url(link.url)}.html"

            # Store the page entry and raw html
            self.job_pages.append(
                (
                    JobPageEntry(url=link.url, file_name=file_name),
                    response.text,
                )
            )

            # Add a delay after each page to mimic human behavior
            random_delay()
