import pymupdf4llm
import requests
import json
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
from py2neo import Graph
from pyvis.network import Network

load_dotenv()

 

NEO4J_URI = os.getenv("ALT_NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("ALT_NEO4J_PASSWORD")
# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"

URI = NEO4J_URI
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

def extract_knowledge_graph_from_paper(folder_path):

    load_dotenv()

    OPEN_ROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    openRouterAPIKey = OPEN_ROUTER_API_KEY

    schema = {
        "name": "KnowledgeGraph",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "description": "Graph nodes representing key entities or concepts",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "Unique ID for the node"
                            },
                            "labels": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of Neo4j labels"
                            },
                            "properties": {
                                "type": "object",
                                "description": "Key-value properties",
                                "properties": {
                                    "name": {"type": "string"},
                                    "description": {"type": "string"}
                                },
                                "required": ["name"]
                            }
                        },
                        "required": ["id", "labels", "properties"]
                    }
                },
                "relationships": {
                    "type": "array",
                    "description": "Graph relationships between nodes",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "target": {"type": "string"},
                            "type": {"type": "string"},
                            "properties": {
                                "type": "object",
                                "description": "Optional relationship properties",
                                "additionalProperties": True
                            }
                        },
                        "required": ["source", "target", "type"]
                    }
                }
            },
            "required": ["nodes", "relationships"],
            "additionalProperties": False
        }
    }

    all_graphs = {}

    for filename in os.listdir(folder_path):
        print(filename)
        if filename.endswith(".md"):  # Only markdown files
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as f:
                text = f.read()


            query = f"""You are an expert in knowledge graph construction from scientific literature.

            From the following academic paper (in markdown format), extract a list of key nodes and the relationships between them. 

            Each node should include:
            - a unique ID
            - a list of Neo4j labels (e.g., Concept, Process, Technology, Entity)
            - properties: name (required), description (optional)

            Each relationship should include:
            - source and target node IDs
            - a Neo4j-style type (e.g., USES, ENABLES, CAUSES)
            - optional properties (e.g., context, evidence)
            Here is the text: {text} """




            breakdown = requests.post(
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
                    "content": query
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
                "json_schema":schema
                }

                
            })
            )

            if breakdown.status_code == 200:
                breakdown_data = breakdown.json()
                breakdown_json = json.loads(breakdown_data.get("choices")[0].get("message").get("content"))
                all_graphs[filename] = breakdown_json
                print(f"Extracted knowledge graph from {filename}:")
                print(breakdown_json)
            else:
                print(breakdown.status_code)
                print("Failed to extract knowledge graph from {filename}:")

    return all_graphs




uri = NEO4J_URI
username = NEO4J_USERNAME
password = NEO4J_PASSWORD
def batch_insert_papers(papers):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("Connection established.")

    with driver.session() as session:
        for filename, graph in papers.items():
            for n in graph["nodes"]:
                session.execute_write(makeNode, n)

            for r in graph["relationships"]:
                session.execute_write(makeRelationship, r)
        session.close()
        driver.close()




def makeNode(tx, node):
    labels = ":".join(f"`{label}`" for label in node["labels"])
    properties = node["properties"].copy()
    properties["id"] = node["id"]
    query = f"""
    MERGE (n:{labels} {{id: $id}})
    SET n += $props
    """
    tx.run(query, id=node["id"], props=properties)

def makeRelationship(tx, relationship):
    query = f"""
    MATCH (a {{id: $source}}), (b {{id: $target}})
    MERGE (a)-[r:{relationship["type"]}]->(b)
    SET r += $props
    """
    tx.run(query, source=relationship["source"], target=relationship["target"], props=relationship.get("properties", {}))


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
        a_node = record["a"]
        b_node = record["b"]
        relationship = record["r"]

        a_id = a_node.identity
        b_id = b_node.identity

        a_props = dict(a_node)
        b_props = dict(b_node)
        rel_type = type(relationship).__name__

        net.add_node(a_id, label=a_props.get("name") or a_props.get("title") or str(a_id), title=json.dumps(a_props, indent=2))
        net.add_node(b_id, label=b_props.get("name") or b_props.get("title") or str(b_id), title=json.dumps(b_props, indent=2))
        net.add_edge(a_id, b_id, label=rel_type)

    # Save the network as an HTML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.abspath(os.path.join(current_dir, "../public"))
    os.makedirs(output_folder, exist_ok=True)

    output_file_path = os.path.join(output_folder, "main_knowledge_graph.html")
    print(f"Saving graph to {output_file_path}...")
    net.save_graph(output_file_path)

if __name__ == "__main__":
    folder_path = os.path.join(os.path.dirname(__file__), "markdown_papers")
    papers = extract_knowledge_graph_from_paper(folder_path)
    batch_insert_papers(papers)
    print("Main knowledge graph data inserted.")
    create_graph()
    print("Main knowledge graph created.")