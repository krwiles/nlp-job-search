import os
import logging
import requests
from bs4 import BeautifulSoup
import openai

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set")

# Configure OpenAI
openai.api_key = api_key
DEFAULT_MODEL = "gpt-4o"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
REQUEST_HEADERS = {"User-Agent": USER_AGENT}
REQUEST_TIMEOUT = 10


class WebsiteFetcher:
    """
    Handles fetching HTML content from a URL.
    """
    @staticmethod
    def fetch(url: str) -> str:
        try:
            response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            logger.info(f"Successfully fetched URL: {url}")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching the URL: {e}")
            raise ConnectionError(f"Error fetching the URL: {e}")


class WebsiteParser:
    """
    Parses HTML content to extract the title, text, and links.
    """
    def __init__(self, html_content: str):
        soup = BeautifulSoup(html_content, 'html.parser')
        self.title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"

        if soup.body:
            for tag in soup.body(["script", "style", "img", "input"]):
                tag.decompose()
            raw_text = soup.body.get_text(separator="\n", strip=True)
            self.text = self._clean_text(raw_text)
        else:
            self.text = ""

        self.links = [a.get("href") for a in soup.find_all("a", href=True)]

    def _clean_text(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    def get_contents(self) -> str:
        return f"Title: {self.title}\n\nText:\n{self.text}"


# System prompt for recruiter
RECRUITER_SYSTEM_PROMPT = (
    "You are a highly skilled job recruiter AI. "
    "Your task is to analyze a job listing and compare it to a candidate's resume. "
    "Identify the skills and qualifications that match between the job description and the resume, "
    "and highlight areas where the candidate's resume is lacking. "
    "Provide a detailed analysis of the strengths and gaps in the candidate's qualifications. "
    "Additionally, calculate and provide a confidence percentage (from 0 to 100) indicating how well the candidate matches the job requirements. "
    "Be honest, concise, and provide your response in Markdown format."
)

def recruiter_user_prompt(website_parser: WebsiteParser, resume: str) -> str:
    return (
        f"Analyze the following job listing and compare it to the provided resume:\n\n"
        f"Job Listing:\n{website_parser.get_contents()}\n\n"
        f"Resume:\n{resume}\n\n"
        "Your task is to identify the skills and qualifications that match between the job description and the resume. "
        "Highlight areas where the resume is lacking compared to the job requirements. "
        "Provide a detailed analysis of the strengths and gaps in the candidate's qualifications. "
        "Finally, calculate and provide a confidence percentage (from 0 to 100) indicating how well the candidate matches the job requirements. "
        "Be clear, concise, and format your response in Markdown."
    )

def evaluate_job_fit(job_url: str, resume: str, model: str = DEFAULT_MODEL):
    try:
        html_content = WebsiteFetcher.fetch(job_url)
        website_parser = WebsiteParser(html_content)
        prompt = recruiter_user_prompt(website_parser, resume)

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": RECRUITER_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message["content"]
        logger.info("OpenAI API call successful")
        print(result)
        return result
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    return None


if __name__ == "__main__":
    job_url = "https://careers.netapp.com/job/united-states/commerce-data-analyst/27600/78602584144"
    
    # Read resume from a text file
    resume_file_path = "krw-resume.txt"  # Ensure this file exists in the same directory or provide the full path
    try:
        with open(resume_file_path, "r", encoding="utf-8") as file:
            sample_resume = file.read().strip()
    except FileNotFoundError:
        logger.error(f"Resume file not found: {resume_file_path}")
        sample_resume = ""
    except Exception as e:
        logger.error(f"Error reading resume file: {e}")
        sample_resume = ""

    if sample_resume:
        evaluate_job_fit(job_url, sample_resume)
    else:
        logger.error("No resume content available to evaluate.")

