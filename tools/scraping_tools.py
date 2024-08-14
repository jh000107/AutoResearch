import re
import requests
import os
from bs4 import BeautifulSoup
import json

from langchain.tools import tool

from crewai_tools import ScrapeWebsiteTool 

class WebScrapingTools():

  @tool
  def web_scraper(url):
    """Useful to scraping content from the given url."""
    tool = ScrapeWebsiteTool(website_url=url)
    return tool.run()
  
  @tool
  def extract_from_arxiv(title, link):
    """Convert the link into a direct url to arXiv pdf file, and extract PDF content."""
    pdf_link = re.sub(r'abs', 'pdf', link)

    response = requests.get(pdf_link)
    if response.status_code == 200:
      save_path = os.path.join('papers', f"{title}.pdf")
      os.makedirs(os.path.dirname(save_path), exist_ok=True)
      with open(save_path, 'wb') as file:
        file.write(response.content)
    else:
      print(f"Failed to download paper '{title}' from {link}")



  # @tool
  # def save_pdf(paper_details_list):
  #   """This tool iterates through the 'paper_details_list' and saves the PDF contents of the papers.
  #       'paper_details_list' should be a list containing dictionaries. This also works for the list
  #    containing only one paper, and this tool is also useful even if the paper doesn't provide a direct link to the PDF."""

    



        