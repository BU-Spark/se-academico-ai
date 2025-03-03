import urllib, urllib.request
import asyncio
import feedparser
from yake import KeywordExtractor
import os

async def search_papers(query):
    query = str(query)
    os.makedirs("papers", exist_ok=True)
    kw_extractor = KeywordExtractor()
    keywords = kw_extractor.extract_keywords(query)
    out = [words for words, score in keywords if len(words.split()) == 1]
    
    toAPI = "search_query=" + "+AND+".join(f"all:{keyword}" for keyword in out)
    url = f"http://export.arxiv.org/api/query?{toAPI}&max_results=3"
    data = urllib.request.urlopen(url)
    feed = feedparser.parse(data)
    
    for entry in feed.entries:
        pdfURL = [d for d in entry.links if d.get("title") == "pdf"][0].href
        name = pdfURL.split("/")[4]
        saveName = f"./papers/{name}.pdf"
        urllib.request.urlretrieve(pdfURL, saveName)
    print("SEARCHC WORKS!!!!!!!")