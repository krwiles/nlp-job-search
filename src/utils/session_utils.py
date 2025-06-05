import threading
import time
import random

import requests

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def create_session() -> requests.Session:
    """Returns a requests session with default headers configured."""
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    return session


def random_delay() -> None:
    """Creates a random delay for the current thread."""
    delay = random.uniform(1, 4)  # Wait between 1 and 4 seconds
    name = threading.current_thread().name
    print(f"{name} sleeping for {delay:.2f} seconds...")
    time.sleep(delay)
