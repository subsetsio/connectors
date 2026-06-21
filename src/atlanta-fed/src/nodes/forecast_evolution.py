"""GDPNow forecast evolution — one row per within-quarter forecast update
(since 2011:Q3): how the GDP nowcast moves as new data releases arrive.

Source: the GDPNow workbook's TrackingDeepArchives (2011-2014) +
TrackingArchives (2014-present) sheets, which together hold the full clean
long-format history. (The in-progress current quarter lives in a separate
wide-block sheet and rolls into the archive at quarter end; we publish the
archived history, which stays fresh each quarter.) Downloads the shared
workbook and parses those sheets into typed parquet.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import date_str, download_workbook, num, read_sheet


# Sheets we parse (everything else in the workbook is model internals).
EVOLUTION_SHEETS = ["TrackingDeepArchives", "TrackingArchives"]

EVOLUTION_SCHEMA = pa.schema([
    ("forecast_date", pa.string()),
    ("quarter_end_date", pa.string()),
    ("gdp_nowcast", pa.float64()),
    ("bea_advance_estimate", pa.float64()),
    ("forecast_error", pa.float64()),
    ("data_release", pa.string()),
])


def fetch_forecast_evolution(node_id: str) -> None:
    asset = node_id
    content = download_workbook()

    col_fd = "Forecast Date"
    col_q = "Quarter being forecasted"
    col_gdp = "GDP Nowcast"
    col_bea = "Advance Estimate From BEA"
    col_err = "Forecast Error"
    col_rel = "Data releases"  # present only in TrackingArchives

    rows = []
    for sheet in EVOLUTION_SHEETS:
        for r in read_sheet(content, sheet):
            fdate = date_str(r.get(col_fd))
            quarter = date_str(r.get(col_q))
            gdp = num(r.get(col_gdp))
            if fdate is None or quarter is None or gdp is None:
                continue
            release = r.get(col_rel)
            release = str(release).strip() if isinstance(release, str) and release.strip() else None
            rows.append({
                "forecast_date": fdate,
                "quarter_end_date": quarter,
                "gdp_nowcast": gdp,
                "bea_advance_estimate": num(r.get(col_bea)),
                "forecast_error": num(r.get(col_err)),
                "data_release": release,
            })

    table = pa.Table.from_pylist(rows, schema=EVOLUTION_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="atlanta-fed-gdpnow-forecast-evolution",
        fn=fetch_forecast_evolution,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="atlanta-fed-gdpnow-forecast-evolution-transform",
        deps=["atlanta-fed-gdpnow-forecast-evolution"],
        sql='''
            SELECT DISTINCT
                CAST(forecast_date AS DATE)        AS forecast_date,
                CAST(quarter_end_date AS DATE)     AS quarter_end_date,
                CAST(gdp_nowcast AS DOUBLE)        AS gdp_nowcast,
                CAST(bea_advance_estimate AS DOUBLE) AS bea_advance_estimate,
                CAST(forecast_error AS DOUBLE)     AS forecast_error,
                data_release
            FROM "atlanta-fed-gdpnow-forecast-evolution"
            WHERE forecast_date IS NOT NULL
              AND gdp_nowcast IS NOT NULL
        ''',
    ),
]
