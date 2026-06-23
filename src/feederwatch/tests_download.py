"""Health-invariant tests for the FeederWatch raw downloads.

Run post-DAG inside the connector. The observations asset is tens of millions
of rows, so we read row counts / schema via parquet metadata
(`raw_parquet_localpath` + ParquetFile) rather than materializing the table.
"""

import pyarrow.parquet as pq

from subsets_utils import raw_parquet_localpath


def _num_rows(asset_id: str) -> int:
    with raw_parquet_localpath(asset_id) as path:
        return pq.ParquetFile(path).metadata.num_rows


def _columns(asset_id: str) -> list[str]:
    with raw_parquet_localpath(asset_id) as path:
        return list(pq.ParquetFile(path).schema_arrow.names)


def test_all_raw_assets_nonempty(spec_ids):
    """Empty payloads usually mean the entry page changed or a download was
    truncated. Every fetched asset must hold rows."""
    for sid in spec_ids:
        n = _num_rows(sid)
        assert n > 0, f"{sid}: raw parquet has 0 rows"


def test_observations_schema():
    """The 24-column checklist schema is the contract the transform casts off
    of; a missing key column means the source layout shifted."""
    names = _columns("feederwatch-observations")
    for col in ("LOC_ID", "OBS_ID", "SPECIES_CODE", "Year", "HOW_MANY"):
        assert col in names, f"observations raw missing column {col!r}"
    assert _num_rows("feederwatch-observations") > 1_000_000, (
        "observations raw far smaller than expected — likely not all year-range "
        "ZIPs were fetched"
    )


def test_site_descriptions_schema():
    names = _columns("feederwatch-site-descriptions")
    for col in ("loc_id", "proj_period_id"):
        assert col in names, f"site descriptions raw missing column {col!r}"


def test_species_translation_schema():
    names = _columns("feederwatch-species-translation")
    for col in ("species_code", "scientific_name", "american_english_name"):
        assert col in names, f"species translation raw missing column {col!r}"
