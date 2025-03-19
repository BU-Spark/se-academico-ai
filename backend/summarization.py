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

async def search_papers(query):
    """Searches arXiv for papers based on a query and downloads them asynchronously."""
    query = str(query)
    papers_dir = Path("./papers")
    markdown_dir = Path("./markdown_papers")

    # Ensure papers_dir exists
    if not papers_dir.exists():
        papers_dir.mkdir(parents=True, exist_ok=True)

    # Only create markdown_dir if it does not exist
    if not markdown_dir.exists():
        markdown_dir.mkdir(parents=True)
    os.makedirs("papers", exist_ok=True)
    os.makedirs("markdown_papers", exist_ok=True)

    kw_extractor = KeywordExtractor()
    keywords = kw_extractor.extract_keywords(query)
    out = [words for words, score in keywords if len(words.split()) == 1]

    toAPI = "search_query=" + "+AND+".join(f"all:{keyword}" for keyword in out)
    url = f"http://export.arxiv.org/api/query?{toAPI}&max_results=3"

    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, url)
        feed = feedparser.parse(data)

        tasks = []
        saved_files = []

        for entry in feed.entries:
            pdf_url = next(d.href for d in entry.links if d.get("title") == "pdf")
            name = pdf_url.split("/")[-1]
            save_path = f"./papers/{name}.pdf"
            tasks.append(download_pdf(session, pdf_url, save_path))
            saved_files.append(save_path)

        await asyncio.gather(*tasks)

    print("Converting now")
    conversion_tasks = []
    for paper in saved_files:
        conversion_tasks.append(convert_pdfs_to_markdown(paper, markdown_dir))

    # Wait for all conversions to complete
    await asyncio.gather(*conversion_tasks)

    print("Finished converting")
    




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
        
        if os.path.isfile(file_path):  
            print(f"Processing file: {file}")
            docs.add(file_path)

    # calling paperqa

    settings = Settings()


    answer_response = docs.query(query
                             , settings=settings)
    print(answer_response.answer)
    return answer_response.answer

   
