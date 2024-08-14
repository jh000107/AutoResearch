import json
import os
import re
import time

import requests
from bs4 import BeautifulSoup

from langchain.tools import tool

from langchain_community.tools.google_scholar import GoogleScholarQueryRun
from langchain_community.utilities.google_scholar import GoogleScholarAPIWrapper




class SearchTools():

  @tool("Search Research Papers")
  def search_research_papers(query):
    """Useful to search on Semantic Scholar about a given query, return relevant research papers, and save pdfs.
    query is provided by the user input as string."""

    url = 'https://api.semanticscholar.org/graph/v1/paper/search'

    headers = {
      'x-api-key': os.environ['SEMANTIC_SCHOLAR_API_KEY']
    }

    def get_paper_data(paper_id):
      url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id
      paper_data_query_params = {'fields': 'title,year,abstract,url,openAccessPdf'}

      response = requests.get(url, params=paper_data_query_params, headers=headers)

      if response.status_code == 200:
        return response.json()
      else:
        return None
      
    query_params = {
      'limit': 5,
      'query': query,
    }

    print(query_params)

    search_response = requests.get(url, params=query_params, headers=headers)

    paper_details_lst = []

    if search_response.status_code == 200:
      search_response = search_response.json()

      print(search_response)

      for i in range(len(search_response['data'])):
        time.sleep(3)

        paper_id = search_response['data'][i]['paperId']
        paper_details = get_paper_data(paper_id)
        print(paper_id, paper_details)

        

        if paper_details is not None:
          paper_details_lst.append(paper_details)

      # Check if paper_details is not None before proceeding
      if paper_details_lst == []:
        return "Failed to retrieve paper details."
      
      # Download PDFs
      else:
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n')
        pdf_paths = []

        for paper_detail in paper_details_lst:
          openAccessPdf = paper_detail['openAccessPdf']
          title = paper_detail['title']
          url = paper_detail['url']
        

          if openAccessPdf is not None:
            response = requests.get(openAccessPdf['url'])
            if response.status_code == 200:
              save_path = os.path.join('papers', f"{title}.pdf")
              os.makedirs(os.path.dirname(save_path), exist_ok=True)
              with open(save_path, 'wb') as file:
                file.write(response.content)
              print(f"Successfully downloaded {title}.pdf")
              pdf_paths.append('./' + save_path)
            else:
              print(f"Failed to download paper '{title}' from {openAccessPdf}")
          else:

            headers = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
              'x-api-key': os.environ['SEMANTIC_SCHOLAR_API_KEY']
            }

            for i in range(2):
              response = requests.get(url, headers=headers, allow_redirects=True)
              if response.status_code == 200:
                break
              else:
                print(f"Attempt: {i+1}: Failed to retrieve the page for {title}. Status code: {response.status_code}.")
                time.sleep(3)
                

            if response.status_code == 200:
              soup = BeautifulSoup(response.content, 'html.parser')
              script_tag = soup.find('script', {'type': 'application/ld+json', 'class': 'schema-data'})
              
              if script_tag:
                json_data = json.loads(script_tag.string)
                if '@graph' in json_data:
                  for item in json_data['@graph'][1]:
                    if item['@type'] == 'Article':
                      direct_link = item['mainEntity']
                      response = requests.get(direct_link)
                      if response.status_code == 200:
                        save_path = os.path.join('papers', f"{title}.pdf")
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)
                        with open(save_path, 'wb') as file:
                          file.write(response.content)
                        print(f"Successfully downloaded {title}.pdf")
                        pdf_paths.append('./' + save_path)
                        break
                      else:
                        print(f"Failed to download paper '{title}' from {direct_link}")
                else:
                  return "JSON-LD script tag not found."
            else:
              print(f"Failed to retrieve the page for {title}. Status code: {response.status_code}. Moving on to next paper.")
              
            
              
                
    else:
      # Handle potential errors or non-200 responses
      print(f"Relevance Search Request failed with status code {search_response.status_code}: {search_response.text}")
    
    return '\n'.join(pdf_paths)
    


  @tool("Search Google Scholar")
  def search_google_scholar(query):
    """Useful to search on Google Scholar about a given topic and return relevant results.
       Then, it outputs a list containing only the titles."""
    google_scholar_tool = GoogleScholarQueryRun(api_wrapper=GoogleScholarAPIWrapper())
    results = google_scholar_tool.run(query)
    titles = re.findall(r'Title: (.*?)\n', results)
    return titles

  @tool("Search Internet")
  def search_internet(query):
    """Useful to search the internet about a given topic and return relevant
    results."""
    return SearchTools.search(query)


  def search(query, n_results=5):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()['organic']

    result_list = []

    stirng = []
    for result in results[:n_results]:
      try:
        result_list.append({
           'title': result['title'],
           'link': result['link'],
           'snippet': result['snippet']
        })
      except KeyError:
        next

    return result_list
