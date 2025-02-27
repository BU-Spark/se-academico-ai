from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "test message 1"}

@app.get("/api")
def special_response():
    return {"message": "test message 2"}


# Function to process text
def process_text(input_text: str) -> str:
    return input_text.upper()  # Example transformation

@app.post("/process-text")
async def process_text_endpoint(request: Request):
    data = await request.json()  # Get JSON data
    text = data.get("text")
    if not text:
        return {"error": "No text provided"}
    result = process_text(text) + "961"
    return {"processed_text": result}  # Return processed text

