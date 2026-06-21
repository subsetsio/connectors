"""JNTO (Japan National Tourism Organization) tourism statistics.

Source shape: statistics.jnto.go.jp is a thin front-end over a set of unlisted
Tableau Public workbooks (profile 'statistics7800'). Each workbook is a distinct
dataset and is downloadable in full as a packaged .twbx (a ZIP that bundles one
or more .hyper extracts) at a stable URL:

    https://public.tableau.com/workbooks/<repo>.twb   (returns a .twbx ZIP)

A workbook bundles several extracts (the dashboard's data source plus small
KPI / lookup / map-coordinate helpers). The publishable dataset is the
*largest* extract; the helpers are auxiliary. For each workbook we download the
.twbx, read its largest .hyper table, rename the (mostly Japanese) columns to
ASCII-safe English, and write one ndjson raw. ndjson (not parquet) because the
per-extract schemas are heterogeneous and a column's type occasionally drifts
(e.g. a provisional visitor count arriving as text).

Fetch shape: stateless full re-pull. Every workbook is tiny (a few KB to ~2MB)
and there is no incremental/since filter on Tableau Public, so we re-download
the full corpus each run and overwrite -- revisions and late corrections are
picked up for free.
"""

import glob
import io
import os
import re
import tempfile
import zipfile
from datetime import date, datetime, time
from decimal import Decimal


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

# --- the entity union (collect/rank-accepted Tableau workbook repo URLs) ------

from constants import ENTITY_IDS


def _sid(entity_id: str) -> str:
    return f"jnto-{entity_id.lower().replace('_', '-')}"


# spec-id -> original workbook repo (the id loses case/underscores, so map back)
ID_TO_REPO = {_sid(e): e for e in ENTITY_IDS}

_WORKBOOK_URL = "https://public.tableau.com/workbooks/{repo}.twb"

# --- column translation (Japanese header -> ASCII-safe English) ---------------
# Covers every header observed across the 17 workbooks' largest extracts.
# Numeric-suffixed display variants (国・地域1, 都道府県1, ...) map to the same
# base name; _clean_columns() de-duplicates collisions with a numeric suffix.

COLMAP = {
    "国・地域": "country_area",
    "国・地域1": "country_area",
    "国・地域2": "country_area",
    "表示用国・地域": "country_area_display",
    "Country/Area": "country_area_en",
    "alpha3Code": "alpha3_code",
    "国籍": "nationality",
    "地域": "region",
    "地域1": "region",
    "Region": "region_en",
    "地域分類": "region_category",
    "地域分類1": "region_category",
    "Area": "area_en",
    "年": "year",
    "Year": "year_en",
    "月": "month",
    "訪日目的": "purpose",
    "訪日目的1": "purpose",
    "目的": "purpose",
    "Purpose": "purpose_en",
    "Purpose_of_visit_to_Japan": "purpose_en",
    "訪日外客数（人）": "visitor_arrivals",
    "訪日外客数（人）1": "visitor_arrivals",
    "暫定値フラグ": "provisional_flag",
    "ソート順": "sort_order",
    "表示内容": "display_content",
    "項目1": "item1",
    "項目2": "item2",
    "項目3": "item3",
    "Item1": "item1_en",
    "Item2": "item2_en",
    "Item3": "item3_en",
    "回答数": "responses",
    "構成比": "composition_ratio",
    "Composition ratio": "composition_ratio_en",
    "比率": "ratio",
    "都道府県": "prefecture",
    "都道府県1": "prefecture",
    "Prefecture": "prefecture_en",
    "購入者単価": "purchaser_unit_price",
    "Purchaser unit price": "purchaser_unit_price_en",
    "性別": "sex",
    "階級": "class_group",
    "年齢": "age",
    "人数": "persons",
    "人数（千人）": "persons_thousands",
    "伸率": "growth_rate",
    "順位": "rank",
    "統計基準": "statistical_basis",
    "外国旅行者数（千人）": "outbound_travelers_thousands",
    "訪問者数": "visitors",
    "種別": "category_type",
    "港名": "port_name",
    "港名1": "port_name",
    "PortName": "port_name_en",
    "外国人参加者数": "foreign_participants",
    "国内参加者数": "domestic_participants",
    "参加者総数": "total_participants",
    "参加者総数（日本語）": "total_participants_ja",
    "参加者総数（英語）": "total_participants_en",
    "開催件数": "events_held",
    "分野": "field",
    "分野（日本語）": "field_ja",
    "分野（英語）": "field_en",
    "開催都市": "host_city",
    "都市名（日本語）": "city_name_ja",
    "都市名（英語）": "city_name_en",
    "No": "no",
}


def _slug(name: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z]+", "_", name).strip("_").lower()
    if s and s[0].isdigit():
        s = "c_" + s
    return s


def _clean_columns(names):
    out, seen = [], set()
    for i, nm in enumerate(names):
        base = COLMAP.get(nm) or _slug(nm) or f"col{i}"
        name, k = base, 2
        while name in seen:
            name = f"{base}_{k}"
            k += 1
        seen.add(name)
        out.append(name)
    return out


def _jsonify(v):
    if v is None or isinstance(v, (str, int, float, bool)):
        return v
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (datetime, date, time)):
        return v.isoformat()
    if isinstance(v, (bytes, bytearray)):
        return bytes(v).decode("utf-8", "replace")
    return str(v)


# --- HTTP (retried, transient-aware) ------------------------------------------


@transient_retry()
def _download_twbx(repo: str) -> bytes:
    resp = get(_WORKBOOK_URL.format(repo=repo), timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _largest_table_rows(twbx: bytes):
    """Open the .twbx ZIP, find the .hyper table with the most rows, and
    return its rows as a list of dicts with ASCII-safe column names."""
    # tableauhyperapi is heavy; import lazily so module import stays cheap.
    from tableauhyperapi import (
        Connection, CreateMode, HyperProcess, Telemetry,
    )

    with tempfile.TemporaryDirectory() as td:
        zf = zipfile.ZipFile(io.BytesIO(twbx))
        hypers = []
        for member in zf.namelist():
            if member.endswith(".hyper"):
                dest = os.path.join(td, os.path.basename(member))
                with open(dest, "wb") as fh:
                    fh.write(zf.read(member))
                hypers.append(dest)
        if not hypers:
            raise RuntimeError("no .hyper extract found inside .twbx")

        with HyperProcess(
            telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU
        ) as hp:
            # Pick the publishable extract deterministically: most rows, then
            # (on a row-count tie, e.g. several yearly conference tables) the
            # richest by column count. Sorted iteration + strict-greater keeps
            # the choice stable across runs so the published schema can't churn.
            best = None  # ((row_count, col_count), hyper_path, table_name)
            for h in sorted(hypers):
                with Connection(hp.endpoint, h, CreateMode.NONE) as conn:
                    for schema in sorted(conn.catalog.get_schema_names(), key=str):
                        for tbl in sorted(conn.catalog.get_table_names(schema), key=str):
                            n = conn.execute_scalar_query(
                                f"SELECT COUNT(*) FROM {tbl}"
                            )
                            ncols = len(conn.catalog.get_table_definition(tbl).columns)
                            key = (n, ncols)
                            if best is None or key > best[0]:
                                best = (key, h, tbl)

            _, hyper_path, table = best
            with Connection(hp.endpoint, hyper_path, CreateMode.NONE) as conn:
                tdef = conn.catalog.get_table_definition(table)
                cols = _clean_columns([c.name.unescaped for c in tdef.columns])
                rows = []
                for r in conn.execute_list_query(f"SELECT * FROM {table}"):
                    rows.append(
                        {cols[i]: _jsonify(v) for i, v in enumerate(r)}
                    )
    return rows


def fetch_one(node_id: str) -> None:
    """Download one JNTO Tableau workbook and write its largest extract as
    ndjson. The runtime passes the spec id, which is also the asset name."""
    asset = node_id
    repo = ID_TO_REPO[node_id]
    twbx = _download_twbx(repo)
    rows = _largest_table_rows(twbx)
    if not rows:
        raise RuntimeError(f"{repo}: largest extract had no rows")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_sid(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# One published Delta table per workbook. The fetch fn already normalized the
# columns, so the transform is a thin pass-through; the runtime's "0 rows = node
# failure" rule is the correctness gate (every largest extract has >=15 rows).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
