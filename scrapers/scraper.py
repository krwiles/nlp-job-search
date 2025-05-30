from abc import ABC, abstractmethod
from typing import List

import requests

from data import JobLink


class Scraper(ABC):
    """
    Abstract base class for website job scrapers.

    This class defines the interface and shared functionality for all scrapers.
    Subclasses must implement the fetch_jobs() method to extract job links from
    their respective websites in a thread safe manner.

    Attributes:
        domain (str): The base domain of the website being scraped.
        job_links (List[JobLink]): A list of scraped job links.
        session (requests.Session): A configured session with default headers.
    """

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

    def __init__(self, domain: str):
        """
        Initialize a scraper with the target domain.

        Args:
            domain (str): The base domain of the website to scrape.
        """
        self.job_links: List[JobLink] = []

        self.domain = domain
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    @abstractmethod
    def fetch_jobs(self) -> None:
        """
        Scrape job listings from the website.

        Subclasses must implement this method to populate self.job_links.
        """
        pass
