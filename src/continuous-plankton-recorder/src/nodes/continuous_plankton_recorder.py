"""Continuous Plankton Recorder (CPR) Survey connector.

Mechanism: GBIF Integrated Publishing Toolkit (IPT) hosted by DASSH (Marine
Biological Association). Each CPR Survey resource is published as a self-contained
Darwin Core Archive (a zip containing a tab-delimited `occurrence.txt` core plus
metadata). We fetch one DwC-A per resource from a stable URL
(https://www.dassh.ac.uk/ipt/archive.do?r=<shortname>), stream its
`occurrence.txt` into all-VARCHAR parquet, and type/rename the columns in the
SQL transform.

Fetch shape: stateless full re-pull. The archives are static per-version files;
each resource is republished (a new version) roughly annually and we re-download
the whole archive each refresh — there is no incremental/`since` query on the IPT
and the full corpus is only a few hundred MB compressed. The largest occurrence
core is ~1.4GB uncompressed (sahfos-cpr-zoo); we extract it to a temp file and
stream it to parquet in batches via DuckDB, so peak memory stays bounded.
"""

import io
import os
import tempfile
import zipfile

import duckdb

from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
)
from constants import ENTITY_IDS

SLUG = "continuous-plankton-recorder"
ARCHIVE_URL = "https://www.dassh.ac.uk/ipt/archive.do"
BATCH_ROWS = 100_000

# node id (slug + normalized entity) -> IPT resource shortname (the `r=` value).
# entity_id IS the shortname; the node id lowercases it and maps '_' -> '-', so
# we keep an explicit reverse map to recover the exact shortname for the URL.
RESOURCE_BY_NODE = {
    f"{SLUG}-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


@transient_retry()
def _download_archive_bytes(shortname: str) -> bytes:
    resp = get(ARCHIVE_URL, params={"r": shortname}, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    """Download one CPR Survey Darwin Core Archive and persist its occurrence
    core as all-VARCHAR parquet (typing happens in the transform)."""
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    shortname = RESOURCE_BY_NODE[node_id]

    blob = _download_archive_bytes(shortname)

    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(io.BytesIO(blob)) as zf:
            names = set(zf.namelist())
            core_name = "occurrence.txt" if "occurrence.txt" in names else "taxon.txt"
            zf.extract(core_name, tmp)
        core_path = os.path.join(tmp, core_name)

        con = duckdb.connect()
        try:
            # fieldsEnclosedBy is empty in the DwC meta, so disable quoting.
            # all_varchar keeps the raw faithful; the transform casts.
            rel = con.sql(
                "SELECT * FROM read_csv('%s', delim='\\t', header=true, "
                "all_varchar=true, quote='', nullstr='')" % core_path
            )
            reader = rel.to_arrow_reader(BATCH_ROWS)
            with raw_parquet_writer(asset, reader.schema) as writer:
                for batch in reader:
                    writer.write_batch(batch)
        finally:
            con.close()


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
