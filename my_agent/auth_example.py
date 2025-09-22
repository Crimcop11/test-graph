"""
Example of adding custom authentication to your LangGraph deployment
This is an optional security enhancement you can implement
"""

from langgraph_sdk import Auth
import os

# Initialize authentication
auth = Auth()

@auth.authenticate
async def get_current_user(authorization: str | None) -> Auth.types.MinimalUserDict:
    """Validate API keys and extract user information."""
    if not authorization:
        raise Auth.exceptions.HTTPException(
            status_code=401,
            detail="Authorization header required"
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid authorization scheme")
        
        # Simple API key validation (replace with your logic)
        valid_api_keys = os.getenv("VALID_API_KEYS", "").split(",")
        if token not in valid_api_keys:
            raise ValueError("Invalid API key")
        
        return {
            "identity": f"user_{token[:8]}",
            "email": f"user_{token[:8]}@example.com",
            "is_authenticated": True
        }
        
    except Exception as e:
        raise Auth.exceptions.HTTPException(
            status_code=401,
            detail=f"Authentication failed: {str(e)}"
        )

# Optional: Add resource-level access control
@auth.on.threads.create
async def on_thread_create(
    ctx: Auth.types.AuthContext,
    value: Auth.types.threads.create.value
):
    """Control who can create new conversation threads."""
    # Add any custom logic here
    return value
