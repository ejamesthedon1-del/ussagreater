"""
Minimal FastAPI app for future admin control endpoints.

This is a placeholder structure for future Signal/Telegram integration.
Not used in initial scope - login hook is integrated directly.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from flow_control.service import force_post_login_route, release_post_login, resolve_post_login_destination
from flow_control.store import get_login_flow
from api.admin import create_admin_routes


app = FastAPI(
    title="Flow Control API",
    description="Server-side flow control layer for login redirects",
    version="1.0.0"
)

# Add hidden admin routes
create_admin_routes(app)


class OverrideRequest(BaseModel):
    """Request model for setting login flow override."""
    user_id: str
    route: str
    expires_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    message: Optional[str] = None


@app.post("/api/flow-control/override")
async def set_override(request: OverrideRequest):
    """
    Set login flow override for a user.
    
    Future endpoint for admin control (Signal/Telegram integration).
    """
    force_post_login_route(
        user_id=request.user_id,
        route=request.route,
        expires_at=request.expires_at,
        updated_by=request.updated_by
    )
    return {"status": "success", "user_id": request.user_id}


@app.delete("/api/flow-control/override/{user_id}")
async def clear_override(user_id: str):
    """
    Clear login flow override for a user.
    
    Future endpoint for admin control (Signal/Telegram integration).
    """
    release_post_login(user_id)
    return {"status": "success", "user_id": user_id}


@app.get("/api/flow-control/override/{user_id}")
async def get_override(user_id: str):
    """
    Get login flow override for a user.
    
    Future endpoint for admin control (Signal/Telegram integration).
    """
    flow = get_login_flow(user_id)
    if flow is None:
        raise HTTPException(status_code=404, detail="No override found")
    
    return {
        "user_id": flow["user_id"],
        "forced_route": flow["forced_route"],
        "message": flow["message"],
        "expires_at": flow["expires_at"].isoformat() if flow["expires_at"] else None,
        "updated_at": flow["updated_at"].isoformat(),
        "updated_by": flow["updated_by"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

