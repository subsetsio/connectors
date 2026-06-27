"""Post-DAG health invariants for NASA FIRMS raw batches.

Each download node writes firehose batches (`<spec_id>-<year>` and
`<spec_id>-recent`). We never load the full corpus here (VIIRS is ~200M rows) —
we check batch presence and validate the small, always-present recent batch.
"""

import re

from subsets_utils import list_raw_files, load_raw_parquet

_CORE = {"country", "latitude", "longitude", "acq_date", "acq_time", "satellite", "frp", "daynight"}


def test_families_have_year_and_recent_batches(spec_ids):
    """A fully-drained run writes many immutable year batches plus one recent
    batch per family. Too few year batches => the archive crawl was truncated."""
    for sid in spec_ids:
        batches = list_raw_files(f"{sid}-*.parquet")
        assert batches, f"{sid}: no raw batch files found"
        years = [b for b in batches if re.search(r"-(19|20)\d\d\.parquet$", b)]
        assert len(years) >= 5, f"{sid}: only {len(years)} archive-year batches (crawl truncated?)"
        assert any(b.endswith("-recent.parquet") for b in batches), f"{sid}: no recent batch"


def test_recent_batch_nonempty_and_typed(spec_ids):
    """The rolling recent batch must hold rows with the core columns. Empty or
    mis-shaped => the active-fire feed changed format or the fetch broke."""
    for sid in spec_ids:
        table = load_raw_parquet(f"{sid}-recent")
        assert table.num_rows > 0, f"{sid}-recent: 0 rows"
        cols = set(table.column_names)
        missing = _CORE - cols
        assert not missing, f"{sid}-recent: missing core columns {sorted(missing)}"
        # latitude must be a real coordinate, not a stringified blob
        lat = table.column("latitude").to_pylist()[:1000]
        assert any(v is not None and -90.0 <= v <= 90.0 for v in lat), f"{sid}-recent: no valid latitudes"
