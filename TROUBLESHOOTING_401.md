# Fixing 401 Unauthorized Error

## Current Credentials

- **Username:** `admin`
- **Password:** `admin123`
- **URL:** `http://localhost:8000/admin-flow-control-secret-2024`

## Common Causes & Solutions

### 1. Browser Caching Old Credentials

**Solution:** Clear browser cache or use incognito mode

**Chrome/Edge:**
- Press `Ctrl+Shift+N` (Windows) or `Cmd+Shift+N` (Mac) for incognito
- Or: Settings → Privacy → Clear browsing data → Cached images and files

**Firefox:**
- Press `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (Mac) for private window

**Safari:**
- Press `Cmd+Shift+N` for private window

### 2. Wrong Credentials Entered

**Check:**
- Username is exactly: `admin` (lowercase, no spaces)
- Password is exactly: `admin123` (no spaces before/after)
- Both are case-sensitive

### 3. Browser Not Prompting for Credentials

**Solution:** Manually enter credentials in URL

Try accessing:
```
http://admin:admin123@localhost:8000/admin-flow-control-secret-2024
```

**Note:** Some browsers block this format. If it doesn't work, use incognito mode instead.

### 4. Server Not Running

**Check:** Make sure the server is running:
```bash
# Should see: "Uvicorn running on http://0.0.0.0:8000"
```

### 5. Wrong URL

**Correct URL:**
```
http://localhost:8000/admin-flow-control-secret-2024
```

**Common mistakes:**
- Missing `http://`
- Wrong port (should be 8000)
- Wrong path (should match exactly)

## Step-by-Step Fix

1. **Stop the server** (Ctrl+C if running)

2. **Clear browser cache** or use incognito mode

3. **Restart server:**
   ```bash
   ./start_admin.sh
   ```

4. **Open NEW incognito/private window**

5. **Visit:** `http://localhost:8000/admin-flow-control-secret-2024`

6. **When prompted, enter:**
   - Username: `admin`
   - Password: `admin123`

7. **Check "Remember password" if you want** (optional)

## Test Authentication

Run this to verify credentials:
```bash
python test_admin_auth.py
```

## Change Credentials

If you want to change the credentials, edit `api/admin.py`:

```python
ADMIN_USERNAME = "your-new-username"  # Change this!
ADMIN_PASSWORD = "your-new-password"  # Change this!
```

Then restart the server.

## Still Not Working?

1. Check server logs for errors
2. Try accessing `http://localhost:8000/health` (should return `{"status":"ok"}`)
3. Verify the admin route is registered:
   ```bash
   curl -u admin:admin123 http://localhost:8000/admin-flow-control-secret-2024
   ```

