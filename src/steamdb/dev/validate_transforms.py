"""Exercise each fetch fn's parse logic + transform SQL on real (small) data."""
import duckdb
import pyarrow as pa
import nodes.steamdb as m

con = duckdb.connect()


def run_transform(table: pa.Table, view: str, spec):
    con.register(view, table)
    out = con.execute(spec.sql).fetch_arrow_table()
    print(f"\n--- {spec.id}: {out.num_rows} rows ---")
    print(out.schema)
    print(out.slice(0, 2).to_pylist())
    assert out.num_rows > 0
    con.unregister(view)


# charts (full)
resp = m._web_json(m.CONCURRENT_URL)["response"]
ts = int(resp["last_update"])
cc = pa.Table.from_pylist([
    {"rank": int(r["rank"]), "appid": int(r["appid"]), "concurrent_in_game": int(r["concurrent_in_game"]),
     "peak_in_game": int(r.get("peak_in_game") or 0), "last_update": ts} for r in resp["ranks"]
], schema=m._CONCURRENT_SCHEMA)
run_transform(cc, "steamdb-concurrent-players", m.TRANSFORM_SPECS[0])

resp = m._web_json(m.MOST_PLAYED_URL)["response"]
rollup = int(resp["rollup_date"])
mp = pa.Table.from_pylist([
    {"rank": int(r["rank"]), "appid": int(r["appid"]),
     "last_week_rank": int(r["last_week_rank"]) if r.get("last_week_rank") is not None else None,
     "peak_in_game": int(r.get("peak_in_game") or 0), "rollup_date": rollup} for r in resp["ranks"]
], schema=m._MOST_PLAYED_SCHEMA)
run_transform(mp, "steamdb-most-played", m.TRANSFORM_SPECS[1])

resp = m._web_json(m.TOP_RELEASES_URL)["response"]
trrows = []
for p in resp["pages"]:
    for i, it in enumerate(p["item_ids"], start=1):
        trrows.append({"month_name": p["name"], "start_of_month": int(p["start_of_month"]),
                       "rank": i, "appid": int(it["appid"])})
tr = pa.Table.from_pylist(trrows, schema=m._TOP_RELEASES_SCHEMA)
run_transform(tr, "steamdb-top-releases", m.TRANSFORM_SPECS[2])

# enrichment — only a handful of appids (free + paid) to validate parse+SQL
sample = [730, 1245620, 570, 271590]
det_rows, rev_rows = [], []
for appid in sample:
    body = m._store_json_limited(f"{m.STORE_API}/api/appdetails?appids={appid}&cc=us&l=en")
    entry = body.get(str(appid)) or {}
    if entry.get("success") and entry.get("data"):
        d = entry["data"]
        price = d.get("price_overview") or {}
        platforms = d.get("platforms") or {}
        rel = d.get("release_date") or {}
        metac = d.get("metacritic") or {}
        recs = d.get("recommendations") or {}
        det_rows.append({
            "appid": int(d.get("steam_appid") or appid), "name": d.get("name"), "type": d.get("type"),
            "is_free": bool(d.get("is_free")),
            "price_final_cents": int(price["final"]) if price.get("final") is not None else None,
            "price_initial_cents": int(price["initial"]) if price.get("initial") is not None else None,
            "price_currency": price.get("currency"),
            "discount_percent": int(price["discount_percent"]) if price.get("discount_percent") is not None else None,
            "genres": m._join_descriptions(d.get("genres")), "categories": m._join_descriptions(d.get("categories")),
            "on_windows": bool(platforms.get("windows")), "on_mac": bool(platforms.get("mac")),
            "on_linux": bool(platforms.get("linux")), "release_date": rel.get("date"),
            "coming_soon": bool(rel.get("coming_soon")),
            "metacritic_score": int(metac["score"]) if metac.get("score") is not None else None,
            "recommendations_total": int(recs["total"]) if recs.get("total") is not None else None,
        })
    rbody = m._store_json_limited(f"{m.STORE_API}/appreviews/{appid}?json=1&num_per_page=0&language=all&purchase_type=all")
    if rbody.get("success"):
        qs = rbody.get("query_summary") or {}
        if qs.get("total_reviews") is not None:
            rev_rows.append({
                "appid": int(appid), "review_score": int(qs["review_score"]),
                "review_score_desc": qs.get("review_score_desc"),
                "total_positive": int(qs["total_positive"]), "total_negative": int(qs["total_negative"]),
                "total_reviews": int(qs["total_reviews"]),
            })

det = pa.Table.from_pylist(det_rows, schema=m._APP_DETAILS_SCHEMA)
run_transform(det, "steamdb-app-details", m.TRANSFORM_SPECS[3])
rev = pa.Table.from_pylist(rev_rows, schema=m._APP_REVIEWS_SCHEMA)
run_transform(rev, "steamdb-app-reviews", m.TRANSFORM_SPECS[4])

print("\nALL TRANSFORMS OK")
