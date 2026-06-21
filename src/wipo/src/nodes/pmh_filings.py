"""WIPO pmh-search subsets: PCT / Madrid / Hague filings (WIPO-administered
systems).

Same ``formcontrols`` shape as ips (``pmhIndicatorMap`` / ``pmhRpTypeMap``:
4001 = yearly, 4003 = monthly). Unlike ips, ``table-result`` returns null unless
the office and origin codes are passed explicitly: we read them from
``loadOffOrgClassList?indicator=<id>`` (``pmhOffList`` / ``pmhOriginList``) and
send them as ``pmhOffSelValues`` / ``pmhOriSelValues``. We fetch the **yearly**
report type only (4001) to keep one clean annual series per subset; the monthly
series (4003, which returns ``YYYY/M`` period columns) is intentionally omitted
from v1.

pmh cells use thousands separators and carry a single value, read from the
``_SeqOrder`` companion (``packed=False``).

Fetch shape: stateless full re-pull every run. Raw is streamed to one parquet
file per subset via ``raw_parquet_writer``.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer
from utils import IPS_SCHEMA, OFFICE_SQL, get_json, parse_office_table

# node id -> pmh-search tab
PMH_TABS = {
    "wipo-pct-filings": "pct",
    "wipo-madrid-filings": "madrid",
    "wipo-hague-filings": "hague",
}


def fetch_pmh(node_id: str) -> None:
    """Fetch one pmh-search tab (yearly statistics) for every indicator.

    pmh table-result requires the office + origin code universe to be passed
    explicitly (per indicator, from loadOffOrgClassList); without it the
    endpoint returns a null envelope.
    """
    asset = node_id
    tab = PMH_TABS[node_id]
    fc = get_json("pmh-search/formcontrols", {"selectedTab": tab})
    indicators = fc.get("pmhIndicatorMap") or []
    rtypes = fc.get("pmhRpTypeMap") or []
    fyears = [int(y) for y in (fc.get("pmhFYears") or []) if str(y).isdigit()]
    toyears = [int(y) for y in (fc.get("pmhToYearList") or []) if str(y).isdigit()]
    if not (indicators and fyears and toyears):
        raise AssertionError(f"{asset}: incomplete formcontrols for tab '{tab}'")
    from_year, to_year = min(fyears), max(toyears)

    yearly = next(
        (rt for rt in rtypes if str(rt.get("label", "")).lower().startswith("yearly")),
        None,
    )
    rt_value = yearly["value"] if yearly else "4001"
    report_type = (yearly.get("label") if yearly else None) or "Yearly statistics"

    written = 0
    with raw_parquet_writer(asset, IPS_SCHEMA) as writer:
        for ind in indicators:
            indicator_value = ind["value"]
            indicator = (ind.get("label") or "").strip()
            sel = get_json("pmh-search/loadOffOrgClassList", {"indicator": indicator_value})
            offices = list((sel.get("pmhOffList") or {}).keys())
            origins = list((sel.get("pmhOriginList") or {}).keys())
            params = {
                "selectedTab": tab,
                "indicator": indicator_value,
                "reportType": rt_value,
                "fromYear": from_year,
                "toYear": to_year,
            }
            if offices:
                params["pmhOffSelValues"] = offices
            if origins:
                params["pmhOriSelValues"] = origins
            data = get_json("pmh-search/table-result", params)
            rows = parse_office_table(data, int(indicator_value), indicator, report_type, packed=False)
            if rows:
                writer.write_table(pa.Table.from_pylist(rows, schema=IPS_SCHEMA))
                written += len(rows)
    if written == 0:
        raise AssertionError(f"{asset}: pmh-search tab '{tab}' produced no rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="wipo-pct-filings", fn=fetch_pmh, kind="download"),
    NodeSpec(id="wipo-madrid-filings", fn=fetch_pmh, kind="download"),
    NodeSpec(id="wipo-hague-filings", fn=fetch_pmh, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=OFFICE_SQL.format(dep=spec.id),
    )
    for spec in DOWNLOAD_SPECS
]
