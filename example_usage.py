#!/usr/bin/env python3
"""
Quick example showing how to use the flow control system.
Run this file to see it in action.
"""

from flow_control.login_hook import resolve_login_redirect
from flow_control.service import force_post_login_route, release_post_login
from flow_control.store import get_login_flow
from datetime import datetime, timedelta, timezone

def main():
    print("=" * 60)
    print("Flow Control System - Interactive Example")
    print("=" * 60)
    print()
    
    user_id = "demo_user"
    default_route = "/dashboard"
    
    # Example 1: No override set
    print("1. Testing WITHOUT override:")
    result = resolve_login_redirect(user_id, default_route)
    print(f"   User: {user_id}")
    print(f"   Default route: {default_route}")
    print(f"   → Redirects to: {result}")
    print(f"   ✓ Returns default route (no override exists)")
    print()
    
    # Example 2: Set an override
    print("2. Setting override to '/special-page':")
    force_post_login_route(user_id, "/special-page", updated_by="demo")
    result = resolve_login_redirect(user_id, default_route)
    print(f"   User: {user_id}")
    print(f"   Default route: {default_route}")
    print(f"   → Redirects to: {result}")
    print(f"   ✓ Override active!")
    print()
    
    # Example 3: Check override details
    print("3. Checking override details:")
    flow = get_login_flow(user_id)
    if flow:
        print(f"   Forced route: {flow['forced_route']}")
        print(f"   Updated by: {flow['updated_by']}")
        print(f"   Updated at: {flow['updated_at']}")
        print(f"   Expires at: {flow['expires_at'] or 'Never'}")
    print()
    
    # Example 4: Clear override
    print("4. Clearing override:")
    release_post_login(user_id)
    result = resolve_login_redirect(user_id, default_route)
    print(f"   → Redirects to: {result}")
    print(f"   ✓ Back to default route")
    print()
    
    # Example 5: Override with expiration
    print("5. Setting override with 1-hour expiration:")
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    force_post_login_route(user_id, "/temporary-page", expires_at=expires_at, updated_by="demo")
    result = resolve_login_redirect(user_id, default_route)
    print(f"   → Redirects to: {result}")
    print(f"   → Expires at: {expires_at}")
    print(f"   ✓ Temporary override set")
    print()
    
    print("=" * 60)
    print("Example complete! Check USAGE_GUIDE.md for more details.")
    print("=" * 60)

if __name__ == "__main__":
    main()

