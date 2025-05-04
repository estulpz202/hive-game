from fastapi import FastAPI  # type: ignore

app = FastAPI()

@app.get("/health")
def health_check():
    """Health check endpoint to verify if the API is running."""
    return {"status": "ok"}
