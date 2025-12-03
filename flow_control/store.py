"""
Storage layer for user login flow overrides.

Pure storage operations with SQLite database.
"""

import sqlite3
from datetime import datetime, timezone
from typing import Optional, Dict
from pathlib import Path


# Database file location
DB_PATH = Path(__file__).parent.parent / "flow_control.db"


def _get_connection() -> sqlite3.Connection:
    """Get database connection, creating database and table if needed."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    
    # Initialize schema if needed
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_login_flow (
            user_id TEXT PRIMARY KEY,
            forced_route TEXT,
            message TEXT,
            expires_at TIMESTAMP,
            updated_at TIMESTAMP NOT NULL,
            updated_by TEXT
        )
    """)
    conn.commit()
    
    return conn


def get_login_flow(user_id: str) -> Optional[Dict]:
    """
    Retrieve login flow override for a user.
    
    Args:
        user_id: User identifier
        
    Returns:
        Dictionary with flow override data, or None if not found
    """
    try:
        conn = _get_connection()
        cursor = conn.execute(
            "SELECT user_id, forced_route, message, expires_at, updated_at, updated_by "
            "FROM user_login_flow WHERE user_id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row is None:
            return None
            
        return {
            "user_id": row["user_id"],
            "forced_route": row["forced_route"],
            "message": row["message"],
            "expires_at": datetime.fromisoformat(row["expires_at"]) if row["expires_at"] else None,
            "updated_at": datetime.fromisoformat(row["updated_at"]),
            "updated_by": row["updated_by"]
        }
    except Exception:
        # Graceful error handling - return None on any error
        return None


def set_login_flow(
    user_id: str,
    forced_route: Optional[str] = None,
    message: Optional[str] = None,
    expires_at: Optional[datetime] = None,
    updated_by: Optional[str] = None
) -> None:
    """
    Set or update login flow override for a user.
    
    Args:
        user_id: User identifier
        forced_route: Route to redirect to after login (None to clear)
        message: Optional message for the override
        expires_at: Optional expiration timestamp
        updated_by: Optional identifier of who set this override
    """
    try:
        conn = _get_connection()
        now = datetime.now(timezone.utc)
        
        # Check if record exists
        cursor = conn.execute(
            "SELECT user_id FROM user_login_flow WHERE user_id = ?",
            (user_id,)
        )
        exists = cursor.fetchone() is not None
        
        if exists:
            # Update existing record
            conn.execute("""
                UPDATE user_login_flow
                SET forced_route = ?,
                    message = ?,
                    expires_at = ?,
                    updated_at = ?,
                    updated_by = ?
                WHERE user_id = ?
            """, (
                forced_route,
                message,
                expires_at.isoformat() if expires_at else None,
                now.isoformat(),
                updated_by,
                user_id
            ))
        else:
            # Insert new record
            conn.execute("""
                INSERT INTO user_login_flow 
                (user_id, forced_route, message, expires_at, updated_at, updated_by)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                forced_route,
                message,
                expires_at.isoformat() if expires_at else None,
                now.isoformat(),
                updated_by
            ))
        
        conn.commit()
        conn.close()
    except Exception:
        # Graceful error handling - silently fail
        pass


def clear_login_flow(user_id: str) -> None:
    """
    Remove login flow override for a user.
    
    Args:
        user_id: User identifier
    """
    try:
        conn = _get_connection()
        conn.execute(
            "DELETE FROM user_login_flow WHERE user_id = ?",
            (user_id,)
        )
        conn.commit()
        conn.close()
    except Exception:
        # Graceful error handling - silently fail
        pass


def get_all_login_flows() -> list:
    """
    Get all login flow overrides.
    
    Returns:
        List of dictionaries with flow override data
    """
    try:
        conn = _get_connection()
        cursor = conn.execute(
            "SELECT user_id, forced_route, message, expires_at, updated_at, updated_by "
            "FROM user_login_flow ORDER BY updated_at DESC"
        )
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            result.append({
                "user_id": row["user_id"],
                "forced_route": row["forced_route"],
                "message": row["message"],
                "expires_at": datetime.fromisoformat(row["expires_at"]) if row["expires_at"] else None,
                "updated_at": datetime.fromisoformat(row["updated_at"]),
                "updated_by": row["updated_by"]
            })
        
        return result
    except Exception:
        return []

