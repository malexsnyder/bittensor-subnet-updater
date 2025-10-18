import json, re
from pathlib import Path

SUBNETS_JSON = Path("data/subnets.json")
DESC_DIR = Path("data/descriptions")
OUT_DIR  = Path("data/profiles"); OUT_DIR.mkdir(parents=True, exist_ok=True)

def slug(s):
    return re.sub(r'[^a-z0-9]+','-', s.lower()).strip('-')

TEMPLATE = """# {name} (Subnet {sid})
**Primary Function:** {function}

**Problem It Solves:** {problem}

**Target Audience:** 
- {aud1}
- {aud2}

**Projected Growth Score (1–10):** {growth} — {growth_reason}

**Conviction Scores**
- **Short-term (1–3 mo):** {st} — {st_reason}
- **Medium-term (3–12 mo):** {mt} — {mt_reason}
- **Long-term (1+ yr):** {lt} — {lt_reason}

**Buy/Sell Conviction Meter:** {conv} — {conv_reason}

**Trending / Alerts (last 48h):** {trend}

**Official Link:** {link}
"""

def main():
    data = json.loads(SUBNETS_JSON.read_text() or '{"subnets": []}')
    for s in data.get("subnets", []):
        sid, name = s["id"], s["name"]
        desc_path = DESC_DIR / f"{sid}.md"
        function_txt = (desc_path.read_text().strip() if desc_path.exists() else
                        "Description not yet available; will update soon.")
        # baseline scaffold; your front-end Agent will refine these live
        content = TEMPLATE.format(
            name=name, sid=sid,
            function=function_txt,
            problem="TBD (auto-fill by live agent or add rules).",
            aud1="Developers / users of this subnet",
            aud2="Investors tracking Bittensor subnets",
            growth="7", growth_reason="baseline; refined by live market signals.",
            st="50", st_reason="baseline; sentiment will update live.",
            mt="60", mt_reason="baseline; dev progress updates live.",
            lt="70", lt_reason="baseline; macro fit updates live.",
            conv="55", conv_reason="baseline synthesis of fundamentals + sentiment.",
            trend="Checked by live agent.",
            link="(website or X will be attached by live agent)"
        )
        OUT_DIR.joinpath(f"{sid}_{slug(name)}.md").write_text(content)

if __name__ == "__main__":
    main()
