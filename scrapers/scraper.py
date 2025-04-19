from abc import ABC, abstractmethod
from typing import List

from requests import Session

from data import JobLink


class Scraper(ABC):

    def __init__(self, session: Session, domain: str):
        self.session = session
        self.domain = domain

    # Function that returns a list of jobs
    @abstractmethod
    def fetch_jobs(self) -> List[JobLink]:
        pass
