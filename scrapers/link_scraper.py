from abc import ABC, abstractmethod
from typing import List

import requests

from data import JobLink
from utils import create_session


class LinkScraper(ABC):
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
    def __init__(self, domain: str):
        """
        Initialize a scraper with the target domain.

        Args:
            domain (str): The base domain of the website to scrape.
        """
        self.domain = domain
        self.session = create_session()
        self.job_links: List[JobLink] = []

    @abstractmethod
    def fetch_jobs(self) -> None:
        """
        Scrape job listings from the website.

        Subclasses must implement this method to populate self.job_links.
        """
        pass
