"""Eurostat connector — node module (download stage).

Source: Eurostat SDMX 2.1 dissemination API (chosen mechanism `sdmx_21`,
agency ESTAT, no auth). Each rank-accepted dataflow is fetched in full from its
stable per-dataset SDMX-CSV endpoint:

    https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{CODE}/?format=SDMX-CSV

SDMX-CSV is tidy (one observation per row). The header is
`DATAFLOW,LAST UPDATE,<dim1>,...,<dimN>,TIME_PERIOD,OBS_VALUE,OBS_FLAG[,CONF_STATUS]`
where the dimension columns differ per dataflow (each has its own DSD). We strip
the fixed envelope columns, lower-case the remaining dimension columns, and emit
a uniform-per-dataset long row: {<dims...>, time_period, value, flag}. Raw is
NDJSON gzip (heterogeneous dimension sets across datasets; stable within a
dataset).

Two facts about this endpoint drive the fetch design:

1. **The body is often gzip — with NO `Content-Encoding` header.** Eurostat
   compresses large responses and serves them as `Content-Type:
   application/vnd.sdmx.data+csv` with the gzip bytes in the body, so httpx does
   NOT transparently decode them. We sniff the two magic bytes (`1f 8b`) on the
   first chunk and, when present, run the byte stream through an incremental
   gzip decompressor. Plain responses pass through untouched.

2. **Some tables are huge.** A single detailed dataflow (e.g. AVIA_GOEXCC)
   decompresses to ~1 GB of CSV. We therefore STREAM: the HTTP body is consumed
   chunk-by-chunk, decompressed on the fly, split into lines, CSV-parsed, and
   written to NDJSON row-by-row via `raw_writer`. Nothing materialises the whole
   table in memory — RSS stays flat regardless of dataset size.

Fetch shape: stateless full re-pull (shape 1). The whole table is re-fetched and
overwritten every run — Eurostat has no per-observation incremental filter, and
re-pulling picks up revisions for free. Cross-run cost is bounded by
`MAINTAIN_SPECS`: a dataflow whose raw already exists and is younger than the
refresh window is skipped pre-spawn, so the backfill is resumable across runs
and scheduled refreshes only re-pull what has aged out.

Per-entity robustness: this is a 5427-node DAG, and one raising node fails the
whole run. So a single dataflow that is missing (404 / permanent 4xx), empty, or
malformed is logged and skipped cleanly — never raised — leaving its raw asset
simply absent (its transform then fails in isolation downstream). Only genuine
transient errors (429/5xx/network) are retried by `transient_retry`.
"""
import csv
import json as _json
import zlib

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_asset_exists,
    raw_writer,
    transient_retry,
)

BASE = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"

# Refresh window: a fetched dataflow is considered fresh (skipped) for this many
# days. Larger than the harness dispatch cadence (7d) so scheduled refreshes
# mostly skip and only aged-out tables re-pull; also makes the initial backfill
# resumable — assets pulled by an earlier (possibly timed-out) run stay fresh
# while later runs fetch the remainder. Eurostat has no single published cadence
# (per-dataset "Last data change" in the inventory); this is an inferred window.
MAINTAIN_MAX_AGE_DAYS = 14

# Fixed SDMX-CSV envelope columns — everything else in the header is a dimension.
_META_COLS = {
    "DATAFLOW",
    "LAST UPDATE",
    "LAST_UPDATE",
    "TIME_PERIOD",
    "OBS_VALUE",
    "OBS_FLAG",
    "CONF_STATUS",
    "OBS_STATUS",
}


def _byte_chunks(resp):
    """Yield decoded body bytes from a streaming response, transparently
    gunzipping when the body is a raw gzip stream (Eurostat sends gzip bytes
    with no Content-Encoding header for large tables)."""
    it = resp.iter_bytes(chunk_size=1 << 16)
    first = next(it, b"")

    def _raw():
        yield first
        yield from it

    if first[:2] != b"\x1f\x8b":
        yield from _raw()
        return

    # zlib.MAX_WBITS | 16 selects gzip framing.
    decomp = zlib.decompressobj(zlib.MAX_WBITS | 16)
    for chunk in _raw():
        out = decomp.decompress(chunk)
        if out:
            yield out
    tail = decomp.flush()
    if tail:
        yield tail


def _text_lines(byte_iter):
    """Split a stream of byte chunks into decoded text lines (LF-delimited)."""
    buf = b""
    for chunk in byte_iter:
        buf += chunk
        while True:
            i = buf.find(b"\n")
            if i < 0:
                break
            yield buf[:i].decode("utf-8", "replace")
            buf = buf[i + 1:]
    if buf:
        yield buf.decode("utf-8", "replace")


def _to_value(raw: str):
    raw = (raw or "").strip()
    if raw == "" or raw == ":":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


@transient_retry()
def _stream_to_ndjson(code: str, asset: str) -> str:
    """Stream one dataflow's SDMX-CSV into NDJSON. Returns a status string.

    Wrapped in transient_retry: 429/5xx/network errors retry the whole
    download (overwriting any partial raw). Permanent conditions return a
    sentinel instead of raising, so one bad dataflow can't fail the DAG.
    """
    url = f"{BASE}/{code}/?format=SDMX-CSV"
    with get_client().stream("GET", url, timeout=(10.0, 600.0)) as resp:
        status = resp.status_code
        # Permanent per-entity conditions: discontinued / not disseminated.
        if status == 404 or (400 <= status < 500 and status != 429):
            resp.read()  # drain so the connection can be reused
            return f"http_{status}"
        resp.raise_for_status()  # 5xx/429 -> raise -> transient_retry handles it

        reader = csv.reader(_text_lines(_byte_chunks(resp)))
        try:
            header = next(reader)
        except StopIteration:
            return "empty"

        dim_idx = [
            (i, h.strip().lower())
            for i, h in enumerate(header)
            if h.strip() not in _META_COLS
        ]
        col = {h.strip(): i for i, h in enumerate(header)}
        tp_i = col.get("TIME_PERIOD")
        val_i = col.get("OBS_VALUE")
        flag_i = col.get("OBS_FLAG")
        if tp_i is None or val_i is None:
            # Not a valid SDMX-CSV table (error page, format change). Skip
            # rather than raise so the rest of the DAG is unaffected; the
            # health tests catch a systematic break across many datasets.
            return f"no_cols:{header[:4]}"

        n = 0
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
            for parts in reader:
                if not parts or len(parts) <= max(tp_i, val_i):
                    continue
                row = {name: parts[i] for i, name in dim_idx if i < len(parts)}
                row["time_period"] = parts[tp_i]
                row["value"] = _to_value(parts[val_i])
                row["flag"] = (
                    parts[flag_i].strip()
                    if (flag_i is not None and flag_i < len(parts))
                    else ""
                )
                fh.write(_json.dumps(row, ensure_ascii=False))
                fh.write("\n")
                n += 1
        return f"rows:{n}"


def fetch_one(node_id: str) -> None:
    asset = node_id  # spec id IS the asset name
    code = node_id[len("eurostat-"):].replace("-", "_").upper()
    try:
        outcome = _stream_to_ndjson(code, asset)
    except Exception as exc:  # noqa: BLE001 — logged; must not abort the 5427-node DAG
        # Exhausted transient retries or an unexpected error on ONE dataflow.
        # Log with the code + exception class and skip; leaving raw absent is
        # a per-entity failure, not a run-wide one.
        print(f"[eurostat] {code}: skipped after error {type(exc).__name__}: {exc}")
        return
    print(f"[eurostat] {code}: {outcome}")


from constants import ENTITY_IDS

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"eurostat-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


def _is_fresh(asset_id: str) -> bool:
    """Skip policy: raw already fetched and younger than the refresh window."""
    return raw_asset_exists(asset_id, "ndjson.gz", max_age_days=MAINTAIN_MAX_AGE_DAYS)


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=s.id,
        description=(
            f"Full re-pull when raw is older than {MAINTAIN_MAX_AGE_DAYS}d "
            "(inferred window — Eurostat publishes no single cadence; per-dataset "
            "Last data change in the dissemination inventory). Resumable backfill."
        ),
        check=_is_fresh,
    )
    for s in DOWNLOAD_SPECS
]

# One thin SQL transform per dataset: pass the tidy long rows through, keeping
# only real observations. Each dataflow publishes its own dimension columns
# (distinct DSD), so a generic SELECT * is the correct uniform shape. (Authored
# here as a starting point; the transform stage refines contracts from profiled
# raw.)
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        temporal="time_period",
        sql=f'SELECT * FROM "{s.id}" WHERE value IS NOT NULL',
    )
    for s in DOWNLOAD_SPECS
]
