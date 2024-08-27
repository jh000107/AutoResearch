# LLM-Based Agentic Framework for Automated Literature Review

## Overview

This project is an advanced AI-driven framework designed to automate the process of performing literature reviews. By leveraging state-of-the-art Large Language Models (LLMs) through the CrewAI and LangChain frameworks, this system automates the searching, scraping, summarizing, and writing of literature reviews. It is particularly useful for researchers looking to streamline the process of gathering and synthesizing academic papers on specific topics.

## Key Files and Directories

- **main.py**: The entry point of the project. It initializes the agents and tasks, receives user input, and orchestrates the entire process from searching to generating a literature review.

- **agents.py**: Contains the definitions for the custom AI agents. These agents are responsible for performing specific roles such as searching for research papers, summarizing them, and writing the final literature review.

- **tasks.py**: Defines the tasks that the agents will perform. These tasks include searching for relevant papers, summarizing their contents, and compiling the summaries into a coherent literature review.

- **tools/**: A directory containing various utility scripts:
  - **scraping_tools.py**: Tools for scraping content from academic websites.
  - **search_tools.py**: Tools for searching academic databases and repositories.
  - **summarize_tools.py**: Tools for summarizing the contents of academic papers.

- **papers/**: A directory where the relevant research papers found during the search process are stored.

## Workflow

The workflow is designed to automate the literature review process based on a user-specified query. The steps are as follows:

1. **User Input**: The user inputs the keywords or topics they want to search for.

2. **Agent Initialization**:
   - **Search Agent**: Utilizes the `SearchTools` to search for high-quality academic papers related to the user’s query using the Semantic Scholar API.
   - **Summary Agent**: Uses `SummarizingTools` to summarize the contents of the retrieved papers.
   - **Literature Review Agent**: Synthesizes the summaries into a coherent literature review.

3. **Task Execution**:
   - **Search Literature**: The `Search Agent` searches for relevant papers using the specified keywords and stores the retrieved PDFs in the `papers/` directory.
   - **Summarize Papers**: The `Summary Agent` reads, analyzes, and summarizes the papers found in the previous step.
   - **Write Literature Review**: The `Literature Review Agent` writes a comprehensive review based on the summaries.

4. **Output**: The framework generates a literature review from the relevant search

## Technology Stack

- **LLM Model**: Utilizes the LLaMA 3 70B model via the Groq API for advanced natural language processing tasks.
- **Search API**: Uses the Semantic Scholar API to find relevant academic papers for the literature review.

  ## Installation

### Clone the repository:

```bash
git clone https://github.com/jh000107/AutoResearch.git
cd AutoResearch
```

### Install and activate the environment & dependencies using Poetry:
```
poetry install --no-root
poetry env list
poetry shell
```

### Set up your environment variables:
- Create a .env file in the root directory.
- Add your OPENAI_API_KEY, GROQ_API_KEY, Semantic Scholar API Key, and other necessary credentials.

### Running the project 
```
python main.py
```
