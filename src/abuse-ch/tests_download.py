"""Post-DAG health invariants for the abuse.ch raw feeds.

Each feed is a full public snapshot; the failure modes we guard against are
silent degradation: an endpoint switching format/auth and returning an empty
or banner-only payload, or a feed shrinking far below its known floor. The
MalwareBazaar dump holds millions of rows, so we check its raw file's presence
rather than materializing it in memory like the smaller feeds.
"""

from subsets_utils import list_raw_files, load_raw_ndjson

# Conservative floors — well below observed live counts, tight enough that a
# banner-only / truncated payload (a handful of rows) trips the test.
_MIN_ROWS = {
    "abuse-ch-urlhaus-urls": 1000,
    "abuse-ch-urlhaus-payloads": 500,
    "abuse-ch-threatfox-iocs": 1000,
    "abuse-ch-feodotracker-c2": 1,
    "abuse-ch-sslbl-certificates": 50,
}
_BIG = "abuse-ch-malwarebazaar-samples"


def test_raw_assets_present(spec_ids):
    """Every download spec must have written at least one raw file."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*")
        assert files, f"{sid}: no raw file written"


def test_small_feeds_meet_floor(spec_ids):
    """Small/medium feeds load fully and must clear their known row floor with
    a usable first record (non-empty dict)."""
    for sid in spec_ids:
        if sid == _BIG or sid not in _MIN_ROWS:
            continue
        rows = load_raw_ndjson(sid)
        floor = _MIN_ROWS[sid]
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows < floor {floor}"
        assert isinstance(rows[0], dict) and rows[0], f"{sid}: first record empty"


def test_malwarebazaar_dump_nonempty(spec_ids):
    """The large MalwareBazaar dump: confirm a raw file exists without loading
    millions of rows into memory."""
    if _BIG not in spec_ids:
        return
    files = list_raw_files(f"{_BIG}.*")
    assert files, f"{_BIG}: no raw file written"
