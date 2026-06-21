"""GDPNow track record — one row per forecast quarter (since 2011:Q3): the
model's final nowcast vs BEA's advance estimate, with forecast errors.

Source: the GDPNow workbook's TrackRecord sheet. Downloads the shared workbook
and parses that one sheet into typed parquet (the SQL transform layer cannot
read xlsx).
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import date_str, download_workbook, num, read_sheet


# Sheet we parse (everything else in the workbook is model internals).
TRACK_RECORD_SHEET = "TrackRecord"

TRACK_RECORD_SCHEMA = pa.schema([
    ("quarter_end_date", pa.string()),
    ("gdpnow_forecast", pa.float64()),
    ("bea_advance_estimate", pa.float64()),
    ("release_date", pa.string()),
    ("error", pa.float64()),
    ("absolute_error", pa.float64()),
    ("squared_error", pa.float64()),
])


def fetch_track_record(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    col_q = "Quarter being forecasted"
    col_f = "Model Forecast Right Before BEA's Advance Estimate"
    col_a = "BEA's Advance Estimate"
    col_r = "Release Date"

    rows = []
    for r in read_sheet(download_workbook(), TRACK_RECORD_SHEET):
        quarter = date_str(r.get(col_q))
        forecast = num(r.get(col_f))
        actual = num(r.get(col_a))
        # A quarter that has not yet been forecast/realized (no model forecast
        # or no BEA advance estimate) is not a track-record row.
        if quarter is None or forecast is None or actual is None:
            continue
        err = actual - forecast
        rows.append({
            "quarter_end_date": quarter,
            "gdpnow_forecast": forecast,
            "bea_advance_estimate": actual,
            "release_date": date_str(r.get(col_r)),
            "error": round(err, 6),
            "absolute_error": round(abs(err), 6),
            "squared_error": round(err * err, 6),
        })

    table = pa.Table.from_pylist(rows, schema=TRACK_RECORD_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="atlanta-fed-gdpnow-track-record",
        fn=fetch_track_record,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="atlanta-fed-gdpnow-track-record-transform",
        deps=["atlanta-fed-gdpnow-track-record"],
        sql='''
            SELECT
                CAST(quarter_end_date AS DATE)     AS quarter_end_date,
                CAST(gdpnow_forecast AS DOUBLE)    AS gdpnow_forecast,
                CAST(bea_advance_estimate AS DOUBLE) AS bea_advance_estimate,
                CAST(release_date AS DATE)         AS release_date,
                CAST(error AS DOUBLE)              AS forecast_error,
                CAST(absolute_error AS DOUBLE)     AS absolute_error,
                CAST(squared_error AS DOUBLE)      AS squared_error
            FROM "atlanta-fed-gdpnow-track-record"
            WHERE quarter_end_date IS NOT NULL
              AND gdpnow_forecast IS NOT NULL
              AND bea_advance_estimate IS NOT NULL
        ''',
    ),
]
