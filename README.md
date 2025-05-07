# Academico AI

## Overview

Welcome to **Academico AI**! This repository is part of the **CS/DS 519 Software Engineering X-lab Practicum** at Boston University. The goal of this project is to build a platform that uses AI and large language models (LLMs) to automate academic paper search, analysis, and knowledge graph creation. It provides researchers with a single platform for all their research needs, streamlining the process and fostering collaboration.

---

## Table of Contents

1. [Project Overview](#overview)
2. [Setup/Running the Project](#getting-started)
3. [Technology Stack](#technology-stack)
4. [How to Contribute](#how-to-contribute)
5. [Project Structure](#project-structure)
6. [Resources](#resources)
7. [Steps](#steps)
8. [Known Bugs/Issues](#Bugs)
9. [Maintainers](#maintainers)
   

---

## Getting Started

### Prerequisites

Ensure you have the following installed:

- [Node.js](https://nodejs.org/)
- [Python 3.11+](https://www.python.org/)
- [MySQL](https://dev.mysql.com/)
- [Git](https://git-scm.com/)

### API Keys

- [OpenAI API Key](https://openai.com/api/) **Paid**
- [Neo4j Desktop or Aura](https://neo4j.com/) **Free**
- [OpenRouter API Keys](https://openrouter.ai/) **Free**
- [Semantic Scholar API Key (Optional)](https://www.semanticscholar.org/product/api)

It is necessary to have an OpenAI API Key, an OpenRouter API Key, and 2 Neo4J Aura instances.

OpenAI is a paid API key.

It is possible to use the project with a free OpenRouter API Key, but the project performs better with paid models.

A Semantic Scholar API Key is not necessarily required, but be mindful that without one, the project uses public shared bandwidth.

### Setup/Running Project

1. Install Rust

   ```bash
   https://rustup.rs # (For Windows)

   brew install rustup-init # (For Mac OS)
   rustup-init

   Verify Installation
   rustc --version
   cargo --version
   ```

2. Clone the repository:

   ```bash
   git clone https://github.com/BU-Spark/se-academico-ai.git
   cd se-academico-ai
   git checkout dev
   ```

3. Activate the Neo4j Aura database instances

   https://login.neo4j.com/u/login/identifier?state=hKFo2SB3c0lHeFpReklWTEdDR2QtLXdlSkM2alFCOGFnYnZFZKFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIFZkMUJuODVvZzRwSkRiNGFpYlRFdndnNmRwSWo5eHBxo2NpZNkgV1NMczYwNDdrT2pwVVNXODNnRFo0SnlZaElrNXpZVG8

4. Set up .env: <br><br>

   **In project directory, create new .env file with the following:**

   ```bash
   OPENAI_API_KEY =
   OPENROUTER_API_KEY =
   NEO4J_URI =
   NEO4J_USERNAME =
   NEO4J_PASSWORD =
   AURA_INSTANCEID =
   ALT_NEO4J_URI =
   ALT_NEO4J_PASSWORD =
   ```

5. Set up the backend: <br><br>

   **Open new terminal**

   ```bash
   # Navigate to project directory
   cd se-academico-ai

   cd backend

   python -m venv venv # Create Python virtual environment


   # Run virtual environment
   .\venv\Scripts\activate  # (For Windows)
   or
   source venv/bin/activate # (For Mac OS)


   pip install -r requirements.txt

   uvicorn main:app --reload # Run backend server
   ```

6. Run the frontend: <br><br>
   **Open new terminal**

   ```bash
   # Navigate to project directory
   cd se-academico-ai

   npm install

   npm run dev # Run Next.js server
   ```

7. Open the app <br>

   **Visit localhost:3000**

## Technology Stack

**Frontend**:

- TypeScript
- React
- Next.js

**Backend**:

- Python
- FastAPI
- OpenRouter/OpenAI
- MySQL
- Neo4j

---

## Technical Architectures

![MainTA](Images/LitReviewTA.png)

![KnowledgeGraphTA](Images/KGTA.png)

## How to Contribute

We welcome contributions from all students! Whether it’s improving UI/UX, enhancing LLM prompts, optimizing backend performance, or fixing bugs, your help is appreciated.

### Contribution Guidelines

1. **Fork the Repository**  
   Click "Fork" at the top-right of the repo page.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/your-username/se-academico-ai.git
   cd se-academico-ai
   ```

3. **Create a Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Push and Open a PR**

   ```bash
   git push origin feature/your-feature-name
   ```

   Then open a Pull Request from GitHub.

---

## Project Structure

```
se-academico-ai/
│
├── backend/                     # FastAPI server
│   ├── main.py                  # API entry point
│   ├── requirements.txt         # Python dependencies
│   ├── app/                     # API logic, models, and routers
│   ├── metadata/                # Metadata-related files
│   ├── papers/                  # Folder for papers
│   ├── markdown_papers/         # Folder for markdown files
│   └── tasks.db                 # SQLite database (temporary)
│
├── app/                         # Next.js frontend
│   ├── api/                     # API routes
│   ├── chatbox/                 # Contains components search page
│   │   ├── chatHistory.tsx
│   │   ├── graph.tsx
│   │   ├── chatBox.tsx
│   │   ├── page.tsx
│   │   └── ...
│   ├── ui                       # Various UI components
│   │   └── global.css
│   ├── page.tsx                 # Main page for app
│   └── package.json             # Node.js dependencies
│
├── .gitignore                   # Git ignore rules
├── README.md                    # Project overview and instructions
└── pnpm-lock.yaml               # Lockfile for dependencies
```

---

## Resources

### Documentation

- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Neo4j Docs](https://neo4j.com/docs/)
- [OpenRouter API](https://openrouter.ai/docs)

### Tutorials

- [Connecting FastAPI and React](https://testdriven.io/blog/fastapi-react/)
- [Knowledge Graphs with Neo4j](https://neo4j.com/developer/guide-knowledge-graph/)

---

## Steps

### Phase 1: MVP Build

- Set up project scaffolding: Next.js frontend, FastAPI backend.
- Integrate OpenAI/OpenRouter API to support paper summarization.
- Allow users to search for academic articles using semantic queries.
- Save paper metadata to local storage/MySQL.

### Phase 2: Knowledge Graphs

- Parse metadata and full text with LLMs.
- Extract concepts, methods, and findings.
- Build knowledge graphs using Neo4j.

### Phase 3: UX & Features

- Develop chatbot interface.
- Enable context-based query understanding.
- Add login/session support (optional).
- Improve article saving, history tracking, and export features.

---

## Maintainers

- Emily Yang (GitHub: [@EmilyYang47](https://github.com/EmilyYang47))
- Hiro Fuji (Github: [@fujiihc](https://github.com/fujiihc))
- Jason Kwok (Github: [@Jkwokhk](https://github.com/Jkwokhk))
- Shawn Lau (GitHub: [@clow427](https://github.com/clow427))


## Bugs

It is important to note that the search feature has some shortcomings.

Given a valid user query with multiple subjects, it is possible that no papers are returned. 

This is because a single search query is made with each user query, so the system would search for papers containing multiple keywords. 

There is a chance that given too many subjects, there are no papers that contain these keywords. If you need multiple search subjects, break them up into separate search queries. 
