from subsets_utils import get

H = {"Accept": "application/json"}


def j(path):
    return get(f"https://statsapi.mlb.com/api/v1/{path}", headers=H, timeout=(10, 120)).json()


# 1. seasons available for sportId=1
seasons = j("seasons?sportId=1")["seasons"]
years = [s["seasonId"] for s in seasons]
print("season count:", len(years), "range:", years[0], "->", years[-1])
print("season record keys:", list(seasons[0].keys()))

# 2. player hitting stats pagination — does it page? totalSize?
d = j("stats?stats=season&group=hitting&season=2024&sportId=1&limit=10&offset=0")
st = d["stats"][0]
print("\nstats top keys:", list(d.keys()))
print("stats block keys:", list(st.keys()))
print("totalSplits:", st.get("totalSplits"), "exactSplits:", st.get("exactSplits"), "returned:", len(st["splits"]))
sp = st["splits"][0]
print("player obj:", sp.get("player"))
print("team obj keys:", list(sp.get("team", {}).keys()))

# 3. full season player count (no limit)
d2 = j("stats?stats=season&group=hitting&season=2024&sportId=1")
print("\nno-limit returned splits:", len(d2["stats"][0]["splits"]), "totalSplits:", d2["stats"][0].get("totalSplits"))

# 4. standings depth — try an old season
for yr in (1901, 1969, 2024):
    try:
        s = j(f"standings?leagueId=103,104&season={yr}")
        recs = s.get("records", [])
        n = sum(len(r["teamRecords"]) for r in recs)
        print(f"standings {yr}: records={len(recs)} teamRecords={n}")
    except Exception as e:
        print(f"standings {yr}: ERR {type(e).__name__} {e}")
