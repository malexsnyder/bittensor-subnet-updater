#!/usr/bin/env python3
"""
OpenAI File Upload Script

This script uploads subnet profile data to OpenAI for use with AI agents.
It reads the OpenAI API key from the OPENAI_API_KEY environment variable
and uploads the consolidated profiles to a file search or vector store.
"""

import os
import json
import tempfile
from pathlib import Path
from openai import OpenAI
from typing import Optional

def get_openai_client() -> OpenAI:
    """Initialize OpenAI client with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    return OpenAI(api_key=api_key)

def consolidate_profiles() -> str:
    """Consolidate all subnet profiles into a single text file."""
    profiles_dir = Path("data/profiles")
    
    if not profiles_dir.exists():
        raise FileNotFoundError("data/profiles directory not found. Run build_profiles_local.py first.")
    
    consolidated_content = []
    consolidated_content.append("# Bittensor Subnet Profiles\n")
    consolidated_content.append(f"Generated on: {os.popen('date').read().strip()}\n")
    consolidated_content.append(f"Total profiles: {len(list(profiles_dir.glob('*.md')))}\n")
    consolidated_content.append("=" * 80 + "\n\n")
    
    # Sort profile files by subnet ID
    profile_files = sorted(profiles_dir.glob("*.md"), key=lambda x: int(x.stem.split('_')[0]))
    
    for profile_file in profile_files:
        with open(profile_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        consolidated_content.append(content)
        consolidated_content.append("\n" + "=" * 80 + "\n\n")
    
    return "\n".join(consolidated_content)

def upload_to_openai(content: str, filename: str = "bittensor_subnet_profiles.txt") -> Optional[str]:
    """Upload content to OpenAI file search."""
    client = get_openai_client()
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    try:
        print(f"Uploading {filename} to OpenAI...")
        
        # Upload file to OpenAI
        with open(temp_file_path, 'rb') as f:
            uploaded_file = client.files.create(
                file=f,
                purpose="file-search"  # Use file-search for AI agent access
            )
        
        print(f"✅ Successfully uploaded file with ID: {uploaded_file.id}")
        print(f"📁 File name: {uploaded_file.filename}")
        print(f"📊 File size: {uploaded_file.bytes} bytes")
        
        return uploaded_file.id
        
    except Exception as e:
        print(f"❌ Error uploading to OpenAI: {e}")
        return None
    
    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)

def list_existing_files():
    """List existing files in OpenAI account."""
    try:
        client = get_openai_client()
        files = client.files.list()
        
        print("\n📋 Existing files in your OpenAI account:")
        for file in files.data:
            if file.purpose == "file-search":
                print(f"  - {file.filename} (ID: {file.id}, Size: {file.bytes} bytes)")
        
        return files.data
    
    except Exception as e:
        print(f"❌ Error listing files: {e}")
        return []

def main():
    """Main function to consolidate and upload subnet profiles."""
    print("🚀 Starting OpenAI upload process...")
    
    try:
        # Check if we have subnet data
        subnets_json = Path("data/subnets.json")
        if not subnets_json.exists():
            print("❌ No subnet data found. Please run fetch_subnets_bt.py first.")
            return
        
        # Consolidate profiles
        print("📝 Consolidating subnet profiles...")
        consolidated_content = consolidate_profiles()
        
        # Show preview
        print(f"📊 Consolidated content length: {len(consolidated_content)} characters")
        print(f"📄 Preview (first 200 chars):")
        print(consolidated_content[:200] + "..." if len(consolidated_content) > 200 else consolidated_content)
        
        # List existing files
        list_existing_files()
        
        # Upload to OpenAI
        file_id = upload_to_openai(consolidated_content)
        
        if file_id:
            print(f"\n🎉 Upload completed successfully!")
            print(f"📋 File ID: {file_id}")
            print(f"💡 You can now use this file in your OpenAI Assistant or API calls")
            print(f"🔗 Use file ID '{file_id}' to reference this data in your AI applications")
        else:
            print("\n❌ Upload failed. Please check your API key and try again.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
