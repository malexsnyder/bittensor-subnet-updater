#!/usr/bin/env python3
"""
OpenAI Vector Store Diagnostic Script

This script helps diagnose common issues with OpenAI vector store connections.
Run this locally to test your setup before using it in GitHub Actions.
"""

import os
import sys
from pathlib import Path

def test_openai_connection():
    """Test OpenAI connection and vector store access."""
    
    print("🔍 OpenAI Vector Store Diagnostic Tool")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        print("💡 Set it with: export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    if not api_key.startswith("sk-"):
        print("❌ OPENAI_API_KEY does not appear to be valid (should start with 'sk-')")
        return False
    
    print(f"✅ API key format looks correct (starts with: {api_key[:10]}...)")
    
    # Test OpenAI import
    try:
        import openai
        print(f"✅ OpenAI SDK imported successfully")
        print(f"📦 OpenAI version: {getattr(openai, '__version__', 'unknown')}")
    except ImportError as e:
        print(f"❌ Error importing openai: {e}")
        return False
    
    # Test new client
    try:
        from openai import OpenAI
        print("✅ New OpenAI client interface available")
    except ImportError as e:
        print(f"❌ New OpenAI client not available: {e}")
        return False
    
    # Test client creation
    try:
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client created successfully")
    except Exception as e:
        print(f"❌ Error creating OpenAI client: {e}")
        return False
    
    # Test vector store access
    vector_store_id = "vs_68f441099ff88191a84e2e4dadfdc104"
    print(f"\n🔍 Testing vector store access: {vector_store_id}")
    
    try:
        vector_store = client.vector_stores.retrieve(vector_store_id)
        print(f"✅ Vector store found: {vector_store.name}")
        print(f"📊 Vector store status: {vector_store.status}")
        print(f"📁 File count: {vector_store.file_counts.total}")
        print(f"💾 Usage: {vector_store.usage_bytes} bytes")
    except Exception as e:
        print(f"❌ Error accessing vector store: {e}")
        print("\n💡 Common issues:")
        print("   - Vector store ID is incorrect")
        print("   - API key doesn't have access to this vector store")
        print("   - Vector store has been deleted")
        print("   - API key has insufficient permissions")
        return False
    
    # Test file upload (with a small test file)
    print(f"\n📤 Testing file upload...")
    
    # Create a small test file
    test_content = "This is a test file for OpenAI vector store upload."
    test_file_path = "test_upload.txt"
    
    try:
        with open(test_file_path, "w") as f:
            f.write(test_content)
        
        with open(test_file_path, "rb") as f:
            file_object = client.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store_id,
                file=f
            )
        
        print(f"✅ Test file uploaded successfully!")
        print(f"📁 File ID: {file_object.id}")
        print(f"📊 Status: {file_object.status}")
        
        # Clean up test file
        os.remove(test_file_path)
        
    except Exception as e:
        print(f"❌ Error uploading test file: {e}")
        print("\n💡 Common upload issues:")
        print("   - File is too large")
        print("   - Vector store is full")
        print("   - File format not supported")
        print("   - Network connectivity issues")
        return False
    
    print(f"\n🎉 All tests passed! Your OpenAI vector store setup is working correctly.")
    return True

def check_data_files():
    """Check if required data files exist."""
    print(f"\n📁 Checking data files...")
    
    required_files = [
        "data/subnets.json",
        "data/profiles"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    if Path("data/profiles").exists():
        profile_count = len(list(Path("data/profiles").glob("*.md")))
        print(f"📊 Found {profile_count} profile files")
    
    return all_exist

def main():
    """Main diagnostic function."""
    print("🚀 Starting OpenAI Vector Store Diagnostics\n")
    
    # Check data files
    data_ok = check_data_files()
    
    # Test OpenAI connection
    openai_ok = test_openai_connection()
    
    print(f"\n📋 Diagnostic Summary:")
    print(f"   Data files: {'✅ OK' if data_ok else '❌ Missing'}")
    print(f"   OpenAI connection: {'✅ OK' if openai_ok else '❌ Failed'}")
    
    if data_ok and openai_ok:
        print(f"\n🎉 Everything looks good! Your setup should work in GitHub Actions.")
    else:
        print(f"\n⚠️  Issues found. Please fix the problems above before running GitHub Actions.")
    
    return 0 if (data_ok and openai_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
