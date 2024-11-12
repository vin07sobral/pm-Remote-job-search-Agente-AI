import os
from crewai import Agent, Task, Crew, Process
from tools.linkedin_scraper_tool import linkedin_scraper_tool
import requests

# Setting up environment variables if needed
def query_lm_studio(prompt: str) -> str:
    url = "http://127.0.0.1:1234/v1/models/"  # Change to LM Studio's actual API endpoint
    payload = {
        "prompt": prompt,
        "max_tokens": LM_STUDIO_MAX_TOKENS,  # Adjust based on your needs
        "temperature": LM_STUDIO_TEMPERATURE  # Adjust model parameters as needed
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# Step 2.1: Define the Research Agent
job_researcher = Agent(
    role="Remote Job Researcher",
    goal="Identify remote Product Management positions from LinkedIn.",
    backstory=(
        "You are an expert in finding and identifying remote job opportunities."
        " You navigate LinkedIn to locate suitable positions and compile them in an easily readable format."
    ),
    tools=[linkedin_scraper_tool],
    language_model=query_lm_studio  # Use the LM Studio query function as the language model
)

# Step 2.2: Define the Job Search Task
job_search_task = Task(
    description=(
        "Search for remote Product Management job listings on LinkedIn. Gather the job title, company name, "
        "location, and a link to the listing. Format the results in a table to provide a clear overview."
    ),
    expected_output="A table containing Job Title, Company, Location, and Job URL.",
    agent=job_researcher,
)

# Step 2.3: Create the Crew with the Researcher and Task
remote_job_research_crew = Crew(
    agents=[job_researcher],
    tasks=[job_search_task],
    process=Process.sequential
)

# Step 3: Run the Crew
result = remote_job_research_crew.kickoff(inputs={'search_query': 'Product Manager', 'location': 'remote'})
print(result)
