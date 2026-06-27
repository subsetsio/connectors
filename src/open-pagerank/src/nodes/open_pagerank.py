"""Open PageRank (DomCop) — Top 10 Million Domains.

Single-dataset connector. DomCop publishes one free, no-auth bulk artefact: a
zipped CSV ranking the top ~10,000,000 internet domains by Open PageRank (a
0-10 PageRank-style domain-authority metric derived from the Common Crawl +
Common Search link graphs). The whole corpus arrives in one stable URL, so the
correct shape is a stateless full re-pull each refresh: download the ~118 MB
zip, stream-parse its single CSV member, and write one typed parquet raw asset.
No incremental filter exists (the file is a full snapshot), so there is no
watermark/cursor — re-fetching the whole file is the only option and is cheap.

The getPageRank REST API is intentionally unused: it is an auth-gated per-domain
lookup with no catalog of its own; the bulk file already delivers the full
ranked corpus.
"""

import csv
import io
import zipfile

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

BULK_URL = "https://www.domcop.com/files/top/top10milliondomains.csv.zip"
# CSV header is: "Rank","Domain","Open Page Rank" (all values quoted strings).
BATCH_ROWS = 250_000
# Safety floor: the corpus is ~10M rows. A successful download well below this
# means the transfer truncated or the source format changed — raise, never
# publish a partial snapshot.
MIN_EXPECTED_ROWS = 1_000_000

RAW_SCHEMA = pa.schema(
    [
        ("rank", pa.int64()),
        ("domain", pa.string()),
        ("open_page_rank", pa.float64()),
    ]
)


@transient_retry()
def _download_zip(url: str) -> bytes:
    # Generous read timeout: the server throttles this static file, so the full
    # ~118 MB transfer can take many minutes. The read timeout is per-chunk, so
    # a slow-but-steady trickle won't trip it.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def _flush(writer, ranks, domains, oprs) -> None:
    writer.write_table(
        pa.table(
            {"rank": ranks, "domain": domains, "open_page_rank": oprs},
            schema=RAW_SCHEMA,
        )
    )


def fetch_top10m(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    content = _download_zip(BULK_URL)

    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        names = zf.namelist()
        member = next((n for n in names if n.lower().endswith(".csv")), names[0])

        total = 0
        ranks: list[int] = []
        domains: list[str] = []
        oprs: list[float] = []

        with raw_parquet_writer(asset, RAW_SCHEMA) as writer:
            with zf.open(member, "r") as raw:
                reader = csv.reader(io.TextIOWrapper(raw, encoding="utf-8"))
                header = next(reader, None)
                if not header or len(header) < 3:
                    raise AssertionError(f"unexpected CSV header: {header!r}")
                for row in reader:
                    if len(row) < 3 or not row[1]:
                        continue
                    ranks.append(int(row[0]))
                    domains.append(row[1])
                    oprs.append(float(row[2]))
                    if len(ranks) >= BATCH_ROWS:
                        _flush(writer, ranks, domains, oprs)
                        total += len(ranks)
                        ranks, domains, oprs = [], [], []
                if ranks:
                    _flush(writer, ranks, domains, oprs)
                    total += len(ranks)

        if total < MIN_EXPECTED_ROWS:
            raise AssertionError(
                f"only {total} rows parsed from {member}; expected "
                f">= {MIN_EXPECTED_ROWS} — transfer truncated or format changed"
            )


DOWNLOAD_SPECS = [
    NodeSpec(
        id="open-pagerank-top-10-million-domains",
        fn=fetch_top10m,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="open-pagerank-top-10-million-domains-transform",
        deps=["open-pagerank-top-10-million-domains"],
        sql='''
            SELECT
                CAST(rank AS BIGINT)            AS rank,
                domain,
                CAST(open_page_rank AS DOUBLE)  AS open_page_rank
            FROM "open-pagerank-top-10-million-domains"
            WHERE rank IS NOT NULL
              AND domain IS NOT NULL
              AND length(domain) > 0
        ''',
    ),
]
