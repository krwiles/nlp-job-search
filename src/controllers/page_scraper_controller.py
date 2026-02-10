import threading
from typing import List

from src.scrapers import PageScraper
from src.utils import FileManager


class PageScraperController:
    """
    A class for managing and running all page scrapers.

    Attributes:
        scraper_list (List[PageScraper]): The list containing references to all instanced scrapers.
        file_manager (FileManager): An instance of the FileManager class for handling all file operations.
    """
    def __init__(self, file_manager: FileManager, scraper_list: List[PageScraper] = None) -> None:
        self.file_manager = file_manager
        self.scraper_list = scraper_list or []


    def add_scraper(self, scraper: PageScraper) -> None:
        self.scraper_list.append(scraper)


    def set_scraper_list(self, scraper_list: List[PageScraper]) -> None:
        self.scraper_list = scraper_list


    def run_scrapers(self) -> None:
        """Runs fetch_pages() for each scraper concurrently using threads."""
        threads = []

        # Create and start a thread for each scraper
        for scraper in self.scraper_list:
            thread = threading.Thread(target=scraper.fetch_pages)
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()


    def save_job_pages(self) -> None:
        """Saves new web pages scraped from each scraper to HTML files and updates the index."""
        for scraper in self.scraper_list:
            # Save all html files from the scraper
            self.file_manager.save_job_pages(scraper.domain, scraper.job_pages)
            
            # Save the page entries to the index
            entries = [entry for (entry, html) in scraper.job_pages]
            self.file_manager.save_index(scraper.domain, entries)

