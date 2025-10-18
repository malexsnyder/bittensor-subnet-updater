import json, time, re
import requests
from bs4 import BeautifulSoup
from pathlib import Path

OUT = Path("data/subnets.json")

def fetch_table():
    url = "https://taomarketcap.com/subnets"
    html = requests.get(url, timeout=30).text
    soup = BeautifulSoup(html, "lxml")
    rows = []
    # NOTE: If TaoMarketCap changes its HTML, you may need to adjust selectors.
    # This generic approach looks for rows with an "ID Name" pattern.
    for tr in soup.select("table tr"):
        tds = [td.get_text(strip=True) for td in tr.select("td")]
        if len(tds) < 1:
            continue
        m = re.match(r"(\d+)\s+(.*)", tds[0])
        if not m:
            continue
        sid, name = int(m.group(1)), m.group(2)
        rows.append({"id": sid, "name": name})
    return rows

def main():
    new = {"subnets": fetch_table(), "timestamp": int(time.time())}
    old = {"subnets":[]}
    if OUT.exists():
        old = json.loads(OUT.read_text() or '{"subnets":[]}')
    # Build diffs for logging/alerts later if you want
    old_map = {s["id"]: s["name"] for s in old.get("subnets", [])}
    changes = {"new_ids": [], "renamed": []}
    for s in new["subnets"]:
        if s["id"] not in old_map:
            changes["new_ids"].append(s)
        elif old_map[s["id"]] != s["name"]:
            changes["renamed"].append({"id": s["id"], "old": old_map[s["id"]], "new": s["name"]})
    OUT.write_text(json.dumps(new, indent=2))
    Path("data/last_diff.json").write_text(json.dumps(changes, indent=2))
    print(json.dumps(changes))

if __name__ == "__main__":
    main()
