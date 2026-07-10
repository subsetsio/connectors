"""EPO Statistics & Trends Centre — the five static JSON files behind the
Technology Dashboard (the former annual Patent Index).

countries.json           wide counts per country x metric x field x year
countries-metadata.json  country dimension (incl. the 'ALL' / 'ROW' aggregates)
fields-metadata.json     the 35 WIPO technology fields
applicant.json           top-10 applicants per country, one edition
field-top-applicants.json  top-10 applicants per technology field, one edition

The two top-applicant files carry their edition year only inside the JSON key
('<cc>_top_applicants_2025_tng'); it is parsed out into an `edition_year`
column so the tables stay self-describing as editions roll forward.
"""

import re

from subsets_utils import NodeSpec, save_raw_ndjson
from utils import fetch_json

# The source's own whole-world aggregate, spelled 'all_countries' in
# countries.json but 'all' in applicant.json. countries-metadata.json gives it
# the canonical country_code 'ALL' ("All states", county_id 500), so both
# normalise onto that and stay joinable to the country dimension.
AGGREGATE = "ALL"

_GRANTS_KEY = re.compile(r"^(?P<country>.+)_(?P<metric>applications|grants)_tng$")
_APPLICANT_KEY = re.compile(r"^(?P<group>.+)_top_applicants_(?P<year>\d{4})_tng$")
_FIELD_APPLICANT_KEY = re.compile(
    r"^(?P<field_id>\d+)_field_top_applicants_(?P<year>\d{4})_tng$"
)


def fetch_countries(node_id: str) -> None:
    """countries-metadata.json: a flat list of country records."""
    save_raw_ndjson(fetch_json("countries-metadata.json"), node_id)


def fetch_fields(node_id: str) -> None:
    """fields-metadata.json: a flat list of technology-field records."""
    save_raw_ndjson(fetch_json("fields-metadata.json"), node_id)


def fetch_patent_applications_grants(node_id: str) -> None:
    """countries.json: dict keyed '<country>_<metric>_tng', each value a list of
    rows keyed by field_id with one column per year. Unpivot to long format:
    (country_code, metric, field_id, year, value)."""
    data = fetch_json("countries.json")
    rows = []
    for key, series in data.items():
        m = _GRANTS_KEY.match(key)
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


def fetch_top_applicants_by_country(node_id: str) -> None:
    """applicant.json: dict keyed '<country>_top_applicants_<year>_tng', each
    value a list of {applicant_name, number_of_applications} in descending rank
    order."""
    data = fetch_json("applicant.json")
    rows = []
    for key, applicants in data.items():
        m = _APPLICANT_KEY.match(key)
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


def fetch_top_applicants_by_field(node_id: str) -> None:
    """field-top-applicants.json: dict keyed
    '<field_id>_field_top_applicants_<year>_tng', each value a list of
    {applicant_name, number_of_applications} in descending rank order."""
    data = fetch_json("field-top-applicants.json")
    rows = []
    for key, applicants in data.items():
        m = _FIELD_APPLICANT_KEY.match(key)
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
    NodeSpec(id="epo-countries", fn=fetch_countries, kind="download"),
    NodeSpec(id="epo-fields", fn=fetch_fields, kind="download"),
    NodeSpec(
        id="epo-patent-applications-grants",
        fn=fetch_patent_applications_grants,
        kind="download",
    ),
    NodeSpec(
        id="epo-top-applicants-by-country",
        fn=fetch_top_applicants_by_country,
        kind="download",
    ),
    NodeSpec(
        id="epo-top-applicants-by-field",
        fn=fetch_top_applicants_by_field,
        kind="download",
    ),
]
