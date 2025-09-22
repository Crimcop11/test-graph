"""
Authentication module for LangGraph Platform deployment
This handles API key validation for securing the endpoint
"""
from langgraph_sdk import Auth
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional

# Initialize authentication
auth = Auth()

# Load API keys from environment variables for better security
def load_api_keys() -> Dict[str, dict]:
    """Load API keys from environment variables"""
    api_keys = {}
    
    # Load keys from environment (format: KEY1:USER1:PERMISSIONS1,KEY2:USER2:PERMISSIONS2)
    keys_env = os.getenv("API_KEYS", "")
    if keys_env:
        for key_config in keys_env.split(","):
            if ":" in key_config:
                parts = key_config.strip().split(":")
                if len(parts) >= 2:
                    key = parts[0]
                    user_id = parts[1]
                    permissions = parts[2].split("|") if len(parts) > 2 else ["read", "write"]
                    api_keys[key] = {
                        "user_id": user_id,
                        "permissions": permissions,
                        "created_at": datetime.now().isoformat(),
                        "last_used": None
                    }
    
    # Fallback to default keys if no environment variables set
    if not api_keys:
        api_keys = {
            "lgp_test_" + secrets.token_urlsafe(16): {
                "user_id": "test-user",
                "permissions": ["read", "write"],
                "created_at": datetime.now().isoformat(),
                "last_used": None
            },
            "lgp_frontend_" + secrets.token_urlsafe(16): {
                "user_id": "frontend-app",
                "permissions": ["read", "write"],
                "created_at": datetime.now().isoformat(),
                "last_used": None
            },
            "lgp_admin_" + secrets.token_urlsafe(16): {
                "user_id": "admin",
                "permissions": ["read", "write", "admin"],
                "created_at": datetime.now().isoformat(),
                "last_used": None
            }
        }
    
    return api_keys

# Load API keys
VALID_API_KEYS = load_api_keys()

def validate_api_key_format(api_key: str) -> bool:
    """Validate API key format"""
    if not api_key or len(api_key) < 20:
        return False
    
    # Check if it starts with expected prefix
    if not api_key.startswith(("lgp_", "sk-", "ak-")):
        return False
    
    # Check if it contains only valid characters
    valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
    return all(c in valid_chars for c in api_key)

def log_api_usage(api_key: str, user_info: dict):
    """Log API key usage for monitoring"""
    if api_key in VALID_API_KEYS:
        VALID_API_KEYS[api_key]["last_used"] = datetime.now().isoformat()

@auth.authenticate
async def authenticate(headers: dict) -> Auth.types.MinimalUserDict:
    """
    Authenticate requests using API key from headers with enhanced security
    """
    # Extract API key from headers
    api_key = headers.get(b"x-api-key")
    
    if not api_key:
        # Try alternative header names
        api_key = headers.get(b"authorization")
        if api_key and api_key.startswith(b"Bearer "):
            api_key = api_key[7:]  # Remove "Bearer " prefix
    
    if not api_key:
        raise Auth.exceptions.HTTPException(
            status_code=401,
            detail="API key required. Provide 'x-api-key' header or 'Authorization: Bearer <key>'"
        )
    
    # Decode bytes to string if needed
    if isinstance(api_key, bytes):
        api_key = api_key.decode('utf-8')
    
    # Validate API key format
    if not validate_api_key_format(api_key):
        raise Auth.exceptions.HTTPException(
            status_code=401,
            detail="Invalid API key format"
        )
    
    # Check if API key exists
    if api_key not in VALID_API_KEYS:
        raise Auth.exceptions.HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    # Get user info
    user_info = VALID_API_KEYS[api_key]
    
    # Log API usage for monitoring
    log_api_usage(api_key, user_info)
    
    return {
        "identity": user_info["user_id"],
        "is_authenticated": True,
        "permissions": user_info["permissions"]
    }
