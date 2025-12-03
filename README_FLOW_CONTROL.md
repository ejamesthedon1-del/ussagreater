# Login Flow Control Layer

A minimal, non-invasive server-side flow control system for managing post-login redirects.

## Features

- **Zero Impact Default**: Preserves 100% of existing behavior when no override is set
- **Automatic Expiration**: Expired overrides are automatically ignored and cleared
- **Graceful Error Handling**: Always falls back to default route on errors
- **Non-Invasive**: Single-line integration point, no changes to existing code structure

## Quick Start

### Integration

In your existing post-login redirect code:

```python
from flow_control.login_hook import resolve_login_redirect

# Replace this:
redirect_url = default_route

# With this:
redirect_url = resolve_login_redirect(user_id, default_route)
```

### Setting Overrides

```python
from flow_control.service import force_post_login_route
from datetime import datetime, timedelta, timezone

# Set override with expiration
expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
force_post_login_route(
    user_id="user123",
    route="/special-page",
    expires_at=expires_at,
    updated_by="admin"
)

# Clear override
from flow_control.service import release_post_login
release_post_login("user123")
```

## Architecture

### Module Structure

- **`flow_control/store.py`**: SQLite database storage layer
- **`flow_control/service.py`**: Business logic for resolving destinations
- **`flow_control/login_hook.py`**: Integration hook function
- **`api/main.py`**: FastAPI app (for future admin control endpoints)

### Database

SQLite database (`flow_control.db`) is automatically created on first use.

Schema:
- `user_id` (TEXT, PRIMARY KEY)
- `forced_route` (TEXT, nullable)
- `message` (TEXT, nullable)
- `expires_at` (TIMESTAMP, nullable)
- `updated_at` (TIMESTAMP, NOT NULL)
- `updated_by` (TEXT, nullable)

## API Endpoints (Future Use)

FastAPI endpoints available for future admin control (e.g., Signal/Telegram):

- `POST /api/flow-control/override` - Set override
- `DELETE /api/flow-control/override/{user_id}` - Clear override
- `GET /api/flow-control/override/{user_id}` - Get override
- `GET /health` - Health check

## Installation

```bash
pip install -r requirements.txt
```

## Testing

The system has been tested with:
- Basic override setting and retrieval
- Expiration handling (expired overrides auto-cleared)
- Hook function (returns default when no override, override when set)
- Error handling (graceful fallback to default)

## Design Principles

1. **Isolation**: Completely isolated module, no dependencies on existing code
2. **Non-Invasive**: Single integration point, no restructuring required
3. **Fail-Safe**: Always falls back to default behavior on errors
4. **Explicit**: No framework magic, clear boundaries, pure functions

## Future Enhancements

- Signal/Telegram integration for admin control
- Admin UI for managing overrides
- Bulk override operations
- Override templates/presets

