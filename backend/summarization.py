import aiohttp
import aiofiles
import asyncio
import feedparser
from yake import KeywordExtractor
import os
import openai
from paperqa import Settings, ask, Docs
from dotenv import load_dotenv
from pdf_conversion import convert_pdfs_to_markdown
from pathlib import Path
import logging
from search import *



# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_data(session, url):
    """Fetches data from a given URL asynchronously."""
    async with session.get(url) as response:
        return await response.read()

async def download_pdf(session, pdf_url, save_path):
    """Downloads a PDF asynchronously and saves it."""
    async with session.get(pdf_url) as response:
        if response.status == 200:
            async with aiofiles.open(save_path, "wb") as f:
                await f.write(await response.read())





async def analyze_papers(query):
    """Analyzes the papers using PaperQA."""
   
    # Initialize the OpenAI API to answer questions in prompt
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Load papers

    docs = Docs()
  

    papers_dir = "markdown_papers"  
    for file in os.listdir(papers_dir):
        file_path = os.path.join(papers_dir, file)

        logger.info(f"File path:{file_path}")
        logger.info(f"Type:{type(file_path)}")
        
        if os.path.isfile(file_path):  
            print(f"Processing file: {file}")
            docs.add(file_path)

    # calling paperqa

    settings = Settings()


    answer_response = docs.query(query
                             , settings=settings)
    print(answer_response.answer)
    return answer_response.answer

   