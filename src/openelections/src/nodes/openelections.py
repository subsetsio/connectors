"""OpenElections connector.

OpenElections publishes standardized US election-results CSVs on GitHub, one
repository per state/territory: `openelections-data-XX`. Each repo holds many
CSV files laid out as `<year>/YYYYMMDD__XX__[party__][office__]electiontype__level.csv`.
Every file is the same kind of thing: rows of (jurisdiction, office, party,
candidate, votes). State, year, election type, office, party and reporting
level are dimension *values* — they become columns of one per-state table.

Fetch strategy: stateless full re-pull. For each state we download the repo's
master-branch tarball in a single request (codeload, no GitHub API rate-limit
budget, no recursive-tree truncation), stream every canonical CSV through a
normaliser, and overwrite one parquet raw asset per state. The whole corpus is
~2-3 GB and a handful of cents to re-pull, so there is no watermark/cursor —
revisions and late corrections are picked up for free. (`master` is the default
branch for every repo in the entity union; we still fall back to `main` for
forward-compat.)

Column sets vary across files and vintages (precinct files add vote-method
breakdowns; some states add election-district columns), so we project every row
onto the stable OpenElections core schema and drop the rest. `votes` is present
on every canonical file.
"""

import io
import re
import csv
import tarfile

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, get, raw_parquet_writer
from constants import ENTITY_IDS

# Normalised raw schema. All result columns are nullable strings except votes —
# files differ in which jurisdiction columns they carry, so we coerce per-row
# and leave absent columns null. The transform casts election_date to DATE.
SCHEMA = pa.schema([
    ("state", pa.string()),
    ("election_date", pa.string()),    # YYYY-MM-DD parsed from the filename
    ("election_type", pa.string()),    # general / primary / special / runoff / ...
    ("election_name", pa.string()),    # full filename middle, e.g. "democratic__primary"
    ("reporting_level", pa.string()),  # county / precinct / ward / state / district / ...
    ("county", pa.string()),
    ("precinct", pa.string()),
    ("office", pa.string()),
    ("district", pa.string()),
    ("party", pa.string()),
    ("candidate", pa.string()),
    ("votes", pa.int64()),
])

_BRANCHES = ("master", "main")
_DATE_PREFIX = re.compile(r"^\d{8}__")
# Election types that appear as a filename token; first match wins.
_KNOWN_TYPES = (
    "primary_runoff", "general_runoff", "primary", "general", "special",
    "runoff", "recall", "caucus", "convention", "municipal",
)
_FLUSH_ROWS = 100_000  # bound peak memory regardless of single-file size


def _get_tarball_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _download_tarball(state: str) -> bytes:
    """Fetch the repo tarball, trying the known default branches in order."""
    last_404 = None
    for branch in _BRANCHES:
        url = (
            f"https://github.com/openelections/openelections-data-{state}"
            f"/archive/refs/heads/{branch}.tar.gz"
        )
        try:
            return _get_tarball_bytes(url)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                last_404 = exc
                continue
            raise
    raise last_404


def _parse_filename(fname: str, state: str) -> dict | None:
    """Parse `YYYYMMDD__XX__...__level.csv` into result metadata, or None if the
    filename is not a canonical dated results file."""
    stem = fname[:-4]  # strip .csv
    parts = stem.split("__")
    if len(parts) < 3:
        return None
    date8 = parts[0]
    if len(date8) != 8 or not date8.isdigit():
        return None
    middle = parts[2:-1]  # tokens between state abbrev and reporting level
    election_name = "__".join(middle) if middle else None
    election_type = next((t for t in middle if t in _KNOWN_TYPES), election_name)
    return {
        "state": state,
        "election_date": f"{date8[0:4]}-{date8[4:6]}-{date8[6:8]}",
        "election_type": election_type,
        "election_name": election_name,
        "reporting_level": parts[-1] or None,
    }


def _to_int(value) -> int | None:
    if value is None:
        return None
    v = value.strip().replace(",", "")
    if v == "":
        return None
    try:
        return int(v)
    except ValueError:
        try:
            return int(float(v))
        except ValueError:
            return None


def _iter_rows(data: bytes, meta: dict):
    """Yield normalised rows from one CSV's bytes, projected onto the core
    schema. Skips files with no recognisable `votes` column."""
    reader = csv.DictReader(io.StringIO(data.decode("utf-8", errors="replace")))
    if not reader.fieldnames:
        return
    # Map normalised header -> original header (header casing/spacing varies).
    hmap = {h.strip().lower().replace(" ", "_"): h for h in reader.fieldnames if h}
    vote_col = next(
        (hmap[k] for k in ("votes", "total_votes", "vote_count", "total") if k in hmap),
        None,
    )
    if vote_col is None:
        return

    def cell(row, *names):
        for n in names:
            if n in hmap:
                val = row.get(hmap[n])
                if val is not None and val.strip() != "":
                    return val.strip()
        return None

    for row in reader:
        yield {
            **meta,
            "county": cell(row, "county"),
            "precinct": cell(row, "precinct"),
            "office": cell(row, "office"),
            "district": cell(row, "district"),
            "party": cell(row, "party"),
            "candidate": cell(row, "candidate"),
            "votes": _to_int(row.get(vote_col)),
        }


def fetch_one(node_id: str) -> None:
    asset = node_id                                  # the spec id IS the asset name
    state = node_id[len("openelections-"):]
    raw = _download_tarball(state)

    buf: list[dict] = []
    total = 0
    with raw_parquet_writer(asset, SCHEMA) as writer:
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
            for member in tar:
                if not member.isfile() or not member.name.endswith(".csv"):
                    continue
                fname = member.name.rsplit("/", 1)[-1]
                if not _DATE_PREFIX.match(fname):
                    continue                         # skip non-canonical CSVs
                meta = _parse_filename(fname, state)
                if meta is None:
                    continue
                handle = tar.extractfile(member)
                if handle is None:
                    continue
                for row in _iter_rows(handle.read(), meta):
                    buf.append(row)
                    if len(buf) >= _FLUSH_ROWS:
                        writer.write_table(pa.Table.from_pylist(buf, schema=SCHEMA))
                        total += len(buf)
                        buf = []
            if buf:
                writer.write_table(pa.Table.from_pylist(buf, schema=SCHEMA))
                total += len(buf)

    if total == 0:
        raise AssertionError(f"{asset}: parsed 0 result rows from the {state} tarball")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"openelections-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
