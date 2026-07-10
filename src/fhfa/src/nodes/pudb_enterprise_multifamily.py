"""Enterprise PUDB — multifamily. One zip per year, latest snapshot only;
each zip holds an fnma + fhlmc CSV that share a schema."""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import _int_casts, _latest_year_zip, _pudb_zip_to_parquet

PUDB_MF_URL = "https://www.fhfa.gov/document/d/pud/{year}_pudb_mf_nfp.zip"
PUDB_MF_COLS = [
    "enterprise", "record_num_mf_nf", "tract_minority_cat", "tract_income_cat",
    "afford_mf", "same_year_acq", "purpose_mf_nf", "seller_type_mf_nf",
    "fed_guarantee_mf_nf", "units_num_cat",
]


def fetch_pudb_enterprise_multifamily(node_id: str) -> None:
    _pudb_zip_to_parquet(_latest_year_zip(PUDB_MF_URL), PUDB_MF_COLS, node_id)


DOWNLOAD_SPECS = []

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fhfa-pudb-enterprise-multifamily-transform",
        deps=["fhfa-pudb-enterprise-multifamily"],
        sql=f'''
            SELECT
            {_int_casts(PUDB_MF_COLS)}
            FROM "fhfa-pudb-enterprise-multifamily"
        ''',
    ),
]
