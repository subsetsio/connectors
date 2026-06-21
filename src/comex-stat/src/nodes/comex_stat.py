"""Comex Stat (Brazilian foreign trade statistics, MDIC/SERPRO) connector.

Mechanism: bulk CSV download (chosen mechanism `bulk_csv`). Two fetch shapes:

* Transaction corpora — one CSV per (flow, year) at /balanca/bd/comexstat-bd/.
  We resolve the latest year from the REST dates endpoint, then stream every year
  from 1997 to latest into ONE parquet asset per flow via `raw_parquet_writer`
  (bounded memory; the published Delta table covers the full history). Stateless
  full re-pull every refresh — the current year's file is overwritten in place as
  new months publish and closed years are occasionally revised, so we never trust
  a stored watermark.
* Reference tables — single auxiliary CSV each under /balanca/bd/tabelas/.

All CSVs are semicolon-delimited, double-quoted, UTF-8. We read every column as a
string (codes carry significant leading zeros — NCM, country, customs unit) and
cast only measures/year/month in the transform SQL.

TLS note: the origin omits its intermediate certificate; `utils.ensure_ca()`
completes the chain in certifi's bundle so verification stays enabled.
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
    save_raw_parquet,
)

from constants import (
    BULK_BASE,
    DATES_URL,
    START_YEAR,
    TRANSACTION_FILES,
    REFERENCE_FILES,
)
from utils import ensure_ca


# --- helpers -----------------------------------------------------------------

@transient_retry()
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _fetch_json(url: str):
    resp = get(url, timeout=(10.0, 60.0))
    resp.raise_for_status()
    return resp.json()


def _read_csv_all_string(raw: bytes) -> pa.Table:
    """Parse a semicolon-delimited, quoted CSV with every column typed as string."""
    header = raw.split(b"\n", 1)[0].decode("utf-8").replace('"', "").strip()
    cols = [c for c in header.split(";") if c]
    return pacsv.read_csv(
        io.BytesIO(raw),
        read_options=pacsv.ReadOptions(encoding="utf-8"),
        parse_options=pacsv.ParseOptions(delimiter=";"),
        convert_options=pacsv.ConvertOptions(
            column_types={c: pa.string() for c in cols},
            strings_can_be_null=True,
        ),
    )


def _latest_year() -> int:
    """Latest year with published data, per the REST dates endpoint."""
    data = _fetch_json(DATES_URL)
    return int(data["data"]["year"])


def _txn_url(subdir: str, prefix: str, year: int, suffix: str) -> str:
    return f"{BULK_BASE}/{subdir}/{prefix}_{year}{suffix}.csv"


# --- fetch fns ---------------------------------------------------------------

def fetch_transactions(node_id: str) -> None:
    """Stream every yearly CSV (1997..latest) for one trade flow into a single
    parquet asset. Schema is fixed from the first year; headers are stable across
    years, and any drift raises loudly rather than silently dropping columns."""
    ensure_ca()
    subdir, prefix, suffix = TRANSACTION_FILES[node_id]
    latest = _latest_year()
    years = list(range(START_YEAR, latest + 1))

    first = _read_csv_all_string(_fetch_bytes(_txn_url(subdir, prefix, years[0], suffix)))
    schema = first.schema
    expected = set(schema.names)

    with raw_parquet_writer(node_id, schema) as writer:
        writer.write_table(first)
        for year in years[1:]:
            table = _read_csv_all_string(_fetch_bytes(_txn_url(subdir, prefix, year, suffix)))
            if set(table.column_names) != expected:
                raise AssertionError(
                    f"{node_id}: column drift in {prefix}_{year}{suffix}.csv: "
                    f"{table.column_names} != {schema.names}"
                )
            writer.write_table(table.select(schema.names))


def fetch_reference(node_id: str) -> None:
    """Fetch a single auxiliary reference table (small enough to hold in memory)."""
    ensure_ca()
    stem = REFERENCE_FILES[node_id]
    raw = _fetch_bytes(f"{BULK_BASE}/tabelas/{stem}.csv")
    table = _read_csv_all_string(raw)
    save_raw_parquet(table, node_id)


# --- download specs ----------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="comex-stat-exports-ncm", fn=fetch_transactions, kind="download"),
    NodeSpec(id="comex-stat-imports-ncm", fn=fetch_transactions, kind="download"),
    NodeSpec(id="comex-stat-exports-municipality", fn=fetch_transactions, kind="download"),
    NodeSpec(id="comex-stat-imports-municipality", fn=fetch_transactions, kind="download"),
    NodeSpec(id="comex-stat-ncm", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-pais", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-uf-mun", fn=fetch_reference, kind="download"),
]


# --- transform specs ---------------------------------------------------------

_NCM_DETAIL_COLS = """
            CAST(CO_ANO AS INTEGER)        AS year,
            CAST(CO_MES AS INTEGER)        AS month,
            CO_NCM                         AS ncm_code,
            CO_UNID                        AS unit_code,
            CO_PAIS                        AS country_code,
            SG_UF_NCM                      AS state,
            CO_VIA                         AS transport_mode_code,
            CO_URF                         AS customs_code,
            TRY_CAST(QT_ESTAT AS BIGINT)   AS statistical_quantity,
            TRY_CAST(KG_LIQUIDO AS BIGINT) AS net_weight_kg,
            TRY_CAST(VL_FOB AS BIGINT)     AS fob_value_usd"""

_MUN_DETAIL_COLS = """
            CAST(CO_ANO AS INTEGER)        AS year,
            CAST(CO_MES AS INTEGER)        AS month,
            SH4                            AS sh4_code,
            CO_PAIS                        AS country_code,
            SG_UF_MUN                      AS state,
            CO_MUN                         AS municipality_code,
            TRY_CAST(KG_LIQUIDO AS BIGINT) AS net_weight_kg,
            TRY_CAST(VL_FOB AS BIGINT)     AS fob_value_usd"""

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="comex-stat-exports-ncm-transform",
        deps=["comex-stat-exports-ncm"],
        sql=f'SELECT{_NCM_DETAIL_COLS}\nFROM "comex-stat-exports-ncm"\nWHERE CO_ANO IS NOT NULL',
    ),
    SqlNodeSpec(
        id="comex-stat-imports-ncm-transform",
        deps=["comex-stat-imports-ncm"],
        sql=f'''SELECT{_NCM_DETAIL_COLS},
            TRY_CAST(VL_FRETE AS BIGINT)   AS freight_value_usd,
            TRY_CAST(VL_SEGURO AS BIGINT)  AS insurance_value_usd
FROM "comex-stat-imports-ncm"
WHERE CO_ANO IS NOT NULL''',
    ),
    SqlNodeSpec(
        id="comex-stat-exports-municipality-transform",
        deps=["comex-stat-exports-municipality"],
        sql=f'SELECT{_MUN_DETAIL_COLS}\nFROM "comex-stat-exports-municipality"\nWHERE CO_ANO IS NOT NULL',
    ),
    SqlNodeSpec(
        id="comex-stat-imports-municipality-transform",
        deps=["comex-stat-imports-municipality"],
        sql=f'SELECT{_MUN_DETAIL_COLS}\nFROM "comex-stat-imports-municipality"\nWHERE CO_ANO IS NOT NULL',
    ),
    SqlNodeSpec(
        id="comex-stat-ncm-transform",
        deps=["comex-stat-ncm"],
        sql='''
            SELECT
                CO_NCM         AS ncm_code,
                CO_UNID        AS unit_code,
                CO_SH6         AS sh6_code,
                CO_PPE         AS ppe_code,
                CO_PPI         AS ppi_code,
                CO_FAT_AGREG   AS factor_aggregate_code,
                CO_CUCI_ITEM   AS cuci_item_code,
                CO_CGCE_N3     AS cgce_n3_code,
                CO_SIIT        AS siit_code,
                CO_ISIC_CLASSE AS isic_class_code,
                CO_EXP_SUBSET  AS exp_subset_code,
                NO_NCM_POR     AS name_pt,
                NO_NCM_ESP     AS name_es,
                NO_NCM_ING     AS name_en
            FROM "comex-stat-ncm"
            WHERE CO_NCM IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="comex-stat-pais-transform",
        deps=["comex-stat-pais"],
        sql='''
            SELECT
                CO_PAIS       AS country_code,
                CO_PAIS_ISON3 AS iso_numeric_code,
                CO_PAIS_ISOA3 AS iso_alpha3_code,
                NO_PAIS       AS name_pt,
                NO_PAIS_ING   AS name_en,
                NO_PAIS_ESP   AS name_es
            FROM "comex-stat-pais"
            WHERE CO_PAIS IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="comex-stat-uf-mun-transform",
        deps=["comex-stat-uf-mun"],
        sql='''
            SELECT
                CO_MUN_GEO AS municipality_code,
                NO_MUN     AS name,
                NO_MUN_MIN AS name_normalized,
                SG_UF      AS state
            FROM "comex-stat-uf-mun"
            WHERE CO_MUN_GEO IS NOT NULL
        ''',
    ),
]
