"""EPO top applicants by country (applicant.json)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import fetch_json


def fetch_top_applicants_by_country(node_id: str) -> None:
    """applicant.json: dict keyed '<country>_top_applicants_<year>_tng', each
    value a ranked list of {applicant_name, number_of_applications}."""
    data = fetch_json("applicant.json")
    rows = []
    for key, applicants in data.items():
        cc = key.split("_top_applicants_")[0].upper()  # 'US'; global -> 'ALL'
        for rec in applicants:
            rows.append(
                {
                    "country_code": cc,
                    "applicant_name": rec.get("applicant_name"),
                    "number_of_applications": rec.get("number_of_applications"),
                }
            )
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="epo-top-applicants-by-country",
        fn=fetch_top_applicants_by_country,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="epo-top-applicants-by-country-transform",
        deps=["epo-top-applicants-by-country"],
        sql='''
            SELECT
                country_code,
                applicant_name,
                CAST(number_of_applications AS BIGINT) AS number_of_applications
            FROM "epo-top-applicants-by-country"
            WHERE applicant_name IS NOT NULL AND applicant_name <> ''
        ''',
    ),
]
