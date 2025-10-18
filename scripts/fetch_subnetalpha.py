import json, re, time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

SUBNETS = Path("data/subnets.json")
DESC_DIR = Path("data/descriptions")
DESC_DIR.mkdir(parents=True, exist_ok=True)

# Very simple discovery by name; Subnet Alpha may change layout.
INDEX_URLS = [
    "https://subnetalpha.ai/",
]

def find_page(name:str):
    name_low = name.lower()
    for index_url in INDEX_URLS:
        html = requests.get(index_url, timeout=30).text
        soup = BeautifulSoup(html, "lxml")
        for a in soup.select("a[href*='/subnet/']"):
            card_text = a.get_text(" ", strip=True).lower()
            if name_low in card_text:
                href = a.get("href", "")
                if href.startswith("http"):
                    return href
                return "https://subnetalpha.ai" + href
    return None

def extract_function_text(url):
    html = requests.get(url, timeout=30).text
    soup = BeautifulSoup(html, "lxml")
    paras = soup.select("p")
    text = "\n\n".join(p.get_text(" ", strip=True) for p in paras[:3]).strip()
    return text

def main():
    subnets = json.loads(SUBNETS.read_text()).get("subnets", [])
    for s in subnets:
        out = DESC_DIR / f"{s['id']}.md"
        if out.exists():  # keep prior description unless you want to overwrite
            continue
        page = find_page(s["name"])
        if not page:
            continue
        txt = extract_function_text(page)
        if txt:
            out.write_text(txt)

if __name__ == "__main__":
    main()
