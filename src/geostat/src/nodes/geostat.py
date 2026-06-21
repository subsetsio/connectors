"""Geostat (National Statistics Office of Georgia) — PxWeb API v1 connector.

One download node per .px statistical table (the rank-accepted entity union),
fetched stateless/full each run: every table is small enough to re-pull in full,
so there is no watermark or cursor. For each table we read its variable metadata
(GET) and then POST a json-stat query selecting every value of every dimension,
splitting into multiple POSTs when the cell count exceeds the server's
maxValues=10000 cap. The json-stat cube is flattened to long format — one row
per cell, with a column per dimension (carrying the dimension's value *label*)
plus a numeric `value` — and saved as NDJSON because the dimension set differs
from table to table (heterogeneous schemas across assets).

TLS note: the server presents an incomplete certificate chain (it omits the
Sectigo intermediate). We repair the chain by supplying that public intermediate
and verifying normally against certifi's roots — verification stays ON, we do not
disable it.
"""

import math
import re
import ssl

import certifi
import httpx
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    post,
    save_raw_ndjson,
    transient_retry,
)
from subsets_utils import http_client as _http_client
from constants import ENTITY_IDS, ENTITY_PATHS

BASE = "https://pc-axis.geostat.ge/PXWeb/api/v1/en/Database/"
MAX_CELLS = 10000  # server config: maxValues per query

# The Sectigo "Public Server Authentication CA DV R36" intermediate the server
# forgets to send; it chains to "Sectigo Public Server Authentication Root R46",
# which is in certifi. Public CA cert — not a secret. Long-lived (valid to 2036).
_SECTIGO_INTERMEDIATE_PEM = """-----BEGIN CERTIFICATE-----
MIIGTDCCBDSgAwIBAgIQOXpmzCdWNi4NqofKbqvjsTANBgkqhkiG9w0BAQwFADBf
MQswCQYDVQQGEwJHQjEYMBYGA1UEChMPU2VjdGlnbyBMaW1pdGVkMTYwNAYDVQQD
Ey1TZWN0aWdvIFB1YmxpYyBTZXJ2ZXIgQXV0aGVudGljYXRpb24gUm9vdCBSNDYw
HhcNMjEwMzIyMDAwMDAwWhcNMzYwMzIxMjM1OTU5WjBgMQswCQYDVQQGEwJHQjEY
MBYGA1UEChMPU2VjdGlnbyBMaW1pdGVkMTcwNQYDVQQDEy5TZWN0aWdvIFB1Ymxp
YyBTZXJ2ZXIgQXV0aGVudGljYXRpb24gQ0EgRFYgUjM2MIIBojANBgkqhkiG9w0B
AQEFAAOCAY8AMIIBigKCAYEAljZf2HIz7+SPUPQCQObZYcrxLTHYdf1ZtMRe7Yeq
RPSwygz16qJ9cAWtWNTcuICc++p8Dct7zNGxCpqmEtqifO7NvuB5dEVexXn9RFFH
12Hm+NtPRQgXIFjx6MSJcNWuVO3XGE57L1mHlcQYj+g4hny90aFh2SCZCDEVkAja
EMMfYPKuCjHuuF+bzHFb/9gV8P9+ekcHENF2nR1efGWSKwnfG5RawlkaQDpRtZTm
M64TIsv/r7cyFO4nSjs1jLdXYdz5q3a4L0NoabZfbdxVb+CUEHfB0bpulZQtH1Rv
38e/lIdP7OTTIlZh6OYL6NhxP8So0/sht/4J9mqIGxRFc0/pC8suja+wcIUna0HB
pXKfXTKpzgis+zmXDL06ASJf5E4A2/m+Hp6b84sfPAwQ766rI65mh50S0Di9E3Pn
2WcaJc+PILsBmYpgtmgWTR9eV9otfKRUBfzHUHcVgarub/XluEpRlTtZudU5xbFN
xx/DgMrXLUAPaI60fZ6wA+PTAgMBAAGjggGBMIIBfTAfBgNVHSMEGDAWgBRWc1hk
lfmSGrASKgRieaFAFYghSTAdBgNVHQ4EFgQUaMASFhgOr872h6YyV6NGUV3LBycw
DgYDVR0PAQH/BAQDAgGGMBIGA1UdEwEB/wQIMAYBAf8CAQAwHQYDVR0lBBYwFAYI
KwYBBQUHAwEGCCsGAQUFBwMCMBsGA1UdIAQUMBIwBgYEVR0gADAIBgZngQwBAgEw
VAYDVR0fBE0wSzBJoEegRYZDaHR0cDovL2NybC5zZWN0aWdvLmNvbS9TZWN0aWdv
UHVibGljU2VydmVyQXV0aGVudGljYXRpb25Sb290UjQ2LmNybDCBhAYIKwYBBQUH
AQEEeDB2ME8GCCsGAQUFBzAChkNodHRwOi8vY3J0LnNlY3RpZ28uY29tL1NlY3Rp
Z29QdWJsaWNTZXJ2ZXJBdXRoZW50aWNhdGlvblJvb3RSNDYucDdjMCMGCCsGAQUF
BzABhhdodHRwOi8vb2NzcC5zZWN0aWdvLmNvbTANBgkqhkiG9w0BAQwFAAOCAgEA
YtOC9Fy+TqECFw40IospI92kLGgoSZGPOSQXMBqmsGWZUQ7rux7cj1du6d9rD6C8
ze1B2eQjkrGkIL/OF1s7vSmgYVafsRoZd/IHUrkoQvX8FZwUsmPu7amgBfaY3g+d
q1x0jNGKb6I6Bzdl6LgMD9qxp+3i7GQOnd9J8LFSietY6Z4jUBzVoOoz8iAU84OF
h2HhAuiPw1ai0VnY38RTI+8kepGWVfGxfBWzwH9uIjeooIeaosVFvE8cmYUB4TSH
5dUyD0jHct2+8ceKEtIoFU/FfHq/mDaVnvcDCZXtIgitdMFQdMZaVehmObyhRdDD
4NQCs0gaI9AAgFj4L9QtkARzhQLNyRf87Kln+YU0lgCGr9HLg3rGO8q+Y4ppLsOd
unQZ6ZxPNGIfOApbPVf5hCe58EZwiWdHIMn9lPP6+F404y8NNugbQixBber+x536
WrZhFZLjEkhp7fFXf9r32rNPfb74X/U90Bdy4lzp3+X1ukh1BuMxA/EEhDoTOS3l
7ABvc7BYSQubQ2490OcdkIzUh3ZwDrakMVrbaTxUM2p24N6dB+ns2zptWCva6jzW
r8IWKIMxzxLPv5Kt3ePKcUdvkBU/smqujSczTzzSjIoR5QqQA6lN1ZRSnuHIWCvh
JEltkYnTAH41QJ6SAWO66GrrUESwN/cgZzL4JLEqz1Y=
-----END CERTIFICATE-----"""

_TIMEOUT = httpx.Timeout(120.0, connect=15.0)


def _ensure_client():
    """Install a subsets_utils HTTP client whose trust store includes the
    intermediate the server omits. Verification stays enabled; we just give it
    the cert needed to build a complete chain. Idempotent per process."""
    if _http_client._client is not None:
        return
    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.load_verify_locations(cadata=_SECTIGO_INTERMEDIATE_PEM)
    _http_client._client = httpx.Client(
        timeout=_TIMEOUT,
        headers={"User-Agent": "subsets.io-connector/1.0 (+https://subsets.io)"},
        follow_redirects=True,
        verify=ctx,
    )


@transient_retry()
def _get_meta(url):
    resp = get(url, timeout=_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _post_data(url, body):
    resp = post(url, json=body, timeout=_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def _col_name(code, used):
    """Sanitize a PxWeb variable code into a stable column name, avoiding the
    reserved measure column and collisions."""
    name = re.sub(r"[^0-9A-Za-z]+", "_", str(code)).strip("_").lower()
    if not name:
        name = "dim"
    if name == "value":
        name = "value_dim"
    base = name
    n = 2
    while name in used:
        name = f"{base}_{n}"
        n += 1
    used.add(name)
    return name


def _blocks(dims):
    """Yield query blocks (list of [code, value_codes]) whose product of
    cardinalities is <= MAX_CELLS, splitting the largest dimension(s) as needed."""
    sizes = [len(v) for _, v in dims]
    total = math.prod(sizes) if sizes else 1
    if total <= MAX_CELLS:
        yield dims
        return
    i = max(range(len(dims)), key=lambda k: sizes[k])
    code, vals = dims[i]
    rest = math.prod(len(v) for j, (_, v) in enumerate(dims) if j != i) or 1
    per = max(1, MAX_CELLS // rest)
    for s in range(0, len(vals), per):
        nd = [[c, list(v)] for c, v in dims]
        nd[i] = [code, vals[s:s + per]]
        if rest > MAX_CELLS:
            # one value of this dim still leaves the rest over the cap: recurse,
            # which splits the next-largest dimension until each block fits.
            yield from _blocks(nd)
        else:
            yield nd


def _coerce(v):
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError:
            return None
    return None


def _decode(dataset, colmap):
    """Flatten a json-stat (v1 'dataset' wrapper) response to long-format rows."""
    order = dataset["id"]
    sizes = dataset["size"]
    # position -> value label, per dimension
    pos_label = {}
    for d in order:
        cat = dataset["dimension"][d]["category"]
        index = cat["index"]
        labels = cat.get("label", {})
        arr = [None] * len(index)
        for code, pos in index.items():
            arr[pos] = labels.get(code, code)
        pos_label[d] = arr

    values = dataset["value"]
    if isinstance(values, dict):
        # sparse form: {str(flat_index): value}
        n = math.prod(sizes) if sizes else 0
        dense = [None] * n
        for k, v in values.items():
            dense[int(k)] = v
        values = dense

    rows = []
    for idx, raw in enumerate(values):
        rem = idx
        row = {}
        for k in range(len(order) - 1, -1, -1):
            d = order[k]
            s = sizes[k]
            pos = rem % s
            rem //= s
            row[colmap[d]] = pos_label[d][pos]
        row["value"] = _coerce(raw)
        rows.append(row)
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    _ensure_client()
    eid = node_id[len("geostat-"):]
    url = BASE + ENTITY_PATHS[eid]

    meta = _get_meta(url)
    variables = meta["variables"]
    # map each dimension code to a clean, unique column name
    used = set()
    colmap = {v["code"]: _col_name(v["code"], used) for v in variables}

    dims = [[v["code"], list(v["values"])] for v in variables]
    rows = []
    for block in _blocks(dims):
        body = {
            "query": [
                {"code": code, "selection": {"filter": "item", "values": vals}}
                for code, vals in block
            ],
            "response": {"format": "json-stat"},
        }
        dataset = _post_data(url, body)["dataset"]
        rows.extend(_decode(dataset, colmap))

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"geostat-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# One published Delta table per table: thin parse pass — drop missing cells and
# type the measure. Dimension columns pass through as the source's value labels.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
