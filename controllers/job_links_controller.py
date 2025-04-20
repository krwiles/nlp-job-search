from data import job_link
from scrapers import *
from typing import List


class JobLinksController:

    scraper_list = []

    def __init__(self) -> None:
        super().__init__()

    def add_scraper(self, scraper: Scraper) -> None:
        pass

    def set_scraper_list(self, scraper_list: List[Scraper]) -> None:
        pass

    def run_scrapers(self) -> None:
        pass

    def update_json(self) -> None:
        pass

    def fetch_new_jobs(self) -> List[List[job_link]]:
        pass
