"""
FastAPI Backend Gateway Entry Point
"""
import os
import sys
from pathlib import Path

# Add project root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes import router
from backend.app.core.config import config

app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=config.API_PREFIX)

@app.get("/")
def root():
    return {
        "system": config.PROJECT_NAME,
        "version": config.VERSION,
        "status": "V2X TELEMETRY CORE RUNNING",
        "endpoints": f"{config.API_PREFIX}/status"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)

