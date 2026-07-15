"""OECD connector — node module.

Source: OECD SDMX 2.1 REST API (chosen mechanism `sdmx_21`, base
https://sdmx.oecd.org/public/rest/, no auth). Each rank-accepted dataflow is
fetched in full from its stable per-dataset SDMX-CSV data endpoint:

    https://sdmx.oecd.org/public/rest/data/{AGENCY},{DATAFLOW}/all?format=csv

The version segment is omitted so the server returns the latest published
version of each dataflow (robust to version churn between collect and run).
The collect entity id is a signable "{agency}-{dataflow_id}" slug. The original
OECD agency and dataflow coordinates are generated into constants.py and used
for the actual SDMX request.

Scope: accept includes the full SDMX dataflow catalog collected by the harness.
Some dataflows are very large or are external references; the fetch path is
streaming and each dataflow remains isolated as its own raw asset.

SDMX-CSV is tidy (one observation per row). The usual header is
`DATAFLOW,<dim1>,...,<dimN>,TIME_PERIOD,OBS_VALUE,<attrs...>` where the
dimension/attribute columns differ per dataflow (each has its own DSD). A few
questionnaire/reference dataflows are not temporal and omit TIME_PERIOD. We
drop only the fixed `DATAFLOW` envelope column, rename TIME_PERIOD/OBS_VALUE to
time_period/value when present, coerce numeric values to float while preserving
qualitative values as strings, and pass every remaining column through verbatim
(lower-cased) — a uniform-per-dataset long row.

Fetch shape: stateless full re-pull (shape 1). The response is **streamed**
line-by-line straight into a gzipped NDJSON writer so even multi-million-row
tables never materialise the whole CSV in memory (the first attempt at this
connector OOM-killed the runner by loading a downscaled table via resp.text).
A discontinued/unmapped dataflow returns 404 → permanent per-entity skip (no raw
written; its transform finds no rows → that one node fails in isolation).

Rate limits: OECD enforces 429s without a documented ceiling; the retry
decorator's exponential backoff (429 is transient) finds the natural pace.
"""
import csv
import fcntl
import itertools
import json as _json
import os
import random
import time

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get_client,
    is_transient,
    raw_asset_exists,
    raw_writer,
)

BASE = "https://sdmx.oecd.org/public/rest/data"

# OECD SDMX enforces 429s with no documented ceiling and throttles shared
# (GitHub Actions) egress IPs aggressively. The first full run lost 38/314
# dataflows to 429s that outlasted the stock 6-attempt backoff. Two levers fix
# it: (1) a patient, Retry-After-honouring retry that rides out sustained
# throttling, and (2) a minimum spacing between request STARTS so a burst of
# small fast tables doesn't itself trip the limiter.
#
# Each DAG node runs in a fresh subprocess, so an in-memory timestamp resets
# between specs. Keep the request clock in /tmp behind an advisory lock so the
# whole runner shares one cadence.
_MIN_REQUEST_SPACING_S = 5.0
_THROTTLE_STATE = "/tmp/subsets-oecd-sdmx-last-request.txt"
_RETRY_CAP_S = 300.0


def _throttle() -> None:
    os.makedirs(os.path.dirname(_THROTTLE_STATE), exist_ok=True)
    with open(_THROTTLE_STATE, "a+") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.seek(0)
        raw = fh.read().strip()
        try:
            last = float(raw) if raw else 0.0
        except ValueError:
            last = 0.0
        wait = last + _MIN_REQUEST_SPACING_S - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        fh.seek(0)
        fh.truncate()
        fh.write(str(time.monotonic()))
        fh.flush()
        fcntl.flock(fh, fcntl.LOCK_UN)


def _oecd_wait(retry_state) -> float:
    """Backoff that honours a 429's Retry-After header when present, else falls
    back to exponential backoff. Capped so one wedged dataflow can't stall the
    whole run indefinitely."""
    exc = retry_state.outcome.exception() if retry_state.outcome else None
    if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 429:
        ra = exc.response.headers.get("Retry-After")
        if ra:
            try:
                return min(float(ra), _RETRY_CAP_S)
            except ValueError:
                pass  # HTTP-date form is rare here; fall through to exponential
    base = wait_exponential(min=10, max=_RETRY_CAP_S)(retry_state)
    return base + random.uniform(0, min(base, 30.0))


# 12 patient attempts (vs the stock 6): cumulative backoff can ride out long
# OECD throttle windows, while the cap prevents one wedged dataflow from
# consuming the whole GitHub job.
_oecd_retry = retry(
    retry=retry_if_exception(is_transient),
    stop=stop_after_attempt(12),
    wait=_oecd_wait,
    reraise=True,
)

# Only DATAFLOW is a pure envelope column we drop; TIME_PERIOD/OBS_VALUE are
# renamed; everything else (dimensions + attributes) is kept as a column.
_DROP_COLS = {"DATAFLOW", "TIME_PERIOD", "OBS_VALUE"}
_TEXT_VALUE_DATAFLOWS = {
    "DSD_QDD_GOV_DGI_2025@DF_GOV_DGI_2025",
    "DSD_QDD_GOV_OGD_2025@DF_GOV_OGD_2025",
    "DSD_QDD_GOV_PUBPRO_2024@DF_GOV_PUBPRO_2024",
}


def _to_value(raw: str):
    raw = (raw or "").strip()
    if raw == "" or raw == ":":
        return None
    try:
        return float(raw)
    except ValueError:
        return raw


# Sentinel: dataflow not available (permanent skip), distinct from "wrote 0".
_SKIP_404 = object()


@_oecd_retry
def _stream_to_ndjson(agency: str, dataflow: str, asset: str):
    url = f"{BASE}/{agency},{dataflow}/all?format=csv"
    _throttle()
    client = get_client()
    with client.stream("GET", url, timeout=(10.0, 600.0)) as resp:
        if resp.status_code == 404:
            return _SKIP_404  # permanent: not available for this data request
        if resp.status_code == 500:
            body = resp.read().decode("utf-8", errors="replace")
            if (
                "Incomplete mapping set" in body
                or "Object reference not set to an instance of an object" in body
            ):
                return _SKIP_404  # permanent source-side SDMX mapping failure
        resp.raise_for_status()  # 5xx/429 -> transient retry; other 4xx -> raise

        reader = csv.reader(resp.iter_lines())
        try:
            header = next(reader)
        except StopIteration:
            return 0  # empty body
        cols = [h.strip() for h in header]
        col = {c: i for i, c in enumerate(cols)}
        tp_i = col.get("TIME_PERIOD")
        val_i = col.get("OBS_VALUE")
        if val_i is None:
            raise AssertionError(
                f"{agency}:{dataflow}: SDMX-CSV missing OBS_VALUE; "
                f"header={cols}"
            )
        keep_idx = [(i, c.lower()) for i, c in enumerate(cols)
                    if c not in _DROP_COLS]

        n = 0
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
            for parts in reader:
                required = [val_i] if tp_i is None else [tp_i, val_i]
                if not parts or len(parts) <= max(required):
                    continue
                row = {name: parts[i] for i, name in keep_idx if i < len(parts)}
                if tp_i is not None:
                    row["time_period"] = parts[tp_i]
                row["value"] = (
                    (parts[val_i] or "").strip() or None
                    if dataflow in _TEXT_VALUE_DATAFLOWS
                    else _to_value(parts[val_i])
                )
                fh.write(_json.dumps(row, ensure_ascii=False))
                fh.write("\n")
                n += 1
        return n


def fetch_one(node_id: str) -> None:
    asset = node_id  # spec id IS the asset name
    coords = _SPEC_TO_ENTITY[node_id]
    agency = coords["agency_id"]
    dataflow = coords["dataflow_id"]

    result = _stream_to_ndjson(agency, dataflow, asset)
    if result is _SKIP_404:
        print(f"[oecd] {agency}:{dataflow}: 404 not available; skipping")
        return
    print(f"[oecd] {agency}:{dataflow}: wrote {result} observations")


from constants import ENTITY_COORDS, ENTITY_IDS

# spec id -> original collect entity id (recovers agency+dataflow, which are
# generated into the public, signable spec id).
_SPEC_TO_ENTITY = {
    f"oecd-{eid.lower().replace('_', '-')}": coords for eid, coords in ENTITY_COORDS.items()
}

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"oecd-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=s.id,
        description=(
            "OECD SDMX dataflows update on source-specific statistical "
            "release schedules; skip raw assets fetched in the last 30 days "
            "using the committed raw manifest (inferred from "
            "https://sdmx.oecd.org/public/rest/dataflow/all/all/latest)."
        ),
        check=lambda aid: (
            _SPEC_TO_ENTITY[aid].partition(":")[2] not in _TEXT_VALUE_DATAFLOWS
            and raw_asset_exists(aid, "ndjson.gz", max_age_days=30)
        ),
    )
    for s in DOWNLOAD_SPECS
]
