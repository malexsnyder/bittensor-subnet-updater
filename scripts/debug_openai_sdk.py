#!/usr/bin/env python3
"""
OpenAI SDK Version and API Structure Debug Script

This script helps identify the exact OpenAI SDK version and available API methods.
"""

import os
import sys

def debug_openai_sdk():
    """Debug OpenAI SDK version and API structure."""
    
    print("🔍 OpenAI SDK Debug Information")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        print("💡 Set it with: export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Import and check version
    try:
        import openai
        version = getattr(openai, '__version__', 'unknown')
        print(f"📦 OpenAI SDK version: {version}")
    except Exception as e:
        print(f"❌ Error importing openai: {e}")
        return False
    
    # Check available attributes
    print(f"\n🔍 OpenAI module attributes:")
    attrs = [attr for attr in dir(openai) if not attr.startswith('_')]
    for attr in attrs[:20]:  # Show first 20
        print(f"   - {attr}")
    if len(attrs) > 20:
        print(f"   ... and {len(attrs) - 20} more")
    
    # Try different client approaches
    print(f"\n🔍 Testing client creation methods:")
    
    # Method 1: New client
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        print("✅ New OpenAI client created successfully")
        
        # Check client attributes
        print(f"   Client type: {type(client)}")
        client_attrs = [attr for attr in dir(client) if not attr.startswith('_')]
        print(f"   Client attributes: {client_attrs[:10]}...")
        
        # Check for files API
        if hasattr(client, 'files'):
            print("✅ client.files exists")
            files_attrs = [attr for attr in dir(client.files) if not attr.startswith('_')]
            print(f"   files attributes: {files_attrs}")
        else:
            print("❌ client.files does not exist")
            
        # Check for vector_stores API
        if hasattr(client, 'vector_stores'):
            print("✅ client.vector_stores exists")
            vs_attrs = [attr for attr in dir(client.vector_stores) if not attr.startswith('_')]
            print(f"   vector_stores attributes: {vs_attrs}")
            
            if hasattr(client.vector_stores, 'files'):
                print("✅ client.vector_stores.files exists")
                vs_files_attrs = [attr for attr in dir(client.vector_stores.files) if not attr.startswith('_')]
                print(f"   vector_stores.files attributes: {vs_files_attrs}")
            else:
                print("❌ client.vector_stores.files does not exist")
        else:
            print("❌ client.vector_stores does not exist")
            
    except Exception as e:
        print(f"❌ New client creation failed: {e}")
    
    # Method 2: Legacy client
    try:
        import openai
        openai.api_key = api_key
        print("✅ Legacy OpenAI client configured")
        
        # Check legacy attributes
        legacy_attrs = [attr for attr in dir(openai) if not attr.startswith('_') and attr[0].isupper()]
        print(f"   Legacy API classes: {legacy_attrs}")
        
    except Exception as e:
        print(f"❌ Legacy client configuration failed: {e}")
    
    print(f"\n📋 Summary:")
    print(f"   SDK Version: {version}")
    print(f"   New Client: {'✅' if 'OpenAI' in str(type(client)) else '❌'}")
    print(f"   Legacy Client: {'✅' if hasattr(openai, 'api_key') else '❌'}")
    
    return True

if __name__ == "__main__":
    debug_openai_sdk()
