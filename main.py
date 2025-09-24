"""Application entrypoint for the masterbrain2.0 FastAPI service."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, status

try:  # pragma: no cover - executed at import time
    import mem0  # type: ignore
except ImportError:  # pragma: no cover - executed when dependency missing
    mem0 = None  # type: ignore[assignment]


logger = logging.getLogger(__name__)

app = FastAPI(title="MasterBrain 2.0 API")


def store_commit_payload(payload: Dict[str, Any]) -> Optional[Any]:
    """Persist commit payload data with mem0 if the integration is available."""

    if mem0 is None or not hasattr(mem0, "add_memory"):
        logger.warning(
            "mem0.add_memory is unavailable; commit payload was not persisted."
        )
        return None

    try:
        return mem0.add_memory(payload)  # type: ignore[attr-defined]
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("mem0.add_memory failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to persist commit data to mem0.",
        ) from exc


def build_ingest_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Create a structured acknowledgement response for ingest requests."""
    memory_reference = store_commit_payload(payload)

    response: Dict[str, Any] = {
        "status": "received",
        "payload": payload,
        "mem0_enabled": memory_reference is not None,
    }

    if memory_reference is not None:
        response["memory_reference"] = memory_reference

    return response


@app.post("/ingest")
async def ingest(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Accept commit payload data and persist it through mem0 when available."""
    return build_ingest_response(payload)


@app.get("/")
async def read_root() -> Dict[str, str]:
    """Basic health check endpoint."""
    return {"message": "MasterBrain 2.0 API is running"}
