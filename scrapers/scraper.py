from abc import ABC, abstractmethod
from typing import List

import requests

from data import JobLink


class Scraper(ABC):

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
        self.job_links: List[JobLink] = []

        self.domain = domain
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    # Function that scrapes job links and stores them in self.job_links
    @abstractmethod
    def fetch_jobs(self) -> None:
        pass
