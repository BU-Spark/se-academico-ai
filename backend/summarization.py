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
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # Raise an error for HTTP errors
            return await response.read()
    except aiohttp.ClientError as e:
        logger.error(f"Network error while fetching data from {url}: {e}")
        return None

async def download_pdf(session, pdf_url, save_path):
    """Downloads a PDF asynchronously and saves it."""
    try:
        async with session.get(pdf_url) as response:
            response.raise_for_status()
            if response.status == 200:
                async with aiofiles.open(save_path, "wb") as f:
                    await f.write(await response.read())
    except aiohttp.ClientError as e:
        logger.error(f"Failed to download PDF from {pdf_url}: {e}")
    except OSError as e:
        logger.error(f"File operation error while saving PDF to {save_path}: {e}")

async def analyze_papers(query):
    """Analyzes the papers using PaperQA."""
    try:
        # Initialize the OpenAI API to answer questions in prompt
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

        # Load papers
        docs = Docs()
        papers_dir = "markdown_papers"
        if not os.path.exists(papers_dir):
            raise FileNotFoundError(f"The directory '{papers_dir}' does not exist.")

        for file in os.listdir(papers_dir):
            file_path = os.path.join(papers_dir, file)
            if os.path.isfile(file_path):
                logger.info(f"Processing file: {file}")
                docs.add(file_path)

        # Calling paperqa
        settings = Settings()
        answer_response = docs.query(query, settings=settings)
        print(answer_response.answer)
        return answer_response.answer

    except FileNotFoundError as e:
        logger.error(f"File or directory error: {e}")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None

