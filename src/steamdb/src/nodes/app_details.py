"""SteamDB app_details — per-app store metadata for the chart-derived universe.

store appdetails over the union of appids across the three charts. Throttled
store host (~16/min per process). Current-state snapshot overwritten each run.
"""
import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import STORE_API, _chart_appids, _store_json_limited

_APP_DETAILS_SCHEMA = pa.schema([
    ("appid", pa.int64()),
    ("name", pa.string()),
    ("type", pa.string()),
    ("is_free", pa.bool_()),
    ("price_final_cents", pa.int64()),
    ("price_initial_cents", pa.int64()),
    ("price_currency", pa.string()),
    ("discount_percent", pa.int32()),
    ("genres", pa.string()),
    ("categories", pa.string()),
    ("on_windows", pa.bool_()),
    ("on_mac", pa.bool_()),
    ("on_linux", pa.bool_()),
    ("release_date", pa.string()),
    ("coming_soon", pa.bool_()),
    ("metacritic_score", pa.int32()),
    ("recommendations_total", pa.int64()),
])


def _join_descriptions(items) -> str | None:
    if not items:
        return None
    parts = [str(x.get("description", "")).strip() for x in items if x.get("description")]
    return ", ".join(parts) if parts else None


def fetch_app_details(node_id: str) -> None:
    rows = []
    for appid in _chart_appids():
        body = _store_json_limited(f"{STORE_API}/api/appdetails?appids={appid}&cc=us&l=en")
        entry = body.get(str(appid)) or {}
        if not entry.get("success") or not entry.get("data"):
            continue  # delisted / region-locked — skip this appid
        d = entry["data"]
        price = d.get("price_overview") or {}
        platforms = d.get("platforms") or {}
        rel = d.get("release_date") or {}
        metacritic = d.get("metacritic") or {}
        recs = d.get("recommendations") or {}
        rows.append({
            "appid": int(d.get("steam_appid") or appid),
            "name": d.get("name"),
            "type": d.get("type"),
            "is_free": bool(d.get("is_free")) if d.get("is_free") is not None else None,
            "price_final_cents": int(price["final"]) if price.get("final") is not None else None,
            "price_initial_cents": int(price["initial"]) if price.get("initial") is not None else None,
            "price_currency": price.get("currency"),
            "discount_percent": int(price["discount_percent"]) if price.get("discount_percent") is not None else None,
            "genres": _join_descriptions(d.get("genres")),
            "categories": _join_descriptions(d.get("categories")),
            "on_windows": bool(platforms.get("windows")) if platforms else None,
            "on_mac": bool(platforms.get("mac")) if platforms else None,
            "on_linux": bool(platforms.get("linux")) if platforms else None,
            "release_date": rel.get("date") or None,
            "coming_soon": bool(rel.get("coming_soon")) if rel.get("coming_soon") is not None else None,
            "metacritic_score": int(metacritic["score"]) if metacritic.get("score") is not None else None,
            "recommendations_total": int(recs["total"]) if recs.get("total") is not None else None,
        })
    if not rows:
        raise AssertionError("app_details produced 0 rows; store appdetails likely throttled/blocked")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_APP_DETAILS_SCHEMA), node_id)

