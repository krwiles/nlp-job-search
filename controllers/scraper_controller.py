import json
import os
import threading
from dataclasses import asdict

from data import JobLink
from scrapers import *
from typing import List


class ScraperController:
    def __init__(self, scraper_list: List[Scraper] = None) -> None:
        self.scraper_list = scraper_list or []

    def add_scraper(self, scraper: Scraper) -> None:
        self.scraper_list.append(scraper)

    def set_scraper_list(self, scraper_list: List[Scraper]) -> None:
        self.scraper_list = scraper_list

    # Runs fetch_jobs() for each scraper using threads.
    def run_scrapers(self) -> None:
        threads = []

        for scraper in self.scraper_list:
            thread = threading.Thread(target=scraper.fetch_jobs)
            threads.append(thread)
            thread.start()

        # Waits for all threads to finish
        for thread in threads:
            thread.join()

    def save_new_job_links(self) -> None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, "..", "resources", "job_links")
        os.makedirs(output_dir, exist_ok=True)

        for scraper in self.scraper_list:
            all_new_jobs: List[JobLink] = scraper.job_links

            # Clean domain for file name
            domain_clean = scraper.domain.replace("https://", "").replace("http://", "").replace("/", "_")
            filename = f"{domain_clean}.json"
            filepath = os.path.join(output_dir, filename)

            # Load existing jobs from file if it exists
            existing_jobs = []
            existing_urls = set()

            if os.path.exists(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        existing_jobs = json.load(f)
                        existing_urls = {job["url"] for job in existing_jobs}
                except Exception as e:
                    print(f"Could not load existing data for {scraper.domain}: {e}")

            # Filter new jobs that don't already exist
            new_jobs = [job for job in all_new_jobs if job.url not in existing_urls]

            if not new_jobs:
                print(f"No new jobs found for {scraper.domain}.")
                continue

            # Add new jobs to existing
            all_jobs_to_save = existing_jobs + [asdict(job) for job in new_jobs]

            # Save updated list
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(all_jobs_to_save, f, indent=2, ensure_ascii=False)
                print(f"Saved {len(new_jobs)} new jobs to {filepath}")
            except Exception as e:
                print(f"Failed to save new jobs for {scraper.domain}: {e}")
