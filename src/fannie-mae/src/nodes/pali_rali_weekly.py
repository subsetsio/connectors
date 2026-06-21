"""Weekly Mortgage Applications (PALI/RALI) (no auth)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import _isodate, _load_rows, _num

# data-and-insights page slug + constant filename prefix.
_PAGE = ("weekly-mortgage-applications-data", "fannie-mae-pali-rali-weekly")


def fetch_pali_rali(node_id: str) -> None:
    """Weekly Mortgage Applications (PALI/RALI). Clean sheet: header row 0 =
    WK_Ending + index columns; data follows weekly. Melt to long format."""
    _, rows = _load_rows(node_id, *_PAGE)
    hdr = rows[0]
    ncols = len(hdr)
    metric_cols = []  # (col_index, metric_name)
    for c in range(1, ncols):
        v = hdr[c]
        if v is not None and str(v).strip():
            metric_cols.append((c, str(v).strip()))
    out = []
    for r in rows[1:]:
        wk = _isodate(r[0])
        if wk is None:
            continue
        for c, metric in metric_cols:
            val = _num(r[c]) if c < len(r) else None
            if val is None:
                continue
            out.append({"week_ending": wk, "metric": metric, "value": val})
    if not out:
        raise AssertionError(f"{node_id}: parsed 0 PALI/RALI rows")
    save_raw_ndjson(out, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fannie-mae-pali-rali-weekly", fn=fetch_pali_rali, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fannie-mae-pali-rali-weekly-transform",
        deps=["fannie-mae-pali-rali-weekly"],
        sql='''
            SELECT
                CAST(week_ending AS DATE) AS week_ending,
                CAST(metric AS VARCHAR)   AS metric,
                CAST(value AS DOUBLE)     AS value
            FROM "fannie-mae-pali-rali-weekly"
            WHERE value IS NOT NULL
        ''',
    ),
]
