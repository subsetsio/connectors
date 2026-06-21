"""Health invariants for the Realtor.com raw downloads.

Each raw asset is a gzipped CSV history file streamed from S3. These checks
catch silent degradation that file-existence alone misses: a truncated /
empty download, the endpoint switching format, or the header changing.

Reads only the first lines via the streaming reader — the Zip-level files are
hundreds of MB uncompressed, so we never load a whole asset into memory.
"""

from subsets_utils import raw_reader


def _head_lines(sid: str, n: int = 200) -> list[str]:
    lines = []
    with raw_reader(sid, "csv.gz", mode="rt", compression="gzip") as f:
        for line in f:
            lines.append(line.rstrip("\n"))
            if len(lines) >= n:
                break
    return lines


def test_all_raw_assets_have_header_and_rows(spec_ids):
    """Every spec's raw CSV must carry the key column and real data rows. A
    header-only or empty file means the S3 object moved or the download
    truncated."""
    for sid in spec_ids:
        lines = _head_lines(sid)
        assert len(lines) >= 100, f"{sid}: only {len(lines)} lines read — truncated/empty?"
        header = lines[0].lower()
        assert "month_date_yyyymm" in header, (
            f"{sid}: missing month_date_yyyymm column — format changed? header={header[:120]}"
        )


def test_core_and_hotness_columns_present(spec_ids):
    """Core files must expose the inventory metrics; Hotness files the hotness
    scores. Guards against a Core/Hotness URL mix-up or schema drift."""
    for sid in spec_ids:
        header = _head_lines(sid, n=1)[0].lower()
        if "hotness" in sid:
            assert "hotness_score" in header, f"{sid}: hotness file missing hotness_score"
        else:
            assert "median_listing_price" in header, f"{sid}: core file missing median_listing_price"
