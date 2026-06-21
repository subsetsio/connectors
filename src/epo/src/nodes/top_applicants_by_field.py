"""EPO top applicants by technology field (field-top-applicants.json)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import fetch_json


def fetch_top_applicants_by_field(node_id: str) -> None:
    """field-top-applicants.json: dict keyed '<field_id>_field_top_applicants_<year>_tng',
    each value a ranked list of {applicant_name, number_of_applications}."""
    data = fetch_json("field-top-applicants.json")
    rows = []
    for key, applicants in data.items():
        field_id = key.split("_field_top_applicants_")[0]
        for rec in applicants:
            rows.append(
                {
                    "field_id": field_id,
                    "applicant_name": rec.get("applicant_name"),
                    "number_of_applications": rec.get("number_of_applications"),
                }
            )
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="epo-top-applicants-by-field",
        fn=fetch_top_applicants_by_field,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="epo-top-applicants-by-field-transform",
        deps=["epo-top-applicants-by-field"],
        sql='''
            SELECT
                CAST(field_id AS INTEGER) AS field_id,
                applicant_name,
                CAST(number_of_applications AS BIGINT) AS number_of_applications
            FROM "epo-top-applicants-by-field"
            WHERE applicant_name IS NOT NULL AND applicant_name <> ''
        ''',
    ),
]
