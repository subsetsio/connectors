"""Wikipedia AQS — global media-request series, broken down by media type.

Unlike the per-project families, this is a single global Wikimedia series
fanned out only across media types, so it uses its own collect loop rather
than the project-universe engine.
"""
import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import BASE, get_json, now_end, to_date


def fetch_mediarequests(node_id: str) -> None:
    """Global Wikimedia media-request series, broken down by media type."""
    end = now_end()
    schema = pa.schema([
        ("media_type", pa.string()),
        ("date", pa.string()),
        ("requests", pa.int64()),
    ])
    media_types = ["all-media-types", "image", "audio", "video", "document", "other"]
    rows: list[dict] = []
    ok = 0
    for mt in media_types:
        url = (f"{BASE}/mediarequests/aggregate/all-referers/{mt}/all-agents/"
               f"monthly/2015010100/{end}")
        try:
            data = get_json(url)
        except httpx.HTTPStatusError as e:
            code = e.response.status_code
            if code != 429 and 400 <= code < 500:
                continue
            raise
        before = len(rows)
        for it in data.get("items", []):
            rows.append({
                "media_type": it["media_type"],
                "date": to_date(it["timestamp"]),
                "requests": it.get("requests"),
            })
        if len(rows) > before:
            ok += 1
    if ok == 0:
        raise RuntimeError(f"{node_id}: no media-request data returned")
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="wikipedia-mediarequests", fn=fetch_mediarequests, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wikipedia-mediarequests-transform",
        deps=["wikipedia-mediarequests"],
        sql='''
            SELECT
                media_type,
                CAST(date AS DATE) AS date,
                requests
            FROM "wikipedia-mediarequests"
            WHERE date IS NOT NULL
              AND requests IS NOT NULL
        ''',
    ),
]
