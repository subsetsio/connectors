"""Post-DAG health invariants for the NCI connector.

These run in-connector after the download nodes, reading raw through the same
`subsets_utils` loader the nodes wrote with. They catch silent degradation that
file-existence alone misses: an endpoint that started returning empty/error
payloads, a truncated site crawl, or a parser that stopped matching the CSV.
"""
from subsets_utils import load_raw_ndjson

_SEER_RATE_NODES = (
    "nci-seer-explorer-seer-incidence",
    "nci-seer-explorer-us-mortality",
    "nci-seer-explorer-preliminary-incidence-rates",
)


def test_all_raw_assets_nonempty(spec_ids):
    """Every download node must have written rows."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_seer_rate_series_are_long(spec_ids):
    """Incidence/mortality must span many years and many cancer sites — a short
    span means the long-term-trends crawl degraded to a recent-rates view or a
    single site."""
    for sid in _SEER_RATE_NODES:
        if sid not in spec_ids:
            continue
        rows = load_raw_ndjson(sid)
        years = {r.get("year") for r in rows if r.get("year") is not None}
        sites = {r.get("site") for r in rows if r.get("site") is not None}
        assert len(years) >= 20, f"{sid}: only {len(years)} distinct years"
        assert len(sites) >= 20, f"{sid}: only {len(sites)} distinct sites"


def test_seer_rate_values_present(spec_ids):
    """The rate column must actually carry parseable numbers, not all nulls."""
    sid = "nci-seer-explorer-seer-incidence"
    if sid in spec_ids:
        rows = load_raw_ndjson(sid)
        numeric = 0
        for r in rows:
            try:
                float(r.get("rate"))
                numeric += 1
            except (TypeError, ValueError):
                pass
        assert numeric > 1000, f"{sid}: only {numeric} numeric rate values"


def test_scp_covers_states(spec_ids):
    """State Cancer Profiles must cover the full state set (50 states +
    territories + national); few areas means pagination/format broke."""
    for sid in ("nci-scp-incidence", "nci-scp-mortality"):
        if sid not in spec_ids:
            continue
        rows = load_raw_ndjson(sid)
        fips = {r.get("fips") for r in rows}
        cancers = {r.get("cancer_code") for r in rows}
        assert len(fips) >= 40, f"{sid}: only {len(fips)} distinct FIPS areas"
        assert len(cancers) >= 10, f"{sid}: only {len(cancers)} cancer types"
