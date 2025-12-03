# How to Access and Use the Flow Control System

## 1. Install Dependencies

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install fastapi uvicorn
```

## 2. Integration in Your Code

### Basic Integration (Single Line Change)

In your existing post-login redirect code, replace the final destination assignment:

**Before:**
```python
# Your existing code
user_id = get_current_user_id()  # Your function to get user ID
default_route = "/dashboard"      # Your default redirect route
redirect_url = default_route
```

**After:**
```python
# Your existing code
from flow_control.login_hook import resolve_login_redirect

user_id = get_current_user_id()  # Your function to get user ID
default_route = "/dashboard"      # Your default redirect route
redirect_url = resolve_login_redirect(user_id, default_route)
```

That's it! The hook will automatically:
- Return `default_route` if no override exists (preserves current behavior)
- Return `forced_route` if an override is set
- Ignore expired overrides automatically

## 3. Setting Overrides Programmatically

### Set an Override

```python
from flow_control.service import force_post_login_route
from datetime import datetime, timedelta, timezone

# Set a permanent override (no expiration)
force_post_login_route(
    user_id="user123",
    route="/special-page",
    updated_by="admin"
)

# Set an override that expires in 24 hours
expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
force_post_login_route(
    user_id="user456",
    route="/temporary-page",
    expires_at=expires_at,
    updated_by="admin"
)
```

### Clear an Override

```python
from flow_control.service import release_post_login

release_post_login("user123")
```

### Check Current Override

```python
from flow_control.store import get_login_flow

flow = get_login_flow("user123")
if flow:
    print(f"User will be redirected to: {flow['forced_route']}")
    print(f"Expires at: {flow['expires_at']}")
else:
    print("No override set")
```

## 4. Using the FastAPI API Endpoints (Optional)

If you want to use the REST API endpoints for admin control:

### Start the FastAPI Server

```bash
uvicorn api.main:app --reload
```

The server will start on `http://localhost:8000`

### API Endpoints

#### Set Override
```bash
curl -X POST "http://localhost:8000/api/flow-control/override" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "route": "/special-page",
    "updated_by": "admin"
  }'
```

#### Get Override
```bash
curl "http://localhost:8000/api/flow-control/override/user123"
```

#### Clear Override
```bash
curl -X DELETE "http://localhost:8000/api/flow-control/override/user123"
```

#### Health Check
```bash
curl "http://localhost:8000/health"
```

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 5. Example: Complete Integration

Here's a complete example showing how to integrate in a Flask/Django/FastAPI app:

```python
from flow_control.login_hook import resolve_login_redirect

def handle_login_success(user_id: str):
    """Handle successful login - redirect user"""
    
    # Your existing default route logic
    default_route = "/dashboard"
    
    # Integrate flow control hook (single line change)
    redirect_url = resolve_login_redirect(user_id, default_route)
    
    # Your existing redirect code
    return redirect(redirect_url)
```

## 6. Testing the System

Test that everything works:

```python
from flow_control.login_hook import resolve_login_redirect
from flow_control.service import force_post_login_route, release_post_login

# Test 1: No override (should return default)
result = resolve_login_redirect("test_user", "/dashboard")
print(result)  # Output: /dashboard

# Test 2: Set override
force_post_login_route("test_user", "/special-page", updated_by="admin")
result = resolve_login_redirect("test_user", "/dashboard")
print(result)  # Output: /special-page

# Test 3: Clear override
release_post_login("test_user")
result = resolve_login_redirect("test_user", "/dashboard")
print(result)  # Output: /dashboard
```

## 7. Database Location

The SQLite database is automatically created at:
- `flow_control.db` (in the project root)

You can inspect it directly:
```bash
sqlite3 flow_control.db
.tables
SELECT * FROM user_login_flow;
```

## Quick Reference

| Action | Code |
|--------|------|
| **Integrate hook** | `redirect_url = resolve_login_redirect(user_id, default_route)` |
| **Set override** | `force_post_login_route(user_id, route, expires_at=..., updated_by=...)` |
| **Clear override** | `release_post_login(user_id)` |
| **Get override** | `get_login_flow(user_id)` |
| **Start API server** | `uvicorn api.main:app --reload` |

## Need Help?

- See `INTEGRATION_EXAMPLE.md` for detailed integration examples
- See `README_FLOW_CONTROL.md` for architecture documentation
- Check the code comments in each module for function documentation

