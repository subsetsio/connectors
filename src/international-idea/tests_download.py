"""Health invariants for International IDEA raw assets, run post-DAG in-connector."""

from subsets_utils import load_raw_ndjson


def test_gsod_indices_panel_nonempty():
    """The GSoD panel must hold thousands of country-year rows carrying the
    ID_year / indicator keys; a collapse means the API changed or was truncated."""
    rows = load_raw_ndjson("international-idea-gsod-indices")
    assert len(rows) >= 5000, f"gsod-indices: only {len(rows)} rows (expected >=5000)"
    first = rows[0]
    assert "ID_year" in first and "ID_country_code" in first, f"missing id keys: {list(first)[:8]}"
    assert any(k.startswith(("A_", "SA_", "SC_")) for k in first), "no indicator columns present"


def test_gsod_indicators_catalog():
    """Indicator catalog should list the GSoD measures with code+name."""
    rows = load_raw_ndjson("international-idea-gsod-indicators")
    assert len(rows) >= 15, f"gsod-indicators: only {len(rows)} rows (expected >=15)"
    assert all(r.get("id") and r.get("name") for r in rows), "indicator row missing id/name"


def test_voter_turnout_rows():
    """Voter turnout 'All' sheet should carry thousands of per-election rows with
    the expected columns; a tiny count means the export schema shifted."""
    rows = load_raw_ndjson("international-idea-voter-turnout")
    assert len(rows) >= 2000, f"voter-turnout: only {len(rows)} rows (expected >=2000)"
    first = rows[0]
    for col in ("Country", "ISO3", "Election Type", "Year", "Voter Turnout"):
        assert col in first, f"voter-turnout missing column {col!r}: {list(first)}"
