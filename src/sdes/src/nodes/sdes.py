"""SDES DiDo connector.

One download node per rank-accepted DiDo datafile. DiDo datafiles are
heterogeneous tabular exports, so the raw stage types each CSV here, once,
and saves parquet — it does not preserve the source CSV bytes.

Why: `read_csv_auto` types a column from a 20480-row prefix sample by default,
and DiDo writes the literal string `secret` into otherwise-numeric measure
columns (CONSO, PDL) for statistically suppressed values — often tens of
thousands of rows deep. A sampled read therefore types such a column DOUBLE and
then dies on the first `secret` ("Could not convert string 'secret' to DOUBLE"),
at CSV-parse time, before any transform CAST can intervene. `sample_size=-1`
types over every row instead, so the column lands as VARCHAR and keeps the
suppression marker intact for the transform to model explicitly.

Pinning the types in parquet here (rather than at read time) also means the
transform's read needs no inference at all, so raw types cannot drift away from
the profile the model was measured against.
"""

import os
import tempfile

import duckdb

from constants import ENTITY_IDS, ENTITY_MILLESIMES
from subsets_utils import NodeSpec, get, record_source_signature, save_raw_parquet

BASE = "https://data.statistiques.developpement-durable.gouv.fr/dido/api/v1"
PREFIX = "sdes-"

SPEC_TO_RID = {f"{PREFIX}{rid.lower().replace('_', '-')}": rid for rid in ENTITY_IDS}
assert len(SPEC_TO_RID) == len(ENTITY_IDS), "spec id collision in ENTITY_IDS"


def _save_csv_as_parquet(content: bytes, node_id: str) -> None:
    """Type `content` over its full extent and save it as the raw parquet asset.

    The schema is DuckDB's full-file inference rather than a hand-declared
    `pa.schema` — there are ~180 heterogeneous datafiles and no per-file schema
    to declare. Inference over every row is deterministic for given bytes, and
    the transform contract re-checks the published shape at bind time, so a
    genuine upstream retype fails the run loudly instead of silently coercing.
    """
    fd, tmp = tempfile.mkstemp(suffix=".csv")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(content)
        con = duckdb.connect()
        try:
            save_raw_parquet(
                con.execute(
                    "SELECT * FROM read_csv_auto(?, sample_size=-1)", [tmp]
                ).arrow(),
                node_id,
            )
        finally:
            con.close()
    finally:
        os.unlink(tmp)


def fetch_one(node_id: str) -> None:
    rid = SPEC_TO_RID[node_id]
    millesime = ENTITY_MILLESIMES[rid]
    url = f"{BASE}/datafiles/{rid}/csv"
    resp = get(url, params={"millesime": millesime}, timeout=(10.0, 900.0))
    resp.raise_for_status()
    _save_csv_as_parquet(resp.content, node_id)
    record_source_signature(node_id, str(resp.url), response=resp)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{rid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for rid in ENTITY_IDS
]
