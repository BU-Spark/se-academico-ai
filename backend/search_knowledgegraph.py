from neo4j import GraphDatabase
from py2neo import Graph
from pyvis.network import Network
import os
import json

from dotenv import load_dotenv

load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"

URI = NEO4J_URI
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

def load_papers(folder_path):
    papers = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), 'r') as f:
                paper = json.load(f)
                papers.append(paper)
    return papers

def create_knowledge_graph(tx, papers):
    # Create Year node
    for paper in papers:
        tx.run("""
            MERGE (y:Year {value: $year})
        """, year=paper["year"])

        # Create Paper node
        tx.run("""
            MERGE (p:Paper {
                title: $title,
                abstract: $abstract,
                publicationDate: date($publicationDate)
            })
            WITH p
            MATCH (y:Year {value: $year})
            MERGE (p)-[:PUBLISHED_IN]->(y)
        """, title=paper["title"], abstract=paper["abstract"],
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
        MATCH (n)-[r]->(m)
        RETURN n, r, m
    """
    data = graph.run(query).data()

    # Add nodes and edges to the Pyvis network
    for record in data:
        node1 = record['n']
        node2 = record['m']
        relationship = record['r']

        net.add_node(node1.identity, label=node1['title'], title=node1['title'])
        net.add_node(node2.identity, label=node2['name'], title=node2['name'])
        net.add_edge(node1.identity, node2.identity, label=relationship.type)

    # Save the network as an HTML file
    output_folder = "../app/public"  # Specify your desired folder
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

    # Save the network as an HTML file in the specified folder
    output_file_path = os.path.join(output_folder, "knowledge_graph.html")
    net.show(output_file_path)


