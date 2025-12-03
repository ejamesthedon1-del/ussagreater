# Hidden Admin Page Access

## 🔒 Secret Admin Interface

A hidden admin page has been created for managing flow control overrides. This page is **not linked anywhere** and requires authentication.

## Access URL

**Default Secret Path:**
```
http://localhost:8000/admin-flow-control-secret-2024
```

⚠️ **IMPORTANT:** Change the secret path in `api/admin.py`:
```python
SECRET_ADMIN_PATH = "your-secret-path-here"  # Change this!
```

## Default Credentials

**Username:** `admin`  
**Password:** `admin123`

⚠️ **IMPORTANT:** Change these in `api/admin.py`:
```python
ADMIN_USERNAME = "your-username"  # Change this!
ADMIN_PASSWORD = "your-password"  # Change this!
```

## How to Access

1. **Start the FastAPI server:**
   ```bash
   source .venv/bin/activate
   uvicorn api.main:app --reload
   ```

2. **Open the secret URL in your browser:**
   ```
   http://localhost:8000/admin-flow-control-secret-2024
   ```

3. **Enter credentials when prompted:**
   - Username: `admin`
   - Password: `admin123`

4. **You'll see the admin interface** with:
   - Form to set new overrides
   - List of current overrides
   - Ability to clear overrides

## Features

- ✅ **Set Overrides:** Set redirect routes for specific users
- ✅ **Set Expiration:** Optional expiration date/time
- ✅ **View All Overrides:** See all current overrides
- ✅ **Clear Overrides:** Remove overrides with one click
- ✅ **Secure:** HTTP Basic Authentication required
- ✅ **Hidden:** Not discoverable - only accessible via direct URL

## Security Recommendations

1. **Change the secret path** to something only you know
2. **Change the admin credentials** to strong passwords
3. **Use HTTPS in production** (the admin page uses HTTP Basic Auth)
4. **Consider IP whitelisting** for additional security
5. **Rotate credentials regularly**

## Customization

Edit `api/admin.py` to customize:
- Secret path (`SECRET_ADMIN_PATH`)
- Admin username (`ADMIN_USERNAME`)
- Admin password (`ADMIN_PASSWORD`)
- Styling (edit the HTML in `create_admin_page()`)

## Example Usage

1. **Set an override:**
   - User ID: `user123`
   - Route: `/special-page`
   - Expires: (optional) Leave empty for permanent
   - Updated By: `admin`

2. **View overrides:**
   - All current overrides appear in the list below

3. **Clear override:**
   - Click "Clear" button next to any override

## Troubleshooting

**Can't access the page?**
- Make sure the FastAPI server is running
- Check the URL matches `SECRET_ADMIN_PATH`
- Verify credentials match `ADMIN_USERNAME` and `ADMIN_PASSWORD`

**Overrides not showing?**
- Check browser console for errors
- Verify database file exists (`flow_control.db`)
- Check server logs for errors

**Authentication not working?**
- Clear browser cache
- Try incognito/private mode
- Verify credentials in `api/admin.py`

