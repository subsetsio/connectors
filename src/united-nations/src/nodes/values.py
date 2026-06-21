"""United Nations — long-format SDG observations (~3.2M rows).

Observations are pulled per series via the bulk POST Series/DataCSV endpoint:
~4s/series and reliable at series granularity, whereas the paginated JSON
Series/Data endpoint is ~15s/page and the per-goal bulk export returns an empty
body for the largest goals (>~200k rows). The CSV body is null-byte padded to a
power-of-2 buffer size by the server, so the padding is stripped before parsing.

`values` is a large, slow (~45min) but bounded crawl with no source-side change
feed (research: no modifiedAfter). It is therefore written as one NDJSON batch
per series with a release-keyed resume watermark (firehose shape): each series's
raw is written, then the watermark advances and state is saved, so a supervisor
interrupt resumes from the last completed series instead of restarting. The SDG
database release tag (e.g. 2026.Q1.G.02) is the source's version marker; when it
changes the watermark resets and the full corpus is re-crawled, which is how
revisions are picked up.
"""
import io
import json

import httpx
import pandas as pd

from subsets_utils import (
    NodeSpec, SqlNodeSpec, post, TRANSIENT_EXC, transient_retry,
    save_raw_ndjson, load_state, save_state,
)

from utils import BASE, get_json

STATE_VERSION = 1


@transient_retry()
def _post_series_csv(series_code: str) -> bytes:
    resp = post(BASE + "Series/DataCSV", data={"seriesCodes": series_code}, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


_CORE_RENAME = {
    "Goal": "goal",
    "Target": "target",
    "Indicator": "indicator",
    "SeriesCode": "series_code",
    "SeriesDescription": "series_description",
    "GeoAreaCode": "geo_area_code",
    "GeoAreaName": "geo_area_name",
    "TimePeriod": "time_period",
    "Value": "value",
    "Time_Detail": "time_detail",
    "TimeCoverage": "time_coverage",
    "UpperBound": "upper_bound",
    "LowerBound": "lower_bound",
    "BasePeriod": "base_period",
    "Source": "source",
    "GeoInfoUrl": "geo_info_url",
    "FootNote": "footnote",
}


def _parse_series_csv(content: bytes) -> list[dict]:
    """Parse one Series/DataCSV body into flat observation records.

    The server null-byte pads the body to a power-of-2 buffer; strip the padding
    before handing the real CSV to pandas (which copes with the quoted,
    sometimes multi-line, footnote field). Bracketed columns are the source's
    per-series disaggregation/attribute fields and vary across series: Units and
    Nature become first-class columns; the rest collapse into a stable JSON
    `dimensions` string so every record shares one schema.
    """
    raw = content.split(b"\x00", 1)[0]
    if not raw.strip():
        return []
    df = pd.read_csv(io.BytesIO(raw), dtype=str, keep_default_na=False)
    bracket_cols = [c for c in df.columns if c.startswith("[") and c.endswith("]")]
    rows = []
    for rec in df.to_dict(orient="records"):
        out = {dst: (rec.get(src) or None) for src, dst in _CORE_RENAME.items()}
        out["units"] = rec.get("[Units]") or None
        out["nature"] = rec.get("[Nature]") or None
        dims = {
            c[1:-1]: rec[c]
            for c in bracket_cols
            if c not in ("[Units]", "[Nature]") and rec.get(c)
        }
        out["dimensions"] = json.dumps(dims, sort_keys=True) if dims else None
        rows.append(out)
    return rows


def fetch_values(node_id: str) -> None:
    """Crawl every series' observations, one NDJSON batch per series.

    node_id == "united-nations-values"; batches are written as
    f"{node_id}-{series_code}" and glob-unioned by the transform's view.
    """
    series_list = get_json("Series/List")
    if not isinstance(series_list, list) or not series_list:
        raise RuntimeError("Series/List returned no records for the values crawl")
    codes = sorted({r["code"] for r in series_list if r.get("code")})
    release = series_list[0].get("release") or ""

    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION or state.get("release") != release:
        watermark = ""  # new release (or fresh state) -> full re-crawl
    else:
        watermark = state.get("watermark", "")

    failed: list[str] = []
    fail_cap = max(25, len(codes) // 10)

    for code in codes:
        if watermark and code <= watermark:
            continue
        try:
            rows = _parse_series_csv(_post_series_csv(code))
        except (httpx.HTTPStatusError, *TRANSIENT_EXC) as exc:
            # Permanent 4xx, or transient that exhausted its retries: skip this
            # one series rather than abort a ~45min crawl. A systemic outage
            # (many failures) raises below via fail_cap.
            failed.append(code)
            print(f"[values] series {code} failed ({type(exc).__name__}: {exc}); skipping")
            if len(failed) > fail_cap:
                raise RuntimeError(
                    f"values crawl: {len(failed)} series failed (cap {fail_cap}) — "
                    f"likely a systemic API outage; aborting at {code}"
                )
            watermark = code
            save_state(node_id, {"schema_version": STATE_VERSION, "release": release, "watermark": watermark})
            continue
        if rows:
            save_raw_ndjson(rows, f"{node_id}-{code}")  # raw FIRST
        watermark = code
        save_state(node_id, {"schema_version": STATE_VERSION, "release": release, "watermark": watermark})

    if failed:
        print(f"[values] crawl complete with {len(failed)} skipped series: {failed[:20]}")


DOWNLOAD_SPECS = [
    NodeSpec(id="united-nations-values", fn=fetch_values, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="united-nations-values-transform",
        deps=["united-nations-values"],
        sql='''
            SELECT
                series_code,
                series_description,
                goal              AS goal_code,
                target            AS target_code,
                indicator         AS indicator_code,
                geo_area_code,
                geo_area_name,
                time_period,
                TRY_CAST(time_period AS INTEGER) AS year,
                TRY_CAST(value AS DOUBLE)        AS value,
                units,
                nature,
                source,
                dimensions,
                time_detail,
                base_period,
                TRY_CAST(upper_bound AS DOUBLE)  AS upper_bound,
                TRY_CAST(lower_bound AS DOUBLE)  AS lower_bound
            FROM "united-nations-values"
            WHERE series_code IS NOT NULL
              AND value IS NOT NULL AND value <> ''
        ''',
    ),
]
