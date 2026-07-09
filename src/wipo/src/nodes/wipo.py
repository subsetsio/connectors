"""WIPO IP Statistics Data Center — every download node.

Three sub-modules of the same REST backend drive three fetch shapes:

``ips-search`` (patent / trademark / industrial design / geographical
indication / country profiles)
    ``formcontrols?selectedTab=<tab>`` enumerates the indicators
    (``ipsIndicatorMap``) and report types (``ipsRpTypeMap``: 11 = by filing
    office, 13 = by applicant origin, 15 = by office + origin); each
    ``table-result`` call returns the full office x origin x year matrix for one
    indicator+reportType over the whole 1980->latest range. No office/origin
    selection params are needed (the backend defaults to all). Value quirk: some
    ips report types pack a resident/non-resident/total style breakdown into a
    single cell as a comma-joined string (e.g. ``"19800,23000,3200"``, variable
    length 1-4). Each cell is exploded faithfully into one row per position,
    recording the position as ``breakdown_index``.

``pmh-search`` (PCT / Madrid / Hague filings — the WIPO-administered systems)
    Same ``formcontrols`` shape (``pmhIndicatorMap`` / ``pmhRpTypeMap``:
    4001 = yearly, 4003 = monthly). Unlike ips, ``table-result`` returns null
    unless the office and origin codes are passed explicitly: they are read from
    ``loadOffOrgClassList?indicator=<id>`` (``pmhOffList`` / ``pmhOriginList``)
    and sent as ``pmhOffSelValues`` / ``pmhOriSelValues``. Only the **yearly**
    report type (4001) is fetched, to keep one clean annual series per subset;
    the monthly series (4003, which returns ``YYYY/M`` period columns rather
    than plain years) is intentionally omitted. pmh cells use thousands
    separators and carry a single value, read from the ``_SeqOrder`` companion.

``keyindicator`` (the 11 pre-computed headline indicators)
    ``keyindicators-json`` lists them; ``keysearch-json/{id}`` returns
    {recordInfo, columns, records} with an extra IP-right column, and (like pmh)
    formats the display cell with thousands separators while route/origin
    breakdowns live in the rows rather than packed in cells.

``wipo-indicators`` is the reference taxonomy joining all three: one row per
indicator (152 across every module and tab), which every value table's
``indicator_id`` points at.

Fetch shape: stateless full re-pull every run — the API exposes no incremental
filter, and the whole corpus is a few hundred small tables. Raw is streamed to
one parquet file per subset via ``raw_parquet_writer`` (one row group per
indicator x reportType) so peak memory stays bounded even for the large
office x origin tables.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, raw_parquet_writer, save_raw_parquet
from utils import IPS_SCHEMA, get_json, parse_office_table, year_columns

# node id -> ips-search tab
IPS_TABS = {
    "wipo-patent-statistics": "patent",
    "wipo-trademark-statistics": "trademark",
    "wipo-industrial-design-statistics": "industrial",
    "wipo-geographical-indication-statistics": "geographical",
    "wipo-country-profiles": "countryprofiles",
}

# node id -> pmh-search tab
PMH_TABS = {
    "wipo-pct-filings": "pct",
    "wipo-madrid-filings": "madrid",
    "wipo-hague-filings": "hague",
}

# Schema for the pre-computed key-indicator subset (has an IP-right column).
KEY_SCHEMA = pa.schema([
    ("indicator_id", pa.int32()),
    ("indicator", pa.string()),
    ("ip_right", pa.string()),
    ("office", pa.string()),
    ("origin", pa.string()),
    ("year", pa.int32()),
    ("breakdown_index", pa.int32()),
    ("value", pa.float64()),
])

# Schema for the cross-module indicator reference catalog.
INDICATOR_SCHEMA = pa.schema([
    ("indicator_id", pa.int32()),
    ("module", pa.string()),
    ("tab", pa.string()),
    ("label", pa.string()),
    ("report_types", pa.string()),
])


# --------------------------------------------------------------------------- #
# ips-search
# --------------------------------------------------------------------------- #
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


# --------------------------------------------------------------------------- #
# pmh-search
# --------------------------------------------------------------------------- #
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
    if yearly is None:
        raise AssertionError(f"{asset}: pmh tab '{tab}' exposes no yearly report type")
    rt_value = yearly["value"]
    report_type = yearly.get("label") or "Yearly statistics"

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


# --------------------------------------------------------------------------- #
# keyindicator
# --------------------------------------------------------------------------- #
def _parse_key_table(data: dict, indicator_id: int, indicator: str) -> list[dict]:
    """Parse a keyindicator keysearch-json envelope into long-format rows.

    Unlike the ips table-result endpoint, keysearch-json formats the displayed
    cell with thousands separators (``"1,202,500"``) and route/origin breakdowns
    live in the rows (the ``origin`` column), not packed in cells -- so each
    (row, year) is a single value. We read the clean numeric companion
    ``<year>_SeqOrder`` rather than parse the comma-formatted display string.
    """
    cols = year_columns(data.get("columns") or [])
    rows: list[dict] = []
    for rec in data.get("records") or []:
        ip_right = rec.get("ipr")
        office = rec.get("office")
        origin = rec.get("origin")
        for code, year in cols:
            raw = rec.get(f"{code}_SeqOrder")
            if raw is None or raw == "":
                continue
            try:
                value = float(raw)
            except (TypeError, ValueError):
                continue
            rows.append({
                "indicator_id": indicator_id,
                "indicator": indicator,
                "ip_right": ip_right,
                "office": office,
                "origin": origin,
                "year": year,
                "breakdown_index": 0,
                "value": value,
            })
    return rows


def fetch_keyindicator(node_id: str) -> None:
    """Fetch all 11 pre-computed headline key indicators."""
    asset = node_id
    catalog = get_json("keyindicator/keyindicators-json", {})
    if not isinstance(catalog, dict) or not catalog:
        raise AssertionError(f"{asset}: empty keyindicators-json catalog")

    written = 0
    with raw_parquet_writer(asset, KEY_SCHEMA) as writer:
        for key_id, label in catalog.items():
            data = get_json(f"keyindicator/keysearch-json/{key_id}", {})
            rows = _parse_key_table(data, int(key_id), str(label))
            if rows:
                writer.write_table(pa.Table.from_pylist(rows, schema=KEY_SCHEMA))
                written += len(rows)
    if written == 0:
        raise AssertionError(f"{asset}: key indicators produced no rows")


# --------------------------------------------------------------------------- #
# indicator reference catalog
# --------------------------------------------------------------------------- #
def fetch_indicators(node_id: str) -> None:
    """Fetch the cross-module indicator taxonomy: one row per indicator.

    The three modules expose the same taxonomy under three shapes: ips carries
    ``indicatorId`` + a per-tab ``ipsRpTypeMap``, pmh carries a string ``value``
    + ``pmhRpTypeMap``, and keyindicator is a flat {id: label} map with no report
    types (each headline indicator is pre-aggregated). ``report_types`` joins the
    available report-type labels for the indicator's tab; it is null for the
    keyindicator module.
    """
    asset = node_id
    rows: list[dict] = []

    for tab in sorted(set(IPS_TABS.values())):
        fc = get_json("ips-search/formcontrols", {"selectedTab": tab})
        report_types = " | ".join(
            (rt.get("label") or str(rt["value"])).strip()
            for rt in (fc.get("ipsRpTypeMap") or [])
        ) or None
        for ind in fc.get("ipsIndicatorMap") or []:
            rows.append({
                "indicator_id": int(ind["indicatorId"]),
                "module": "ips-search",
                "tab": tab,
                "label": (ind.get("label") or "").strip(),
                "report_types": report_types,
            })

    for tab in sorted(set(PMH_TABS.values())):
        fc = get_json("pmh-search/formcontrols", {"selectedTab": tab})
        report_types = " | ".join(
            (rt.get("label") or str(rt["value"])).strip()
            for rt in (fc.get("pmhRpTypeMap") or [])
        ) or None
        for ind in fc.get("pmhIndicatorMap") or []:
            rows.append({
                "indicator_id": int(ind["value"]),
                "module": "pmh-search",
                "tab": tab,
                "label": (ind.get("label") or "").strip(),
                "report_types": report_types,
            })

    for key_id, label in (get_json("keyindicator/keyindicators-json", {}) or {}).items():
        rows.append({
            "indicator_id": int(key_id),
            "module": "keyindicator",
            "tab": None,
            "label": str(label).strip(),
            "report_types": None,
        })

    if not rows:
        raise AssertionError(f"{asset}: indicator catalog produced no rows")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=INDICATOR_SCHEMA), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="wipo-patent-statistics", fn=fetch_ips, kind="download"),
    NodeSpec(id="wipo-trademark-statistics", fn=fetch_ips, kind="download"),
    NodeSpec(id="wipo-industrial-design-statistics", fn=fetch_ips, kind="download"),
    NodeSpec(id="wipo-geographical-indication-statistics", fn=fetch_ips, kind="download"),
    NodeSpec(id="wipo-country-profiles", fn=fetch_ips, kind="download"),
    NodeSpec(id="wipo-pct-filings", fn=fetch_pmh, kind="download"),
    NodeSpec(id="wipo-madrid-filings", fn=fetch_pmh, kind="download"),
    NodeSpec(id="wipo-hague-filings", fn=fetch_pmh, kind="download"),
    NodeSpec(id="wipo-key-indicators", fn=fetch_keyindicator, kind="download"),
    NodeSpec(id="wipo-indicators", fn=fetch_indicators, kind="download"),
]
