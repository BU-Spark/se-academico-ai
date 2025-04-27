from neo4j import GraphDatabase
from py2neo import Graph
from pyvis.network import Network
import os
import json
import matplotlib.pyplot as plt
import networkx as nx

from dotenv import load_dotenv

load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"

URI = NEO4J_URI
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

def load_papers(folder_path):
    '''
    Loads the metadata of papers from JSON files in the specified folder.
    '''
    papers = []
    print(f"Loading papers from {folder_path}...")

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(folder_path, filename), 'r') as f:
                    paper = json.load(f)
                    papers.append(paper)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {filename}: {e}")
    return papers

def create_knowledge_graph(tx, papers):
    # Create Year node
    for paper in papers:
        if not paper.get("title"):
            print(f"Skipping paper due to missing title: {paper.get('title', 'Unknown Title')}")
            continue
        tx.run("""
            MERGE (y:Year {value: $year})
        """, year=paper["year"])

        # Create Paper node
        tx.run("""
            MERGE (p:Paper {
                title: $title,
                publicationDate: date($publicationDate)
            })
            WITH p
            MATCH (y:Year {value: $year})
            MERGE (p)-[:PUBLISHED_IN]->(y)
        """, title=paper["title"], 
                publicationDate=paper["publicationDate"], year=paper["year"])

        # Create Authors and link to paper
        for author in paper["authors"]:
            tx.run("""
                MERGE (a:Author {authorId: $authorId, name: $name})
                WITH a
                MATCH (p:Paper {title: $title})
                MERGE (a)-[:WROTE]->(p)
            """, authorId=author["authorId"], name=author["name"], title=paper["title"])

        # Create Topics and link to paper
        for topic in paper.get("topics", []):
            if topic:
                tx.run("""
                    MERGE (t:Topic {name: $topic})
                    WITH t
                    MATCH (p:Paper {title: $title})
                    MERGE (p)-[:COVERS]->(t)
                """, topic=topic, title=paper["title"])

def batch_insert_papers(papers):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("Connection established.")

 

    with driver.session() as session:
        session.execute_write(create_knowledge_graph, papers)
        print("Knowledge graph data inserted.")
        session.close()
        driver.close()

def create_graph():
    # Create a Pyvis network
    net = Network(notebook=True)

    # Connect to Neo4j
    graph = Graph(URI, auth=AUTH)

    # Fetch nodes and relationships from Neo4j
    query = """
    MATCH (a)-[r]->(b)
    RETURN a, r, b LIMIT 100
    """

    results = graph.run(query)

    for record in results:
        a = dict(record["a"])
        b = dict(record["b"])
        rel = type(record["r"]).__name__

        a_id = record["a"].identity
        b_id = record["b"].identity

        net.add_node(a_id, label=a.get("name") or a.get("title"), title=str(a))
        net.add_node(b_id, label=b.get("name") or b.get("title"), title=str(b))
        net.add_edge(a_id, b_id, label=rel)

    # Save the network as an HTML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.abspath(os.path.join(current_dir, "../public"))
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

    # Save the network as an HTML file in the specified folder
    output_file_path = os.path.join(output_folder, "knowledge_graph.html")
    print(f"Saving graph to {output_file_path}...")
    net.save_graph(output_file_path)

if __name__ == "__main__":
    folder_path = "backend/metadata"
    papers = load_papers(folder_path)
    batch_insert_papers(papers)
    print("Knowledge graph data inserted.")
    create_graph()
    print("Graph created and saved as HTML.")

