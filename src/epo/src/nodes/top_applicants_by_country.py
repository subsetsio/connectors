"""EPO top applicants by country (applicant.json)."""

import re

from subsets_utils import NodeSpec, save_raw_ndjson
from utils import fetch_json

# '<country>_top_applicants_<year>_tng' — the edition year moves forward with
# each annual Patent Index release, so parse it rather than hard-coding it.
KEY_RE = re.compile(r"^(?P<group>.+)_top_applicants_(?P<year>\d{4})_tng$")

# The source's whole-world aggregate. Not an ISO 3166-1 code, so it can never
# collide with a real country_code.
AGGREGATE = "ALL"


def fetch_top_applicants_by_country(node_id: str) -> None:
    """applicant.json: dict keyed '<country>_top_applicants_<year>_tng', each
    value a list of {applicant_name, number_of_applications} in descending
    rank order."""
    data = fetch_json("applicant.json")
    rows = []
    for key, applicants in data.items():
        m = KEY_RE.match(key)
        if m is None:
            raise ValueError(f"unrecognised applicant.json key: {key!r}")
        group = m.group("group")
        cc = AGGREGATE if group == "all" else group.upper()
        for rank, rec in enumerate(applicants, start=1):
            rows.append(
                {
                    "country_code": cc,
                    "edition_year": m.group("year"),
                    "rank": rank,
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
