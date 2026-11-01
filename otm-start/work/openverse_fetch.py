"""Builds a small real-recording SFX library from Openverse: commercial-use licences only (CC0 / CC BY), short
files, one folder per sound type, plus credits.json / CREDITS.md for attribution.
usage: python openverse_fetch.py OUT_DIR"""
import json, os, re, sys, time, urllib.parse, urllib.request
OUT = sys.argv[1]
QUERIES = {  # type folder: search terms
    "whoosh": ["whoosh", "swoosh", "swish"], "hit": ["impact hit", "punch impact", "thud"], "pop": ["pop sound", "bubble pop"],
    "click": ["mouse click", "button click"], "tick": ["clock tick", "ticking clock"], "paper": ["page turn", "paper"],
    "chime": ["chime", "bell ding"], "riser": ["riser", "tension rise"], "keys": ["keyboard typing"], "door": ["door open", "door close"],
    "coin": ["coin"], "boom": ["boom", "deep impact"], "glitch": ["glitch"], "balloon": ["balloon pop"],
}
API = "https://api.openverse.org/v1/audio/"
credits, n_ok = [], 0
def get(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": "otm-video-builder/1.0"})
    return urllib.request.urlopen(req, timeout=timeout).read()
for kind, qs in QUERIES.items():
    os.makedirs(f"{OUT}/{kind}", exist_ok=True); got = 0
    for q in qs:
        if got >= 6: break
        params = urllib.parse.urlencode({"q": q, "license_type": "commercial", "page_size": 20, "length": "short"})
        try: res = json.loads(get(f"{API}?{params}"))["results"]
        except Exception as e: print("search fail", q, e); continue
        for r in res:
            if got >= 6: break
            if r.get("license") not in ("cc0", "by"): continue
            dur = (r.get("duration") or 0) / 1000
            if dur and (dur < 0.08 or dur > 8): continue
            ext = (r.get("filetype") or "mp3").lower()
            name = re.sub(r"[^a-z0-9]+", "_", (r.get("title") or "s").lower()).strip("_")[:40]
            fn = f"{OUT}/{kind}/{name}_{r['id'][:6]}.{ext}"
            try:
                data = get(r["url"])
                if len(data) < 2000: continue
                open(fn, "wb").write(data)
            except Exception as e: print("dl fail", r["url"][:60], e); continue
            got += 1; n_ok += 1
            credits.append(dict(file=os.path.relpath(fn, OUT), kind=kind, title=r.get("title"), creator=r.get("creator"),
                                license=r.get("license"), license_version=r.get("license_version"), license_url=r.get("license_url"),
                                source=r.get("foreign_landing_url"), provider=r.get("provider")))
            time.sleep(0.2)
    print(kind, got)
json.dump(credits, open(f"{OUT}/credits.json", "w"), indent=1)
with open(f"{OUT}/CREDITS.md", "w") as f:
    f.write("# Sound credits (Openverse)\n\n")
    for c in credits:
        f.write(f"- {c['file']}: \"{c['title']}\" by {c['creator']}, {c['license'].upper()} {c['license_version']} ({c['source']})\n")
print("total", n_ok)
