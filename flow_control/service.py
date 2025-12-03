"""
Business logic layer for resolving post-login destinations.

Pure business logic with no side effects beyond calling store layer.
"""

from datetime import datetime, timezone
from typing import Optional
from .store import get_login_flow, set_login_flow, clear_login_flow


def resolve_post_login_destination(user_id: str) -> Optional[str]:
    """
    Resolve post-login destination for a user.
    
    Checks for valid override, ignoring expired ones and auto-clearing them.
    
    Args:
        user_id: User identifier
        
    Returns:
        Forced route if valid override exists, None otherwise
    """
    flow = get_login_flow(user_id)
    
    if flow is None:
        return None
    
    # Check expiration
    if flow["expires_at"] is not None:
        now = datetime.now(timezone.utc)
        expires_at = flow["expires_at"]
        
        # Handle timezone-aware datetime comparison
        if isinstance(expires_at, datetime):
            # Ensure both are timezone-aware for comparison
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            if expires_at < now:
                # Expired - clear it and return None
                clear_login_flow(user_id)
                return None
    
    # Return forced route if present
    return flow.get("forced_route")


def force_post_login_route(
    user_id: str,
    route: str,
    expires_at: Optional[datetime] = None,
    updated_by: Optional[str] = None
) -> None:
    """
    Force a post-login route for a user.
    
    Args:
        user_id: User identifier
        route: Route to redirect to after login
        expires_at: Optional expiration timestamp
        updated_by: Optional identifier of who set this override
    """
    set_login_flow(
        user_id=user_id,
        forced_route=route,
        expires_at=expires_at,
        updated_by=updated_by
    )


def release_post_login(user_id: str) -> None:
    """
    Release (clear) post-login override for a user.
    
    Args:
        user_id: User identifier
    """
    clear_login_flow(user_id)

