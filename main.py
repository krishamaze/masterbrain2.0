"""Application entrypoint for the masterbrain2.0 FastAPI service."""
from typing import Any, Dict

from fastapi import FastAPI


app = FastAPI(title="MasterBrain 2.0 API")


def build_ingest_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Create a simple acknowledgement response for ingest requests."""
    return {"status": "received", "payload": payload}


@app.post("/ingest")
async def ingest(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Accept payload data and return a confirmation response."""
    return build_ingest_response(payload)


@app.get("/")
async def read_root() -> Dict[str, str]:
    """Basic health check endpoint."""
    return {"message": "MasterBrain 2.0 API is running"}
