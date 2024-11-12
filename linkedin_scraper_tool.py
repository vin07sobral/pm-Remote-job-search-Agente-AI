from crewai_tools import tool
import requests
from bs4 import BeautifulSoup

@tool
def linkedin_scraper_tool(search_query: str, location: str = "remote", num_results: int = 10) -> str:
    """
    Scrapes LinkedIn for job listings based on the search query and location.
    
    Parameters:
    - search_query: The job title or keywords to search (e.g., 'Product Manager')
    - location: Job location (e.g., 'remote')
    - num_results: Number of job listings to retrieve

    Returns:
    - A table formatted string with job title, company, location, and job URL.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location={location}&trk=homepage-jobseeker_jobs-search-bar_search-submit&f_TPR=r86400&position=1&pageNum=0"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []

    # Scrape job elements
    job_elements = soup.select('.jobs-search__results-list li')
    for job_element in job_elements[:num_results]:
        title = job_element.select_one('.base-search-card__title').text.strip()
        company = job_element.select_one('.base-search-card__subtitle').text.strip()
        loc = job_element.select_one('.job-search-card__location').text.strip()
        link = job_element.select_one('.base-card__full-link')['href']
        jobs.append([title, company, loc, link])

    # Format as a table
    table = "| Job Title | Company | Location | Job URL |\n|---|---|---|---|\n"
    for job in jobs:
        table += f"| {job[0]} | {job[1]} | {job[2]} | [Link]({job[3]}) |\n"

    return table
