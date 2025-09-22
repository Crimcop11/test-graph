"""
Authentication module for LangGraph Platform deployment
This handles API key validation for securing the endpoint
"""
from langgraph_sdk import Auth
import os

# Initialize authentication
auth = Auth()

# Define valid API keys (in production, store these securely)
VALID_API_KEYS = {
    "test-api-key-123": {"user_id": "user-1", "permissions": ["read", "write"]},
    "frontend-api-key-456": {"user_id": "frontend", "permissions": ["read", "write"]},
    # Add more API keys as needed
}

@auth.authenticate
async def authenticate(headers: dict) -> Auth.types.MinimalUserDict:
    """
    Authenticate requests using API key from headers
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
    
    # Validate API key
    if api_key not in VALID_API_KEYS:
        raise Auth.exceptions.HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    # Get user info
    user_info = VALID_API_KEYS[api_key]
    
    return {
        "identity": user_info["user_id"],
        "is_authenticated": True,
        "permissions": user_info["permissions"]
    }
