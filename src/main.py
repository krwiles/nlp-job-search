import json

from .controllers import LinkScraperController, PageScraperController
from .data import JobLink
from .scrapers import get_all_scrapers, PageScraper
from .utils import FileManager


if __name__ == "__main__":
    file_manager = FileManager()  # Create file manager instance
    
    all_scrapers = get_all_scrapers()  # Instantiate all link scrapers

    # Create Link Scraper Controller
    link_scraper_controller = LinkScraperController(
        file_manager=file_manager, 
        scraper_list=all_scrapers
    )

    link_scraper_controller.run_scrapers()  # Fetch all job links
    link_scraper_controller.save_new_job_links()  # Save all job links

    ########################################################

    all_domains = [scraper.domain for scraper in all_scrapers]  # Put all domains in a list
    all_page_scrapers = []  # List for page scrapers
    
    # Create all page scrapers
    for domain in all_domains:
        file_path = link_scraper_controller.output_dir / f"{file_manager.clean_url(domain)}.json"
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        pages = [JobLink(job["url"], job["raw_text"]) for job in data[-5:]]  # Most recent 5 for testing

        all_page_scrapers.append(
            PageScraper(
                file_manager=file_manager, 
                domain=domain, 
                job_links=pages
            )
        )

    page_scraper_controller = PageScraperController(all_page_scrapers)  # Create Page Scraper Controller
    page_scraper_controller.run_scrapers()  # Fetch all pages
    page_scraper_controller.save_job_pages()  # Save all pages
