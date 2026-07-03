"""AAVSO VSX (Variable Star Index) catalog connector.

Downloads AAVSO's Variable Star Index — the master catalog of known and
suspected variable stars (~10.3M objects) — via the CDS VizieR TAP service
(table B/vsx/vsx), the chosen `vizier_tap` mechanism. AAVSO publishes no bulk
dump of the AID observation time series, so the publishable unit for this
connector is the object catalog itself.

Shape: stateless full re-pull. The catalog is bounded (~10.3M rows) and fully
re-fetchable each run, so there is no watermark/cursor. It is large enough that
we page through it by the monotonic `recno` key (TOP N WHERE recno > last
ORDER BY recno) and stream batches straight to a single parquet asset, keeping
memory bounded. Re-pulling the whole catalog also picks up VSX revisions for
free. Raw is written typed (numerics as doubles, empties as nulls); the
transform only trims, renames and projects.
"""

import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
)

_TAP = "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync"
_TABLE = "B/vsx/vsx"

# Column order is fixed by the explicit SELECT below; the raw parquet schema
# mirrors it exactly so every streamed page conforms. Flag/passband columns
# stay string; coordinates/magnitudes/epoch/period are parsed to doubles
# (empty cells -> null).
_SCHEMA = pa.schema([
    ("recno", pa.int64()),
    ("OID", pa.int64()),
    ("Name", pa.string()),
    ("V", pa.int64()),
    ("RAJ2000", pa.float64()),
    ("DEJ2000", pa.float64()),
    ("Type", pa.string()),
    ("l_max", pa.string()),
    ("max", pa.float64()),
    ("u_max", pa.string()),
    ("n_max", pa.string()),
    ("f_min", pa.string()),
    ("l_min", pa.string()),
    ("min", pa.float64()),
    ("u_min", pa.string()),
    ("n_min", pa.string()),
    ("Epoch", pa.float64()),
    ("u_Epoch", pa.string()),
    ("l_Period", pa.string()),
    ("Period", pa.float64()),
    ("u_Period", pa.string()),
    ("Sp", pa.string()),
    ("n_OID", pa.string()),
])
_COLS = [f.name for f in _SCHEMA]
_COL_TYPES = {f.name: f.type for f in _SCHEMA}

_PAGE = 100_000          # rows per TAP request; TOP 200000 confirmed honored
_MAX_PAGES = 400         # safety ceiling: ~104 pages expected for ~10.3M rows


@transient_retry()
def _fetch_page(after_recno: int) -> bytes:
    """One page of the catalog, CSV bytes, ordered by recno."""
    query = (
        f'SELECT TOP {_PAGE} {",".join(_COLS)} FROM "{_TABLE}" '
        f"WHERE recno > {after_recno} ORDER BY recno"
    )
    resp = get(
        _TAP,
        params={"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv", "QUERY": query},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    return resp.content


def fetch_catalog(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    after = 0
    pages = 0
    total = 0
    with raw_parquet_writer(asset, _SCHEMA) as writer:
        while True:
            if pages >= _MAX_PAGES:
                raise RuntimeError(
                    f"{asset}: hit safety cap of {_MAX_PAGES} pages "
                    f"(after recno={after}, {total} rows) — VSX likely grew; "
                    "raise _MAX_PAGES."
                )
            raw = _fetch_page(after)
            table = pacsv.read_csv(
                io.BytesIO(raw),
                convert_options=pacsv.ConvertOptions(
                    column_types=_COL_TYPES, strings_can_be_null=True
                ),
            ).select(_COLS)
            n = table.num_rows
            pages += 1
            if n == 0:
                break
            writer.write_table(table)
            total += n
            after = table.column("recno")[n - 1].as_py()
            if n < _PAGE:
                break
    print(f"  {asset}: wrote {total:,} rows over {pages} page(s)")


DOWNLOAD_SPECS = [
    NodeSpec(id="aavso-vsx-catalog", fn=fetch_catalog, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="aavso-vsx-catalog-transform",
        deps=["aavso-vsx-catalog"],
        key=("oid",),
        sql='''
            SELECT
                recno,
                OID                                   AS oid,
                TRIM(Name)                            AS name,
                V                                     AS variability_flag,
                RAJ2000                               AS ra_deg,
                DEJ2000                               AS dec_deg,
                NULLIF(TRIM(Type), '')                AS variability_type,
                NULLIF(TRIM(l_max), '')               AS max_mag_limit_flag,
                "max"                                 AS max_mag,
                NULLIF(TRIM(n_max), '')               AS max_mag_band,
                NULLIF(TRIM(f_min), '')               AS min_is_amplitude_flag,
                NULLIF(TRIM(l_min), '')               AS min_mag_limit_flag,
                "min"                                 AS min_mag,
                NULLIF(TRIM(n_min), '')               AS min_mag_band,
                Epoch                                 AS epoch_jd,
                Period                                AS period_days,
                NULLIF(TRIM(Sp), '')                  AS spectral_type
            FROM "aavso-vsx-catalog"
            WHERE OID IS NOT NULL
        ''',
    ),
]
