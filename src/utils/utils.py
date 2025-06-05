def clean_url(url: str) -> str:
    """Cleans a URL string for file name use."""
    return (url.replace("https://", "")
            .replace("http://", "")
            .replace("/", "_"))
