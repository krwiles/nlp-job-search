from controllers import ScraperController
from scrapers import get_all_scrapers

if __name__ == "__main__":

    scraper_controller = ScraperController(get_all_scrapers())

    scraper_controller.run_scrapers()
    scraper_controller.save_new_job_links()
