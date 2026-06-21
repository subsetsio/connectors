import subsets_utils as su

print("=== subsets_utils surface ===")
for n in ["shared_limiter", "is_transient", "save_raw_parquet", "save_raw_ndjson", "get"]:
    print(n, hasattr(su, n))

g = lambda u: su.get(u, timeout=(10, 60))

cc = g("https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/").json()["response"]
mp = g("https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/").json()["response"]
tr = g("https://api.steampowered.com/ISteamChartsService/GetTopReleasesPages/v1/").json()["response"]
print("\nconcurrent keys:", list(cc.keys()), "| sample:", cc["ranks"][0], "| n=", len(cc["ranks"]))
print("most_played keys:", list(mp.keys()), "| sample:", mp["ranks"][0], "| n=", len(mp["ranks"]))
pages = tr["pages"]
print("top_releases pages:", len(pages))
for p in pages:
    print("   ", p["name"], "items:", len(p["item_ids"]), "sample:", p["item_ids"][:2])

ids = set()
for r in cc["ranks"]:
    ids.add(r["appid"])
for r in mp["ranks"]:
    ids.add(r["appid"])
for p in pages:
    for it in p["item_ids"]:
        ids.add(it["appid"])
print("\nUNION appids:", len(ids))

d = g("https://store.steampowered.com/api/appdetails?appids=730&cc=us&l=en").json()["730"]
print("\nappdetails success:", d["success"])
data = d["data"]
print("price_overview:", data.get("price_overview"))
print("platforms:", data.get("platforms"), "release_date:", data.get("release_date"))
print("metacritic:", data.get("metacritic"), "recommendations:", data.get("recommendations"))
print("genres:", data.get("genres"), "type:", data.get("type"), "is_free:", data.get("is_free"))

ad3 = g("https://store.steampowered.com/api/appdetails?appids=1245620&cc=us&l=en").json()["1245620"]["data"]
print("\nelden price_overview:", ad3.get("price_overview"))
print("elden metacritic:", ad3.get("metacritic"))

rev = g("https://store.steampowered.com/appreviews/730?json=1&num_per_page=0&language=all&purchase_type=all").json()
print("\nreviews query_summary:", rev["query_summary"])
