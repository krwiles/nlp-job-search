import json
import threading
from dataclasses import asdict
from pathlib import Path
from typing import List

from data import JobLink
from scrapers import *


class ScraperController:
    """
    A class for managing and running all website scrapers.

    Attributes:
        scraper_list (list): The list containing references to all instanced scrapers.
    """
    def __init__(self, scraper_list: List[LinkScraper] = None) -> None:
        self.scraper_list = scraper_list or []

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
        base_dir = Path(__file__).resolve().parent
        output_dir = base_dir / ".." / "resources" / "job_links"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save job_links for each scraper
        for scraper in self.scraper_list:
            all_new_jobs = scraper.job_links

            # Clean domain for file name
            domain_clean = (scraper.domain
                            .replace("https://", "")
                            .replace("http://", "")
                            .replace("/", "_"))
            file_name = f"{domain_clean}.json"
            file_path = output_dir / file_name

            # Load existing jobs from file if it exists
            existing_jobs = []
            existing_urls = set()
            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        existing_jobs = json.load(f)
                        existing_urls = {job["url"] for job in existing_jobs}
                except Exception as e:
                    print(f"Could not load existing data for {scraper.domain}: {e}")

            # Filter new jobs that don't already exist
            new_jobs = [job for job in all_new_jobs if job.url not in existing_urls]

            # End loop if there are no new job_links to save
            if not new_jobs:
                print(f"No new jobs found for {scraper.domain}.")
                continue

            # Add new jobs to existing
            all_jobs_to_save = existing_jobs + [asdict(job) for job in new_jobs]

            # Save updated list
            try:
                with file_path.open("w", encoding="utf-8") as f:
                    json.dump(all_jobs_to_save, f, indent=2, ensure_ascii=False)
                print(f"Saved {len(new_jobs)} new jobs to {file_path}")
            except Exception as e:
                print(f"Failed to save new jobs for {scraper.domain}: {e}")
