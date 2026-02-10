from abc import ABC, abstractmethod
from typing import List

from src.data import JobLink
from src.utils import SessionUtils


class LinkScraper(ABC):
    """
    Abstract base class for website job scrapers.

    This class defines the interface and shared functionality for all scrapers.
    Subclasses must implement the fetch_jobs() method to extract job links from
    their respective websites in a thread safe manner.

    Attributes:
        domain (str): The base domain of the website being scraped.
        job_links (List[JobLink]): A list of scraped job links.
        session_utils (SessionUtils): A configured session utility instance.
    """
    def __init__(self, domain: str):
        self.domain = domain
        self.session_utils = SessionUtils()
        self.job_links: List[JobLink] = []


    @abstractmethod
    def fetch_jobs(self) -> None:
        """
        Scrape job listings from the website.

        Subclasses must implement this method to populate self.job_links.
        """
        pass
