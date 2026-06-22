import json
from subsets_utils import get

RAW = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"


def j(url):
    r = get(url, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r.json()


comps = j(f"{RAW}/competitions.json")
print("competition-seasons:", len(comps))
print("sample comp:", json.dumps(comps[0], indent=2)[:600])

total_matches = 0
total_360 = 0
seen_match = None
for c in comps:
    ms = j(f"{RAW}/matches/{c['competition_id']}/{c['season_id']}.json")
    total_matches += len(ms)
    total_360 += sum(1 for m in ms if m.get("match_status_360") == "available")
    if seen_match is None:
        seen_match = ms[0]
print("TOTAL matches:", total_matches)
print("TOTAL 360-available matches:", total_360)
print("sample match keys:", sorted(seen_match.keys()))
print("sample match:", json.dumps(seen_match, indent=2)[:1200])

mid = seen_match["match_id"]
ev = j(f"{RAW}/events/{mid}.json")
print("events in sample match:", len(ev))
print("event[0] keys:", sorted(ev[0].keys()))
print("event sample (a pass):")
for e in ev:
    if isinstance(e.get("pass"), dict):
        print(json.dumps(e, indent=2)[:1500])
        break

lu = j(f"{RAW}/lineups/{mid}.json")
print("lineups teams:", len(lu), "team keys:", sorted(lu[0].keys()))
print("player[0]:", json.dumps(lu[0]["lineup"][0], indent=2)[:800])
