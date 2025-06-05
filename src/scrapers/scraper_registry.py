from typing import List

from src.scrapers.link_scrapers import *
from src.scrapers import LinkScraper


def get_all_scrapers() -> List[LinkScraper]:
    return [
        CiscoJobScraper(),
        TalentBrewScraper("https://www.lockheedmartinjobs.com"),
        TalentBrewScraper("https://careers.netapp.com"),
    ]
