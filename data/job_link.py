import datetime
from dataclasses import dataclass, field


@dataclass
class JobLink:
    url: str
    raw_text: str
    # "field" ensures that the timestamp is computed each time an instance of JobLink is created, not globally
    date_scraped: datetime.datetime = field(default_factory=datetime.datetime.now, init=False)

    def __str__(self) -> str:
        date_str = self.date_scraped.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"URL: {self.url}\n"
            f"Raw Text: {self.raw_text or 'N/A'}\n"
            f"Date Scraped: {date_str}"
        )