# Login Flow Control Integration Guide

## Overview

The flow control layer provides a non-invasive way to override post-login redirects. By default, it has zero impact on existing behavior.

## Integration Point

In your existing post-login redirect code, replace the final destination assignment with a call to the hook:

### Before:
```python
# Existing post-login redirect code
user_id = get_current_user_id()  # Your existing function
default_route = "/dashboard"  # Your existing default route
redirect_url = default_route
```

### After:
```python
# Existing post-login redirect code
from flow_control.login_hook import resolve_login_redirect

user_id = get_current_user_id()  # Your existing function
default_route = "/dashboard"  # Your existing default route
redirect_url = resolve_login_redirect(user_id, default_route)
```

That's it! The hook will:
- Return `default_route` if no override exists (preserves current behavior)
- Return `forced_route` if a valid override exists
- Automatically ignore and clear expired overrides
- Fall back to `default_route` on any errors

## Setting Overrides (Future Admin Control)

For now, overrides can be set programmatically:

```python
from flow_control.service import force_post_login_route
from datetime import datetime, timedelta

# Set an override that expires in 24 hours
expires_at = datetime.utcnow() + timedelta(hours=24)
force_post_login_route(
    user_id="user123",
    route="/special-page",
    expires_at=expires_at,
    updated_by="admin"
)

# Set a permanent override (no expiration)
force_post_login_route(
    user_id="user456",
    route="/another-page",
    updated_by="admin"
)

# Clear an override
from flow_control.service import release_post_login
release_post_login("user123")
```

## FastAPI Endpoints (Future Use)

The FastAPI app in `api/main.py` provides REST endpoints for future admin control (e.g., Signal/Telegram integration):

- `POST /api/flow-control/override` - Set override
- `DELETE /api/flow-control/override/{user_id}` - Clear override
- `GET /api/flow-control/override/{user_id}` - Get override

These are not used in the initial scope but are available for future integration.

## Database

The SQLite database (`flow_control.db`) is automatically created on first use. No manual setup required.

## Error Handling

All functions gracefully handle errors:
- Store functions return `None` or silently fail
- Service functions return `None` if no valid override
- Hook function always returns `default_route` on error

This ensures the system never breaks existing functionality.

