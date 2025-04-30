import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import openai

# Load API key
api_key = 'REDACTED'  # Replace with your OpenAI API key

# Configure OpenAI
openai.api_key = api_key
MODEL = "gpt-4o"  # Latest available model

# Fake browser header
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Class to handle webpage scraping
class Website:
    def __init__(self, url: str):
        self.url = url
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ConnectionError(f"Error fetching the URL: {e}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No Title"
        
        if soup.body:
            for tag in soup.body(["script", "style", "img", "input"]):
                tag.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""
        
        self.links = [a.get("href") for a in soup.find_all("a", href=True)]

    def get_contents(self) -> str:
        return f"Title: {self.title}\n\nText:\n{self.text}"

# --- SYSTEM PROMPT TO SET ROLE ---
recruiter_system_prompt = (
    "You are a helpful job recruiter AI. "
    "You analyze job listings and compare them to a candidate's resume. "
    "Your goal is to evaluate how well the candidate matches the job, and summarize this match in an honest and concise way. "
    "Be clear about strengths and gaps. Provide your response in Markdown format."
)

# --- USER PROMPT: WEBSITE + RESUME INPUT ---
def recruiter_user_prompt(website: Website, resume: str) -> str:
    return (
        f"I want you to analyze a job listing from the following webpage:\n\n{website.get_contents()}\n\n"
        f"My resume summary is as follows:\n\n{resume}\n\n"
        "Please compare the job description with my resume. Let me know how well I match the role, and highlight key areas where I am strong or lacking."
    )

# --- RUN THE OPENAI CALL ---
def evaluate_job_fit(job_url: str, resume: str):
    website = Website(job_url)
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": recruiter_system_prompt},
                {"role": "user", "content": recruiter_user_prompt(website, resume)}
            ]
        )
        result = response.choices[0].message["content"]
        #display(Markdown(result))
        print(result)
        return result
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

# === USAGE ===
if __name__ == "__main__":
    job_url = "https://careers.netapp.com/job/united-states/commerce-data-analyst/27600/78602584144"
    sample_resume = """
    Data Analyst with 3+ years experience in SQL, Tableau, and Python. 
    Specialized in eCommerce analytics and customer behavior insights. 
    Familiar with Snowflake, PowerBI, and A/B testing frameworks. 
    Strong communication skills and background in business intelligence.
    """
    evaluate_job_fit(job_url, sample_resume)
