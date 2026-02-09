from pathlib import Path


class FileManager:
    
    def __init__(self) -> None:
        pass
        
    def clean_url(self, url: str) -> str:
        """Cleans a URL string for file name use."""
        return (url.replace("https://", "")
                .replace("http://", "")
                .replace("/", "_"))
