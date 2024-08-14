from dotenv import load_dotenv
load_dotenv()

from crewai import Crew, Process
# from decouple import config

from textwrap import dedent

from agents import AutoResearchAgents
from tasks import AutoResearchTasks

from file_io import save_markdown


print("## Welcome to the autoresearch Crew")
print('-------------------------------')
keywords = input("What are the keywords you want to search for?\n")


agents = AutoResearchAgents()
tasks = AutoResearchTasks()

# Create Agents
search_agent = agents.search_agent()
summary_agent = agents.summary_agent()
paper_classifying_agent = agents.paper_classifying_agent()


# Create Tasks
search_literature = tasks.search_literature(search_agent, keywords)
summarize_papers = tasks.summarize_papers(summary_agent,[search_literature], save_markdown)
classify_papers = tasks.classify_summarized_papers(paper_classifying_agent, [summarize_papers])


research_crew = Crew(
    agents=[
        search_agent,
        summary_agent,
        paper_classifying_agent,
    ],
    tasks=[
        search_literature,
        summarize_papers,
        classify_papers
    ],
    verbose=True,
)

search_result = research_crew.kickoff()

