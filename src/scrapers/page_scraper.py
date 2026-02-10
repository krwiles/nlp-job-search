import json
from pathlib import Path
from typing import List

from src.data import JobLink, JobPageEntry
from src.utils import FileManager
from src.utils import SessionUtils


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
        file_manager (FileManager): A file manager instance used for file operations
            such as cleaning filenames and handling output paths.
        index_page_entries (List[JobPageEntry]): Entries already present in the index.
        index_urls (Set[str]): The set of URLs already indexed.
        session_utils (SessionUtils): A configured session utility instance.
    """

    def __init__(self, domain: str, file_manager: FileManager, job_links: List[JobLink]) -> None:
        self.file_manager = file_manager
        self.domain = domain
        self.job_links: List[JobLink] = job_links  # Links to check
        self.job_pages: List[(JobPageEntry, str)] = []  # List to store fetched web pages

        self.index_page_entries = self.file_manager.load_index(self.domain)
        self.index_urls = set(entry.url for entry in self.index_page_entries)

        self.session_utils = SessionUtils()

    def fetch_pages(self) -> None:
        """
        Fetch the html from each job link.

        This method checks the index for each job link, then requests any page that hasn't already been saved.
        """
        self.job_pages: List[(JobPageEntry, str)] = []  # Make sure the list is empty so not to duplicate data

        for link in self.job_links:
            if link.url in self.index_urls:
                print(f"Skipping {link.url} - already in index")
                continue

            # Get the page HTML
            print(f"Fetching web page from {link.url}")
            response = self.session_utils.session.get(link.url)
            response.raise_for_status()  # Checks for error codes in response

            file_name = f"{self.file_manager.clean_url(link.url)}.html"

            # Store the page entry and raw html
            self.job_pages.append(
                (
                    JobPageEntry(url=link.url, file_name=file_name),
                    response.text,
                )
            )

            # Add a delay after each page to mimic human behavior
            self.session_utils.random_delay()
