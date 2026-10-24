"""
FastAPI Microservices Routing Endpoints for V2X Gateway and Mobile Terminals
"""
from fastapi import APIRouter, HTTPException
from backend.app.core.db import get_latest_active_dispatch, get_all_records, update_status, acknowledge_hospital, acknowledge_police
from backend.app.services.ann_service import ann_engine
from backend.app.services.corridor_service import corridor_engine

router = APIRouter()

@router.get("/status")
def get_corridor_status():
    active = get_latest_active_dispatch()
    return {"active_emergency": active is not None, "data": active}

@router.get("/records")
def get_all_dispatches():
    return {"total_cases": len(get_all_records()), "dispatches": get_all_records()}

@router.post("/acknowledge/hospital/{incident_id}")
def ack_hospital(incident_id: str):
    acknowledge_hospital(incident_id)
    return {"status": "SUCCESS", "message": f"Hospital ICU Acknowledged #{incident_id}"}

@router.post("/acknowledge/police/{incident_id}")
def ack_police(incident_id: str):
    acknowledge_police(incident_id)
    return {"status": "SUCCESS", "message": f"Police Escort Mobilized #{incident_id}"}

@router.post("/resolve/{incident_id}")
def resolve_corridor(incident_id: str):
    update_status(incident_id, "RESOLVED")
    return {"status": "SUCCESS", "message": f"Corridor #{incident_id} Resolved."}

