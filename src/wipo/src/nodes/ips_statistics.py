"""WIPO ips-search subsets: patent / trademark / industrial design /
geographical indication / country-profiles statistics.

``formcontrols?selectedTab=<tab>`` enumerates the indicators
(``ipsIndicatorMap``) and report types (``ipsRpTypeMap``: 11 = by filing office,
13 = by applicant origin, 15 = by office + origin); each ``table-result`` call
returns the full office x origin x year matrix for one indicator+reportType over
the whole 1980->latest range. No office/origin selection params are needed for
ips (the backend defaults to all).

Value quirk: some ips report types pack a resident/non-resident/total style
breakdown into a single cell as a comma-joined string (e.g. ``"19800,23000,3200"``,
variable length 1-4). We explode each cell faithfully into one row per position,
recording the position as ``breakdown_index`` and the numeric value as ``value``.

Fetch shape: stateless full re-pull every run. Raw is streamed to one parquet
file per subset via ``raw_parquet_writer`` (one row group per indicator x
reportType) so peak memory stays bounded even for the large office x origin
tables.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer
from utils import IPS_SCHEMA, OFFICE_SQL, get_json, parse_office_table

# node id -> ips-search tab
IPS_TABS = {
    "wipo-patent-statistics": "patent",
    "wipo-trademark-statistics": "trademark",
    "wipo-industrial-design-statistics": "industrial",
    "wipo-geographical-indication-statistics": "geographical",
    "wipo-country-profiles": "countryprofiles",
}


def fetch_ips(node_id: str) -> None:
    """Fetch one ips-search tab: every indicator x report type x year."""
    asset = node_id
    tab = IPS_TABS[node_id]
    fc = get_json("ips-search/formcontrols", {"selectedTab": tab})
    indicators = fc.get("ipsIndicatorMap") or []
    rtypes = fc.get("ipsRpTypeMap") or []
    fyears = [int(y) for y in (fc.get("ipsFYears") or []) if str(y).isdigit()]
    toyears = [int(y) for y in (fc.get("ipsToYearList") or []) if str(y).isdigit()]
    if not (indicators and rtypes and fyears and toyears):
        raise AssertionError(f"{asset}: incomplete formcontrols for tab '{tab}'")
    from_year, to_year = min(fyears), max(toyears)

    written = 0
    with raw_parquet_writer(asset, IPS_SCHEMA) as writer:
        for ind in indicators:
            indicator_id = int(ind["indicatorId"])
            indicator = (ind.get("label") or "").strip()
            for rt in rtypes:
                rt_value = rt["value"]
                report_type = rt.get("label") or str(rt_value)
                data = get_json("ips-search/table-result", {
                    "selectedTab": tab,
                    "indicator": indicator_id,
                    "reportType": rt_value,
                    "fromYear": from_year,
                    "toYear": to_year,
                })
                rows = parse_office_table(data, indicator_id, indicator, report_type, packed=True)
                if rows:
                    writer.write_table(pa.Table.from_pylist(rows, schema=IPS_SCHEMA))
                    written += len(rows)
    if written == 0:
        raise AssertionError(f"{asset}: ips-search tab '{tab}' produced no rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="wipo-patent-statistics", fn=fetch_ips, kind="download"),
    NodeSpec(id="wipo-trademark-statistics", fn=fetch_ips, kind="download"),
    NodeSpec(id="wipo-industrial-design-statistics", fn=fetch_ips, kind="download"),
    NodeSpec(id="wipo-geographical-indication-statistics", fn=fetch_ips, kind="download"),
    NodeSpec(id="wipo-country-profiles", fn=fetch_ips, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=OFFICE_SQL.format(dep=spec.id),
    )
    for spec in DOWNLOAD_SPECS
]
