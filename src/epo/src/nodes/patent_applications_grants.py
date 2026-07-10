"""EPO patent applications & grants (countries.json) — long-format counts."""

import re

from subsets_utils import NodeSpec, save_raw_ndjson
from utils import fetch_json

# '<country>_<metric>_tng', where country is a 2-letter code or the literal
# 'all_countries' aggregate.
KEY_RE = re.compile(r"^(?P<country>.+)_(?P<metric>applications|grants)_tng$")

# The source's whole-world aggregate, normalised to the same sentinel the
# top-applicants tables use. Not an ISO 3166-1 code, so it can never collide
# with a real country_code.
AGGREGATE = "ALL"


def fetch_patent_applications_grants(node_id: str) -> None:
    """countries.json: dict keyed '<country>_<metric>_tng', each value a list of
    rows keyed by field_id with year columns. Unpivot into long format:
    (country_code, metric, field_id, year, value)."""
    data = fetch_json("countries.json")
    rows = []
    for key, series in data.items():
        m = KEY_RE.match(key)
        if m is None:
            raise ValueError(f"unrecognised countries.json key: {key!r}")
        country = m.group("country")
        cc = AGGREGATE if country == "all_countries" else country.upper()
        metric = m.group("metric")
        for rec in series:
            field_id = rec.get("field_id")
            for col, val in rec.items():
                if col.isdigit():  # year columns only
                    rows.append(
                        {
                            "country_code": cc,
                            "metric": metric,
                            "field_id": field_id,
                            "year": col,
                            "value": val,
                        }
                    )
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="epo-patent-applications-grants",
        fn=fetch_patent_applications_grants,
        kind="download",
    ),
]
