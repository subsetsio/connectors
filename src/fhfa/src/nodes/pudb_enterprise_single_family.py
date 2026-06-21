"""Enterprise PUDB — single-family. One zip per year, latest snapshot only;
each zip holds an fnma + fhlmc CSV that share a schema."""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import _int_casts, _latest_year_zip, _pudb_zip_to_parquet

PUDB_SF_URL = "https://www.fhfa.gov/document/d/pud/{year}_pudb_sf_nfb.zip"
PUDB_SF_COLS = [
    "enterprise", "record_num_sf_nfb", "metro", "tract_minority_cat",
    "tract_income_cat", "income_cat", "same_year_acq", "purpose_sf_nfb",
    "fed_guarantee_sf_nfb", "seller_type_sf_nfb", "race_ethnicity_borr",
    "race_ethnicity_coborr", "sex_borr", "sex_coborr", "occupancy_sf_nfb",
    "units_num", "unit_own_occ", "afford_sf",
]


def fetch_pudb_enterprise_single_family(node_id: str) -> None:
    _pudb_zip_to_parquet(_latest_year_zip(PUDB_SF_URL), PUDB_SF_COLS, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fhfa-pudb-enterprise-single-family", fn=fetch_pudb_enterprise_single_family, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fhfa-pudb-enterprise-single-family-transform",
        deps=["fhfa-pudb-enterprise-single-family"],
        sql=f'''
            SELECT
            {_int_casts(PUDB_SF_COLS)}
            FROM "fhfa-pudb-enterprise-single-family"
        ''',
    ),
]
