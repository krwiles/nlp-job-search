from controllers import ScraperController
from scrapers import get_all_scrapers

if __name__ == "__main__":

    scraper_list = get_all_scrapers()
    scraper_controller = ScraperController(scraper_list)

    scraper_controller.run_scrapers()
    scraper_controller.save_new_job_links()
