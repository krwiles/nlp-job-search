from typing import List

from scrapers import *


def get_all_scrapers() -> List[LinkScraper]:
    return [
        CiscoJobScraper(),
        TalentBrewScraper("https://www.lockheedmartinjobs.com"),
        TalentBrewScraper("https://careers.netapp.com"),
    ]
