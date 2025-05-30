from controllers import ScraperController
from scrapers import *

if __name__ == "__main__":

    domain1 = "https://www.lockheedmartinjobs.com"
    domain2 = "https://careers.netapp.com"

    scraper1 = CiscoJobScraper()
    scraper2 = TalentBrewScraper(domain1)
    scraper3 = TalentBrewScraper(domain2)

    scraper_controller = ScraperController()

    scraper_controller.add_scraper(scraper1)
    scraper_controller.add_scraper(scraper2)
    scraper_controller.add_scraper(scraper3)

    scraper_controller.run_scrapers()

    scraper_controller.save_new_job_links()
