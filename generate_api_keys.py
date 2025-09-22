#!/usr/bin/env python3
"""
API Key Generator for LangGraph Platform deployment
Generates secure API keys and updates environment configuration
"""
import secrets
import os
from datetime import datetime

def generate_api_key(prefix: str = "lgp", length: int = 32) -> str:
    """Generate a secure API key with specified prefix and length"""
    random_part = secrets.token_urlsafe(length)
    return f"{prefix}_{random_part}"

def generate_api_keys():
    """Generate a set of API keys for different use cases"""
    keys = {
        "test": generate_api_key("lgp_test", 24),
        "frontend": generate_api_key("lgp_frontend", 32),
        "admin": generate_api_key("lgp_admin", 40),
        "mobile": generate_api_key("lgp_mobile", 28),
        "webhook": generate_api_key("lgp_webhook", 36)
    }
    
    return keys

def create_env_config(keys: dict):
    """Create environment configuration for API keys"""
    env_lines = []
    env_lines.append("# API Keys for LangGraph Platform Deployment")
    env_lines.append("# Generated on: " + datetime.now().isoformat())
    env_lines.append("")
    
    # Individual key exports
    for name, key in keys.items():
        env_lines.append(f"# {name.upper()}_API_KEY")
        env_lines.append(f"export {name.upper()}_API_KEY=\"{key}\"")
        env_lines.append("")
    
    # Combined API_KEYS environment variable
    api_keys_env = ",".join([
        f"{key}:{name}-user:read|write" 
        for name, key in keys.items()
    ])
    env_lines.append("# Combined API_KEYS for LangGraph Platform")
    env_lines.append(f"export API_KEYS=\"{api_keys_env}\"")
    
    return "\n".join(env_lines)

def main():
    """Generate API keys and create configuration files"""
    print("🔑 Generating secure API keys for LangGraph Platform...")
    
    # Generate keys
    keys = generate_api_keys()
    
    # Display generated keys
    print("\n📋 Generated API Keys:")
    print("=" * 50)
    for name, key in keys.items():
        print(f"{name.upper():<12}: {key}")
    
    # Create environment configuration
    env_config = create_env_config(keys)
    
    # Write to .env.api_keys file (excluded from git)
    with open(".env.api_keys", "w") as f:
        f.write(env_config)
    
    print(f"\n✅ API keys saved to .env.api_keys")
    print("⚠️  Remember to add .env.api_keys to your .gitignore!")
    
    # Create a sample .env file
    sample_env = """# Sample .env file for LangGraph Platform
# Copy the API keys from .env.api_keys to this file

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# LangSmith Configuration
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=your_project_name

# API Keys (copy from .env.api_keys)
# TEST_API_KEY=lgp_test_...
# FRONTEND_API_KEY=lgp_frontend_...
# ADMIN_API_KEY=lgp_admin_...
# MOBILE_API_KEY=lgp_mobile_...
# WEBHOOK_API_KEY=lgp_webhook_...
"""
    
    with open(".env.sample", "w") as f:
        f.write(sample_env)
    
    print("📄 Sample .env file created as .env.sample")
    print("\n🚀 Next steps:")
    print("1. Copy .env.api_keys to .env and add your other environment variables")
    print("2. Update your deployment with the new API keys")
    print("3. Test the API with the generated keys")

if __name__ == "__main__":
    main()
