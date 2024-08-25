from langchain.tools import tool
import PyPDF2

from crewai import Agent
from crewai import Task

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from tools.search_tools import SearchTools

import os

class SummarizingTools():

    # @tool("Summarize PDF")
    # def read_pdf(pdf_path):
    #     """Useful to read and extract PDF content from the given PDF path."""
    #     text = ""
    #     with open(pdf_path, 'rb') as file:
    #         reader = PyPDF2.PdfReader(file)
    #         num_pages = len(reader.pages)
    #         for page_num in range(num_pages):
    #             page = reader.pages[page_num]
    #             text += page.extract_text() if page.extract_text() else ""
    #     return text
    
    @tool("Summarize PDF")
    def summarize_pdf(pdf_path):
        """Useful to read and extract PDF content from the given PDF path."""
        
        def extract_text_from_pdf(pdf_path):
            text = ""
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text += page.extract_text() if page.extract_text else ""
            return text
        
        def split_text_into_chunks(text):
            text = [text[i:i + 8000] for i in range(0, len(text), 8000)]
            return text
        
        summaries = []

        text = extract_text_from_pdf(pdf_path)
        text_chunks = split_text_into_chunks(text)

        # llm = ChatOpenAI(
        #     model="crewai-llama3-8b",
        #     base_url="http://localhost:11434/v1",
        #     api_key="NA"
        # )

        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192"
        )

        for chunk in text_chunks:
            agent = Agent(
                role='Summarizing Expert',
                goal=
                'Do amazing summaries based on the content you are working with',
                backstory=
                'You are a Summarizing Expert at a AI research lab and you need to summarize about a given topic',
                allow_delegation=False,
                verbose=True,
                tools=[SearchTools.dummy_tool],
                llm=llm,
            )

            task = Task(
                agent=agent,
                description=
                f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary and nothing else.\n\nCONTENT\n------------\n{chunk}'
            )

            summary = task.execute()
            summaries.append(summary)
        
        chunks_combined = "\n\n".join(summaries)
        
        overall_agent = Agent(
                role='Summarizing Expert',
                goal=
                'Provide an overall summmary when given chunks of summaries of the research paper',
                backstory=
                'You are a Summarizing Expert at a AI research lab and you need to summarize about a given research paper',
                allow_delegation=False,
                tools=[SearchTools.dummy_tool],
                llm=llm
        )
        
        overall_task = Task(
                agent=overall_agent,
                description=
                f'Analyze and summarize the given chunks of summaries of one research paper content below. Gather critical and neccessary information, and output overall sumamry containing crucial information about the paper.\n\nCONTENT\n------------\n{chunks_combined}'
        )
        
        overall_summary = overall_task.execute()

        return overall_summary



