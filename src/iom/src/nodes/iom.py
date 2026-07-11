"""IOM connector - Missing Migrants bulk CSV feed.

Missing Migrants is a single unauthenticated bulk CSV re-pulled in full every
run. DTM is intentionally not downloaded: the HDX metadata denies
redistribution and derivative works.

Raw is saved as all-string parquet (faithful copy of the CSV cells, "" -> null);
the model stage profiles this raw and compiles the typed transform.

Missing Migrants sits behind a WAF that 403s both our default User-Agent and
browser-like UAs but serves a 200 to a plain bot UA (observed while probing) --
hence the explicit MM_HEADERS below.
"""
import csv
import io

import pyarrow as pa
from subsets_utils import NodeSpec, get, save_raw_parquet, transient_retry

# --- sources ----------------------------------------------------------------

MM_CSV_URL = (
    "https://missingmigrants.iom.int/sites/g/files/tmzbdl601/files/"
    "report-migrant-incident/Missing_Migrants_Global_Figures_allData.csv"
)
# This host's WAF blocks the default and browser UAs but allows a plain bot UA.
MM_HEADERS = {"User-Agent": "subsets-bot/1.0"}

# CSV header -> snake_case raw column name. Authoritative column contract;
# a missing header raises (the source changed shape) rather than silently
# producing a short table.
MM_COLUMNS = {
    "Main ID": "main_id",
    "Incident ID": "incident_id",
    "Incident Type": "incident_type",
    "Region of Incident": "region_of_incident",
    "Incident Date": "incident_date",
    "Incident Year": "incident_year",
    "Month": "month",
    "Number of Dead": "number_dead",
    "Minimum Estimated Number of Missing": "min_estimated_missing",
    "Total Number of Dead and Missing": "total_dead_and_missing",
    "Number of Survivors": "number_survivors",
    "Number of Females": "number_females",
    "Number of Males": "number_males",
    "Number of Children": "number_children",
    "Country of Origin": "country_of_origin",
    "Region of Origin": "region_of_origin",
    "Cause of Death": "cause_of_death",
    "Country of Incident": "country_of_incident",
    "Migration Route": "migration_route",
    "Location of Incident": "location_of_incident",
    "Coordinates": "coordinates",
    "UNSD Geographical Grouping": "unsd_geographical_grouping",
    "Information Source": "information_source",
    "URL": "source_url",
    "Source Quality": "source_quality",
}


# --- helpers ----------------------------------------------------------------


@transient_retry()
def _http_get(url, *, headers=None, params=None):
    resp = get(url, headers=headers or {}, params=params or {}, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp


def _parse_csv(content_bytes):
    """Return (header, rows) from CSV bytes, stripping a UTF-8 BOM if present."""
    text = content_bytes.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(text))
    header = next(reader)
    rows = list(reader)
    return header, rows


def _save_csv_as_parquet(header, rows, colmap, asset):
    """Write the selected CSV columns as an all-string parquet ("" -> null)."""
    idx = {h: i for i, h in enumerate(header)}
    missing = [h for h in colmap if h not in idx]
    if missing:
        raise AssertionError(f"{asset}: CSV header missing expected columns: {missing}")

    schema = pa.schema([pa.field(name, pa.string()) for name in colmap.values()])
    columns = {}
    for src_col, name in colmap.items():
        i = idx[src_col]
        columns[name] = [
            (row[i] if i < len(row) and row[i] != "" else None) for row in rows
        ]
    table = pa.Table.from_pydict(columns, schema=schema)
    save_raw_parquet(table, asset)


# --- fetch fns --------------------------------------------------------------


def fetch_missing_migrants(node_id):
    asset = node_id
    header, rows = _parse_csv(_http_get(MM_CSV_URL, headers=MM_HEADERS).content)
    _save_csv_as_parquet(header, rows, MM_COLUMNS, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="iom-missing-migrants", fn=fetch_missing_migrants, kind="download"),
]
