"""
Integration hook for post-login redirect resolution.

Pure function that can be called from existing post-login redirect code.
"""

from .service import resolve_post_login_destination


def resolve_login_redirect(user_id: str, default_route: str) -> str:
    """
    Resolve login redirect destination.
    
    Returns forced route if override exists, otherwise returns default route.
    This is the integration point - call this function instead of using
    default_route directly.
    
    Args:
        user_id: User identifier
        default_route: Default route to use if no override exists
        
    Returns:
        Final redirect route (forced route if override exists, default otherwise)
    """
    try:
        forced_route = resolve_post_login_destination(user_id)
        return forced_route if forced_route is not None else default_route
    except Exception:
        # Graceful error handling - always fall back to default route
        return default_route

