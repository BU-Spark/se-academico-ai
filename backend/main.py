from fastapi import FastAPI, Request, Query
from summarization import search_papers, analyze_papers
import aiosqlite

from pathlib import Path
import shutil

import logging
import asyncio

# Remove SQLITE packages after demo
import sqlite3
import time

from summarization import search_papers

import nest_asyncio
nest_asyncio.apply()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



app = FastAPI()

# Demo DB Setup - REMOVE LATER
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
# reset table
cursor.execute('DROP TABLE IF EXISTS tasks')

# Clear papers on setup
def clear_papers_folder():
    folder = Path('./papers')
    if folder.exists():
        for file_path in folder.iterdir():
            try:
                if file_path.is_file() or file_path.is_symlink():
                    file_path.unlink()
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.error(f'Failed to delete {file_path}. Reason: {e}')
    else:
        folder.mkdir(parents=True, exist_ok=True)
    logger.info("Cleared papers folder")
    
clear_papers_folder()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    result TEXT,
    processed BOOLEAN NOT NULL DEFAULT 0
)
''')
conn.commit()
logger.info("db initialized")

@app.get("/")
def read_root():
    return {"message": "test message 1"}

@app.get("/api")
def special_response():
    return {"message": "something"}

@app.post("/submit-query")
async def submit_query(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        logger.error("No text provided in submit-query")
        return {"error": "No text provided"}
    
    # Insert the query into the database
    cursor.execute('INSERT INTO tasks (query, processed) VALUES (?, ?)', (text, False))
    conn.commit()
    task_id = cursor.lastrowid  # Get the task_id of the newly inserted row
    logger.info(f"Query submitted: {text}, Task ID: {task_id}")
    
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    logger.info(f"Current database state: {tasks}")
    return {"result": "submitted successfully", "task_id": task_id}

@app.get("/poll-db")
async def poll_db(task_id: int = Query(..., description="The ID of the task to poll")):
    if not task_id:
        logger.error("No task ID provided in poll-db")
        return {"error": "No task ID provided"}
    
    cursor.execute('SELECT * FROM tasks WHERE task_id = ?', (task_id,))
    task = cursor.fetchone()
    if not task:
        logger.error(f"Task not found: Task ID {task_id}")
        return {"error": "Task not found"}
    
    logger.info(f"Task polled: {task}")
    return {"task_id": task[0], "query": task[1], "result": task[2], "processed": task[3]}
    
async def process_tasks():
    async with aiosqlite.connect('tasks.db') as db:
        while True:
            async with db.execute('SELECT * FROM tasks WHERE processed = 0 LIMIT 1') as cursor:
                task = await cursor.fetchone()
                if task:
                    task_id, query, result, processed = task
                    logger.info(f"Processing task: {task_id}")
                    # Simulate processing the task
                    await search_papers(query)
                    result = await analyze_papers(query)
                    await db.execute('UPDATE tasks SET result = ?, processed = 1 WHERE task_id = ?', (str(result), task_id))
                    await db.commit()
                    logger.info(f"Task {task_id} processed with result: {result}")
            await asyncio.sleep(5)
        
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_tasks())

# Close the database connection when the app shuts down
@app.on_event("shutdown")
def shutdown_event():
    conn.close()
    logger.info("Database connection closed")

#@app.post("/process-text")
#async def process_text_endpoint(request: Request):
#    data = await request.json()  # Get JSON data
#    text = data.get("text")
#    if not text:
#        return {"error": "No text provided"}
#    result = search_papers(text)
#    return {"processed_text": result}  # Return processed textx
