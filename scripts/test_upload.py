#!/usr/bin/env python3
"""
Test script for OpenAI upload functionality

This script tests the upload_to_openai.py script locally.
Make sure to set your OPENAI_API_KEY environment variable before running.
"""

import os
import sys
from pathlib import Path

def test_upload():
    """Test the OpenAI upload functionality."""
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("💡 Set it with: export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    # Check if we have the required data
    if not Path("data/subnets.json").exists():
        print("❌ No subnet data found. Run fetch_subnets_bt.py first")
        return False
    
    if not Path("data/profiles").exists():
        print("❌ No profiles found. Run build_profiles_local.py first")
        return False
    
    # Import and run the upload script
    try:
        sys.path.append(str(Path("scripts")))
        from upload_to_openai import main
        
        print("🧪 Testing OpenAI upload...")
        result = main()
        
        if result == 0:
            print("✅ Test completed successfully!")
            return True
        else:
            print("❌ Test failed")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = test_upload()
    sys.exit(0 if success else 1)
