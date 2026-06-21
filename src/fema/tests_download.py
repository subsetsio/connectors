"""Health-invariant tests for the FEMA connector raw layer.

Run post-DAG, in-connector, through the same subsets_utils loaders the download
nodes used to write. Catch silent degradation that file-existence alone misses:
empty / truncated payloads, or a parquet that didn't actually parse.
"""
from subsets_utils import load_raw_file
import pyarrow.parquet as pa_pq
import io


def test_all_raw_assets_parse_and_nonempty(spec_ids):
    """Each dataset's raw asset must be a readable parquet with >0 rows. An
    empty or unparseable file means the OpenFEMA full-file endpoint returned an
    error page or a truncated stream instead of the dataset."""
    empty, broken = [], []
    for sid in spec_ids:
        data = load_raw_file(sid, extension="parquet", binary=True)
        if not data:
            empty.append(sid)
            continue
        try:
            md = pa_pq.read_metadata(io.BytesIO(data))
        except Exception as e:  # noqa: BLE001 - report which asset, then fail
            broken.append(f"{sid}: {type(e).__name__}")
            continue
        if md.num_rows == 0:
            empty.append(sid)
    assert not broken, f"unparseable parquet: {broken}"
    assert not empty, f"empty parquet (0 rows / 0 bytes): {empty}"


def test_flagship_has_expected_scale(spec_ids):
    """Disaster Declarations Summaries is the flagship table and has tens of
    thousands of rows (69,936 at last catalog read). If it comes back tiny, the
    full-file download silently truncated."""
    sid = "fema-disasterdeclarationssummaries"
    if sid not in spec_ids:
        return
    data = load_raw_file(sid, extension="parquet", binary=True)
    md = pa_pq.read_metadata(io.BytesIO(data))
    assert md.num_rows >= 50000, (
        f"{sid}: only {md.num_rows} rows; expected >=50000 (truncated download?)"
    )
