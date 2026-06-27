"""Post-DAG health invariants — catch silent degradation (empty payloads,
truncated downloads, wrong format) that file-existence checks miss."""
from subsets_utils import load_raw_parquet, load_raw_ndjson

DOCS = "open-source-asset-pricing-predictor-docs"
LS = "open-source-asset-pricing-long-short-returns"
PORTS = "open-source-asset-pricing-portfolio-sorts"


def test_predictor_docs_nonempty():
    rows = load_raw_ndjson(DOCS)
    assert len(rows) >= 250, f"{DOCS}: only {len(rows)} signal rows (expected ~331)"
    assert all("Acronym" in r for r in rows[:5]), "SignalDoc rows missing Acronym key"
    assert sum(1 for r in rows if r.get("Acronym")) >= 250, "too few non-null acronyms"


def test_long_short_nonempty():
    t = load_raw_parquet(LS)
    assert len(t) >= 100_000, f"{LS}: only {len(t)} long rows after melt"
    assert set(t.column_names) == {"date", "predictor", "ret"}, t.column_names
    assert t.column("predictor").combine_chunks().null_count == 0
    n_pred = len(set(t.column("predictor").to_pylist()))
    assert n_pred >= 150, f"{LS}: only {n_pred} distinct predictors (expected ~212)"


def test_portfolio_sorts_nonempty():
    t = load_raw_parquet(PORTS)
    assert len(t) >= 500_000, f"{PORTS}: only {len(t)} rows (expected ~800k)"
    expected = {"signalname", "port", "date", "ret", "signallag", "Nlong", "Nshort"}
    assert set(t.column_names) == expected, t.column_names
    ports = set(t.column("port").to_pylist())
    assert "LS" in ports and "01" in ports, f"port leg coverage looks wrong: {sorted(ports)}"
