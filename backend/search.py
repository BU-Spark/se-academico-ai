import urllib, urllib.request
import requests
import json
import os
import re
import aiohttp
import aiofiles
import asyncio
from dotenv import load_dotenv
from pdf_conversion import convert_pdfs_to_markdown
from pathlib import Path



def clean_name(name, max_length=50):
    """
    cleans the name by removing invalid characters and truncating to max_length.
    """
    cleaned = re.sub(r'[<>:"/\\|?*]', '_', name)
    return cleaned[:max_length]

async def fetch_post_json(session, url, headers, payload):
    """
    Fetches JSON data from a given URL with headers and payload.
    """
    async with session.post(url, headers=headers, json=payload) as resp:
        if resp.status == 200:
            return await resp.json()
        else:
            print(f"Error {resp.status} from {url}")
            return None
        
async def fetch_get_json(session, url, params):
    """
    Fetches JSON data from a given URL with parameters.
    """
    async with session.get(url, params=params) as resp:
        if resp.status == 200:
            return await resp.json()
        else:
            print(f"Error {resp.status} from {url}")
            return None
        

async def download_pdf(session, url, path):
    """
    Downloads a PDF file from a given URL and saves it to the specified path.
    """
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(path, "wb") as f:
                    await f.write(await resp.read())
                return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return False


async def save_metadata(metadata, path):
    """
    Saves metadata to a JSON file.
    """
    async with aiofiles.open(path, "w") as f:
        await f.write(json.dumps(metadata))



async def search_and_download_async(query):

    # load dotenv() and get the OpenRouter API key
    load_dotenv()
    openRouterAPIKey = os.getenv("OPENROUTER_API_KEY")
    if not openRouterAPIKey:
        # If the API key is not set in the environment variables, use the provided api_key
        # This is useful for testing purposes
        # and can be removed in production
        exception = "OpenRouter API key not found in environment variables."
        print(exception)
        return
      

    headers = {
        "Authorization": f"Bearer {openRouterAPIKey}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        # Step 1: Sentence breakdown
        sentence_payload = {
            # You can also pick different models
            "model": "deepseek/deepseek-r1",
            "messages": [{
                "role": "user",
                # The content of the query is passed here
                # and gets split into subject_queries, query_conditions, and unrelated
                # These are used to discover relationships in the query
                # and to extract keywords for the Semantic Scholar search
                # Feel free to modify the prompt in "content" to suit your needs
                 "content": f"Given a query: '{query}', split the query into its unchanged component sentences. These sentences will belong to the following categories: subject_queries, query_conditions, or unrelated. subject_queries are sentences that explicitly reference a topic that users want to know more about. Different subject_queries may seem unrelated to each other, but this is acceptable. query_conditions are sentences that explicitly specify requirements for academic papers, such as publication date, author, number of citations, etc. Content requirements , topics, and subjects are subject_queries, not query_conditions. unrelated are sentences that are not subject_queries or query_conditions. Sentences can contain a combination of subject_queries and query_conditions, in which case, split the sentences and organize the split fragments into their respective groups. All fragments and sentences should be unchanged from the original query. Return nothing but the organized, unchanged sentences and fragments."
            }],
            "provider": {
                
                "require_parameters": True,
                "order": ["Fireworks"],
                "allow_fallbacks": False
            },
            # The response format is specified here
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "output",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "subject_queries": {"type": "string",
                                              "description": "List of subject_queries strings"},
                                                },
                            "query_conditions": {"type": "string",
                                                 "description":"List of query_conditions strings"
                                                 },
                            "unrelated": {"type": "string",
                                          "description":"List of unrelated strings"
                                        }
                        },
                        "required": ["subject_queries", "query_conditions"],
                        "additionalProperties": False
                    }
                }
            }
        
    
        sentence_result = await fetch_post_json(session, "https://openrouter.ai/api/v1/chat/completions", headers, sentence_payload)
        if not sentence_result:
            print("Failed to fetch sentence breakdown.")
            # Handle error
            return
        print(sentence_result)
        
        breakdown_data = json.loads(sentence_result.get("choices")[0].get("message").get("content"))

        subject_queries = breakdown_data.get("subject_queries")
        query_conditions = breakdown_data.get("query_conditions")

        # Step 2: Keyword extraction
        keyword_payload = {
            "model": "deepseek/deepseek-r1",
            "messages": [{
                "role": "user",
                # Same as above... Feel free to modify the prompt
                # This tries to extract keywords from the subject_queries and query_conditions
                # and returns them in a format that can be used for the Semantic Scholar search
                "content": f"Given subject_queries: '{subject_queries}' consists of separated sentences and fragments. From subject_queries, extract the relevant subject_keywords for a search of an academic paper database. Do not give keywords that are not in the sentence or are redundant, and only return the relevant subject_keywords about a topic or idea, nothing more. Given query_conditions: '{query_conditions}' consists of separated sentences and fragments. From query_conditions extract the relevant conditional keywords for a search of an academic paper database. subject_queries are sentences that explicitly reference a topic that users want to know more about. Different subject_queries may seem unrelated to each other, but this is acceptable. query_conditions are sentences that explicitly specify requirements for academic papers, such as publication date, author, number of citations, etc. Keywords should be individual words."
            }],
            "provider": {
                "require_parameters": True,
                "order": ["Fireworks"],
                "allow_fallbacks": False
            },
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "output",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "subject_keywords": {"type": "string",
                                                 "description":"List of comma separated subject_keywords"
                                                 },
                            "condition_keywords": {"type": "string",
                                                   "description":"List of comma separated condition_keywords"
                                                 }
                        },
                        "required": ["subject_keywords", "condition_keywords"],
                        "additionalProperties": False
                    }
                }
            }
        }

        keyword_result = await fetch_post_json(session, "https://openrouter.ai/api/v1/chat/completions", headers, keyword_payload)
        if not keyword_result:
            return

        keywords_json = json.loads(keyword_result.get("choices")[0].get("message").get("content"))
        print(keywords_json)
        ss_query = keywords_json["subject_keywords"].split(",")

        # Step 3: Semantic Scholar search
        ss_url = "http://api.semanticscholar.org/graph/v1/paper/search/bulk"
        query_params = {
            "query": ss_query,
            "fields": "title,year,abstract,citationCount,url,publicationTypes,publicationDate,openAccessPdf,authors",
            "openAccessPdf": "true",
        }

        ss_data = await fetch_get_json(session, ss_url, query_params)
        if not ss_data or "data" not in ss_data:
            print("No data returned from Semantic Scholar.")
            return

        papers = [(i["openAccessPdf"]["url"], i["title"], i["year"], i["abstract"], i["publicationDate"], i["authors"])
                  for i in ss_data["data"] if i.get("openAccessPdf")]

        # Step 4: Download PDFs + metadata
        pdf_dir = "./papers"
        metadata_dir = "./metadata"
        os.makedirs(pdf_dir, exist_ok=True)
        os.makedirs(metadata_dir, exist_ok=True)

        tasks = []
        for i, (pdf_url, title, year, abstract, pub_date, authors) in enumerate(papers[:3]):
            clean_title = clean_name(title)
            pdf_path = os.path.join(pdf_dir, f"{clean_title}.pdf")
            meta_path = os.path.join(metadata_dir, f"{clean_title}.json")
            metadata = {
                "title": title,
                "authors": authors,
                "publicationDate": pub_date,
                "abstract": abstract,
                "year": year,
                
                # "topics": ss_query,
            }

            tasks.append(download_pdf(session, pdf_url, pdf_path))
            tasks.append(save_metadata(metadata, meta_path))

        await asyncio.gather(*tasks)

        # Step 5: Convert PDFs to markdown
        markdown_dir = Path("./markdown_papers")
        if not markdown_dir.exists():
            markdown_dir.mkdir(parents=True)
        paper_dir = Path("./papers")
        conversion_tasks = []
        for paper in os.listdir(paper_dir):
            # Check if the file is a PDF
            # and if it is not already converted
            # to markdown
            if paper.endswith("pdf"):
                pdf_path = os.path.join(paper_dir, paper)
                conversion_tasks.append(convert_pdfs_to_markdown(pdf_path, markdown_dir))
        # Use asyncio.gather to run all conversion tasks concurrently
        # wait for all tasks to complete
        # This will convert all the PDFs in the paper_dir to markdown and save them in markdown_dir
        # Note: You might want to limit the number of concurrent tasks
        # to avoid overwhelming the system
        await asyncio.gather(*conversion_tasks)
        
        
