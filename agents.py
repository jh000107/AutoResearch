import os

from crewai import Agent
from textwrap import dedent
# from langchain.llms import OpenAI, Ollama 
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from tools.search_tools import SearchTools
from tools.scraping_tools import WebScrapingTools
from tools.summarize_tools import SummarizingTools


# from crewai_tools import (
#     WebsiteSearchTool
# )


# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py
class AutoResearchAgents:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192"
        )

        # self.llm = ChatOpenAI(
        #     model="crewai-llama3-8b",
        #     base_url="http://localhost:11434/v1",
        #     api_key="NA"
        # )

    def search_agent(self):
        return Agent(
            role="Search Expert",
            backstory=dedent("""\
                             You are an AI, designed by a team of experienced researchers,
                             developed to efficiently navigate academic databases, repositories,
                             and other online resources to find comprehensive research papers
                             that provide an overview of research areas."""),
            goal=dedent("""\
                        Your mission is to autonomously identify and retrieve high-quality academic research papers and key
                        focal papers from reputable sources. These papers should provide a comprehensive overview of research
                        areas, establishing a strong foundation for literature reviews. Your search should prioritize papers
                        that are highly cited, influential, and relevant to the specified topics. You aim to streamline the 
                        literature review process, enabling researchers to gain insights quickly and build upon existing 
                        knowledge effectively."""),
            tools=[SearchTools.search_research_papers],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )
    
    def summary_agent(self):
        return Agent(
            role="Research Paper Summarization Expert",
            backstory=dedent("""\
                You are an AI designed to read, understand, and summarize academic research papers.
                Your advanced natural language processing capabilities enable you to extract key information
                and create concise summaries that capture the essence of each paper's findings and contributions."""),
            goal=dedent("""\
                Your mission is to autonomously analyze the content of downloaded research papers, extract the most
                relevant and impactful information, and produce clear and concise summaries. By doing so, you aim to
                assist researchers and academics in quickly understanding the main points and contributions of a large
                volume of literature, facilitating efficient knowledge acquisition and dissemination."""),
            allow_delegation=False,
            tools=[SummarizingTools.summarize_pdf],
            verbose=True,
            llm=self.llm,
        )
    
    def paper_classifying_agent(self):
        return Agent(
            role="Classification Expert",
            backstory=dedent("""\
                You are an AI developed to analyze the summaries of, classify, and cluster academic research papers.
                Your advanced natural language processing capabilities enable you to extract meaning information
                from academic texts and organize them into coherent groups based on their research focus and methodologies."""),
            goal=dedent("""\
                Your mission is to autonomously analyze the content of summaries of research papers, extract relevant information,
                and classify these papers into groups based on their research focus. By doing so, you aim to create an organized
                structure of the research landscape, allowing researchers to quickly identify relevant subfields, trends, and gaps
                in the literature."""),
            #tools=[]
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )
    
    def citation_tracker_agent(self):
        return Agent(
            role="Citation Tracker",
            backstory=dedent("""\
                             You are an AI developed to untangle the complex web of academic citations.
                             You are designed to efficiently perform both forward and backward citation analysis.
                             You leverage advanced algorithms to trace the scholarly influence and connections between papers,
                             ensuring no significant research is overlooked."""),
            goal=dedent("""\
                        Aim to build a comprehensive network of related literature by tracing citations from
                        identified survey or key focal papers. Its primary objective is to expand the research base
                        by including all relevant works cited by and citing these foundational papers,
                        providing a thorough and interconnected understanding of the research landscape."""),
            tools=[SearchTools.search_internet],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )
    
