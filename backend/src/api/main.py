"""Entrypoint for the FastAPI Hive backend server."""
from fastapi import FastAPI  # type: ignore

from api.router import api_router

# Create the FastAPI app instance
app = FastAPI(
    title="Hive Game API",
    description="API for interacting with the Hive board game backend",
    version="0.1.0",
)

# Registers all routes
app.include_router(api_router)

@app.get("/")
def root():
    """Returns welcome message."""
    return {"message": "Welcome to the Hive API!"}
