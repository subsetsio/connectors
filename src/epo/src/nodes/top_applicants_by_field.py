"""EPO top applicants by technology field (field-top-applicants.json)."""

import re

from subsets_utils import NodeSpec, save_raw_ndjson
from utils import fetch_json

# '<field_id>_field_top_applicants_<year>_tng' — the edition year moves forward
# with each annual Patent Index release, so parse it rather than hard-coding it.
KEY_RE = re.compile(r"^(?P<field_id>\d+)_field_top_applicants_(?P<year>\d{4})_tng$")


def fetch_top_applicants_by_field(node_id: str) -> None:
    """field-top-applicants.json: dict keyed
    '<field_id>_field_top_applicants_<year>_tng', each value a list of
    {applicant_name, number_of_applications} in descending rank order."""
    data = fetch_json("field-top-applicants.json")
    rows = []
    for key, applicants in data.items():
        m = KEY_RE.match(key)
        if m is None:
            raise ValueError(f"unrecognised field-top-applicants.json key: {key!r}")
        for rank, rec in enumerate(applicants, start=1):
            rows.append(
                {
                    "field_id": m.group("field_id"),
                    "edition_year": m.group("year"),
                    "rank": rank,
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
