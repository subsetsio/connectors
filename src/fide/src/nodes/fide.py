"""FIDE (International Chess Federation) official rating list connector.

One subset: `players` — the entire FIDE rated-player corpus, one row per player,
sourced from the combined bulk XML download (standard + rapid + blitz ratings in
a single wide record per player). Stateless full re-pull: FIDE republishes the
whole list monthly (~mid-month) at a stable URL, so each refresh fetches the
combined zip and overwrites. No incremental filter exists (and at ~48MB zipped /
~800MB XML the full pull is cheap), so full re-pull is the correct shape.

The XML is large uncompressed, so the fetch streams it with iterparse and writes
parquet in row-group batches rather than materializing the whole corpus in RAM.
"""

import io
import zipfile
import xml.etree.ElementTree as ET

import pyarrow as pa
from subsets_utils import NodeSpec, get, raw_parquet_writer

# Combined list: one <player> per rated player with standard/rapid/blitz fields.
COMBINED_URL = "https://ratings.fide.com/download/players_list_xml.zip"

BATCH_SIZE = 100_000

# Explicit contract for the wide combined record. Integer rating/games/k and
# birth-year fields are nullable: FIDE emits an empty element for players with no
# rating in a given time control, which we carry as NULL (distinct from a real 0).
SCHEMA = pa.schema([
    ("fideid", pa.int64()),
    ("name", pa.string()),
    ("country", pa.string()),
    ("sex", pa.string()),
    ("title", pa.string()),
    ("w_title", pa.string()),
    ("o_title", pa.string()),
    ("foa_title", pa.string()),
    ("rating", pa.int32()),
    ("games", pa.int32()),
    ("k", pa.int32()),
    ("rapid_rating", pa.int32()),
    ("rapid_games", pa.int32()),
    ("rapid_k", pa.int32()),
    ("blitz_rating", pa.int32()),
    ("blitz_games", pa.int32()),
    ("blitz_k", pa.int32()),
    ("birthday", pa.int32()),
    ("flag", pa.string()),
])

_STR_FIELDS = ("name", "country", "sex", "title", "w_title", "o_title", "foa_title", "flag")
_INT_FIELDS = ("rating", "games", "k", "rapid_rating", "rapid_games", "rapid_k",
               "blitz_rating", "blitz_games", "blitz_k", "birthday")


def _download_combined() -> bytes:
    resp = get(COMBINED_URL, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _txt(elem, tag):
    child = elem.find(tag)
    if child is None or child.text is None:
        return None
    s = child.text.strip()
    return s if s else None


def _to_int(s):
    if s is None:
        return None
    try:
        return int(s)
    except ValueError:
        return None


def fetch_players(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    raw = _download_combined()
    zf = zipfile.ZipFile(io.BytesIO(raw))
    inner = zf.namelist()[0]  # single XML file per the bulk-download layout

    cols = {f.name: [] for f in SCHEMA}
    n_in_batch = 0

    with raw_parquet_writer(asset, SCHEMA) as writer:
        def flush():
            nonlocal n_in_batch
            if n_in_batch == 0:
                return
            batch = pa.RecordBatch.from_arrays(
                [pa.array(cols[f.name], type=f.type) for f in SCHEMA],
                schema=SCHEMA,
            )
            writer.write_batch(batch)
            for v in cols.values():
                v.clear()
            n_in_batch = 0

        with zf.open(inner) as stream:
            root = None
            for event, elem in ET.iterparse(stream, events=("start", "end")):
                if event == "start" and root is None:
                    root = elem
                    continue
                if event != "end" or elem.tag != "player":
                    continue

                cols["fideid"].append(_to_int(_txt(elem, "fideid")))
                for f in _STR_FIELDS:
                    cols[f].append(_txt(elem, f))
                for f in _INT_FIELDS:
                    cols[f].append(_to_int(_txt(elem, f)))
                n_in_batch += 1

                elem.clear()
                if root is not None:
                    root.clear()  # drop accumulated processed siblings — bounds memory

                if n_in_batch >= BATCH_SIZE:
                    flush()

        flush()


DOWNLOAD_SPECS = [
    NodeSpec(id="fide-players", fn=fetch_players, kind="download"),
]
