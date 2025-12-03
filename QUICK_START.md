# Quick Start - Activate and Use Flow Control

## Step 1: Activate Virtual Environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

You should see `(.venv)` in your terminal prompt.

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Use the System

### Option A: Use in Your Code (Recommended)

Add this single line to your login redirect code:

```python
from flow_control.login_hook import resolve_login_redirect

# Replace: redirect_url = default_route
# With:
redirect_url = resolve_login_redirect(user_id, default_route)
```

### Option B: Test It Now

Run the example script:
```bash
python example_usage.py
```

### Option C: Start the API Server

```bash
uvicorn api.main:app --reload
```

Then visit: http://localhost:8000/docs

## Step 4: Set Overrides

```python
from flow_control.service import force_post_login_route

force_post_login_route("user123", "/special-page", updated_by="admin")
```

## Deactivate Virtual Environment

When done:
```bash
deactivate
```

