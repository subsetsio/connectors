import csv
import errno
import io
import json
import math
import re

import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from constants import ENTITY_IDS, SPEC_TO_CODE
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    TRANSIENT_EXC,
    get,
    post,
    raw_asset_exists,
    raw_writer,
)

BASE = "http://statistici.insse.ro:8077/tempo-ins"
PREFIX = "insse-"
LANGUAGE = "en"
MAX_CELLS = 25000

TIMEOUT = httpx.Timeout(180.0, connect=20.0, write=30.0, pool=30.0)
HEADERS = {
    "User-Agent": "Mozilla/5.0 subsets.io connector (+https://subsets.io)",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en;q=0.8",
    "Content-Type": "application/json",
    "Origin": "http://statistici.insse.ro:8077",
    "Referer": "http://statistici.insse.ro:8077/tempo-online/",
}
INSSE_TRANSIENT_EXC = TRANSIENT_EXC + (
    httpx.ReadError,
    httpx.RemoteProtocolError,
    ConnectionResetError,
    BrokenPipeError,
)


def _is_insse_transient(exc: BaseException) -> bool:
    if isinstance(exc, INSSE_TRANSIENT_EXC):
        return True
    if isinstance(exc, OSError):
        if exc.errno in {errno.ECONNRESET, errno.EPIPE, errno.ETIMEDOUT}:
            return True
        if "connection reset by peer" in str(exc).lower():
            return True
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        return status == 429 or 500 <= status < 600
    return False


def _insse_retry(fn):
    return retry(
        retry=retry_if_exception(_is_insse_transient),
        stop=stop_after_attempt(6),
        wait=wait_exponential(multiplier=1, min=2, max=90),
        reraise=True,
    )(fn)


def _matrix_code(node_id: str) -> str:
    try:
        return SPEC_TO_CODE[node_id]
    except KeyError as exc:
        raise ValueError(f"unexpected INSSE node id: {node_id}") from exc


def _slug(value: str, fallback: str, used: set[str]) -> str:
    text = re.sub(r"[^0-9A-Za-z]+", "_", str(value)).strip("_").lower()
    text = text or fallback
    if text and text[0].isdigit():
        text = f"dim_{text}"
    if text == "value":
        text = "value_dim"
    base = text
    n = 2
    while text in used:
        text = f"{base}_{n}"
        n += 1
    used.add(text)
    return text


@_insse_retry
def _get_metadata(code: str) -> dict:
    resp = get(
        f"{BASE}/matrix/{code}",
        params={"lang": LANGUAGE},
        headers=HEADERS,
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def _dimension_fields(metadata: dict) -> list[dict]:
    used = {"matrix_code", "source_row_number", "value_raw", "value"}
    fields = []
    for index, dim in enumerate(metadata.get("dimensionsMap") or [], start=1):
        label = str(dim.get("label") or f"dimension_{index}")
        name = _slug(label, f"dimension_{index}", used)
        fields.append(
            {
                "name": name,
                "source_label": label,
                "source_code": dim.get("dimCode"),
                "options": dim.get("options") or [],
            }
        )
    return fields


def _query_dimensions(fields: list[dict]) -> list[tuple[str, list[str]]]:
    dims = []
    for field in fields:
        values = [
            str(opt["nomItemId"])
            for opt in field["options"]
            if opt.get("nomItemId") is not None
        ]
        if values:
            dims.append((str(field["source_code"]), values))
    return dims


def _split_blocks(dims: list[tuple[str, list[str]]]):
    sizes = [len(values) for _, values in dims]
    total = math.prod(sizes) if sizes else 1
    if total <= MAX_CELLS:
        yield dims
        return

    largest = max(range(len(dims)), key=lambda i: sizes[i])
    rest = math.prod(size for i, size in enumerate(sizes) if i != largest) or 1
    chunk = max(1, MAX_CELLS // rest)
    code, values = dims[largest]
    for start in range(0, len(values), chunk):
        block = [(dim_code, list(dim_values)) for dim_code, dim_values in dims]
        block[largest] = (code, values[start:start + chunk])
        if math.prod(len(v) for _, v in block) > MAX_CELLS:
            yield from _split_blocks(block)
        else:
            yield block


def _pivot_payload(code: str, metadata: dict, block: list[tuple[str, list[str]]]) -> dict:
    details = metadata.get("details") or {}
    return {
        "language": LANGUAGE,
        "encQuery": ":".join(",".join(values) for _, values in block),
        "matCode": code,
        "matMaxDim": details.get("matMaxDim"),
        "matUMSpec": details.get("matUMSpec"),
        "matRegJ": details.get("matRegJ"),
    }


def _decode_text_response(resp: httpx.Response) -> str:
    content = resp.content
    for encoding in ("utf-8-sig", "cp1250", "latin-1"):
        try:
            return content.decode(encoding).lstrip("\ufeff")
        except UnicodeDecodeError:
            continue
    return content.decode("latin-1").lstrip("\ufeff")


@_insse_retry
def _post_pivot(code: str, metadata: dict, block: list[tuple[str, list[str]]]) -> str:
    resp = post(
        f"{BASE}/pivot",
        headers=HEADERS,
        json=_pivot_payload(code, metadata, block),
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    text = _decode_text_response(resp)
    lowered = text.lower()
    if "pragul" in lowered and "celule" in lowered:
        raise RuntimeError(f"{code}: TEMPO cell limit exceeded despite split")
    if "<html" in lowered:
        raise RuntimeError(f"{code}: TEMPO returned HTML instead of CSV")
    return text


def _number_or_none(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text in {":", "-", "..."}:
        return None
    text = text.replace("\u00a0", "").replace(" ", "")
    try:
        return float(text)
    except ValueError:
        return None


def _rows_from_csv(text: str, code: str, fields: list[dict], row_start: int):
    reader = csv.reader(io.StringIO(text))
    header = next(reader, None)
    if not header:
        return
    width = len(fields)
    for offset, parts in enumerate(reader, start=row_start):
        if not parts or all(not part.strip() for part in parts):
            continue
        if len(parts) < width + 1:
            raise RuntimeError(f"{code}: short CSV row at {offset}: {parts!r}")
        row = {
            "matrix_code": code,
            "source_row_number": offset,
        }
        for field, value in zip(fields, parts[:width]):
            row[field["name"]] = value.strip() or None
        raw_value = parts[width].strip() if len(parts) > width else None
        row["value_raw"] = raw_value or None
        row["value"] = _number_or_none(raw_value)
        yield row


def fetch_matrix(node_id: str) -> None:
    code = _matrix_code(node_id)
    metadata = _get_metadata(code)
    fields = _dimension_fields(metadata)
    dims = _query_dimensions(fields)
    if not dims:
        raise RuntimeError(f"{code}: matrix metadata exposed no queryable dimensions")

    row_number = 1
    metadata_row = {
        "matrix_code": code,
        "source_row_number": 0,
        "record_type": "metadata",
        "matrix_name": metadata.get("matrixName"),
        "periodicities": metadata.get("periodicitati"),
        "last_updated": metadata.get("ultimaActualizare"),
        "definition": metadata.get("definitie"),
        "methodology": metadata.get("metodologie"),
        "dimension_metadata": [
            {
                "name": field["name"],
                "source_label": field["source_label"],
                "source_code": field["source_code"],
            }
            for field in fields
        ],
        "value_raw": None,
        "value": None,
    }

    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as out:
        out.write(json.dumps(metadata_row, separators=(",", ":")) + "\n")
        for block in _split_blocks(dims):
            text = _post_pivot(code, metadata, block)
            for row in _rows_from_csv(text, code, fields, row_number):
                row["record_type"] = "observation"
                out.write(json.dumps(row, separators=(",", ":")) + "\n")
                row_number += 1

    if row_number == 1:
        raise RuntimeError(f"{code}: pivot returned no observation rows")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id.lower().replace('_', '-')}", fn=fetch_matrix)
    for entity_id in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "TEMPO matrices are updated on source-specific cadences with no "
            "per-matrix validator headers; re-fetch at least every 7 days "
            "(inferred from INSSE TEMPO online refresh behavior)."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "ndjson.gz", max_age_days=7),
    )
    for spec in DOWNLOAD_SPECS
]
