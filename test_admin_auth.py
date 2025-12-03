#!/usr/bin/env python3
"""
Test script to verify admin credentials
"""

from api.admin import ADMIN_USERNAME, ADMIN_PASSWORD

print("=" * 60)
print("Admin Credentials Check")
print("=" * 60)
print()
print(f"Username: {ADMIN_USERNAME}")
print(f"Password: {ADMIN_PASSWORD}")
print()
print("=" * 60)
print("To access the admin page:")
print(f"  URL: http://localhost:8000/admin-flow-control-secret-2024")
print(f"  Username: {ADMIN_USERNAME}")
print(f"  Password: {ADMIN_PASSWORD}")
print("=" * 60)
print()
print("If you're getting 401 Unauthorized:")
print("  1. Make sure you're using the exact credentials above")
print("  2. Try incognito/private browsing mode")
print("  3. Clear browser cache")
print("  4. Try a different browser")

