"""BioTIME connector — biodiversity time-series corpus.

Source: BioTIME 1.0 (Dornelas et al. 2018, file revision 24_06_2021), published
on Zenodo record 5026943 under CC-BY/ODbL. Two static, immutable bulk artefacts:

  - records: BioTIMEQuery_24_06_2021.zip → one large CSV (~8.5M rows) of raw
    species abundance/biomass observations, partitioned internally by STUDY_ID.
  - studies: BioTIMEMetadata_24_06_2021.csv → one row per STUDY_ID (381 studies)
    of study-level metadata (realm, taxa, location, span, methods, license).

Fetch shape: static/immutable artefact (no incremental filter — these are
versioned snapshots). Full re-pull each refresh; a later MaintainSpec gates
whether the fetch runs at all. Raw is saved faithfully as all-string columns
(the source uses the literal "NA" for missing values across mixed-type columns);
the SQL transforms do all typing via TRY_CAST so a stray "NA" becomes NULL
rather than crashing a parquet write.
"""
import csv
import io
import zipfile

import pyarrow as pa
from subsets_utils import NodeSpec, get, save_raw_parquet, raw_parquet_writer

QUERY_ZIP_URL = "https://zenodo.org/api/records/5026943/files/BioTIMEQuery_24_06_2021.zip/content"
META_CSV_URL = "https://zenodo.org/api/records/5026943/files/BioTIMEMetadata_24_06_2021.csv/content"
CITATIONS_CSV_URL = "https://zenodo.org/api/records/5026943/files/BioTIMECitations_24_06_2021.csv/content"

# Raw column names for the records table. The source CSV's first column is an
# unnamed running row index; the rest map 1:1 to the documented query schema.
RECORDS_COLS = [
    "row_id", "study_id", "day", "month", "year", "sample_desc", "plot",
    "id_species", "latitude", "longitude", "abundance", "biomass",
    "genus", "species", "genus_species",
]
RECORDS_SCHEMA = pa.schema([(c, pa.string()) for c in RECORDS_COLS])

RECORDS_BATCH = 250_000  # rows per parquet row-group flush


def _download_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _download_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content.decode("utf-8", "replace")


def _batch_to_table(rows: list[list[str]]) -> pa.Table:
    # Pad/truncate defensively to the declared width, then column-orient.
    width = len(RECORDS_COLS)
    cols = [[] for _ in range(width)]
    for r in rows:
        if len(r) != width:
            r = (r + [None] * width)[:width]
        for i in range(width):
            cols[i].append(r[i])
    return pa.table({RECORDS_COLS[i]: pa.array(cols[i], type=pa.string()) for i in range(width)},
                    schema=RECORDS_SCHEMA)


def fetch_records(node_id: str) -> None:
    """Download the zipped query CSV and stream it to parquet as strings."""
    asset = node_id
    content = _download_bytes(QUERY_ZIP_URL)
    zf = zipfile.ZipFile(io.BytesIO(content))
    member = zf.namelist()[0]
    with raw_parquet_writer(asset, RECORDS_SCHEMA) as w:
        with zf.open(member) as fh:
            reader = csv.reader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"))
            next(reader)  # drop header — positions are fixed and documented
            batch: list[list[str]] = []
            for row in reader:
                batch.append(row)
                if len(batch) >= RECORDS_BATCH:
                    w.write_table(_batch_to_table(batch))
                    batch = []
            if batch:
                w.write_table(_batch_to_table(batch))


def fetch_studies(node_id: str) -> None:
    """Download the metadata CSV (one row per STUDY_ID) and save as strings."""
    asset = node_id
    text = _download_text(META_CSV_URL)
    reader = csv.reader(io.StringIO(text))
    header = [h.strip().lower() for h in next(reader)]
    rows = list(reader)
    width = len(header)
    cols = [[] for _ in range(width)]
    for r in rows:
        if len(r) != width:
            r = (r + [None] * width)[:width]
        for i in range(width):
            cols[i].append(r[i])
    schema = pa.schema([(h, pa.string()) for h in header])
    table = pa.table({header[i]: pa.array(cols[i], type=pa.string()) for i in range(width)},
                     schema=schema)
    save_raw_parquet(table, asset)


def fetch_citations(node_id: str) -> None:
    """Download the study citation mapping CSV and save as strings."""
    asset = node_id
    text = _download_text(CITATIONS_CSV_URL)
    reader = csv.reader(io.StringIO(text))
    header = [h.strip().lower() for h in next(reader)]
    rows = list(reader)
    width = len(header)
    cols = [[] for _ in range(width)]
    for r in rows:
        if len(r) != width:
            r = (r + [None] * width)[:width]
        for i in range(width):
            cols[i].append(r[i])
    schema = pa.schema([(h, pa.string()) for h in header])
    table = pa.table({header[i]: pa.array(cols[i], type=pa.string()) for i in range(width)},
                     schema=schema)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="biotime-citations", fn=fetch_citations, kind="download"),
    NodeSpec(id="biotime-records", fn=fetch_records, kind="download"),
    NodeSpec(id="biotime-studies", fn=fetch_studies, kind="download"),
]
