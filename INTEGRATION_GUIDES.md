# Platform Integration Guides

Step-by-step guides for integrating the flow control system into different platforms.

## Table of Contents
1. [Flask](#flask)
2. [Django](#django)
3. [FastAPI](#fastapi)
4. [Express.js (Node.js)](#expressjs-nodejs)
5. [Generic Python](#generic-python)
6. [Custom Backend](#custom-backend)

---

## Flask

### Step 1: Install Dependencies
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Find Your Login Route
Locate your login success handler, typically something like:
```python
@app.route('/login', methods=['POST'])
def login():
    # ... authentication logic ...
    if login_successful:
        return redirect('/dashboard')  # <-- This is what we'll modify
```

### Step 3: Integrate the Hook
```python
from flask import Flask, redirect, session
from flow_control.login_hook import resolve_login_redirect

@app.route('/login', methods=['POST'])
def login():
    # ... your existing authentication logic ...
    
    if login_successful:
        user_id = session.get('user_id')  # or however you get user_id
        default_route = '/dashboard'
        
        # Single line integration
        redirect_url = resolve_login_redirect(user_id, default_route)
        
        return redirect(redirect_url)
```

### Complete Example
```python
from flask import Flask, request, redirect, session, render_template
from flow_control.login_hook import resolve_login_redirect

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Your authentication logic here
        if authenticate_user(username, password):
            user_id = get_user_id(username)  # Your function
            session['user_id'] = user_id
            
            # Integration point - single line change
            default_route = '/dashboard'
            redirect_url = resolve_login_redirect(user_id, default_route)
            
            return redirect(redirect_url)
    
    return render_template('login.html')
```

---

## Django

### Step 1: Install Dependencies
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Find Your Login View
Locate your login view, typically in `views.py`:
```python
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    # ... authentication logic ...
    if user is not None:
        login(request, user)
        return redirect('/dashboard')  # <-- This is what we'll modify
```

### Step 3: Integrate the Hook
```python
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from flow_control.login_hook import resolve_login_redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Integration point - single line change
            default_route = '/dashboard'
            redirect_url = resolve_login_redirect(str(user.id), default_route)
            
            return redirect(redirect_url)
    
    return render(request, 'login.html')
```

### Using Django's LOGIN_REDIRECT_URL
If you're using Django's built-in login system:

**Option A: Override the redirect in your view**
```python
from django.contrib.auth.views import LoginView
from flow_control.login_hook import resolve_login_redirect

class CustomLoginView(LoginView):
    def get_success_url(self):
        default_route = super().get_success_url()  # Gets LOGIN_REDIRECT_URL
        user_id = str(self.request.user.id)
        return resolve_login_redirect(user_id, default_route)
```

**Option B: Use a custom authentication backend**
```python
# In your settings.py or custom auth backend
from flow_control.login_hook import resolve_login_redirect

def get_login_redirect_url(user_id):
    default_route = '/dashboard'  # or settings.LOGIN_REDIRECT_URL
    return resolve_login_redirect(user_id, default_route)
```

---

## FastAPI

### Step 1: Install Dependencies
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Integrate in Your Login Endpoint
```python
from fastapi import FastAPI, Form, HTTPException, RedirectResponse
from fastapi.responses import RedirectResponse
from flow_control.login_hook import resolve_login_redirect

app = FastAPI()

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Your authentication logic
    user = authenticate_user(username, password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Set session/token here
    user_id = str(user.id)
    default_route = "/dashboard"
    
    # Integration point - single line change
    redirect_url = resolve_login_redirect(user_id, default_route)
    
    return RedirectResponse(url=redirect_url, status_code=302)
```

### Complete Example with JWT
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from flow_control.login_hook import resolve_login_redirect
import jwt

app = FastAPI()

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate user
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create token
    access_token = create_access_token(data={"sub": user.username})
    
    # Integration point
    user_id = str(user.id)
    default_route = "/dashboard"
    redirect_url = resolve_login_redirect(user_id, default_route)
    
    return RedirectResponse(url=redirect_url, status_code=302)
```

---

## Express.js (Node.js)

### Step 1: Create Python Bridge
Since Express is Node.js, you'll need to call Python from Node:

**Option A: Use child_process**
```javascript
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

async function resolveLoginRedirect(userId, defaultRoute) {
    const pythonCode = `
from flow_control.login_hook import resolve_login_redirect
print(resolve_login_redirect("${userId}", "${defaultRoute}"))
`;
    
    const { stdout } = await execPromise(
        `python3 -c "${pythonCode.replace(/\n/g, ' ')}"`
    );
    
    return stdout.trim();
}

// In your login route
app.post('/login', async (req, res) => {
    // ... authentication logic ...
    
    if (loginSuccessful) {
        const userId = req.user.id;
        const defaultRoute = '/dashboard';
        
        const redirectUrl = await resolveLoginRedirect(userId, defaultRoute);
        res.redirect(redirectUrl);
    }
});
```

**Option B: Use FastAPI as Microservice**
Run the FastAPI server separately and call it from Express:

```javascript
// In Express
const axios = require('axios');

async function resolveLoginRedirect(userId, defaultRoute) {
    try {
        // Call your FastAPI endpoint
        const response = await axios.post('http://localhost:8000/api/resolve-redirect', {
            user_id: userId,
            default_route: defaultRoute
        });
        return response.data.redirect_url;
    } catch (error) {
        return defaultRoute; // Fallback
    }
}
```

Then add this endpoint to `api/main.py`:
```python
@app.post("/api/resolve-redirect")
async def resolve_redirect(request: dict):
    from flow_control.login_hook import resolve_login_redirect
    redirect_url = resolve_login_redirect(
        request["user_id"], 
        request["default_route"]
    )
    return {"redirect_url": redirect_url}
```

---

## Generic Python

### For Any Python Web Framework

```python
from flow_control.login_hook import resolve_login_redirect

def handle_login_success(user_id: str, default_route: str = "/dashboard"):
    """
    Generic login success handler.
    
    Args:
        user_id: User identifier (string)
        default_route: Default redirect route if no override
    
    Returns:
        Final redirect URL
    """
    return resolve_login_redirect(user_id, default_route)

# Usage in your code:
user_id = get_current_user_id()  # Your function
redirect_url = handle_login_success(user_id, "/dashboard")
return redirect(redirect_url)
```

---

## Custom Backend

### Step 1: Identify Your Login Flow

Find where users are redirected after successful login:
- Look for `redirect()` calls
- Search for `return redirect(...)`
- Find `Location` header setting
- Look for JavaScript `window.location` assignments

### Step 2: Add the Import

At the top of your file:
```python
from flow_control.login_hook import resolve_login_redirect
```

### Step 3: Replace the Redirect

**Before:**
```python
# Your existing code
user_id = get_user_id()  # However you get the user ID
redirect_url = "/dashboard"  # Your default route
return redirect(redirect_url)
```

**After:**
```python
# Your existing code
user_id = get_user_id()  # However you get the user ID
default_route = "/dashboard"  # Your default route

# Single line integration
redirect_url = resolve_login_redirect(user_id, default_route)
return redirect(redirect_url)
```

### Step 4: Test

1. Test without override (should use default route)
2. Set an override: `force_post_login_route("test_user", "/special-page")`
3. Test with override (should redirect to special page)
4. Clear override: `release_post_login("test_user")`
5. Test again (should use default route)

---

## Setting Overrides (Admin Control)

### Programmatically
```python
from flow_control.service import force_post_login_route, release_post_login
from datetime import datetime, timedelta, timezone

# Set permanent override
force_post_login_route("user123", "/special-page", updated_by="admin")

# Set temporary override (24 hours)
expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
force_post_login_route(
    "user456", 
    "/temporary-page", 
    expires_at=expires_at,
    updated_by="admin"
)

# Clear override
release_post_login("user123")
```

### Via API (if using FastAPI)
```bash
# Start server
uvicorn api.main:app --reload

# Set override
curl -X POST "http://localhost:8000/api/flow-control/override" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "route": "/special-page", "updated_by": "admin"}'

# Get override
curl "http://localhost:8000/api/flow-control/override/user123"

# Clear override
curl -X DELETE "http://localhost:8000/api/flow-control/override/user123"
```

---

## Common Patterns

### Pattern 1: Session-Based Login
```python
from flow_control.login_hook import resolve_login_redirect

def login_handler(request):
    # Authenticate
    user = authenticate(request.POST['username'], request.POST['password'])
    
    if user:
        request.session['user_id'] = str(user.id)
        default_route = '/dashboard'
        redirect_url = resolve_login_redirect(str(user.id), default_route)
        return redirect(redirect_url)
```

### Pattern 2: Token-Based Login
```python
from flow_control.login_hook import resolve_login_redirect

def login_handler(request):
    user = authenticate(request.POST['username'], request.POST['password'])
    
    if user:
        token = create_token(user)
        user_id = str(user.id)
        default_route = '/dashboard'
        redirect_url = resolve_login_redirect(user_id, default_route)
        return redirect(f"{redirect_url}?token={token}")
```

### Pattern 3: OAuth/SSO Login
```python
from flow_control.login_hook import resolve_login_redirect

def oauth_callback(request):
    # Handle OAuth callback
    user = get_or_create_user_from_oauth(request)
    
    if user:
        user_id = str(user.id)
        default_route = '/dashboard'
        redirect_url = resolve_login_redirect(user_id, default_route)
        return redirect(redirect_url)
```

---

## Testing Your Integration

1. **Test default behavior:**
   ```python
   # Should return default route
   result = resolve_login_redirect("test_user", "/dashboard")
   assert result == "/dashboard"
   ```

2. **Test with override:**
   ```python
   from flow_control.service import force_post_login_route
   
   force_post_login_route("test_user", "/special-page")
   result = resolve_login_redirect("test_user", "/dashboard")
   assert result == "/special-page"
   ```

3. **Test expiration:**
   ```python
   from datetime import datetime, timedelta, timezone
   
   past = datetime.now(timezone.utc) - timedelta(hours=1)
   force_post_login_route("test_user", "/expired", expires_at=past)
   result = resolve_login_redirect("test_user", "/dashboard")
   assert result == "/dashboard"  # Should ignore expired override
   ```

---

## Troubleshooting

### Issue: Import Error
**Solution:** Make sure you're in the virtual environment:
```bash
source .venv/bin/activate
```

### Issue: Module Not Found
**Solution:** Check that `flow_control` directory is in your Python path or project root.

### Issue: Database Errors
**Solution:** The database is auto-created. Check file permissions:
```bash
ls -la flow_control.db
```

### Issue: Override Not Working
**Solution:** 
1. Check user_id format matches what you're setting
2. Verify override exists: `get_login_flow(user_id)`
3. Check expiration hasn't passed

---

## Next Steps

1. ✅ Integrate the hook in your login flow
2. ✅ Test with and without overrides
3. ✅ Set up admin interface (optional)
4. ✅ Configure Signal/Telegram integration (future)

For more details, see:
- `USAGE_GUIDE.md` - Detailed usage examples
- `INTEGRATION_EXAMPLE.md` - Code examples
- `README_FLOW_CONTROL.md` - Architecture docs

