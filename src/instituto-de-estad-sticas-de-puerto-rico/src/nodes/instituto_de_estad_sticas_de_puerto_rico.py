"""Instituto de Estadísticas de Puerto Rico — Datos.PR CKAN portal connector.

Mechanism: CKAN 2.7.0 Action API at https://datos.estadisticas.pr/api/3/action.
One download node per rank-active package; each fetches the package's tabular
resources and normalizes them into a single per-package raw parquet.

Heterogeneity handling: a CKAN package bundles several resources in mixed
formats (CSV/TXT/XLSX/XLS/JSON/ZIP plus non-tabular PDF/KML). We expand every
resource into one or more "tables" (a CSV file, an Excel sheet, a JSON array, a
ZIP member), group those tables by their column signature, and concatenate the
single dominant group (the one with the most data). This captures the common
case of a package partitioned into same-schema yearly files while avoiding a
wide union-of-everything schema explosion. All values are stored as strings
(the portal's CSVs are untyped and drift across years); two discriminator
columns — `source_resource` and `source_file` — record provenance. The SQL
transform republishes the raw table verbatim.

Strategy: stateless full re-pull. The portal is small (~100 packages) and most
files re-download in seconds; the one large file (comercio-externo, ~1.5GB) is
streamed to parquet in batches so it never lands in RAM whole. Freshness is the
maintain step's concern.

TLS note: datos.estadisticas.pr serves an incomplete certificate chain (the
RapidSSL intermediate is omitted). We add that public DigiCert intermediate to
the trust store via SSL_CERT_FILE so verification succeeds on the Linux runner
too — no verify=False.
"""

import csv
import io
import json
import os
import re
import tempfile
import zipfile

import certifi
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    get_client,
    raw_parquet_writer,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "instituto-de-estad-sticas-de-puerto-rico"
BASE = "https://datos.estadisticas.pr/api/3/action"

# Public DigiCert intermediate (RapidSSL TLS RSA CA G1 -> DigiCert Global Root
# G2). The server omits it from its chain; we supply it so the leaf validates.
_RAPIDSSL_INTERMEDIATE = """-----BEGIN CERTIFICATE-----
MIIEszCCA5ugAwIBAgIQCyWUIs7ZgSoVoE6ZUooO+jANBgkqhkiG9w0BAQsFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBH
MjAeFw0xNzExMDIxMjI0MzNaFw0yNzExMDIxMjI0MzNaMGAxCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
b20xHzAdBgNVBAMTFlJhcGlkU1NMIFRMUyBSU0EgQ0EgRzEwggEiMA0GCSqGSIb3
DQEBAQUAA4IBDwAwggEKAoIBAQC/uVklRBI1FuJdUEkFCuDL/I3aJQiaZ6aibRHj
ap/ap9zy1aYNrphe7YcaNwMoPsZvXDR+hNJOo9gbgOYVTPq8gXc84I75YKOHiVA4
NrJJQZ6p2sJQyqx60HkEIjzIN+1LQLfXTlpuznToOa1hyTD0yyitFyOYwURM+/CI
8FNFMpBhw22hpeAQkOOLmsqT5QZJYeik7qlvn8gfD+XdDnk3kkuuu0eG+vuyrSGr
5uX5LRhFWlv1zFQDch/EKmd163m6z/ycx/qLa9zyvILc7cQpb+k7TLra9WE17YPS
n9ANjG+ECo9PDW3N9lwhKQCNvw1gGoguyCQu7HE7BnW8eSSFAgMBAAGjggFmMIIB
YjAdBgNVHQ4EFgQUDNtsgkkPSmcKuBTuesRIUojrVjgwHwYDVR0jBBgwFoAUTiJU
IBiV5uNu5g/6+rkS7QYXjzkwDgYDVR0PAQH/BAQDAgGGMB0GA1UdJQQWMBQGCCsG
AQUFBwMBBggrBgEFBQcDAjASBgNVHRMBAf8ECDAGAQH/AgEAMDQGCCsGAQUFBwEB
BCgwJjAkBggrBgEFBQcwAYYYaHR0cDovL29jc3AuZGlnaWNlcnQuY29tMEIGA1Ud
HwQ7MDkwN6A1oDOGMWh0dHA6Ly9jcmwzLmRpZ2ljZXJ0LmNvbS9EaWdpQ2VydEds
b2JhbFJvb3RHMi5jcmwwYwYDVR0gBFwwWjA3BglghkgBhv1sAQEwKjAoBggrBgEF
BQcCARYcaHR0cHM6Ly93d3cuZGlnaWNlcnQuY29tL0NQUzALBglghkgBhv1sAQIw
CAYGZ4EMAQIBMAgGBmeBDAECAjANBgkqhkiG9w0BAQsFAAOCAQEAGUSlOb4K3Wtm
SlbmE50UYBHXM0SKXPqHMzk6XQUpCheF/4qU8aOhajsyRQFDV1ih/uPIg7YHRtFi
CTq4G+zb43X1T77nJgSOI9pq/TqCwtukZ7u9VLL3JAq3Wdy2moKLvvC8tVmRzkAe
0xQCkRKIjbBG80MSyDX/R4uYgj6ZiNT/Zg6GI6RofgqgpDdssLc0XIRQEotxIZcK
zP3pGJ9FCbMHmMLLyuBd+uCWvVcF2ogYAawufChS/PT61D9rqzPRS5I2uqa3tmIT
44JhJgWhBnFMb7AGQkvNq9KNS9dd3GWc17H/dXa1enoxzWjE0hBdFjxPhUb0W3wi
8o34/m8Fxw==
-----END CERTIFICATE-----
"""

# Map every download spec id back to its real CKAN package name (slugging is
# lossy: '_' -> '-'). Built once at import from the imported constant — a pure
# in-memory transform, not I/O.
SLUG_TO_PKG = {f"{SLUG}-{e.lower().replace('_', '-')}": e for e in ENTITY_IDS}

# Formats we extract tabular rows from. PDF/KML/shapefile are skipped.
_TABULAR_FORMATS = {"CSV", "TXT", "TSV", "XLSX", "XLS", "JSON"}
_CSV_LIKE = {"CSV", "TXT", "TSV"}
_EXCEL_LIKE = {"XLSX", "XLS"}

_BATCH_ROWS = 50_000          # rows per parquet batch when streaming
# A single non-CSV resource larger than this is skipped (logged) to protect RSS;
# CSV/TXT are streamed regardless of size so they are never capped.
_MAX_INMEM_BYTES = 400 * 1024 * 1024

_http_ready = False


def _ensure_http() -> None:
    """Point the HTTP client at a CA bundle that includes the missing RapidSSL
    intermediate, then reset the client so it rebuilds with that trust store."""
    global _http_ready
    if _http_ready:
        return
    fd, path = tempfile.mkstemp(prefix="iepr_ca_", suffix=".pem")
    with os.fdopen(fd, "w") as f:
        f.write(open(certifi.where()).read())
        f.write("\n")
        f.write(_RAPIDSSL_INTERMEDIATE)
    os.environ["SSL_CERT_FILE"] = path
    configure_http()  # close & rebuild client so it reads the new SSL_CERT_FILE
    _http_ready = True


@transient_retry()
def _api(action: str, **params):
    resp = get(f"{BASE}/{action}", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"CKAN action {action} returned success=false")
    return body["result"]


@transient_retry()
def _download_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _sanitize_cols(cols):
    """Trim, fill blanks, and de-duplicate column names."""
    out = []
    seen = {}
    for i, c in enumerate(cols):
        name = (str(c) if c is not None else "").strip()
        name = re.sub(r"\s+", " ", name)
        if not name or name.lower() == "nan":
            name = f"col_{i}"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 1
        out.append(name)
    return out


def _decode(b: bytes) -> str:
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return b.decode("utf-8", errors="replace")


def _sniff_delimiter(sample: str) -> str:
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
    except csv.Error:
        # fall back to the most frequent candidate on the header line
        head = sample.splitlines()[0] if sample else ""
        return max(",;\t|", key=lambda d: head.count(d)) if head else ","


# --- "table" = a signature + a generator of dict rows --------------------------
# Each tabular source becomes a Table: (columns, source_resource, source_file,
# rows_iter). rows_iter yields dicts keyed by the sanitized columns.

class Table:
    __slots__ = ("columns", "source_resource", "source_file", "rows_iter")

    def __init__(self, columns, source_resource, source_file, rows_iter):
        self.columns = columns
        self.source_resource = source_resource
        self.source_file = source_file
        self.rows_iter = rows_iter

    @property
    def signature(self):
        return tuple(self.columns)


def _csv_table(text: str, source_resource: str, source_file: str):
    delim = _sniff_delimiter(text[:8192])
    reader = csv.reader(io.StringIO(text), delimiter=delim)
    try:
        header = next(reader)
    except StopIteration:
        return None
    cols = _sanitize_cols(header)

    def rows():
        for raw in reader:
            if not raw or all((v is None or v == "") for v in raw):
                continue
            row = {}
            for i, col in enumerate(cols):
                row[col] = raw[i] if i < len(raw) else None
            yield row

    return Table(cols, source_resource, source_file, rows())


def _excel_tables(content: bytes, source_resource: str, fmt: str):
    import pandas as pd

    engine = "openpyxl" if fmt == "XLSX" else "xlrd"
    try:
        xl = pd.ExcelFile(io.BytesIO(content), engine=engine)
    except Exception as e:  # noqa: BLE001 - logged, resource skipped
        print(f"[{source_resource}] excel open failed: {type(e).__name__}: {e}")
        return []
    tables = []
    for sheet in xl.sheet_names:
        try:
            df = xl.parse(sheet, dtype=str)
        except Exception as e:  # noqa: BLE001
            print(f"[{source_resource}] sheet {sheet} parse failed: {e}")
            continue
        if df.shape[0] == 0 or df.shape[1] == 0:
            continue
        cols = _sanitize_cols(list(df.columns))
        records = df.where(df.notna(), None).values.tolist()

        def rows(records=records, cols=cols):
            for rec in records:
                yield {cols[i]: rec[i] for i in range(len(cols))}

        tables.append(Table(cols, source_resource, f"{source_file_sheet(sheet)}", rows()))
    return tables


def source_file_sheet(sheet):
    return f"sheet:{sheet}"


def _json_table(content: bytes, source_resource: str, source_file: str):
    try:
        data = json.loads(content)
    except Exception as e:  # noqa: BLE001
        print(f"[{source_resource}] json parse failed: {e}")
        return None
    # Only flat arrays of objects are tabular; GeoJSON / nested dicts are skipped.
    if isinstance(data, dict):
        for key in ("data", "result", "records", "rows"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        return None
    cols, seen = [], set()
    for rec in data[:2000]:
        for k in rec:
            if k not in seen:
                seen.add(k)
                cols.append(str(k))
    san = _sanitize_cols(cols)
    mapping = dict(zip(cols, san))

    def rows():
        for rec in data:
            if isinstance(rec, dict):
                yield {mapping[k]: _scalar(v) for k, v in rec.items() if k in mapping}

    return Table(san, source_resource, source_file, rows())


def _scalar(v):
    if v is None or isinstance(v, str):
        return v
    if isinstance(v, (int, float, bool)):
        return str(v)
    return json.dumps(v, ensure_ascii=False)


def _zip_tables(content: bytes, source_resource: str):
    try:
        zf = zipfile.ZipFile(io.BytesIO(content))
    except Exception as e:  # noqa: BLE001
        print(f"[{source_resource}] bad zip: {e}")
        return []
    tables = []
    for info in zf.infolist():
        if info.is_dir():
            continue
        name = info.filename
        ext = name.rsplit(".", 1)[-1].upper() if "." in name else ""
        try:
            member = zf.read(info)
        except Exception as e:  # noqa: BLE001
            print(f"[{source_resource}] zip member {name} read failed: {e}")
            continue
        if ext in _CSV_LIKE:
            t = _csv_table(_decode(member), source_resource, name)
            if t:
                tables.append(t)
        elif ext in _EXCEL_LIKE:
            tables.extend(_excel_tables(member, source_resource, ext))
        elif ext == "JSON":
            t = _json_table(member, source_resource, name)
            if t:
                tables.append(t)
        # PDF/shapefile/other members ignored
    return tables


def _stream_csv_table(url: str, source_resource: str, source_file: str):
    """Stream a (possibly very large) remote CSV/TXT as a Table without holding
    the whole body in memory. Header is read first to fix the signature."""
    client = get_client()

    # peek header + a sample for delimiter sniffing
    with client.stream("GET", url, timeout=(10.0, 300.0)) as resp:
        resp.raise_for_status()
        sample = b""
        for chunk in resp.iter_bytes(chunk_size=65536):
            sample += chunk
            if len(sample) >= 16384 or b"\n" in sample:
                if sample.count(b"\n") >= 1 and len(sample) >= 16384:
                    break
                if len(sample) >= 65536:
                    break
    text_sample = _decode(sample)
    delim = _sniff_delimiter(text_sample[:8192])
    header_line = text_sample.splitlines()[0] if text_sample else ""
    cols = _sanitize_cols(next(csv.reader(io.StringIO(header_line), delimiter=delim)))

    def rows():
        with client.stream("GET", url, timeout=(10.0, 600.0)) as resp:
            resp.raise_for_status()
            buf = ""
            first = True
            for chunk in resp.iter_bytes(chunk_size=1 << 20):
                buf += chunk.decode("utf-8", errors="replace")
                lines = buf.split("\n")
                buf = lines.pop()  # keep partial last line
                for line in lines:
                    if first:  # skip header
                        first = False
                        continue
                    line = line.rstrip("\r")
                    if not line:
                        continue
                    rec = next(csv.reader(io.StringIO(line), delimiter=delim), [])
                    yield {cols[i]: (rec[i] if i < len(rec) else None)
                           for i in range(len(cols))}
            if buf.strip() and not first:
                rec = next(csv.reader(io.StringIO(buf), delimiter=delim), [])
                yield {cols[i]: (rec[i] if i < len(rec) else None)
                       for i in range(len(cols))}

    return Table(cols, source_resource, source_file, rows())


def _expand_resource(res):
    """Yield Table objects for one CKAN resource."""
    fmt = (res.get("format") or "").upper()
    url = res.get("url")
    rname = res.get("name") or res.get("id") or "resource"
    if not url or fmt not in _TABULAR_FORMATS:
        return []
    size = res.get("size") or 0
    try:
        size = int(size)
    except (TypeError, ValueError):
        size = 0

    if fmt in _CSV_LIKE:
        # stream CSV/TXT directly (handles the 1.5GB file); never capped
        return [_stream_csv_table(url, rname, url.rsplit("/", 1)[-1])]

    if size and size > _MAX_INMEM_BYTES:
        print(f"[{rname}] skipping {fmt} resource ~{size}B (> in-mem cap)")
        return []
    content = _download_bytes(url)
    if len(content) > _MAX_INMEM_BYTES:
        print(f"[{rname}] skipping {fmt} resource {len(content)}B (> in-mem cap)")
        return []
    if fmt in _EXCEL_LIKE:
        return _excel_tables(content, rname, fmt)
    if fmt == "JSON":
        t = _json_table(content, rname, url.rsplit("/", 1)[-1])
        return [t] if t else []
    return []


def _norm_sig(columns):
    """Signature for grouping: case/space-insensitive column set order."""
    return tuple(c.strip().lower() for c in columns)


def fetch_one(node_id: str) -> None:
    _ensure_http()
    pkg = SLUG_TO_PKG[node_id]
    asset = node_id

    result = _api("package_show", id=pkg)
    resources = result.get("resources", []) or []

    tables = []
    for res in resources:
        try:
            tables.extend(t for t in _expand_resource(res) if t is not None)
        except Exception as e:  # noqa: BLE001 - one bad resource must not sink the package
            print(f"[{pkg}] resource {res.get('name')} expand failed: "
                  f"{type(e).__name__}: {e}")

    if not tables:
        raise RuntimeError(f"{pkg}: no tabular data extracted from "
                           f"{len(resources)} resources")

    # Group by normalized signature; pick the dominant group (most tables, then
    # most columns). Tables in a group share columns and concatenate cleanly.
    groups = {}
    for t in tables:
        groups.setdefault(_norm_sig(t.columns), []).append(t)
    dominant_sig = max(
        groups,
        key=lambda s: (len(groups[s]), len(s)),
    )
    chosen = groups[dominant_sig]
    columns = chosen[0].columns  # display names from the first table in the group

    if len(groups) > 1:
        dropped = sum(len(v) for k, v in groups.items() if k != dominant_sig)
        print(f"[{pkg}] {len(groups)} schema groups; publishing dominant "
              f"({len(chosen)} tables, {len(columns)} cols), dropping {dropped} "
              f"off-schema tables")

    schema = pa.schema(
        [("source_resource", pa.string()), ("source_file", pa.string())]
        + [(c, pa.string()) for c in columns]
    )

    total = 0
    with raw_parquet_writer(asset, schema) as writer:
        batch = {name: [] for name in schema.names}
        n = 0
        for t in chosen:
            for row in t.rows_iter:
                batch["source_resource"].append(t.source_resource)
                batch["source_file"].append(t.source_file)
                for c in columns:
                    v = row.get(c)
                    batch[c].append(None if v is None else str(v))
                n += 1
                total += 1
                if n >= _BATCH_ROWS:
                    writer.write_table(pa.table(batch, schema=schema))
                    batch = {name: [] for name in schema.names}
                    n = 0
        if n:
            writer.write_table(pa.table(batch, schema=schema))

    if total == 0:
        raise RuntimeError(f"{pkg}: dominant schema group produced 0 rows")
    print(f"[{pkg}] wrote {total} rows, {len(columns)} cols")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
