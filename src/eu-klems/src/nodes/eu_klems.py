"""EU KLEMS connector (wiiw KLEMS 2019 release).

Six bulk CSV modules, each a stable URL under https://euklems.eu/bulk/.
Mechanism: bulk_csv (per research). Each file is the full all-countries table
in one shot — no auth, no pagination, no incremental filter. Fetch shape (1):
stateless full re-pull, overwrite each refresh (the source republishes per
release, not continuously; freshness is the maintain step's concern).

The modules ship in two physical layouts:
  * wide-by-year  — descriptor cols (incl. a `var` column naming the measure)
                    plus one column per year 1995..2017
                    (Capital, Growth-Accounts statistical, Labour, National-Accounts).
  * long-by-year / wide-by-variable — a `year` column plus one column per
                    measure (Analytical Growth-Accounts, Intangibles).

Both are normalized in the fetch fn to one long shape: the module's descriptor
columns + `var` (the measure code) + `year` (int) + `value` (double). All-null
melted cells are dropped. Each module publishes its own Delta table — schemas
differ across modules (different descriptor/industry/breakdown columns), which
is exactly why collect kept them as six separate subsets.
"""
import io


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

# NOTE: pandas / pyarrow are imported *inside* the fetch functions, not at module
# level. The harness's local spec-introspection runs from the repo root where a
# `secrets.py` shadows the stdlib module numpy lazily imports; a module-level
# `import pandas` would trip that during introspection. Production runs standalone
# (clean sys.path) so the deferred import resolves normally there.

# entity_id -> bulk filename. spec id = f"eu-klems-{entity_id}" (ids are already
# lowercase/hyphenated). The entity union (rank-active subsets) is exactly these six.
_MODULE_FILE = {
    "analytical-growth-accounts": "Analytical_Growth-Accounts.csv",
    "analytical-intangibles": "Analytical_Intangibles-(suppl).csv",
    "statistical-capital": "Statistical_Capital.csv",
    "statistical-growth-accounts": "Statistical_Growth-Accounts.csv",
    "statistical-labour": "Statistical_Labour.csv",
    "statistical-national-accounts": "Statistical_National-Accounts.csv",
}

_BULK_BASE = "https://euklems.eu/bulk/"

# Descriptor (dimension) columns that may appear across the modules. Everything
# that is neither one of these nor a 4-digit year column is a measure column.
_DIM_COLS = {
    "country", "db", "var", "code", "Sort_ID", "indnr", "nace_r2",
    "gender", "age", "edu", "year",
}


@transient_retry()
def _download_csv(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _normalize_long(df):
    """Melt either physical layout to one long frame: descriptors + var + year + value."""
    import pandas as pd

    year_cols = [c for c in df.columns if str(c).isdigit()]
    if year_cols:
        # wide-by-year: a `var` column already names the measure; melt the years.
        id_vars = [c for c in df.columns if c not in year_cols]
        long = df.melt(id_vars=id_vars, value_vars=year_cols,
                       var_name="year", value_name="value")
    else:
        # long-by-year / wide-by-variable: a `year` column exists; the measure
        # name lives in the column header — melt the measure columns into `var`.
        dim_vars = [c for c in df.columns if c in _DIM_COLS]
        measure_cols = [c for c in df.columns if c not in _DIM_COLS and not str(c).isdigit()]
        if not measure_cols:
            raise AssertionError("no measure columns found in long-by-year layout")
        long = df.melt(id_vars=dim_vars, value_vars=measure_cols,
                       var_name="var", value_name="value")

    long["year"] = pd.to_numeric(long["year"], errors="raise").astype("int32")
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    long = long.dropna(subset=["value"])
    return long


def _to_arrow(long):
    """Explicit, stable types: year int32, value float64, every descriptor a string."""
    import pyarrow as pa

    fields = []
    arrays = []
    for col in long.columns:
        if col == "year":
            fields.append(pa.field("year", pa.int32()))
            arrays.append(pa.array(long["year"].to_numpy(), type=pa.int32()))
        elif col == "value":
            fields.append(pa.field("value", pa.float64()))
            arrays.append(pa.array(long["value"].to_numpy(), type=pa.float64()))
        else:
            fields.append(pa.field(col, pa.string()))
            # Coerce descriptor codes (some are ints upstream) to clean strings.
            s = long[col].astype("string")
            arrays.append(pa.array(s.where(s.notna(), None).to_list(), type=pa.string()))
    return pa.Table.from_arrays(arrays, schema=pa.schema(fields))


def fetch_one(node_id: str) -> None:
    import pandas as pd

    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len("eu-klems-"):]
    filename = _MODULE_FILE[entity_id]
    content = _download_csv(_BULK_BASE + filename)
    df = pd.read_csv(io.BytesIO(content))
    long = _normalize_long(df)
    if long.empty:
        raise AssertionError(f"{asset}: normalized frame is empty")
    table = _to_arrow(long)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"eu-klems-{eid}", fn=fetch_one, kind="download")
    for eid in _MODULE_FILE
]

# One published Delta table per module. Raw is already long and typed; the
# transform is the correctness gate — it republishes only non-null observations
# (a 0-row result fails the node).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}" WHERE value IS NOT NULL',
    )
    for s in DOWNLOAD_SPECS
]
