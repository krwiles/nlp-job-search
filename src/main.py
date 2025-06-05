import json

from controllers import LinkScraperController
from controllers.page_scraper_controller import PageScraperController
from src.data import JobLink
from src.scrapers import get_all_scrapers, PageScraper
from src.utils import clean_url

if __name__ == "__main__":

    all_scrapers = get_all_scrapers()  # Instantiate all link scrapers

    link_scraper_controller = LinkScraperController(all_scrapers)  # Create Link Scraper Controller

    link_scraper_controller.run_scrapers()  # Fetch all job links
    link_scraper_controller.save_new_job_links()  # Save all job links

    ########################################################

    all_domains = [scraper.domain for scraper in all_scrapers]  # Put all domains in a list
    all_page_scrapers = []  # List for page scrapers
    # Create all page scrapers
    for domain in all_domains:
        file_path = link_scraper_controller.output_dir / f"{clean_url(domain)}.json"
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # TODO: make job_link and job_page_entry have an optional date in the constructor
        pages = [JobLink(obj["url"], obj["raw_text"]) for obj in data[-5:]]  # Most recent 5 for testing

        all_page_scrapers.append(PageScraper(domain, pages))

    page_scraper_controller = PageScraperController(all_page_scrapers)  # Create Page Scraper Controller

    page_scraper_controller.run_scrapers()  # Fetch all pages
    page_scraper_controller.save_job_pages()  # Save all pages
