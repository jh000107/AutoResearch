from crewai import Task
from textwrap import dedent

from tools.search_tools import SearchTools
from tools.scraping_tools import WebScrapingTools


# This is an example of how to define custom tasks.
# You can define as many tasks as you want.
# You can also define custom agents in agents.py
class AutoResearchTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"
    
    def find_survey_papers_semanticScholar(self, agent, keywords, callback_function):
        return Task(
            description=dedent(
                f"""
            **Task**: Find Survey Papers or Highly Relevant Focal Papers
            **Description**: Search for comprehensive survey papers of review articles that provide an
                overview of the research area specified by the given keywords. The agent will search through academic databases
                by using Semantic Scholar API to identify survey papers. If survey papers are not found, the agent will proceed to
                identify key focal papers that are highly relevant to the research keywords.
            
            Prioritize the most recent data as possible, and make sure to use actual papers.

            This task should be conisdered as finished when it successfully returned an output from 'search_semantic_scholar' tool.
            Search for: "{keywords} survey papers". "{keywords} survey papers" should be directly passed in as 'query' parameter for the tool.

            **MAKE SURE TO USE ACTUAL SEARCH RESULTS.**

            The output for this task should be a list of dictionaries without any other text. Just a list.

            
            
            **Note**: {self.__tip_section}
        """
            ),
            agent=agent,
            expected_output="""A list of research papers.
                Example Output:
                [
                    {
                        "paperId": "example paperId",
                        "url": "example url",
                        "title": "example title",
                        "abstract": "example abstract",
                        "year": year in 4 digits,
                        "isOpenAccess": True or False,
                        "openAccessPdf": None or "example pdf url",
                        "authors": [...]
                    }
                ]
            """,
            callback=callback_function,
        )
    
    # def download_pdfs(self, agent, paper_details):
    #     return Task(
    #         description=dedent(
    #             f"""
    #             **Task**: Download PDFs
    #             **Description**: Automate the downloading of PDF files based on details
    #             retrieved  during the literature search process. This task efficiently handles the
    #             extraction of PDF links from search results and ensures that the documents are downloaded
    #             and stored for further analysis.

    #             To efficiently perform the above, take the output from 'search_literature' task, which is {paper_details}, and use it for the tool 'save_pdf'.

    #              **Note**: {self.__tip_section}
    #             """
    #         ),
    #         agent=agent,
    #     )

    
    def search_literature(self, agent, keywords):
        return Task(
            description=dedent(
                f"""
            **Task**: Find Survey Papers or Highly Relevant Focal Papers
            **Description**: Search for comprehensive research papers that provide an
                overview of the research area specified by the given {keywords}. The agent will search through academic databases
                by using Semantic Scholar API to identify research papers, and download the pdf contents of the papers.

            Search for "{keywords}".

            You MUST use the actual results from the search. DO NOT make up on your own.

            **Parameters for the tool**:
             - query: {keywords}
            
            **Note**: {self.__tip_section}
        """
            ),
            agent=agent,
            expected_output="""Paths to downloaded PDF files only.
            Example Output:
            ./papers/example_paper_title1.pdf
            """
        )
    
    def summarize_papers(self, agent, context, callback_function):
        return Task(
            description=dedent(
                """
                **Task**: Read, Analyze, and Summarize the Content of Research Papers
                **Description**: This task involves reading and analyzing the content of downloaded research papers,
                    extracting key points, findings, and contributions, and generating concise summaries. The goal is to
                    provide clear and brief overviews that capture the essence of each paper, enabling researchers to quickly
                    understand the main insights and significance of the literature.
                
                Your final answer MUST be a report that includes a comprehensive summary of the downloaded
                research papers.

                **Parameters for the tool**:
                - pdf_path: pdf_path must be the file path to a downloaded research paper.

                **Note**: {self.__tip_section}
                """),
            agent=agent,
            context=context,
            callback=callback_function
        )
    
    def classify_summarized_papers(self, agent, context):
        return Task(
            description=dedent(
                """
                **Task**: Classify Summarized Research Papers into Groups
                **Description**: This task involves analyzing the summaries of research papers and classifying them into groups
                    based on their research focus, methodologies, and findings. The goal is to create organized groups of research
                    papers, making it easier to identify relevant subfields, trends, and gaps in the literature.
                
                Your final answer MUST be a report that includes the classification of each summarized research paper into its
                respective group.

                **Note**: {self.__tip_section}

            """),

            agent=agent,
            context=context,
        )
    
    def extract_arxiv_pdf(self, agent):
        return Task(
            description=dedent(
                """
                **Task**: Extract PDF Content from arXiv
                **Description**: Take the output from the 'find_survey_papers'. Then, only take the arXiv papers and convert the output into a list of dictionaries like the following:
                [
                    {
                    "Title": "A Survey of Large Language Models: Applications, Techniques, and Trends",
                     "Link": "https://arxiv.org/abs/2303.18223"
                     },
                     {
                     "Title": "Retrieval-Augmented Generation for Large Language Models: A Survey",
                     "Link": "https://arxiv.org/abs/2312.10997"
                     }
                ]

                Then, for each paper, convert the link into a direct url to pdf, and extract the content using 'extract_from_arxiv' tool.

                When using 'extract_from_arxiv' tool, make sure to pass only one paper per the use of the tool.
                You should passs "Title" and "Link" when using the tool.

                 **Note**: {self.__tip_section}
                """
            ),
            agent=agent
        )
    
    

    def track_citations(self, agent, pdfs, search_databases, include_full_text=False):
        return Task(
            description=dedent(
                f"""
            **Task**: Track Citations
            **Description**: Conduct a comprehensive citation analysis for the specified PDFs.
                This involves searching the internet and academic databases to identify all papers cited by these papers (backward citation)
                and all papers that cite these papers (forward citation). The task ensures an expanded research base by
                including a network of related works.

            **Parameters**:
            - PDFs: {pdfs}
            - SearchDatabases: {search_databases}
            - IncludeFullText: {include_full_text}
                                       
            **Note**: {self.__tip_section()}
        """
            ),
            agent=agent,
        )


#fA list of survey or key focal papers on {keywords}.
#             Example Output:
#             # Survey/focal Papers on Topic: {keywords}\\n\\n
#             1. **Title:** "A Survey of Large Language Models: Applications, Techniques, and Trends"
#             - **Link:** [arXiv:2303.18223](https://arxiv.org/abs/2303.18223)
#             - **Snippet:** "This survey provides a comprehensive overview of large language models, detailing their applications, underlying techniques, and emerging trends. It covers various domains where LLMs have been successfully implemented and discusses future directions in the field."

#             2. **Title:** "A Survey on Evaluation of Large Language Models"
#             - **Link:** [arXiv:2307.03109](https://arxiv.org/abs/2307.03109)
#             - **Snippet:** "Large language models (LLMs) are gaining increasing popularity in both academia and industry, owing to their unprecedented performance in various applications. This paper surveys the methods and metrics used to evaluate LLMs, highlighting the challenges and best practices in the evaluation process."

#             3. **Title:** "Retrieval-Augmented Generation for Large Language Models: A Survey"
#             - **Link:** [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)
#             - **Snippet:** "This survey explores the integration of retrieval mechanisms with large language models to enhance their performance. It discusses various retrieval-augmented generation (RAG) techniques and their applications in improving the accuracy and credibility of LLM outputs."

#             4. **Title:** "A Survey of Large Language Models"
#             - **Link:** [Papers With Code](https://paperswithcode.com/paper/a-survey-of-large-language-models)
#             - **Snippet:** "This survey reviews the recent advances of large language models, introducing the background, key findings, and mainstream techniques. It focuses on pre-training, adaptation tuning, utilization, and capacity evaluation of LLMs, summarizing available resources and discussing future directions."

#             5. **Title:** "Large Language Models: A Survey"
#             - **Link:** [arXiv:2402.06196](https://arxiv.org/abs/2402.06196)
#             - **Snippet:** "This paper surveys the development and capabilities of large language models, from early neural language models to recent advancements like GPT-4 and LLaMA. It examines their impact on natural language understanding and generation, and the challenges associated with scaling these models."
#             