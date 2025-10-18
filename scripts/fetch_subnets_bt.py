#!/usr/bin/env python3
"""
Bittensor Subnet Fetcher

This script uses the Bittensor Subtensor SDK to fetch live subnet data directly
from the Bittensor blockchain (Finney network) using only public data.
No credentials or private keys required.
"""

import json
import time
from pathlib import Path
import bittensor as bt
from typing import Dict, List, Any

# Output file
OUT = Path("data/subnets.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

def get_subnet_info(subtensor: bt.Subtensor, subnet_id: int) -> Dict[str, Any]:
    """
    Fetch basic subnet information from the Bittensor blockchain.
    Uses only public data - no credentials required.
    
    Args:
        subtensor: Bittensor Subtensor instance
        subnet_id: The subnet ID to fetch information for
        
    Returns:
        Dictionary containing subnet information
    """
    try:
        # Check if subnet exists
        subnet_exists = subtensor.subnet_exists(subnet_id)
        
        if not subnet_exists:
            return {
                "id": subnet_id,
                "name": f"Subnet {subnet_id}",
                "error": "Subnet does not exist",
                "last_update": int(time.time())
            }
        
        # Get basic subnet information
        data = {
            "id": subnet_id,
            "name": f"Subnet {subnet_id}",
            "exists": subnet_exists,
            "last_update": int(time.time())
        }
        
        # Try to get additional information that might work
        try:
            # Check if subnet is active
            is_active = subtensor.is_subnet_active(subnet_id)
            data["is_active"] = is_active
        except Exception as e:
            data["is_active"] = None
            data["is_active_error"] = str(e)
        
        try:
            # Get subnet owner
            subnet_owner = subtensor.get_subnet_owner_hotkey(subnet_id)
            data["owner_hotkey"] = subnet_owner
        except Exception as e:
            data["owner_hotkey"] = None
            data["owner_error"] = str(e)
        
        try:
            # Get subnet price
            subnet_price = subtensor.get_subnet_price(subnet_id)
            data["price"] = float(subnet_price) if subnet_price else 0
        except Exception as e:
            data["price"] = None
            data["price_error"] = str(e)
        
        try:
            # Get subnet hyperparameters
            hyperparameters = subtensor.get_subnet_hyperparameters(subnet_id)
            # Convert to dict for JSON serialization
            if hyperparameters:
                data["hyperparameters"] = dict(hyperparameters)
            else:
                data["hyperparameters"] = None
        except Exception as e:
            data["hyperparameters"] = None
            data["hyperparameters_error"] = str(e)
            
        return data
        
    except Exception as e:
        print(f"Error fetching subnet {subnet_id}: {e}")
        return {
            "id": subnet_id,
            "name": f"Subnet {subnet_id}",
            "error": str(e),
            "last_update": int(time.time())
        }

def main():
    """Main function to fetch all subnet data from Bittensor blockchain."""
    print("Connecting to Bittensor Finney network (public data only)...")
    
    try:
        # Initialize subtensor connection to Finney network
        # This uses only public blockchain data - no credentials needed
        subtensor = bt.Subtensor(network="finney")
        print("Connected to Bittensor Finney network successfully!")
        
        # Get all registered subnets (public data)
        print("Fetching registered subnets...")
        subnet_ids = subtensor.get_subnets()
        print(f"Found {len(subnet_ids)} registered subnets")
        
        # Fetch detailed information for each subnet
        subnets_data = []
        for i, subnet_id in enumerate(subnet_ids, 1):
            print(f"Fetching subnet {subnet_id} ({i}/{len(subnet_ids)})...")
            subnet_info = get_subnet_info(subtensor, subnet_id)
            subnets_data.append(subnet_info)
            
            # Small delay to avoid overwhelming the network
            time.sleep(0.1)
        
        # Prepare final data structure
        output_data = {
            "subnets": subnets_data,
            "total_count": len(subnets_data),
            "timestamp": int(time.time()),
            "network": "finney",
            "source": "bittensor_subtensor_sdk_public",
            "note": "Data fetched using only public blockchain information - no credentials required"
        }
        
        # Save to file
        OUT.write_text(json.dumps(output_data, indent=2))
        print(f"\nSuccessfully fetched and saved {len(subnets_data)} subnets to {OUT}")
        
        # Print summary
        print("\nSummary:")
        print(f"- Total subnets: {len(subnets_data)}")
        print(f"- Data saved to: {OUT}")
        print(f"- Network: Finney")
        print(f"- Data source: Public blockchain only")
        print(f"- Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        
    except Exception as e:
        print(f"Error connecting to Bittensor network: {e}")
        print("Please ensure you have a stable internet connection and the bittensor package is installed.")
        print("This script uses only public blockchain data and requires no credentials.")
        
        # Save empty data structure on error
        error_data = {
            "subnets": [],
            "total_count": 0,
            "timestamp": int(time.time()),
            "network": "finney",
            "source": "bittensor_subtensor_sdk_public",
            "error": str(e),
            "note": "Data fetched using only public blockchain information - no credentials required"
        }
        OUT.write_text(json.dumps(error_data, indent=2))

if __name__ == "__main__":
    main()
