"""Health-invariant tests for un-population-division raw assets.

Run post-DAG, in-connector, through subsets_utils loaders.

Memory note: the WPP life-table files are huge (the complete single-age life
table is ~1.9 GB of zstd parquet, several times that decompressed in Arrow).
`load_raw_parquet` pulls the *entire* file into an Arrow table, so checking all
nine assets that way stacks the whole corpus in RAM and OOMs the 16 GB cloud
runner during the post-DAG test phase. Every check here instead reads only what
it needs: file/row-group metadata for counts and schema (zero data pages), and a
single streamed column (`Time` / `Variant`) for the value checks — peak memory
stays at one record batch regardless of file size. `raw_parquet_localpath`
streams the remote parquet to a tempfile so pyarrow reads it by path.
"""

import pyarrow.compute as pc
import pyarrow.parquet as pq

from subsets_utils import raw_parquet_localpath

_CORE_COLUMNS = ("LocID", "Location", "Variant", "Time")


def _raw_ids(spec_ids):
    """Raw parquets exist only for the download specs; the DAG also passes the
    `-transform` spec ids (published subsets, no raw asset) — filter them out."""
    return [s for s in spec_ids if not s.endswith("-transform")]


def test_all_raw_assets_nonempty(spec_ids):
    """Every subset's raw parquet must hold rows. An empty payload usually means
    the source renamed/moved a file or the gzip stream was truncated. Row count
    comes from the file footer — no data pages are read."""
    for sid in _raw_ids(spec_ids):
        with raw_parquet_localpath(sid) as path:
            n_rows = pq.ParquetFile(path).metadata.num_rows
        assert n_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_core_identity_columns_present(spec_ids):
    """Every WPP CSV carries these keys; their absence means the column layout
    drifted and the pinned schema silently mismatched. Schema comes from the
    footer — no data pages are read."""
    for sid in _raw_ids(spec_ids):
        with raw_parquet_localpath(sid) as path:
            names = set(pq.ParquetFile(path).schema_arrow.names)
        for col in _CORE_COLUMNS:
            assert col in names, f"{sid}: missing core column {col!r} (have {sorted(names)[:8]}...)"


def test_full_year_span(spec_ids):
    """Standard projections span 1950..2100. If a download grabbed only the
    estimates slice (or only projections), the Time range collapses - catch it.
    Prefers per-row-group min/max statistics (no data read); falls back to a
    streamed scan of just the Time column if a file lacks statistics."""
    for sid in _raw_ids(spec_ids):
        with raw_parquet_localpath(sid) as path:
            tmin, tmax = _time_span(pq.ParquetFile(path))
        assert tmin is not None and tmin <= 1950, f"{sid}: min year {tmin}, expected <= 1950"
        assert tmax is not None and tmax >= 2100, f"{sid}: max year {tmax}, expected >= 2100"


def test_medium_variant_present(spec_ids):
    """Every raw asset must contain the Medium (standard) projection. Most files
    are Medium-only by filename; the fertility files faithfully carry all 18
    projection variants (the transform filters to Medium). Either way, a missing
    Medium variant means the wrong file was fetched. Streams just the Variant
    column one batch at a time and stops as soon as 'Medium' is seen."""
    for sid in _raw_ids(spec_ids):
        found = False
        with raw_parquet_localpath(sid) as path:
            for batch in pq.ParquetFile(path).iter_batches(columns=["Variant"]):
                if "Medium" in pc.unique(batch.column("Variant")).to_pylist():
                    found = True
                    break
        assert found, f"{sid}: Medium variant absent"


def _time_span(pf):
    """(min, max) of the Time column. Uses row-group statistics when present
    (no data pages read), else streams the single column in batches."""
    md = pf.metadata
    names = pf.schema_arrow.names
    if "Time" not in names:
        return None, None
    col_idx = names.index("Time")

    tmin = tmax = None
    have_stats = md.num_row_groups > 0
    for rg in range(md.num_row_groups):
        st = md.row_group(rg).column(col_idx).statistics
        if st is None or not st.has_min_max:
            have_stats = False
            break
        tmin = st.min if tmin is None else min(tmin, st.min)
        tmax = st.max if tmax is None else max(tmax, st.max)
    if have_stats:
        return tmin, tmax

    tmin = tmax = None
    for batch in pf.iter_batches(columns=["Time"]):
        col = batch.column("Time")
        bmin = pc.min(col).as_py()
        bmax = pc.max(col).as_py()
        if bmin is not None:
            tmin = bmin if tmin is None else min(tmin, bmin)
        if bmax is not None:
            tmax = bmax if tmax is None else max(tmax, bmax)
    return tmin, tmax
