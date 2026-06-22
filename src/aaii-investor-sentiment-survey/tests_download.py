from subsets_utils import load_raw_parquet


def test_raw_nonempty_and_full_history(spec_ids):
    """The single .xls carries the entire 1987-present weekly history. A short
    table means the download silently got the Incapsula challenge page, a
    truncated snapshot, or a reshaped sheet."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 1500, f"{sid}: only {len(table)} rows; expected full weekly history (>=1500)"


def test_sentiment_columns_present(spec_ids):
    """Core sentiment columns must survive parsing; a missing one means the
    sheet layout drifted."""
    expected = {"date", "bullish", "neutral", "bearish", "total"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = expected - cols
        assert not missing, f"{sid}: missing columns {missing}; got {sorted(cols)}"


def test_shares_are_fractions(spec_ids):
    """Bullish/neutral/bearish are fractions in 0..1 (e.g. 0.36), not percent
    points (36). A max above ~1.5 means a units regression."""
    import pyarrow.compute as pc

    for sid in spec_ids:
        table = load_raw_parquet(sid)
        for col in ("bullish", "neutral", "bearish"):
            mx = pc.max(table[col]).as_py()
            assert mx is None or mx <= 1.5, f"{sid}: {col} max={mx}; expected fractions in 0..1"
