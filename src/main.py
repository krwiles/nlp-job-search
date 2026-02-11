from .controllers import LinkScraperController, PageScraperController
from .scrapers import get_all_scrapers, PageScraper
from .utils import FileManager


def LinkScraperWorkflow(file_manager, all_scrapers):
    # Instantiate Link Scraper Controller
    link_scraper_controller = LinkScraperController(
        file_manager=file_manager, 
        scraper_list=all_scrapers
    )
    # Run scraper controller
    link_scraper_controller.run_scrapers()
    link_scraper_controller.save_new_job_links()


def PageScraperWorkflow(file_manager, all_scrapers):
    all_domains = [scraper.domain for scraper in all_scrapers]  # Put all domains in a list
    all_page_scrapers = []  # List for page scrapers
    
    # TODO: Add functionality to acquire desired job links for each domain, 
    # currently just taking the most recent 5 for testing.
    for domain in all_domains:
        links = file_manager.load_job_links(domain)  # Load job links for the domain
        pages = links[-5:]  # Most recent 5 for testing

        # Create Page Scraper for the domain and add to list of page scrapers
        all_page_scrapers.append(
            PageScraper(
                file_manager=file_manager, 
                domain=domain, 
                job_links=pages
            )
        )
    
    # Create Page Scraper Controller
    page_scraper_controller = PageScraperController(
        file_manager=file_manager, 
        scraper_list=all_page_scrapers
    )
    
    # Run scraper controller
    page_scraper_controller.run_scrapers()
    page_scraper_controller.save_job_pages()


if __name__ == "__main__":
    file_manager = FileManager()  # Instantiate file manager for handling all file operations
    all_scrapers = get_all_scrapers()  # Instantiate all link scrapers
    
    LinkScraperWorkflow(file_manager, all_scrapers)
    PageScraperWorkflow(file_manager, all_scrapers)
    