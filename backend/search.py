import urllib, urllib.request
import requests
import json
import os
import re


query = ""




###################################
#QUERY BREAKDOWN/KEYWORD EXTRACTION
###################################

#fill API key here
openRouterAPIKey = ""
sentence_breakdown = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {openRouterAPIKey}",
    "Content-Type": "application/json"
  },
  data=json.dumps({
      #meta-llama/llama-3.2-3b-instruct
      #deepseek/deepseek-r1-zero:free
      #deepseek/deepseek-r1
    "model": "deepseek/deepseek-r1",
    "messages": [
      {
        "role": "user",
        "content": f"Given a query: '{query}', split the query into its unchanged component sentences. These sentences will belong to the following categories: subject_queries, query_conditions, or unrelated. subject_queries are sentences that explicitly reference a topic that users want to know more about. Different subject_queries may seem unrelated to each other, but this is acceptable. query_conditions are sentences that explicitly specify requirements for academic papers, such as publication date, author, number of citations, etc. Content requirements , topics, and subjects are subject_queries, not query_conditions. unrelated are sentences that are not subject_queries or query_conditions. Sentences can contain a combination of subject_queries and query_conditions, in which case, split the sentences and organize the split fragments into their respective groups. All fragments and sentences should be unchanged from the original query. Return nothing but the organized, unchanged sentences and fragments."
      }
    ],
    "provider": {
      #that one provider caches things which for now isn't particularly useful...
      "require_parameters": True,
      "order": [
        "Fireworks"
      ],
      "allow_fallbacks": False
    },
    "response_format": {
      "type": "json_schema",
      "json_schema":{
          "name":"output",
          "strict":True,
          "schema":{
              "type": "object",
              "properties":{
                  "subject_queries":{
                      "type":"string",
                      "description":"List of subject_queries strings"
                  },
                  "query_conditions":{
                      "type":"string",
                      "description":"List of query_conditions strings"
                  },
                  "unrelated":{
                      "type":"string",
                      "description":"List of unrelated strings"
                  }
              },
              "required":["subject_queries", "query_conditions"],
              "additionalProperties": False
          }
      }
    }

    
  })
)

if sentence_breakdown.status_code == 200:
    breakdown_data = sentence_breakdown.json()
    breakdown_json = json.loads(breakdown_data.get("choices")[0].get("message").get("content"))
else:
    print(sentence_breakdown.status_code)
    exit(1)

subject_queries = breakdown_json.get("subject_queries")
query_conditions = breakdown_json.get("query_conditions")

keyword_breakdown = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {openRouterAPIKey}",
    "Content-Type": "application/json"
  },
  data=json.dumps({
      #meta-llama/llama-3.2-3b-instruct
      #deepseek/deepseek-r1-zero:free
      #deepseek/deepseek-r1
    "model": "deepseek/deepseek-r1",
    "messages": [
      {
        "role": "user",
        "content": f"Given subject_queries: '{subject_queries}' consists of separated sentences and fragments. From subject_queries, extract the relevant subject_keywords for a search of an academic paper database. Do not give keywords that are not in the sentence or are redundant, and only return the relevant subject_keywords about a topic or idea, nothing more. Given query_conditions: '{query_conditions}' consists of separated sentences and fragments. From query_conditions extract the relevant conditional keywords for a search of an academic paper database. subject_queries are sentences that explicitly reference a topic that users want to know more about. Different subject_queries may seem unrelated to each other, but this is acceptable. query_conditions are sentences that explicitly specify requirements for academic papers, such as publication date, author, number of citations, etc. Keywords should be individual words."
      }
    ],
    "provider": {
      #that one provider caches things which for now isn't particularly useful...
      "require_parameters": True,
      "order": [
        "Fireworks"
      ],
      "allow_fallbacks": False
    },
    "response_format": {
      "type": "json_schema",
      "json_schema":{
          "name":"output",
          "strict":True,
          "schema":{
              "type": "object",
              "properties":{
                  "subject_keywords":{
                      "type":"string",
                      "description":"List of comma separated subject_keywords"
                  },
                  "condition_keywords":{
                      "type":"string",
                      "description":"List of comma separated condition_keywords"
                  }
              },
              "required":["subject_keywords", "condition_keywords"],
              "additionalProperties": False
          }
      }
    }

    
  })
)

if keyword_breakdown.status_code == 200:
    breakdown2_data = keyword_breakdown.json()
    keywords_json = json.loads(breakdown2_data.get("choices")[0].get("message").get("content"))
else:
    print(keyword_breakdown.status_code)
    exit(1)
print(keywords_json)




ssQuery = keywords_json['subject_keywords']



#############################
#SEMANTIC SCHOLAR SEARCH/SAVE
#############################



url = "http://api.semanticscholar.org/graph/v1/paper/search/bulk"


query_params = {
    "query": ssQuery,
    "fields": "title,year,abstract,citationCount,url,publicationTypes,publicationDate,openAccessPdf,authors",
    "openAccessPdf": True,
}

#WE CANT GET AN API KEY

response = requests.get(url, params=query_params).json()['data']
pdfs = [(i["openAccessPdf"]["url"], i["title"], i["year"], i["abstract"], i["publicationDate"], i["authors"]) for i in response if i.get("openAccessPdf")]

def cleanName(name, max_length=50):
  cleaned = re.sub(r'[<>:"/\|?*]', '_', name)
  return cleaned[:max_length]

directory = r"C:\\Users\\fujii\Downloads\\519ProjectTesting\\Papers"

i = 0
max = 3
#save3
pdfDir = directory + "\\PDFs"
metaDir = directory + "\\Metadata"
os.makedirs(pdfDir, exist_ok=True)
os.makedirs(metaDir, exist_ok=True)

for pdf, title, year, abstract, pubDate, authors in pdfs:
    if i < max:
      name = cleanName(title)
      savePDF = os.path.join(pdfDir, f"{name}.pdf")
      try:
          with urllib.request.urlopen(pdf) as response:
              file_size = int(response.getheader("Content-Length") or 0)
              if file_size != 0:
                urllib.request.urlretrieve(pdf, savePDF)
                metadata = {
                   "title":title,
                   "authors": authors,
                   "publicationDate": pubDate,
                   "abstract": abstract,
                   "year": year
                }
                saveMeta = os.path.join(metaDir, f"{name}.json")
                with open(saveMeta, "w") as file:
                  json.dump(metadata, file)
                i+=1     
      except:
        pass
    else:
       break

