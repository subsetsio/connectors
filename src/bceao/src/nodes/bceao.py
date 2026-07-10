"""BCEAO EDEN connector — economic & financial time series for the WAEMU/UEMOA zone.

Source: https://edenpub.bceao.int (a legacy PHP/AJAX app, reverse-engineered).
There is no documented API; we drive the same POST endpoints the web UI uses:

  - secteursDAO.php   (idSecteur=<S>)                         -> sub-sectors of a sector
  - variablesDAO.php  (idSousSecteur, idLocalite=;<C>, idFrequence) -> series tokens
  - exportRapport.php (paysUemoa, frequence, export=xcl, parametre=...) -> CSV data

A series fetch token is <LOC><CODE> where LOC is the 1-char country code repeated
3x (CCC=Burkina, AAA=Cote d'Ivoire, ZZZ=UEMOA aggregate, ...) and CODE is the
country-independent indicator code (e.g. SR1011A0BP). The export CSV is
semicolon-delimited, French locale (comma = decimal separator, '-' = missing),
one row per series with periods as columns (serie='l'); metadonnee=1 adds
UNITE/MAGNITUDE/SOURCE/TYPE/METHODE metadata columns.

We publish two tables:
  - bceao-values : long-format observations (one row per series x locality x period)
  - bceao-series : the indicator catalog (reference: code, label, sector, unit, ...)
  - bceao-predefined-tables : EDEN's curated predefined-table catalog

Strategy: stateless full re-pull each run (no incremental filter exists; the whole
corpus is a few thousand series and re-pulls in minutes). Period windows are
discovered from the source (index.php embeds the available-year list per frequency)
— never hardcoded.

Frequency scope: we fetch the four substantive frequencies A(annual), M(monthly),
T(quarterly) and J(daily). EDEN also exposes three rare/legacy frequencies —
S (semestrial, 1999-2010, discontinued), H (weekly) and D (ten-day) — which carry
only a handful of series and whose export period encoding is unstable; they are
intentionally excluded here and noted so the omission is explicit, not silent.

TLS: edenpub serves a certificate without its intermediate ("Thawte TLS RSA CA G1");
the chain fails default verification. We trust it properly (NOT verify=False) by
adding the public DigiCert intermediate to the CA bundle via SSL_CERT_FILE.
"""

import html
import os
import re
import tempfile
from datetime import date

import certifi
import pyarrow as pa
from subsets_utils import (
    NodeSpec, post, configure_http, transient_retry,
    raw_parquet_writer, save_raw_parquet,
)

BASE = "https://edenpub.bceao.int"

# Public DigiCert intermediate the server fails to send. Bundling it lets the
# default TLS verifier build a complete chain — no verification is disabled.
_THAWTE_INTERMEDIATE_PEM = """-----BEGIN CERTIFICATE-----
MIIEizCCA3OgAwIBAgIQCQ7oxd5b+mLSri/3CXxIVzANBgkqhkiG9w0BAQsFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBH
MjAeFw0xNzExMDIxMjI0MjVaFw0yNzExMDIxMjI0MjVaMF4xCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
b20xHTAbBgNVBAMTFFRoYXd0ZSBUTFMgUlNBIENBIEcxMIIBIjANBgkqhkiG9w0B
AQEFAAOCAQ8AMIIBCgKCAQEAxjngmPhVetC0b/ozbYJdzOBUA1sMog47030cAP+P
23ANUN8grXECL8NhDEF4F1R9tL0wY0mczHaR0a7lYanlxtwWo1s2uGnnyDs6mOCs
66ew2w3YETr6Tb14xgjpu1gGFtAeewaikO9Fud8hxGJTSwn8xeNkfKVWpD2L4vFN
36FNgxeilK6aE4ykgGAzNlokTp6hNOLAYpDySdLAPKzuJSQ7JCEZ6O+SDKywIdXL
oMTnpxuBKGSG88NWTo3CHCOGmQECia2yqdPDjgLqnEiYNjwQL8uMqj8rOvlMgviB
cHA7xty+7/uYLN6ZS7Vq1/F/lVhVOf5ej6jZdmB85szFbQIDAQABo4IBQDCCATww
HQYDVR0OBBYEFKWM/jLM6w8s1BnGCLgAJIhdw8W3MB8GA1UdIwQYMBaAFE4iVCAY
lebjbuYP+vq5Eu0GF485MA4GA1UdDwEB/wQEAwIBhjAdBgNVHSUEFjAUBggrBgEF
BQcDAQYIKwYBBQUHAwIwEgYDVR0TAQH/BAgwBgEB/wIBADA0BggrBgEFBQcBAQQo
MCYwJAYIKwYBBQUHMAGGGGh0dHA6Ly9vY3NwLmRpZ2ljZXJ0LmNvbTBCBgNVHR8E
OzA5MDegNaAzhjFodHRwOi8vY3JsMy5kaWdpY2VydC5jb20vRGlnaUNlcnRHbG9i
YWxSb290RzIuY3JsMD0GA1UdIAQ2MDQwMgYEVR0gADAqMCgGCCsGAQUFBwIBFhxo
dHRwczovL3d3dy5kaWdpY2VydC5jb20vQ1BTMA0GCSqGSIb3DQEBCwUAA4IBAQC6
km0KA4sTb2VYpEBm/uL2HL/pZX9B7L/hbJ4NcoBe7V56oCnt7aeIo8sMjCRWTCWZ
D1dY0+2KZOC1dKj8d1VXXAtnjytDDuPPf6/iow0mYQTO/GAg/MLyL6CDm3FzDB8V
tsH/aeMgP6pgD1XQqz+haDnfnJTKBuxhcpnx3Adbleue/QnPf1hHYa8L+Rv8Pi5U
h4V9FwHOfphdMXOxi14OqmsiTbc5cOs9/uukH+YVsuFdWTna6IVw1qh+tEtyH16R
vmi7pkqyZYULOPMIE7avrljVVBZuikwARtY8tCVV6Pp9l3VeagBqb2ffgqNJt3C0
TYNYQI+BXG1R1cABlold
-----END CERTIFICATE-----
"""

# 1-char country code (EDEN's own) -> name. Prefix = this letter x3.
COUNTRIES = {
    "B": "Benin", "C": "Burkina Faso", "A": "Cote d'Ivoire", "S": "Guinea-Bissau",
    "D": "Mali", "H": "Niger", "K": "Senegal", "T": "Togo", "Z": "UEMOA (aggregate)",
}
SECTORS = {
    "SR": "Secteur reel", "SF": "Secteur monetaire et financier",
    "FP": "Secteur des finances publiques", "SE": "Secteur exterieur",
    "SS": "Secteur social",
}
FREQUENCIES = {"A": "annual", "M": "monthly", "T": "quarterly", "J": "daily"}

# metadonnee=1 leading columns (everything after these is a period column).
_META_COLS = {
    "CODE", "LIBELLE", "UNITE DE MESURE", "MAGNITUDE", "SOURCE",
    "TYPE SERIE", "METHODE OBSERVATION",
}
_FR_MONTHS = {
    "JAN": 1, "FEV": 2, "MAR": 3, "AVR": 4, "MAI": 5, "JUN": 6,
    "JUL": 7, "AUG": 8, "AOU": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
}

_VALUES_SCHEMA = pa.schema([
    ("locality", pa.string()),
    ("country", pa.string()),
    ("frequency", pa.string()),
    ("series_code", pa.string()),
    ("label", pa.string()),
    ("sector", pa.string()),
    ("subsector", pa.string()),
    ("unit", pa.string()),
    ("magnitude", pa.string()),
    ("source", pa.string()),
    ("series_type", pa.string()),
    ("method", pa.string()),
    ("period", pa.string()),
    ("date", pa.date32()),
    ("value", pa.float64()),
])

_SERIES_SCHEMA = pa.schema([
    ("series_code", pa.string()),
    ("frequency", pa.string()),
    ("label", pa.string()),
    ("sector", pa.string()),
    ("subsector", pa.string()),
    ("unit", pa.string()),
    ("valuation", pa.string()),
    ("localities", pa.string()),
    ("locality_count", pa.int64()),
])

_PREDEFINED_TABLE_SCHEMA = pa.schema([
    ("table_id", pa.string()),
    ("frequency", pa.string()),
    ("label", pa.string()),
])

_OPTION_RE = re.compile(r"<option value='([A-Z0-9]+)'>\[[^\]]*\]\s*\[([^\]]*)\]\s*(?:\[([^\]]*)\])?")
_PREDEFINED_TABLE_RE = re.compile(r"soumettreTab\('([A-Z])','([0-9]+)','((?:\\'|[^'])*)'\)")
_SUBSECTOR_RE = re.compile(r"value='([A-Z]{2}[0-9]+)'[^>]*name='groupe_soussecteurs'")
_IDANNEE_RE = re.compile(r"case '([A-Z])'\s*:\s*idAnnee\s*=\s*'([^']*)'")


def _ensure_tls() -> None:
    """Make the default verifier trust edenpub by adding the missing
    intermediate to the CA bundle (idempotent; safe to call per fetch)."""
    if os.environ.get("_BCEAO_TLS_READY"):
        return
    bundle = certifi.contents() + "\n" + _THAWTE_INTERMEDIATE_PEM
    fh = tempfile.NamedTemporaryFile("w", suffix=".pem", prefix="bceao-ca-", delete=False)
    fh.write(bundle)
    fh.close()
    os.environ["SSL_CERT_FILE"] = fh.name
    os.environ["_BCEAO_TLS_READY"] = "1"
    configure_http()  # rebuild the shared client so it picks up the new bundle


@transient_retry()
def _dao(path: str, data: dict) -> str:
    resp = post(f"{BASE}/{path}", data=data, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.text


def _discover_year_ranges() -> dict:
    """Parse the per-frequency available-year list embedded in index.php JS."""
    html = _dao("index.php", {})
    ranges = {}
    for freq, arr in _IDANNEE_RE.findall(html):
        years = [int(y) for y in arr.split(";") if y.strip().isdigit()]
        if years:
            ranges[freq] = (min(years), max(years))
    return ranges


def _subsectors() -> dict:
    """Map every sub-sector id -> its parent sector id (scraped, not hardcoded)."""
    out = {}
    for sector in SECTORS:
        html = _dao("secteursDAO.php", {"idSecteur": sector})
        for sub in _SUBSECTOR_RE.findall(html):
            out[sub] = sector
    return out


def _tokens(subsector: str, country: str, freq: str) -> list:
    """[(token, label, unit)] for a (sub-sector, country, frequency)."""
    html = _dao("variablesDAO.php", {
        "idSousSecteur": subsector, "idLocalite": ";" + country, "idFrequence": freq,
    })
    rows = []
    for token, label, unit in _OPTION_RE.findall(html):
        rows.append((token, re.sub(r"\s+", " ", label).strip(), (unit or "").strip()))
    return rows


def _predefined_tables() -> list:
    """Scrape EDEN's curated predefined-table definitions from the index page."""
    html_text = _dao("index.php", {})
    rows = []
    seen = set()
    for freq, table_id, raw_label in _PREDEFINED_TABLE_RE.findall(html_text):
        label = html.unescape(raw_label.replace("\\'", "'"))
        label = re.sub(r"\s+", " ", label).strip()
        key = (table_id, freq)
        if key in seen:
            continue
        seen.add(key)
        rows.append({"table_id": table_id, "frequency": freq, "label": label})
    return rows


def _period_window(freq: str, y0: int, y1: int):
    if freq == "A":
        return (str(y0), str(y1))
    if freq == "M":
        return (f"1;{y0}", f"12;{y1}")
    if freq == "T":
        return (f"1;{y0}", f"4;{y1}")
    if freq == "J":
        return (f"1;1;{y0}", f"31;12;{y1}")
    raise ValueError(f"unsupported frequency {freq!r}")


def _export(country: str, freq: str, tokens: list, win) -> str:
    param = f"{freq}*{';'.join(tokens)}*{win[0]}*{win[1]}*1*l"
    resp = _export_post(country, freq, param)
    return resp


@transient_retry()
def _export_post(country: str, freq: str, param: str) -> str:
    resp = post(f"{BASE}/exportRapport.php", data={
        "paysUemoa": country, "frequence": freq, "export": "xcl", "parametre": param,
    }, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.text


def _parse_value(cell: str):
    s = cell.strip()
    if s == "-" or s == "" or s.upper() in ("ND", "NA"):
        return None
    s = s.replace("\xa0", "").replace(" ", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _period_to_date(freq: str, label: str):
    label = label.strip()
    if freq == "A":
        if re.fullmatch(r"\d{4}", label):
            return date(int(label), 1, 1)
    elif freq == "M":
        m = re.fullmatch(r"([A-Za-z]{3})(\d{4})", label)
        if m:
            mon = _FR_MONTHS.get(m.group(1).upper())
            if mon:
                return date(int(m.group(2)), mon, 1)
    elif freq == "T":
        m = re.fullmatch(r"Trim(\d)-(\d{4})", label)
        if m:
            q = int(m.group(1))
            if 1 <= q <= 4:
                return date(int(m.group(2)), (q - 1) * 3 + 1, 1)
    elif freq == "J":
        m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", label)
        if m:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    return None


def _parse_export(text: str):
    """Yield dicts {token, label, unit, magnitude, source, series_type, method,
    periods: [(period_label, raw_value)]} from one export CSV."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if len(lines) < 2:
        return
    header = [h.strip() for h in lines[1].split(";")]
    # period columns = header positions whose name is not a known metadata label
    period_idx = [(i, h) for i, h in enumerate(header) if h and h not in _META_COLS]
    try:
        i_code = header.index("CODE")
        i_lib = header.index("LIBELLE")
    except ValueError:
        return
    i_unit = header.index("UNITE DE MESURE") if "UNITE DE MESURE" in header else None
    i_mag = header.index("MAGNITUDE") if "MAGNITUDE" in header else None
    i_src = header.index("SOURCE") if "SOURCE" in header else None
    i_typ = header.index("TYPE SERIE") if "TYPE SERIE" in header else None
    i_met = header.index("METHODE OBSERVATION") if "METHODE OBSERVATION" in header else None
    for line in lines[2:]:
        if not line.strip():
            continue
        cells = line.split(";")
        if len(cells) <= i_code:
            continue
        token = cells[i_code].strip()
        if not token:
            continue

        def g(idx):
            return cells[idx].strip() if idx is not None and idx < len(cells) else ""

        yield {
            "token": token,
            "label": g(i_lib),
            "unit": g(i_unit),
            "magnitude": g(i_mag),
            "source": g(i_src),
            "series_type": g(i_typ),
            "method": g(i_met),
            "periods": [(h, cells[i]) for i, h in period_idx if i < len(cells)],
        }


def _chunk(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


# Per-frequency export batch sizes (smaller for wide period windows / large CSVs).
_CHUNK = {"A": 60, "M": 35, "T": 40, "J": 8}
_FLUSH_ROWS = 100_000


def fetch_values(node_id: str) -> None:
    asset = node_id
    _ensure_tls()
    sub_to_sector = _subsectors()
    year_ranges = _discover_year_ranges()

    buf = []
    total = 0
    with raw_parquet_writer(asset, _VALUES_SCHEMA) as writer:
        def flush():
            nonlocal buf
            if buf:
                writer.write_table(pa.Table.from_pylist(buf, schema=_VALUES_SCHEMA))
                buf = []

        for country, country_name in COUNTRIES.items():
            for freq in FREQUENCIES:
                if freq not in year_ranges:
                    continue
                # collect this (country, freq)'s tokens across all sub-sectors
                tok_meta = {}  # token -> (subsector, label, unit)
                for sub, sector in sub_to_sector.items():
                    for token, label, unit in _tokens(sub, country, freq):
                        tok_meta[token] = (sub, label, unit)
                if not tok_meta:
                    continue
                y0, y1 = year_ranges[freq]
                win = _period_window(freq, y0, y1)
                for batch in _chunk(list(tok_meta), _CHUNK[freq]):
                    csv = _export(country, freq, batch, win)
                    for rec in _parse_export(csv):
                        token = rec["token"]
                        code = token[3:] if len(token) > 3 else token
                        sub = code[:3]
                        sector = code[:2]
                        for plabel, raw in rec["periods"]:
                            val = _parse_value(raw)
                            if val is None:
                                continue
                            d = _period_to_date(freq, plabel)
                            if d is None:
                                continue
                            buf.append({
                                "locality": token[0],
                                "country": country_name,
                                "frequency": freq,
                                "series_code": code,
                                "label": rec["label"],
                                "sector": sector,
                                "subsector": sub,
                                "unit": rec["unit"],
                                "magnitude": rec["magnitude"],
                                "source": rec["source"],
                                "series_type": rec["series_type"],
                                "method": rec["method"],
                                "period": plabel,
                                "date": d,
                                "value": val,
                            })
                            total += 1
                    if len(buf) >= _FLUSH_ROWS:
                        flush()
        flush()
    if total == 0:
        raise AssertionError("bceao-values produced 0 observations — export shape changed?")
    print(f"  bceao-values: wrote {total} observations")


def fetch_series(node_id: str) -> None:
    asset = node_id
    _ensure_tls()
    sub_to_sector = _subsectors()
    # (series_code, freq) -> {label, sector, subsector, unit, localities:set}
    catalog = {}
    for country in COUNTRIES:
        for freq in FREQUENCIES:
            for sub, sector in sub_to_sector.items():
                for token, label, unit in _tokens(sub, country, freq):
                    code = token[3:] if len(token) > 3 else token
                    key = (code, freq)
                    rec = catalog.get(key)
                    if rec is None:
                        rec = {
                            "label": label, "sector": code[:2], "subsector": code[:3],
                            "unit": unit, "localities": set(),
                        }
                        catalog[key] = rec
                    rec["localities"].add(token[0])
                    if not rec["label"] and label:
                        rec["label"] = label

    rows = []
    for (code, freq), rec in catalog.items():
        locs = sorted(rec["localities"])
        rows.append({
            "series_code": code,
            "frequency": freq,
            "label": rec["label"],
            "sector": rec["sector"],
            "subsector": rec["subsector"],
            "unit": rec["unit"],
            "valuation": code[-2:] if len(code) >= 2 else "",
            "localities": ",".join(locs),
            "locality_count": len(locs),
        })
    if not rows:
        raise AssertionError("bceao-series produced 0 series — catalog scrape changed?")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_SERIES_SCHEMA), asset)
    print(f"  bceao-series: wrote {len(rows)} (series, frequency) rows")


def fetch_predefined_tables(node_id: str) -> None:
    _ensure_tls()
    rows = _predefined_tables()
    if not rows:
        raise AssertionError("bceao-predefined-tables produced 0 rows - table scrape changed?")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_PREDEFINED_TABLE_SCHEMA), node_id)
    print(f"  bceao-predefined-tables: wrote {len(rows)} predefined table rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="bceao-predefined-tables", fn=fetch_predefined_tables, kind="download"),
    NodeSpec(id="bceao-series", fn=fetch_series, kind="download"),
    NodeSpec(id="bceao-values", fn=fetch_values, kind="download"),
]
