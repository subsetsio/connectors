from subsets_utils import get

H = {"Accept": "application/json"}


def j(path):
    return get(f"https://statsapi.mlb.com/api/v1/{path}", headers=H, timeout=(10, 120)).json()


# all seasons
alls = j("seasons?sportId=1&all=true")["seasons"]
years = [int(s["seasonId"]) for s in alls]
print("all seasons:", len(years), min(years), "->", max(years))

# playerPool variants for player hitting 2024
for pool in ("qualified", "all", "rookies", "qualifier"):
    try:
        d = j(f"stats?stats=season&group=hitting&season=2024&sportId=1&playerPool={pool}&limit=1")
        print(f"pool={pool}: totalSplits={d['stats'][0].get('totalSplits')}")
    except Exception as e:
        print(f"pool={pool}: ERR {e}")

# default (no pool) totalSplits across groups
for g in ("hitting", "pitching", "fielding"):
    d = j(f"stats?stats=season&group={g}&season=2024&sportId=1&limit=1")
    da = j(f"stats?stats=season&group={g}&season=2024&sportId=1&playerPool=all&limit=1")
    print(f"group={g}: default={d['stats'][0].get('totalSplits')} all={da['stats'][0].get('totalSplits')}")

# offset paging sanity: pull offset 0 and 50, check distinct players
d0 = j("stats?stats=season&group=hitting&season=2024&sportId=1&playerPool=all&limit=50&offset=0")
d1 = j("stats?stats=season&group=hitting&season=2024&sportId=1&playerPool=all&limit=50&offset=50")
ids0 = {s["player"]["id"] for s in d0["stats"][0]["splits"]}
ids1 = {s["player"]["id"] for s in d1["stats"][0]["splits"]}
print("offset0 n=", len(ids0), "offset50 n=", len(ids1), "overlap=", len(ids0 & ids1))

# team stats — does it paginate / need playerPool? totalSplits
dt = j("teams/stats?stats=season&group=hitting&season=2024&sportId=1")
print("team hitting splits returned:", len(dt["stats"][0]["splits"]), "totalSplits:", dt["stats"][0].get("totalSplits"))
print("team split sample:", {k: dt["stats"][0]["splits"][0].get(k) for k in ("season", "team", "rank")})
