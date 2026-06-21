"""Health invariants for the IBGE download stage.

Run post-DAG, in-connector, through the same subsets_utils loaders the fetch
nodes wrote with. Catches silent degradation the file-existence check misses:
wholesale-empty payloads, a format/auth change that turns every table blank.
"""

from subsets_utils import load_raw_ndjson


def test_municipios_populated():
    """The geography reference must hold every Brazilian municipality."""
    rows = load_raw_ndjson("ibge-municipios")
    assert len(rows) > 5000, f"municipios reference has only {len(rows)} rows"


def test_most_aggregates_nonempty(spec_ids):
    """The vast majority of aggregate tables must carry observations. A handful
    of empties (a discontinued table the API now blanks) is tolerable; a broad
    emptiness means the data endpoint changed shape or the level pick broke."""
    agg_ids = [s for s in spec_ids if s != "ibge-municipios"]
    if not agg_ids:
        return
    empty = 0
    for sid in agg_ids:
        try:
            if len(load_raw_ndjson(sid)) == 0:
                empty += 1
        except Exception:
            empty += 1
    assert empty <= len(agg_ids) * 0.1, (
        f"{empty}/{len(agg_ids)} aggregate assets empty or unreadable"
    )


def test_aggregate_rows_well_formed(spec_ids):
    """Spot-check a populated aggregate carries the expected long-format keys."""
    for sid in spec_ids:
        if sid == "ibge-municipios":
            continue
        try:
            rows = load_raw_ndjson(sid)
        except Exception:
            continue
        if not rows:
            continue
        row = rows[0]
        for key in ("aggregado", "variavel_id", "periodo", "valor", "localidade_id"):
            assert key in row, f"{sid}: row missing {key!r}"
        return
