"""Rosstat — Russian Federal State Statistics Service open-data connector.

Mechanism: the Russian Open Data Standard 4.0 portal at rosstat.gov.ru/opendata.
Each accepted dataset is fetched per-entity via a two-hop resolve:

    1. GET https://rosstat.gov.ru/opendata/<slug>/meta.csv  (the passport)
       -> the row whose key starts with 'data-' gives the data file URL.
    2. GET that data file. It is one of:
       - a semicolon-delimited CSV (line 1 = dataset-title preamble, line 2 =
         header, data follows), or
       - a .zip wrapping exactly one such CSV (the IKT survey years).
    The data file is normalized to wide NDJSON (one object per row, keyed by the
    cleaned header names) so the SQL transform can `SELECT *` over it.

Stateless full re-pull: every refresh fetches the whole corpus and overwrites.
The corpus is ~46 small/medium CSVs (KBs to ~75MB); no incremental filter is
needed and revisions are picked up for free.

Encoding: text on this portal is inconsistently encoded — some files are raw
CP1251, some are CP1251 bytes mis-decoded as latin1 and re-saved as UTF-8
(double-encoding mojibake), some are pure ASCII coded microdata. `_smart_decode`
auto-detects per file by maximizing recovered Cyrillic.

TLS: rosstat.gov.ru is served under the Russian Trusted (Минцифры) CA, which is
not in the default trust store, and the server omits the intermediate. We pin
the verified Root + issuing Sub CA below and verify against them (plus the
system roots). No `verify=False` is used.
"""
import csv
import io
import json
import re
import ssl
import zipfile

import httpx

from subsets_utils import NodeSpec, SqlNodeSpec, get, raw_writer
from subsets_utils import (
    http_client,
    transient_retry,
)

# Entity union (rank-accepted), copied from work/entity_union.json.
from constants import ENTITY_IDS

# spec id (lowercased, underscores->dashes) -> original case-sensitive slug.
SLUG_BY_NODE_ID = {
    f"rosstat-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}

BASE = "https://rosstat.gov.ru/opendata"

# Russian Trusted Sub CA (issuing, AKI matches rosstat leaf) + Root CA.
# Verified to chain the *.rosstat.gov.ru leaf. Refresh if the chain rotates.
_RUSSIAN_TRUSTED_CA_PEM = """-----BEGIN CERTIFICATE-----
MIIG6DCCBNCgAwIBAgICEAUwDQYJKoZIhvcNAQELBQAwcDELMAkGA1UEBhMCUlUx
PzA9BgNVBAoMNlRoZSBNaW5pc3RyeSBvZiBEaWdpdGFsIERldmVsb3BtZW50IGFu
ZCBDb21tdW5pY2F0aW9uczEgMB4GA1UEAwwXUnVzc2lhbiBUcnVzdGVkIFJvb3Qg
Q0EwHhcNMjQwNzE1MTI1MDQxWhcNMjkwNzE5MTI1MDQxWjBvMQswCQYDVQQGEwJS
VTE/MD0GA1UECgw2VGhlIE1pbmlzdHJ5IG9mIERpZ2l0YWwgRGV2ZWxvcG1lbnQg
YW5kIENvbW11bmljYXRpb25zMR8wHQYDVQQDDBZSdXNzaWFuIFRydXN0ZWQgU3Vi
IENBMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA1j0rkZECOt1S8o7I
JY+4YKAxuEa5xaHKHXT2EpkuC/0krqMOjUy2oPIRNgR5g8X0Jl6jamxeGLc4Q1tf
ju6or9oSRYThIUhRsFDQNBiBBEXoBgWxTfiKB2eyT97+pz5TBtBiRCPaLGRHYLRb
9Jz2HkJlxbtNPjtDrF5DPHym+mZ1M1z3hIQYAqJwLpsEBnsw/VxWMlxqHoeewd0h
uJMd71KQ5vOKlz7KrIZ6EobNNa6wItuvsfj3kYCK7O78uLHGXXFxdr8Hae9lMUmC
8F7AFwa+bO1LRlTlqW7rE3rLf+jj70N01N8T3o22v14YBaFBWQWncAVYD2JuL3tH
252+kdNOERf1fLbLRigJAbd+hOhWYlNf963TFDgnNPliHNIW72SygVBnI2V3JwO1
dp1hVKpK/zt8ziGdHW4gmOLTsH50YKdR4jNqUgQv4wASlKn9OpN6zHYc5G8h86fY
BM+zxE5ikGI+I/vIqBuI0eaDU92AWN/YjFLpu8tMu9kLRSCf1vug6FIfDPWVo7iP
ac/SI2v8jnnpaW7ph/Pz3WkzaG7ZZJsfFs+8dploWc6LOoDtbFBhMdGMxu024msC
0PSjZb5ODXPIaO2NsA7fMiAtZcoK6anTUJh4zOP/stA9qsJGNxdrEmiPXSmBZY/N
Y0wkZgZ6JTDhw7038bPvctkblJkCAwEAAaOCAYswggGHMB0GA1UdDgQWBBR3Pdk5
r0K93FvKduru/c4+YSkwXzAfBgNVHSMEGDAWgBTh0YHlzlpfBKrS6badZrHF+qws
hzAOBgNVHQ8BAf8EBAMCAYYwEgYDVR0TAQH/BAgwBgEB/wIBADCBmAYIKwYBBQUH
AQEEgYswgYgwQAYIKwYBBQUHMAKGNGh0dHA6Ly9udWMtY2RwLnZvc2tob2QucnUv
Y2RwL3Jvb3RjYV9zc2xfcnNhMjAyMi5jcnQwRAYIKwYBBQUHMAKGOGh0dHA6Ly9u
dWMtY2RwLmRpZ2l0YWwuZ292LnJ1L2NkcC9yb290Y2Ffc3NsX3JzYTIwMjIuY3J0
MIGFBgNVHR8EfjB8MDqgOKA2hjRodHRwOi8vbnVjLWNkcC52b3NraG9kLnJ1L2Nk
cC9yb290Y2Ffc3NsX3JzYTIwMjIuY3JsMD6gPKA6hjhodHRwOi8vbnVjLWNkcC5k
aWdpdGFsLmdvdi5ydS9jZHAvcm9vdGNhX3NzbF9yc2EyMDIyLmNybDANBgkqhkiG
9w0BAQsFAAOCAgEAmsINXtQ7wwUWvIeOr80MdJS/5G4xhyZOVEmeUorThquT672y
cCg3XCxc4fwbiZqSSbBqntQ7RtiTAKMYMvBageKoVHbzz+R4jX01tKcTx8cDePrz
dJ73bLNUorE7RU9QsW4KyiUeRmjMDV23AUlEvuQFTwgkHXvbac1BBdPn9CrssQuF
5EGohZKcQPFiAAc4SHbRNhlr7uAwgpc/erzI9EAcvA6BVAXcVKoeGpV01uexUgZ6
St5RP9UmDWNA7T4yVXWJ233N0Q8bl+6AswINQ3PosPu6yQQHQjr65YS06epK+AeI
6j+oGR4xI7EhTQhQvaobnGmX/8QQ7XDRYCP2HXYxiffnn/CfZ/BVyKLYeY1ZipjE
nzqdQIC2+Q3WtY8jsVRQMP38WFRmtsIt5snehnPTs5bKGVIcYzj3o3Ex/K7agEz0
zAJ0JR5ivXZOvNkT0g9x1v+S1IkU3e/nX1a+tpRquMtnHX0L2lXArNHUbaOO9EJt
d57WaIpofV5cVhhwShOgAuBc9UMJF3/n4t4RKiPxtsK8P67gcmphMhslj7AMYrYM
ej2NvQZY4m3ub3CPC/PrTjDONvb+8g5xrKtxBjYqC74HSB4dg9G3WimSDUuP2Su6
G2y2TUeyJuCvCLz289VoO0vg7cNdMobE3KCqAiiNhN2VBFxHAUKmUoRcRdw=
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIFwjCCA6qgAwIBAgICEAAwDQYJKoZIhvcNAQELBQAwcDELMAkGA1UEBhMCUlUx
PzA9BgNVBAoMNlRoZSBNaW5pc3RyeSBvZiBEaWdpdGFsIERldmVsb3BtZW50IGFu
ZCBDb21tdW5pY2F0aW9uczEgMB4GA1UEAwwXUnVzc2lhbiBUcnVzdGVkIFJvb3Qg
Q0EwHhcNMjIwMzAxMjEwNDE1WhcNMzIwMjI3MjEwNDE1WjBwMQswCQYDVQQGEwJS
VTE/MD0GA1UECgw2VGhlIE1pbmlzdHJ5IG9mIERpZ2l0YWwgRGV2ZWxvcG1lbnQg
YW5kIENvbW11bmljYXRpb25zMSAwHgYDVQQDDBdSdXNzaWFuIFRydXN0ZWQgUm9v
dCBDQTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAMfFOZ8pUAL3+r2n
qqE0Zp52selXsKGFYoG0GM5bwz1bSFtCt+AZQMhkWQheI3poZAToYJu69pHLKS6Q
XBiwBC1cvzYmUYKMYZC7jE5YhEU2bSL0mX7NaMxMDmH2/NwuOVRj8OImVa5s1F4U
zn4Kv3PFlDBjjSjXKVY9kmjUBsXQrIHeaqmUIsPIlNWUnimXS0I0abExqkbdrXbX
YwCOXhOO2pDUx3ckmJlCMUGacUTnylyQW2VsJIyIGA8V0xzdaeUXg0VZ6ZmNUr5Y
Ber/EAOLPb8NYpsAhJe2mXjMB/J9HNsoFMBFJ0lLOT/+dQvjbdRZoOT8eqJpWnVD
U+QL/qEZnz57N88OWM3rabJkRNdU/Z7x5SFIM9FrqtN8xewsiBWBI0K6XFuOBOTD
4V08o4TzJ8+Ccq5XlCUW2L48pZNCYuBDfBh7FxkB7qDgGDiaftEkZZfApRg2E+M9
G8wkNKTPLDc4wH0FDTijhgxR3Y4PiS1HL2Zhw7bD3CbslmEGgfnnZojNkJtcLeBH
BLa52/dSwNU4WWLubaYSiAmA9IUMX1/RpfpxOxd4Ykmhz97oFbUaDJFipIggx5sX
ePAlkTdWnv+RWBxlJwMQ25oEHmRguNYf4Zr/Rxr9cS93Y+mdXIZaBEE0KS2iLRqa
OiWBki9IMQU4phqPOBAaG7A+eP8PAgMBAAGjZjBkMB0GA1UdDgQWBBTh0YHlzlpf
BKrS6badZrHF+qwshzAfBgNVHSMEGDAWgBTh0YHlzlpfBKrS6badZrHF+qwshzAS
BgNVHRMBAf8ECDAGAQH/AgEEMA4GA1UdDwEB/wQEAwIBhjANBgkqhkiG9w0BAQsF
AAOCAgEAALIY1wkilt/urfEVM5vKzr6utOeDWCUczmWX/RX4ljpRdgF+5fAIS4vH
tmXkqpSCOVeWUrJV9QvZn6L227ZwuE15cWi8DCDal3Ue90WgAJJZMfTshN4OI8cq
W9E4EG9wglbEtMnObHlms8F3CHmrw3k6KmUkWGoa+/ENmcVl68u/cMRl1JbW2bM+
/3A+SAg2c6iPDlehczKx2oa95QW0SkPPWGuNA/CE8CpyANIhu9XFrj3RQ3EqeRcS
AQQod1RNuHpfETLU/A2gMmvn/w/sx7TB3W5BPs6rprOA37tutPq9u6FTZOcG1Oqj
C/B7yTqgI7rbyvox7DEXoX7rIiEqyNNUguTk/u3SZ4VXE2kmxdmSh3TQvybfbnXV
4JbCZVaqiZraqc7oZMnRoWrXRG3ztbnbes/9qhRGI7PqXqeKJBztxRTEVj8ONs1d
WN5szTwaPIvhkhO3CO5ErU2rVdUr89wKpNXbBODFKRtgxUT70YpmJ46VVaqdAhOZ
D9EUUn4YaeLaS8AjSF/h7UkjOibNc4qVDiPP+rkehFWM66PVnP1Msh93tc+taIfC
EYVMxjh8zNbFuoc7fzvvrFILLe7ifvEIUqSVIC/AzplM/Jxw7buXFeGP1qVCBEHq
391d/9RAfaZ12zkwFsl+IKwE/OZxW8AHa9i1p4GO0YSNuczzEm4=
-----END CERTIFICATE-----
"""


def _ensure_tls():
    """Rebuild the shared httpx client to trust the Russian CA + system roots.

    The shared subsets_utils client doesn't plumb a custom CA, so we install a
    verifying SSLContext on it once. All HTTP still flows through
    subsets_utils.get (logging/tracking intact); we only swap the transport's
    trust store.
    """
    if getattr(http_client, "_rosstat_tls", False):
        return
    ctx = ssl.create_default_context(cadata=_RUSSIAN_TRUSTED_CA_PEM)
    ctx.load_default_certs()  # keep the normal roots too
    cfg = http_client._client_config
    client = httpx.Client(
        timeout=cfg.get("timeout", 30),
        headers=cfg.get("headers"),
        follow_redirects=True,
        verify=ctx,
    )
    if http_client._client is not None:
        http_client._client.close()
    http_client._client = client
    http_client._rosstat_tls = True


@transient_retry()
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _smart_decode(raw: bytes) -> str:
    """Decode this portal's inconsistent CSV encodings to correct Unicode."""
    try:
        u = raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1251", "replace")  # raw CP1251 bytes
    # Valid UTF-8: either genuinely correct, or CP1251 double-encoded mojibake.
    try:
        fixed = u.encode("latin1").decode("cp1251")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return u

    def cyr(s: str) -> int:
        return sum(1 for c in s if "Ѐ" <= c <= "ӿ")

    return (fixed if cyr(fixed) > cyr(u) else u)


def _strip_bom(text: str) -> str:
    return text.lstrip("﻿")


_NUMISH = re.compile(r"^[\d][\d\s.,'\"/:°%–-]*$")


def _detect_delim(text: str) -> str:
    """Pick the delimiter giving the widest, quote-aware parse of the head.

    Files on this portal are inconsistently ';' or ',' delimited (and may quote
    fields that contain the other character), so count fields with a real CSV
    parser rather than raw character counts.
    """
    best_med, best_delim = 0, ";"
    for delim in (";", ",", "\t"):
        counts = []
        for i, row in enumerate(csv.reader(io.StringIO(text), delimiter=delim)):
            if i >= 25:
                break
            counts.append(len(row))
        med = sorted(counts)[len(counts) // 2] if counts else 1
        if med > best_med:
            best_med, best_delim = med, delim
    return best_delim


def _num_frac(row) -> float:
    """Fraction of non-empty cells that look numeric / coded (not text labels)."""
    cells = [c.strip().strip('"').strip() for c in row]
    cells = [c for c in cells if c]
    if not cells:
        return 1.0
    return sum(bool(_NUMISH.match(c)) for c in cells) / len(cells)


def _dedupe(names):
    out, seen = [], {}
    for name in names:
        name = (name or "").strip().strip('"').strip() or "col"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 1
        out.append(name)
    return out


def _plan_columns(sample):
    """From a small head sample decide rows-to-skip and the column names.

    Returns (skip_rows, names). A leading row with a single non-empty cell is a
    dataset-title preamble. The next row is a header iff it reads as text labels
    while the body below carries numeric/coded values — otherwise the file is
    header-less (the OK* classifiers) and we synthesize positional names.
    """
    i = 0
    while i < len(sample) and sum(1 for c in sample[i] if c.strip()) <= 1:
        i += 1  # drop title preamble line(s)
    if i >= len(sample):
        return i, []
    head = sample[i]
    body = sample[i + 1:i + 11]
    body_num = sorted(_num_frac(r) for r in body)[len(body) // 2] if body else 0.0
    is_header = _num_frac(head) < 0.3 and body_num >= 0.3

    if is_header:
        keep = [j for j, c in enumerate(head) if c.strip()]
        names = _dedupe([head[j] for j in keep])
        return i + 1, list(zip(keep, names))
    # header-less: width from the sample, drop all-empty trailing columns
    width = max((len(r) for r in sample[i:]), default=0)
    last = 0
    for r in sample[i:]:
        for j in range(width):
            if j < len(r) and r[j].strip():
                last = max(last, j)
    keep = list(range(last + 1))
    return i, list(zip(keep, [f"col_{j}" for j in keep]))


def _resolve_data_url(slug: str) -> str:
    raw = _fetch_bytes(f"{BASE}/{slug}/meta.csv")
    text = raw.decode("cp1251", "replace")
    for row in csv.reader(io.StringIO(text)):
        if len(row) >= 2 and row[0].startswith("data-"):
            return row[1]
    raise AssertionError(f"{slug}: no 'data-' row in meta.csv")


def _csv_text_from_data(url: str) -> str:
    """Return the decoded CSV text, unwrapping a single-member .zip if needed."""
    payload = _fetch_bytes(url)
    if url.lower().endswith(".zip") or payload[:2] == b"PK":
        zf = zipfile.ZipFile(io.BytesIO(payload))
        members = [m for m in zf.namelist() if m.lower().endswith(".csv")]
        if not members:
            raise AssertionError(f"{url}: zip has no .csv member ({zf.namelist()})")
        payload = zf.read(members[0])
    return _strip_bom(_smart_decode(payload))


def fetch_one(node_id: str) -> None:
    """Resolve one dataset's data file and write it as wide NDJSON.

    Russian Open Data Standard CSV layout: row 1 is a title preamble, row 2 is
    the column header, data follows; delimiter is ';'. Streamed row-by-row to
    bound memory on the larger (tens-of-MB) microdata files.
    """
    _ensure_tls()
    slug = SLUG_BY_NODE_ID[node_id]
    text = _csv_text_from_data(_resolve_data_url(slug))

    delim = _detect_delim(text)

    # Peek a head sample to decide title/header handling and the columns.
    sample = []
    for row in csv.reader(io.StringIO(text), delimiter=delim):
        if any(c.strip() for c in row):
            sample.append(row)
        if len(sample) >= 50:
            break
    skip_rows, cols = _plan_columns(sample)
    if not cols:
        raise AssertionError(f"{slug}: could not determine any columns")

    # Stream the body (text held once in memory; rows written one at a time).
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip",
                    encoding="utf-8") as fh:
        seen = 0
        n = 0
        for row in csv.reader(io.StringIO(text), delimiter=delim):
            if not any(c.strip() for c in row):
                continue  # blank line
            seen += 1
            if seen <= skip_rows:
                continue  # title preamble + header
            rec = {name: (row[i] if i < len(row) else "") for i, name in cols}
            fh.write(json.dumps(rec, ensure_ascii=False))
            fh.write("\n")
            n += 1
    if n == 0:
        raise AssertionError(f"{slug}: produced 0 data rows")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"rosstat-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per dataset. Schemas are heterogeneous (each dataset
# ships its own column list), so the transform is a thin pass-through over the
# normalized wide NDJSON.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
