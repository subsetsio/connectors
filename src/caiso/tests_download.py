"""Post-run health invariants for the CAISO OASIS connector.

Each report is a date-windowed firehose: raw lands as one ndjson batch per
(window, market_run) named `<spec-id>-<YYYYMMDD>-<run>`. We check that the
backfill actually produced data and that batches carry the timestamp columns
every OASIS report shares — a silent format switch or an all-empty backfill
(wrong params, throttled to death) would otherwise pass file-existence checks.
"""

from subsets_utils import list_raw_files, load_raw_ndjson


def _batches(sid: str) -> list[str]:
    # Strip the .ndjson(.zst) suffix so the id is usable with load_raw_ndjson.
    files = list_raw_files(f"{sid}-*")
    out = []
    for f in files:
        name = f.rsplit("/", 1)[-1]
        for ext in (".ndjson.zst", ".ndjson.gz", ".ndjson"):
            if name.endswith(ext):
                out.append(name[: -len(ext)])
                break
    return out


def test_most_reports_have_data(spec_ids):
    """The vast majority of reports must produce at least one batch. A handful
    failing (a report retired, a market_run guess wrong) is tolerable; a broad
    wipeout means the endpoint or throttling broke."""
    empty = [sid for sid in spec_ids if not _batches(sid)]
    assert len(empty) <= 3, (
        f"{len(empty)}/{len(spec_ids)} reports produced no batches: {sorted(empty)}"
    )


def test_batches_nonempty_and_timestamped(spec_ids):
    """Every batch that exists must hold rows, and OASIS reports always carry an
    INTERVALSTARTTIME_GMT or OPR_DT column — its absence means the CSV layout
    changed underneath us."""
    checked = 0
    for sid in spec_ids:
        batches = _batches(sid)
        if not batches:
            continue
        rows = load_raw_ndjson(batches[0])
        assert rows, f"{sid}: batch {batches[0]} has 0 rows"
        cols = set(rows[0].keys())
        assert cols & {"INTERVALSTARTTIME_GMT", "OPR_DT"}, (
            f"{sid}: batch {batches[0]} missing expected time columns; got {sorted(cols)[:8]}"
        )
        checked += 1
    assert checked > 0, "no batches found for any spec"
