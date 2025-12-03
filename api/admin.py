"""
Hidden Admin Page for Flow Control Management

This page is not linked anywhere and requires authentication.
Access via: /admin/flow-control (or your chosen secret path)
"""

from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets
from flow_control.service import force_post_login_route, release_post_login, resolve_post_login_destination
from flow_control.store import get_login_flow, get_all_login_flows

# Security configuration
SECRET_ADMIN_PATH = "admin-flow-control-secret-2024"  # Change this to something secret!
ADMIN_USERNAME = "admin"  # Change this!
ADMIN_PASSWORD = "admin123"  # Change this!

security = HTTPBasic()


def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify admin credentials"""
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def create_admin_page():
    """Create the admin interface HTML"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flow Control Admin</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 14px; }
        .content { padding: 30px; }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .section h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: 500;
            font-size: 14px;
        }
        input[type="text"],
        input[type="datetime-local"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus,
        input[type="datetime-local"]:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-right: 10px;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-danger {
            background: #e74c3c;
            color: white;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .btn:active {
            transform: translateY(0);
        }
        .override-list {
            margin-top: 20px;
        }
        .override-item {
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .override-info {
            flex: 1;
        }
        .override-info strong {
            color: #333;
            display: block;
            margin-bottom: 5px;
        }
        .override-info span {
            color: #666;
            font-size: 13px;
            display: block;
            margin-top: 3px;
        }
        .override-actions {
            display: flex;
            gap: 10px;
        }
        .alert {
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        .empty-state svg {
            width: 64px;
            height: 64px;
            margin-bottom: 15px;
            opacity: 0.5;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Flow Control Admin</h1>
            <p>Manage user login redirect overrides</p>
        </div>
        <div class="content">
            <!-- Set Override Section -->
            <div class="section">
                <h2>Set Override</h2>
                <form method="POST" action="/admin/flow-control-secret-2024/set">
                    <div class="form-group">
                        <label for="user_id">User ID</label>
                        <input type="text" id="user_id" name="user_id" required placeholder="e.g., user123">
                    </div>
                    <div class="form-group">
                        <label for="route">Redirect Route</label>
                        <input type="text" id="route" name="route" required placeholder="e.g., /special-page">
                    </div>
                    <div class="form-group">
                        <label for="expires_at">Expires At (Optional)</label>
                        <input type="datetime-local" id="expires_at" name="expires_at">
                        <small style="color: #666; font-size: 12px; display: block; margin-top: 5px;">
                            Leave empty for permanent override
                        </small>
                    </div>
                    <div class="form-group">
                        <label for="updated_by">Updated By</label>
                        <input type="text" id="updated_by" name="updated_by" placeholder="Your name/ID">
                    </div>
                    <button type="submit" class="btn btn-primary">Set Override</button>
                </form>
            </div>

            <!-- Current Overrides Section -->
            <div class="section">
                <h2>Current Overrides</h2>
                <div id="overrides-list">
                    <p class="empty-state">Loading overrides...</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Load current overrides
        async function loadOverrides() {
            try {
                const response = await fetch('/admin/flow-control-secret-2024/list');
                const data = await response.json();
                
                const listEl = document.getElementById('overrides-list');
                
                if (data.overrides && data.overrides.length > 0) {
                    listEl.innerHTML = data.overrides.map(override => `
                        <div class="override-item">
                            <div class="override-info">
                                <strong>User ID: ${override.user_id}</strong>
                                <span>Route: ${override.forced_route}</span>
                                <span>Expires: ${override.expires_at || 'Never'}</span>
                                <span>Updated: ${override.updated_at} by ${override.updated_by || 'N/A'}</span>
                            </div>
                            <div class="override-actions">
                                <form method="POST" action="/admin/flow-control-secret-2024/clear" style="display: inline;">
                                    <input type="hidden" name="user_id" value="${override.user_id}">
                                    <button type="submit" class="btn btn-danger">Clear</button>
                                </form>
                            </div>
                        </div>
                    `).join('');
                } else {
                    listEl.innerHTML = '<p class="empty-state">No overrides set</p>';
                }
            } catch (error) {
                document.getElementById('overrides-list').innerHTML = 
                    '<p class="empty-state" style="color: #e74c3c;">Error loading overrides</p>';
            }
        }

        // Load on page load
        loadOverrides();
        
        // Reload after form submission
        document.querySelector('form').addEventListener('submit', function(e) {
            setTimeout(loadOverrides, 500);
        });
    </script>
</body>
</html>
    """


def create_admin_routes(app: FastAPI):
    """Add admin routes to FastAPI app"""
    
    @app.get(f"/{SECRET_ADMIN_PATH}", response_class=HTMLResponse)
    async def admin_page(username: str = Depends(verify_admin)):
        """Hidden admin page - only accessible via direct URL"""
        return create_admin_page()
    
    @app.post(f"/{SECRET_ADMIN_PATH}/set")
    async def set_override(
        request: Request,
        user_id: str = Form(...),
        route: str = Form(...),
        expires_at: Optional[str] = Form(None),
        updated_by: Optional[str] = Form(None),
        username: str = Depends(verify_admin)
    ):
        """Set an override"""
        try:
            expires_datetime = None
            if expires_at:
                # Convert from HTML datetime-local format to datetime
                # datetime-local format: "2024-12-03T14:30"
                if 'T' in expires_at:
                    expires_datetime = datetime.fromisoformat(expires_at)
                else:
                    expires_datetime = datetime.fromisoformat(expires_at.replace(' ', 'T'))
                # Make timezone-aware if not already
                if expires_datetime.tzinfo is None:
                    expires_datetime = expires_datetime.replace(tzinfo=timezone.utc)
            
            force_post_login_route(
                user_id=user_id,
                route=route,
                expires_at=expires_datetime,
                updated_by=updated_by or username
            )
            
            return RedirectResponse(
                url=f"/{SECRET_ADMIN_PATH}?success=Override set successfully",
                status_code=302
            )
        except Exception as e:
            return RedirectResponse(
                url=f"/{SECRET_ADMIN_PATH}?error={str(e)}",
                status_code=302
            )
    
    @app.post(f"/{SECRET_ADMIN_PATH}/clear")
    async def clear_override(
        request: Request,
        user_id: str = Form(...),
        username: str = Depends(verify_admin)
    ):
        """Clear an override"""
        try:
            release_post_login(user_id)
            return RedirectResponse(
                url=f"/{SECRET_ADMIN_PATH}?success=Override cleared",
                status_code=302
            )
        except Exception as e:
            return RedirectResponse(
                url=f"/{SECRET_ADMIN_PATH}?error={str(e)}",
                status_code=302
            )
    
    @app.get(f"/{SECRET_ADMIN_PATH}/list")
    async def list_overrides(username: str = Depends(verify_admin)):
        """Get all current overrides (API endpoint)"""
        overrides = get_all_login_flows()
        
        # Format for JSON response
        formatted_overrides = []
        for override in overrides:
            formatted_overrides.append({
                "user_id": override["user_id"],
                "forced_route": override["forced_route"],
                "expires_at": override["expires_at"].isoformat() if override["expires_at"] else None,
                "updated_at": override["updated_at"].isoformat(),
                "updated_by": override["updated_by"]
            })
        
        return {"overrides": formatted_overrides}
    
    return app

