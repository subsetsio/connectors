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
    SqlNodeSpec,
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
            zf.extract("occurrence.txt", tmp)
        occ_path = os.path.join(tmp, "occurrence.txt")

        con = duckdb.connect()
        try:
            # fieldsEnclosedBy is empty in the DwC meta, so disable quoting.
            # all_varchar keeps the raw faithful; the transform casts.
            rel = con.sql(
                "SELECT * FROM read_csv('%s', delim='\\t', header=true, "
                "all_varchar=true, quote='', nullstr='')" % occ_path
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


# --- transforms: one published Delta table per subset -------------------------
# The four "rich" occurrence cores (North Atlantic + Pacific phyto/zoo) carry the
# full DwC sampling fields (date, position, depth, taxon). The three "lean" cores
# (Scotian Shelf, BCO-DMO, public CPR) carry occurrence + count + ids only, with
# sampling event position/time living in the archive's event extension.

RICH_SQL = """
SELECT
    occurrenceID                              AS occurrence_id,
    eventID                                   AS event_id,
    catalogNumber                             AS catalog_number,
    basisOfRecord                             AS basis_of_record,
    TRY_CAST(year AS INTEGER)                 AS year,
    TRY_CAST(month AS INTEGER)                AS month,
    TRY_CAST(day AS INTEGER)                  AS day,
    eventTime                                 AS event_time,
    TRY_CAST(decimalLatitude AS DOUBLE)       AS decimal_latitude,
    TRY_CAST(decimalLongitude AS DOUBLE)      AS decimal_longitude,
    TRY_CAST(minimumDepthInMeters AS DOUBLE)  AS minimum_depth_m,
    TRY_CAST(maximumDepthInMeters AS DOUBLE)  AS maximum_depth_m,
    samplingProtocol                          AS sampling_protocol,
    TRY_CAST(sampleSizeValue AS DOUBLE)       AS sample_size_value,
    sampleSizeUnit                            AS sample_size_unit,
    taxonID                                   AS taxon_id,
    scientificNameID                          AS scientific_name_id,
    scientificName                            AS scientific_name,
    acceptedNameUsage                         AS accepted_name_usage,
    TRY_CAST(modified AS TIMESTAMP)           AS modified
FROM "{dep}"
WHERE occurrenceID IS NOT NULL
"""

SCOTIAN_SQL = """
SELECT
    occurrenceID                       AS occurrence_id,
    eventID                            AS event_id,
    catalogNumber                      AS catalog_number,
    basisOfRecord                      AS basis_of_record,
    TRY_CAST(individualCount AS BIGINT) AS individual_count,
    occurrenceStatus                   AS occurrence_status,
    taxonID                            AS taxon_id,
    scientificNameID                   AS scientific_name_id
FROM "{dep}"
WHERE occurrenceID IS NOT NULL
"""

BCODMO_SQL = """
SELECT
    occurrenceID                       AS occurrence_id,
    eventID                            AS event_id,
    catalogNumber                      AS catalog_number,
    basisOfRecord                      AS basis_of_record,
    TRY_CAST(individualCount AS BIGINT) AS individual_count,
    taxonID                            AS taxon_id,
    scientificNameID                   AS scientific_name_id,
    scientificName                     AS scientific_name
FROM "{dep}"
WHERE occurrenceID IS NOT NULL
"""

CPR_PUBLIC_SQL = """
SELECT
    occurrenceID                       AS occurrence_id,
    eventID                            AS event_id,
    catalogNumber                      AS catalog_number,
    basisOfRecord                      AS basis_of_record,
    TRY_CAST(individualCount AS BIGINT) AS individual_count,
    lifeStage                          AS life_stage,
    occurrenceStatus                   AS occurrence_status,
    taxonID                            AS taxon_id,
    scientificNameID                   AS scientific_name_id,
    scientificName                     AS scientific_name
FROM "{dep}"
WHERE occurrenceID IS NOT NULL
"""

SQL_BY_ENTITY = {
    "sahfos-cpr-phyto": RICH_SQL,
    "sahfos-cpr-zoo": RICH_SQL,
    "pacific-cpr-phyto": RICH_SQL,
    "pacific-cpr-zoo": RICH_SQL,
    "scotian_shelf": SCOTIAN_SQL,
    "bco-dmo": BCODMO_SQL,
    "cpr_public": CPR_PUBLIC_SQL,
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=SQL_BY_ENTITY[RESOURCE_BY_NODE[s.id]].format(dep=s.id),
    )
    for s in DOWNLOAD_SPECS
]
