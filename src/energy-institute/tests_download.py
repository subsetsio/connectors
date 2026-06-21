from subsets_utils import load_raw_parquet


def test_panel_nonempty(spec_ids):
    """The panel raw must hold the full country-year panel. A truncated download
    or a Cloudflare 403 challenge page slipping through would show up as far
    fewer rows than the ~7.7k country-years the source carries."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 5000, f"{sid}: only {len(table)} rows (expected ~7.7k country-years)"


def test_panel_is_wide(spec_ids):
    """The raw must keep the wide source layout - the identifier columns plus
    the ~90 measure columns. A format switch (e.g. the source moving to a long
    export) would collapse the column count and break the transform."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert {"Country", "Year", "ISO3166_alpha3"} <= cols, (
            f"{sid}: missing identifier columns; got {sorted(cols)[:8]}"
        )
        assert len(cols) > 50, f"{sid}: only {len(cols)} columns (expected ~100 wide panel)"
