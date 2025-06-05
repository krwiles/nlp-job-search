import json
import threading
from dataclasses import asdict
from typing import List

from src.scrapers import PageScraper


class PageScraperController:
    """
    A class for managing and running all page scrapers.

    Attributes:
        scraper_list (List[PageScraper]): The list containing references to all instanced scrapers.
    """
    def __init__(self, scraper_list: List[PageScraper] = None) -> None:
        self.scraper_list = scraper_list or []

    def add_scraper(self, scraper: PageScraper) -> None:
        """Add a scraper to the self.scraper_list"""
        self.scraper_list.append(scraper)

    def set_scraper_list(self, scraper_list: List[PageScraper]) -> None:
        """Replace the entire self.scraper_list"""
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
            new_entries = []
            for (entry, html) in scraper.job_pages:
                new_entries.append(entry)

                file_path = scraper.output_dir / entry.file_name
                try:
                    file_path.write_text(html, encoding="utf-8")
                except Exception as e:
                    print(f"Failed to save {entry}: {e}")

            # Update index
            all_entries = scraper.index_page_entries + [asdict(n) for n in new_entries]
            index = scraper.output_dir / "index.json"
            try:
                with index.open("w", encoding="utf-8") as f:
                    json.dump(all_entries, f, indent=2, ensure_ascii=False)
                print(f"Saved {len(new_entries)} new pages to {scraper.output_dir}")
            except Exception as e:
                print(f"Failed to save index for {scraper.domain}: {e}")
