"""Download raw Steam Charts tables."""

from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone

import httpx
import pyarrow as pa
from lxml import html

from subsets_utils import NodeSpec, get, save_raw_parquet

BASE_URL = "https://steamcharts.com"

GAMES_SCHEMA = pa.schema([
    ("app_id", pa.int64()),
    ("name", pa.string()),
    ("rank", pa.int64()),
    ("current_players", pa.int64()),
    ("peak_players_30d", pa.int64()),
    ("player_hours_30d", pa.int64()),
    ("source_page", pa.int64()),
    ("fetched_at", pa.timestamp("us", tz="UTC")),
])

MONTHLY_SCHEMA = pa.schema([
    ("app_id", pa.int64()),
    ("app_name", pa.string()),
    ("period_label", pa.string()),
    ("period_start", pa.date32()),
    ("is_last_30_days", pa.bool_()),
    ("avg_players", pa.float64()),
    ("gain", pa.float64()),
    ("percent_gain", pa.float64()),
    ("peak_players", pa.int64()),
    ("fetched_at", pa.timestamp("us", tz="UTC")),
])

CHART_SCHEMA = pa.schema([
    ("app_id", pa.int64()),
    ("app_name", pa.string()),
    ("observed_at", pa.timestamp("ms", tz="UTC")),
    ("players", pa.int64()),
    ("fetched_at", pa.timestamp("us", tz="UTC")),
])


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _fetch(url: str, *, accept_json: bool = False):
    headers = {"Accept": "application/json" if accept_json else "text/html,application/xhtml+xml"}
    resp = get(url, headers=headers, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _text_content(node) -> str:
    return " ".join(node.text_content().split())


def _parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    cleaned = value.replace(",", "").strip()
    if cleaned in {"", "-"}:
        return None
    return int(float(cleaned))


def _parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    cleaned = value.replace(",", "").replace("%", "").replace("+", "").strip()
    if cleaned in {"", "-"}:
        return None
    return float(cleaned)


def _parse_month(label: str):
    if label == "Last 30 Days":
        return None
    return datetime.strptime(label, "%B %Y").date().replace(day=1)


def _top_url(page: int) -> str:
    return f"{BASE_URL}/top" if page == 1 else f"{BASE_URL}/top/p.{page}"


def _read_top_page(page: int) -> tuple[list[dict], bool]:
    try:
        resp = _fetch(_top_url(page))
    except httpx.HTTPStatusError as exc:
        if page > 1 and exc.response.status_code == 404:
            return [], False
        raise
    doc = html.fromstring(resp.text)
    rows = []
    for tr in doc.xpath('//table[@id="top-games"]/tbody/tr'):
        cells = tr.xpath("./td")
        if len(cells) < 6:
            continue
        app_links = cells[1].xpath('.//a[contains(@href, "/app/")]/@href')
        if not app_links:
            continue
        app_match = re.search(r"/app/(\d+)", app_links[0])
        if not app_match:
            continue
        name = _text_content(cells[1])
        rank_text = _text_content(cells[0]).rstrip(".")
        rows.append({
            "app_id": int(app_match.group(1)),
            "name": name,
            "rank": _parse_int(rank_text),
            "current_players": _parse_int(_text_content(cells[2])),
            "peak_players_30d": _parse_int(_text_content(cells[4])),
            "player_hours_30d": _parse_int(_text_content(cells[5])),
            "source_page": page,
        })
    next_links = doc.xpath('//link[@rel="next"]/@href | //div[contains(@class, "pagination-heading")]//a[contains(@href, "/top/p.")]/@href')
    return rows, bool(next_links)


def _enumerate_games() -> list[dict]:
    seen = set()
    out = []
    page = 1
    while True:
        rows, has_next = _read_top_page(page)
        if not rows:
            break
        for row in rows:
            app_id = row["app_id"]
            if app_id in seen:
                continue
            seen.add(app_id)
            out.append(row)
        if not has_next:
            break
        page += 1
        if page > 1000:
            raise RuntimeError("refusing to crawl more than 1000 top pages")
        time.sleep(0.1)
    return out


def _read_app_page(app_id: int) -> tuple[str, list[dict]]:
    resp = _fetch(f"{BASE_URL}/app/{app_id}")
    doc = html.fromstring(resp.text)
    title = doc.xpath('string(//h1[@id="app-title"]/a)')
    app_name = " ".join(title.split()) or str(app_id)
    rows = []
    fetched_at = _now()
    for tr in doc.xpath('//table[contains(@class, "common-table")]/tbody/tr'):
        cells = [_text_content(td) for td in tr.xpath("./td")]
        if len(cells) != 5:
            continue
        label = cells[0]
        rows.append({
            "app_id": app_id,
            "app_name": app_name,
            "period_label": label,
            "period_start": _parse_month(label),
            "is_last_30_days": label == "Last 30 Days",
            "avg_players": _parse_float(cells[1]),
            "gain": _parse_float(cells[2]),
            "percent_gain": _parse_float(cells[3]),
            "peak_players": _parse_int(cells[4]),
            "fetched_at": fetched_at,
        })
    return app_name, rows


def _read_chart(app_id: int, app_name: str) -> list[dict]:
    resp = _fetch(f"{BASE_URL}/app/{app_id}/chart-data.json", accept_json=True)
    data = json.loads(resp.text)
    fetched_at = _now()
    rows = []
    for point in data:
        if not isinstance(point, list) or len(point) != 2:
            raise ValueError(f"unexpected chart point for app {app_id}: {point!r}")
        rows.append({
            "app_id": app_id,
            "app_name": app_name,
            "observed_at": datetime.fromtimestamp(point[0] / 1000, tz=timezone.utc),
            "players": _parse_int(str(point[1])),
            "fetched_at": fetched_at,
        })
    return rows


def _is_not_found(exc: httpx.HTTPStatusError) -> bool:
    return exc.response.status_code == 404


def fetch_games(node_id: str) -> None:
    fetched_at = _now()
    rows = []
    for row in _enumerate_games():
        row = dict(row)
        row["fetched_at"] = fetched_at
        rows.append(row)
    table = pa.Table.from_pylist(rows, schema=GAMES_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_monthly_stats(node_id: str) -> None:
    rows = []
    for game in _enumerate_games():
        try:
            _, app_rows = _read_app_page(game["app_id"])
        except httpx.HTTPStatusError as exc:
            if _is_not_found(exc):
                continue
            raise
        rows.extend(app_rows)
        time.sleep(0.1)
    table = pa.Table.from_pylist(rows, schema=MONTHLY_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_chart_values(node_id: str) -> None:
    rows = []
    for game in _enumerate_games():
        try:
            rows.extend(_read_chart(game["app_id"], game["name"]))
        except httpx.HTTPStatusError as exc:
            if _is_not_found(exc):
                continue
            raise
        time.sleep(0.1)
    table = pa.Table.from_pylist(rows, schema=CHART_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="steam-charts-chart-values",
        fn=fetch_chart_values,
        kind="download",
    ),
    NodeSpec(
        id="steam-charts-games",
        fn=fetch_games,
        kind="download",
    ),
    NodeSpec(
        id="steam-charts-monthly-stats",
        fn=fetch_monthly_stats,
        kind="download",
    ),
]
