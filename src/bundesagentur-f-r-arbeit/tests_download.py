"""Health-invariant tests for the Bundesagentur fuer Arbeit connector.

These run post-DAG inside the connector and load raw through subsets_utils,
catching silent degradation (empty payloads, all-null parses, broken period
parsing) that file existence alone misses.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every table returns its full history in one request; an empty raw asset
    means the endpoint switched shape or the table code drifted."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        assert len(t) > 0, f"{sid}: raw parquet has 0 rows"


def test_periods_parsed(spec_ids):
    """Periods are German 'Monat Jahr' labels; if parsing breaks, every `date`
    goes null and the transform would publish nothing. Require the bulk to
    parse."""
    for sid in spec_ids:
        t = load_raw_parquet(sid).to_pydict()
        dates = t["date"]
        parsed = sum(1 for d in dates if d is not None)
        assert parsed >= 0.9 * len(dates), (
            f"{sid}: only {parsed}/{len(dates)} periods parsed to a date"
        )


def test_values_present(spec_ids):
    """A table whose values are entirely null is a broken parse, not real data."""
    for sid in spec_ids:
        t = load_raw_parquet(sid).to_pydict()
        vals = t["value"]
        nonnull = sum(1 for v in vals if v is not None)
        assert nonnull > 0, f"{sid}: every value is null"


def test_metric_present(spec_ids):
    """metricName drives the series dimension; all-null means the response key
    changed."""
    for sid in spec_ids:
        t = load_raw_parquet(sid).to_pydict()
        assert any(m for m in t["metric"]), f"{sid}: no metric names"
