from dataclasses import asdict
import json
from pathlib import Path
from typing import List, Tuple

from src.data import JobPageEntry, JobLink

class FileManager:
    def __init__(self) -> None:
        # Find or create output directory
        project_root = Path(__file__).resolve().parent.parent.parent
        self.output_dir_pages = project_root / "scraped_data" / "job_pages"
        self.output_dir_pages.mkdir(parents=True, exist_ok=True)
        self.output_dir_links = project_root / "scraped_data" / "job_links"
        self.output_dir_links.mkdir(parents=True, exist_ok=True)
    
    
    def clean_url(self, url: str) -> str:
        """Cleans a URL string for file name use."""
        return (url.replace("https://", "")
                .replace("http://", "")
                .replace("/", "_"))
    
    
    def load_index(self, domain: str) -> List[JobPageEntry]:
        """Returns a list of page entries from the index for a given domain."""
        index = self.output_dir_pages / self.clean_url(domain) / "index.json"
        index_page_entries = []
        
        if index.exists():
            try:
                with open(index, "r") as f:
                    data = json.load(f)
                    index_page_entries = [JobPageEntry(**entry) for entry in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Could not load index for {domain}: {e}")
        
        return index_page_entries
    
    
    def save_index(self, domain: str, entries: List[JobPageEntry]) -> None:
        """Saves a list of page entries to the index for a given domain."""
        index = self.output_dir_pages / self.clean_url(domain) / "index.json"
        
        all_entries = [asdict(entry) for entry in self.load_index(domain)] + [asdict(entry) for entry in entries]
        try:
            with open(index, "w", encoding="utf-8") as f:
                json.dump(all_entries, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save index for {domain}: {e}")
    
    
    def save_job_pages(self, domain: str, job_pages: List[Tuple[JobPageEntry, str]]) -> None:
        """Saves the job pages to HTML files for a given domain"""
        domain_dir = self.output_dir_pages / self.clean_url(domain)
        domain_dir.mkdir(parents=True, exist_ok=True)

        for (entry, html) in job_pages:
            file_path = domain_dir / entry.file_name
            try:
                file_path.write_text(html, encoding="utf-8")
            except Exception as e:
                print(f"Failed to save {entry}: {e}")
    
    
    def load_job_links(self, domain: str) -> List[JobLink]:
        """Loads the job links for a given domain from the output directory."""
        file_path = self.output_dir_links / f"{self.clean_url(domain)}.json"
        job_links = []
        
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    job_links = [JobLink(**job) for job in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Could not load job links for {domain}: {e}")
        
        return job_links
    
    def save_job_links(self, domain: str, job_links: List[JobLink]) -> None:
        """Saves the job links for a given domain to the output directory."""
        file_path = self.output_dir_links / f"{self.clean_url(domain)}.json"
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([asdict(job) for job in job_links], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save job links for {domain}: {e}")