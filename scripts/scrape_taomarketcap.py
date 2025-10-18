import json
import requests
from pathlib import Path
import time

# Output file
OUT = Path("data/subnets.json")

def main():
    print("Fetching subnet data from TaoMarketCap API...")
    # TaoMarketCap uses a JSON API endpoint that returns subnet info.
    # It may change paths occasionally, but this endpoint is live as of now:
    url = "https://taomarketcap.com/api/subnets"

    response = requests.get(url, timeout=30)
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        OUT.write_text(json.dumps({"subnets": [], "timestamp": int(time.time())}, indent=2))
        return

    data = response.json()

    # Convert data into our preferred format
    subnets = []
    for s in data:
        subnets.append({
            "id": s.get("id"),
            "name": s.get("name", "").strip(),
            "price": s.get("price"),
            "emission": s.get("emission"),
            "delegates": s.get("delegates"),
            "uid_count": s.get("uids")
        })

    # Save results
    OUT.write_text(json.dumps({"subnets": subnets, "timestamp": int(time.time())}, indent=2))
    print(f"Fetched and saved {len(subnets)} subnets.")

if __name__ == "__main__":
    main()
# minor edit to trigger new run
# sync fix commit
