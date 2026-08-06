"""LAGOS-NE lake water clarity connector (EDI package edi.101, LAGOS-NE-LIMNO).

Source: Environmental Data Initiative PASTA+ REST API
(https://pasta.lternet.edu/package). The package is LAGOS-NE-LIMNO -- in-situ
measurements of lake water quality (Secchi clarity, chlorophyll, nutrients) plus
a lake identifier/morphometry reference table, for thousands of US lakes.

Fetch shape: stateless full re-pull (shape 1). The accepted package revision is
immutable (edi.101.3), so there is no incremental delta to chase. EDI's PASTA+
service began returning 403 for unauthenticated public package/data methods in
August 2026, but the same public archived objects remain readable from EDI's
DataONE member node. The DataONE object identifiers are the original PASTA data
object URLs for revision 3, which keeps the data lineage and checksums stable.

Raw format: parquet via pyarrow's CSV reader. These are single immutable
snapshots (one full table per revision, never batched), the CSVs are clean and
well-typed, and "NA"/"" are the only missing-value tokens -- so pyarrow's type
inference (with those tokens declared null) is deterministic and correct here,
giving int64 ids, date32 sampledate, and double measurements without a 92-column
hand-written schema. The transform then re-asserts types via the test specs.
"""

import io

import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
)

SLUG = "lagos-ne"
DATAONE_OBJECT_BASE = "https://gmn.edirepository.org/mn/v2/object"

# Published subsets (the rank-accepted entity union). Each is the slug of a
# dataTable entityName in the EDI EML.
PROGRAMS = f"{SLUG}-data-source-and-program-information"
MEAS = f"{SLUG}-in-situ-measurements-of-epilimnetic-nutrients-and-secchi-data"
MORPH = f"{SLUG}-lake-identifiers-and-morphometry"

DATAONE_OBJECT_URLS = {
    PROGRAMS: (
        f"{DATAONE_OBJECT_BASE}/"
        "https%3A%2F%2Fpasta.lternet.edu%2Fpackage%2Fdata%2Feml%2Fedi%2F101%2F3%2F"
        "5dcf92157f1038958029a88c6b15f51f"
    ),
    MEAS: (
        f"{DATAONE_OBJECT_BASE}/"
        "https%3A%2F%2Fpasta.lternet.edu%2Fpackage%2Fdata%2Feml%2Fedi%2F101%2F3%2F"
        "5e2709d0c92cee77a52a6753087e75e5"
    ),
    MORPH: (
        f"{DATAONE_OBJECT_BASE}/"
        "https%3A%2F%2Fpasta.lternet.edu%2Fpackage%2Fdata%2Feml%2Fedi%2F101%2F3%2F"
        "df2f94197ed33bc6f3052511b23a721e"
    ),
}


def fetch_one(node_id: str) -> None:
    asset = node_id  # spec id IS the asset name
    try:
        url = DATAONE_OBJECT_URLS[node_id]
    except KeyError as exc:
        raise AssertionError(
            f"no DataONE object URL configured for {node_id!r}; "
            f"available: {sorted(DATAONE_OBJECT_URLS)}"
        ) from exc
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    convert = pacsv.ConvertOptions(null_values=["NA", ""], strings_can_be_null=True)
    table = pacsv.read_csv(io.BytesIO(resp.content), convert_options=convert)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=PROGRAMS, fn=fetch_one, kind="download"),
    NodeSpec(id=MEAS, fn=fetch_one, kind="download"),
    NodeSpec(id=MORPH, fn=fetch_one, kind="download"),
]
