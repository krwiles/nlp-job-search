import threading
from dataclasses import asdict
from pathlib import Path
from typing import List

from src.data import JobLink
from src.scrapers import LinkScraper
from src.utils import FileManager


class LinkScraperController:
    """
    A class for managing and running all link scrapers.

    Attributes:
        scraper_list (List[LinkScraper]): The list containing references to all instanced scrapers.
        output_dir (Path): The output directory where job links are stored
    """
    def __init__(self, file_manager: FileManager, scraper_list: List[LinkScraper] = None) -> None:
        self.file_manager = file_manager
        self.scraper_list = scraper_list or []

        project_root = Path(__file__).resolve().parent.parent.parent
        self.output_dir = project_root / "scraped_data" / "job_links"
        self.output_dir.mkdir(parents=True, exist_ok=True)


    def add_scraper(self, scraper: LinkScraper) -> None:
        self.scraper_list.append(scraper)


    def set_scraper_list(self, scraper_list: List[LinkScraper]) -> None:
        self.scraper_list = scraper_list


    def run_scrapers(self) -> None:
        """Runs fetch_jobs() for each scraper concurrently using threads."""
        threads = []

        # Create and start a thread for each scraper
        for scraper in self.scraper_list:
            thread = threading.Thread(target=scraper.fetch_jobs)
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()


    def save_new_job_links(self) -> None:
        """Saves new JobLinks scraped from each scaper to individual JSON files."""
        # Save job_links for each scraper
        for scraper in self.scraper_list:
            # Load existing jobs from file if it exists
            existing_jobs = self.file_manager.load_job_links(scraper.domain)
            existing_urls = set(job.url for job in existing_jobs)

            # Filter new jobs that don't already exist
            new_jobs = [job for job in scraper.job_links if job.url not in existing_urls]

            # End loop if there are no new job_links to save
            if not new_jobs:
                print(f"No new jobs found for {scraper.domain}.")
                continue

            # Add new jobs to existing
            all_jobs_to_save = existing_jobs + new_jobs
            self.file_manager.save_job_links(scraper.domain, all_jobs_to_save)
            
            print(f"Saved {len(new_jobs)} new job links for {scraper.domain}. Total saved: {len(all_jobs_to_save)}.")
