"""Banco de Espana - bulk CSV/ZIP time-series connector.

Mechanism: bulk_csv_zip (the highest-suitability mechanism from research).
Each publication exposes one ZIP under
https://www.bde.es/webbe/es/estadisticas/compartido/datos/zip/<pub>.zip
containing many wide "table" CSVs (latin-1 / ISO-8859-1 encoded). Each table
CSV groups a set of related time series: a few metadata header rows (some mix
of series code, sequential number, alias, description, units, frequency;
older tables carry a reduced, partly unlabelled header) followed by
observation rows keyed by a Spanish period label (daily "DD MMM YYYY" or the
older spaceless "DD MMMYYYY", monthly/quarterly/semestral "MMM YYYY", annual
"YYYY"); "_" marks a missing observation.

One DOWNLOAD_SPEC per rank-active table file (the entity union). The catalogue's
value-file names do NOT map cleanly to the ZIP member names (e.g. catalogue
"BE230A" is member "be23a.csv", and same-named members can collide), so the
entity_id -> real ZIP member is resolved offline by matching each table's series
alias against the ZIP contents and embedded here as ENTITY_FILE. Each fetch
pulls its publication ZIP (cached per-runner in the OS temp dir so the shared
archive is not re-downloaded once per table), extracts its member, and reshapes
the wide matrix into long format (one row per series x period with a real value).
Stateless full re-pull: the ZIPs are small, the source exposes no incremental
filter, and re-fetching picks up revisions for free. One thin SQL TRANSFORM per
table publishes the long Delta table.
"""
import csv
import datetime
import io
import math
import os
import re
import tempfile
import unicodedata
import zipfile

import httpx
import pyarrow as pa
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, get, save_raw_parquet

SLUG = "banco-de-espana"
_ZIP_BASE = "https://www.bde.es/webbe/es/estadisticas/compartido/datos/zip/"
# Transient per-runner cache for the shared publication ZIPs. NOT the raw data
# layer (that goes through subsets_utils); just avoids re-pulling a ~9 MB archive
# once per table file. /tmp is fresh on every cloud run, so it never goes stale.
_CACHE_DIR = os.path.join(tempfile.gettempdir(), "bde_zip_cache")

_PUBS = ("be", "si", "ti", "tc", "pb")

_MONTHS = {
    "ENE": 1, "FEB": 2, "MAR": 3, "ABR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AGO": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DIC": 12,
}

# First column of a metadata header row -> long-format field (accent-stripped,
# upper-cased before lookup). A row whose first cell parses as a period label
# marks the start of observations; an unlabelled header row is the series
# identifier (older tables omit the "CODIGO/ALIAS DE LA SERIE" label).
_META_LABELS = {
    "CODIGO DE LA SERIE": "series_code",
    "NOMBRE DE LA SERIE": "series_code",
    "ALIAS DE LA SERIE": "alias",
    "DESCRIPCION DE LA SERIE": "description",
    "DESCRIPCION DE LAS UNIDADES": "units",
    "FRECUENCIA": "frequency",
    "NUMERO SECUENCIAL": "_skip",
}

_MISSING = {"", "_", "...", ".", "ND", "N/A", "NA", "NAN", "S/E"}

_RE_DMY = re.compile(r"^(\d{1,2})\s+([A-Z]{3})\s*(\d{4})$")
_RE_MY = re.compile(r"^([A-Z]{3})\s*(\d{4})$")
_RE_Y = re.compile(r"^(\d{4})$")

RAW_SCHEMA = pa.schema([
    ("series_code", pa.string()),
    ("alias", pa.string()),
    ("description", pa.string()),
    ("units", pa.string()),
    ("frequency", pa.string()),
    ("period_label", pa.string()),
    ("date", pa.date32()),
    ("value", pa.float64()),
])

_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError,
    httpx.ProxyError,
)


def _is_transient(exc):
    if isinstance(exc, _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _download_zip(pub):
    resp = get(_ZIP_BASE + pub + ".zip", timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _zip_bytes(pub):
    """Return the publication ZIP bytes, caching to a per-runner temp file."""
    os.makedirs(_CACHE_DIR, exist_ok=True)
    path = os.path.join(_CACHE_DIR, pub + ".zip")
    try:
        if os.path.getsize(path) > 0:
            with open(path, "rb") as fh:
                return fh.read()
    except OSError:
        pass
    data = _download_zip(pub)
    tmp = path + "." + str(os.getpid()) + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, path)  # atomic publish into the cache
    return data


def _norm(text):
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return stripped.strip().upper()


def _parse_period(label):
    s = _norm(label)
    m = _RE_DMY.match(s)
    if m:
        month = _MONTHS.get(m.group(2))
        if month:
            try:
                return datetime.date(int(m.group(3)), month, int(m.group(1)))
            except ValueError:
                return None
    m = _RE_MY.match(s)
    if m:
        month = _MONTHS.get(m.group(1))
        if month:
            return datetime.date(int(m.group(2)), month, 1)
    m = _RE_Y.match(s)
    if m:
        return datetime.date(int(m.group(1)), 1, 1)
    return None


def _parse_value(cell):
    text = cell.strip()
    if text.upper() in _MISSING:
        return None
    try:
        value = float(text)
    except ValueError:
        try:
            value = float(text.replace(",", "."))
        except ValueError:
            return None
    if math.isnan(value) or math.isinf(value):
        return None
    return value


def _pub_of(entity_id):
    for pub in _PUBS:
        if entity_id.startswith(pub):
            return pub
    raise ValueError("cannot determine publication for entity " + repr(entity_id))


def fetch_one(node_id):
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len(SLUG) + 1:].replace("-", "_")
    member = ENTITY_FILE.get(entity_id)
    if member is None:
        raise KeyError(node_id + ": no ZIP member mapped for " + entity_id)
    pub = _pub_of(entity_id)

    with zipfile.ZipFile(io.BytesIO(_zip_bytes(pub))) as zf:
        names = {n.lower(): n for n in zf.namelist()}
        real = names.get(member.lower())
        if real is None:
            raise FileNotFoundError(
                node_id + ": " + member + " not found in " + pub + ".zip"
            )
        raw_text = zf.read(real).decode("latin-1")

    rows = list(csv.reader(io.StringIO(raw_text)))

    # Observations start at the first row whose first cell parses as a period.
    obs_start = None
    for i, row in enumerate(rows):
        if row and len(row) >= 2 and _parse_period(row[0]) is not None:
            obs_start = i
            break
    if obs_start is None:
        raise ValueError(node_id + ": no observation rows found")

    header = rows[:obs_start]
    ncols = max((len(r) - 1 for r in header), default=0)
    if ncols <= 0:
        raise ValueError(node_id + ": no data columns in header")

    cols_meta = [dict() for _ in range(ncols)]
    for row in header:
        if not row:
            continue
        field = _META_LABELS.get(_norm(row[0]))
        if field is None:
            # Unlabelled identifier row (older tables): use as alias if we have
            # not already captured one; otherwise ignore.
            if any("alias" in c for c in cols_meta):
                continue
            field = "alias"
        if field == "_skip":
            continue
        for j in range(ncols):
            cols_meta[j][field] = row[1 + j].strip() if 1 + j < len(row) else ""

    series_code, alias, description, units, frequency = [], [], [], [], []
    period_label, date_col, value_col = [], [], []
    for row in rows[obs_start:]:
        if not row:
            continue
        label = row[0].strip()
        if not label:
            continue
        parsed_date = _parse_period(label)
        for j in range(ncols):
            cell = row[1 + j] if 1 + j < len(row) else ""
            value = _parse_value(cell)
            if value is None:  # drop missing observations; keeps raw compact
                continue
            meta = cols_meta[j]
            code = meta.get("series_code") or meta.get("alias")
            series_code.append(code or None)
            alias.append(meta.get("alias") or None)
            description.append(meta.get("description") or None)
            units.append(meta.get("units") or None)
            frequency.append(meta.get("frequency") or None)
            period_label.append(label)
            date_col.append(parsed_date)
            value_col.append(value)

    table = pa.table(
        {
            "series_code": series_code,
            "alias": alias,
            "description": description,
            "units": units,
            "frequency": frequency,
            "period_label": period_label,
            "date": date_col,
            "value": value_col,
        },
        schema=RAW_SCHEMA,
    )
    save_raw_parquet(table, asset)


# entity_id -> real ZIP member, resolved offline by matching each table's series
# alias against the publication ZIP contents (the catalogue value-file names are
# not reliable member names). Keys are exactly the rank-active entity union.
ENTITY_FILE = {
    'be0101': 'be0101.csv',
    'be0103': 'be0103.csv',
    'be0104': 'be0104.csv',
    'be0105': 'be0105.csv',
    'be0106': 'be0106.csv',
    'be0107': 'be0107.csv',
    'be0110': 'be0110.csv',
    'be0111': 'be0111.csv',
    'be0112': 'be0112.csv',
    'be0113': 'be0113.csv',
    'be0114': 'be0114.csv',
    'be0115': 'be0115.csv',
    'be0116': 'be0116.csv',
    'be012a': 'be012a.csv',
    'be012b': 'be012b.csv',
    'be0199': 'be0199.csv',
    'be0201': 'be0201.csv',
    'be0202': 'be0202.csv',
    'be0203': 'be0203.csv',
    'be0204': 'be0204.csv',
    'be0205': 'be0205.csv',
    'be0206': 'be0206.csv',
    'be0207': 'be0207.csv',
    'be0209': 'be0209.csv',
    'be0210': 'be0210.csv',
    'be0211': 'be0211.csv',
    'be0301': 'be0301.csv',
    'be0302': 'be0302.csv',
    'be0303': 'be0303.csv',
    'be0304': 'be0304.csv',
    'be0305': 'be0305.csv',
    'be0306': 'be0306.csv',
    'be0307': 'be0307.csv',
    'be0308': 'be0308.csv',
    'be0309': 'be0309.csv',
    'be0310': 'be0310.csv',
    'be0311': 'be0311.csv',
    'be0312': 'be0312.csv',
    'be0313': 'be0313.csv',
    'be0314': 'be0314.csv',
    'be0315': 'be0315.csv',
    'be0316': 'be0316.csv',
    'be0317': 'be0317.csv',
    'be0318': 'be0318.csv',
    'be0319': 'be0319.csv',
    'be0320': 'be0320.csv',
    'be0321': 'be0321.csv',
    'be0322': 'be0322.csv',
    'be0401': 'be0401.csv',
    'be0402': 'be0402.csv',
    'be0403': 'be0403.csv',
    'be0404': 'be0404.csv',
    'be0405': 'be0405.csv',
    'be0406': 'be0406.csv',
    'be0407': 'be0407.csv',
    'be0408': 'be0408.csv',
    'be0409': 'be0409.csv',
    'be040a': 'be04a.csv',
    'be040c': 'be04c.csv',
    'be0410': 'be0410.csv',
    'be0411': 'be0411.csv',
    'be0412': 'be0412.csv',
    'be0413': 'be0413.csv',
    'be0414': 'be0414.csv',
    'be0417': 'be0417.csv',
    'be0418': 'be0418.csv',
    'be0419': 'be0419.csv',
    'be0422': 'be0422.csv',
    'be0423': 'be0423.csv',
    'be0424': 'be0424.csv',
    'be0427': 'be0427.csv',
    'be0428': 'be0428.csv',
    'be0429': 'be0429.csv',
    'be0430': 'be0430.csv',
    'be0431': 'be0431.csv',
    'be0432': 'be0432.csv',
    'be0436': 'be0436.csv',
    'be0437': 'be0437.csv',
    'be0438': 'be0438.csv',
    'be0439': 'be0439.csv',
    'be0440': 'be0440.csv',
    'be0441': 'be0441.csv',
    'be0445': 'be0445.csv',
    'be0446': 'be0446.csv',
    'be0447': 'be0447.csv',
    'be0448': 'be0448.csv',
    'be0449': 'be0449.csv',
    'be0451': 'be0451.csv',
    'be0452': 'be0452.csv',
    'be0453': 'be0453.csv',
    'be0454': 'be0454.csv',
    'be0455': 'be0455.csv',
    'be0456': 'be0456.csv',
    'be0457': 'be0457.csv',
    'be0458': 'be0458.csv',
    'be0481': 'be0481.csv',
    'be0482': 'be0482.csv',
    'be0483': 'be0483.csv',
    'be0484': 'be0484.csv',
    'be0485': 'be0485.csv',
    'be0486': 'be0486.csv',
    'be0499': 'be0499.csv',
    'be0601': 'be0601.csv',
    'be0602': 'be0602.csv',
    'be0603': 'be0603.csv',
    'be0604': 'be0604.csv',
    'be0605': 'be0605.csv',
    'be0606': 'be0606.csv',
    'be0607': 'be0607.csv',
    'be0608': 'be0608.csv',
    'be0609': 'be0609.csv',
    'be0610': 'be0610.csv',
    'be0611': 'be0611.csv',
    'be0612': 'be0612.csv',
    'be0701': 'be0701.csv',
    'be0702': 'be0702.csv',
    'be0703': 'be0703.csv',
    'be0704': 'be0704.csv',
    'be0705': 'be0705.csv',
    'be0706': 'be0706.csv',
    'be0707': 'be0707.csv',
    'be0708': 'be0708.csv',
    'be0709': 'be0709.csv',
    'be070a': 'be07a.csv',
    'be0710': 'be0710.csv',
    'be0711': 'be0711.csv',
    'be0712': 'be0712.csv',
    'be0716': 'be0716.csv',
    'be0717': 'be0717.csv',
    'be0718': 'be0718.csv',
    'be0719': 'be0719.csv',
    'be0801': 'be0801.csv',
    'be0802': 'be0802.csv',
    'be0803': 'be0803.csv',
    'be0804': 'be0804.csv',
    'be0805': 'be0805.csv',
    'be0806': 'be0806.csv',
    'be0807': 'be0807.csv',
    'be0808': 'be0808.csv',
    'be0809': 'be0809.csv',
    'be080a': 'be08a.csv',
    'be080c': 'be08c.csv',
    'be0810': 'be0810.csv',
    'be0811': 'be0811.csv',
    'be0812': 'be0812.csv',
    'be0813': 'be0813.csv',
    'be0814': 'be0814.csv',
    'be0815': 'be0815.csv',
    'be0816': 'be0816.csv',
    'be0817': 'be0817.csv',
    'be0818': 'be0818.csv',
    'be0819': 'be0819.csv',
    'be0820': 'be0820.csv',
    'be0821': 'be0821.csv',
    'be0822': 'be0822.csv',
    'be0823': 'be0823.csv',
    'be0824': 'be0824.csv',
    'be0825': 'be0825.csv',
    'be0831': 'be0831.csv',
    'be0832': 'be0832.csv',
    'be0833': 'be0833.csv',
    'be0834': 'be0834.csv',
    'be0835': 'be0835.csv',
    'be0841': 'be0841.csv',
    'be0842': 'be0842.csv',
    'be0843': 'be0843.csv',
    'be0844': 'be0844.csv',
    'be0845': 'be0845.csv',
    'be0851': 'be0851.csv',
    'be0852': 'be0852.csv',
    'be0853': 'be0853.csv',
    'be0854': 'be0854.csv',
    'be0891': 'be0891.csv',
    'be0892': 'be0892.csv',
    'be0901': 'be0901.csv',
    'be0902': 'be0902.csv',
    'be0904': 'be0904.csv',
    'be0905': 'be0905.csv',
    'be0910': 'be0910.csv',
    'be0911': 'be0911.csv',
    'be0912': 'be0912.csv',
    'be0913': 'be0913.csv',
    'be0914': 'be0914.csv',
    'be0915': 'be0915a.csv',
    'be0916': 'be0916a.csv',
    'be0921': 'be0921.csv',
    'be0922': 'be0922.csv',
    'be0923': 'be0923.csv',
    'be0924': 'be0924.csv',
    'be0925': 'be0925.csv',
    'be0926': 'be0926.csv',
    'be0927': 'be0927.csv',
    'be0930': 'be0930.csv',
    'be0931': 'be0931.csv',
    'be0932': 'be0932.csv',
    'be0933': 'be0933.csv',
    'be0934': 'be0934.csv',
    'be0935': 'be0935.csv',
    'be0936': 'be0936.csv',
    'be0937': 'be0937.csv',
    'be0938': 'be0938.csv',
    'be0939': 'be0939.csv',
    'be0940': 'be0940.csv',
    'be0941': 'be0941.csv',
    'be0942': 'be0942.csv',
    'be0943': 'be0943.csv',
    'be1101': 'be1101.csv',
    'be1102': 'be1102.csv',
    'be1103': 'be1103.csv',
    'be1104': 'be1104.csv',
    'be1105': 'be1105.csv',
    'be1106': 'be1106.csv',
    'be1107': 'be1107.csv',
    'be1108': 'be1108.csv',
    'be1109': 'be1109.csv',
    'be110a': 'be11a.csv',
    'be110b': 'be11b.csv',
    'be1110': 'be1110.csv',
    'be1111': 'be1111.csv',
    'be1112': 'be1112.csv',
    'be1113': 'be1113.csv',
    'be1114': 'be1114.csv',
    'be1115': 'be1115.csv',
    'be1116': 'be1116.csv',
    'be1201': 'be1201.csv',
    'be1202': 'be1202.csv',
    'be1203': 'be1203.csv',
    'be1204': 'be1204.csv',
    'be1205': 'be1205.csv',
    'be1206': 'be1206.csv',
    'be1207': 'be1207.csv',
    'be1208': 'be1208.csv',
    'be1209': 'be1209.csv',
    'be120a': 'be12a.csv',
    'be120b': 'be12b.csv',
    'be120c': 'be12c.csv',
    'be1210': 'be1210.csv',
    'be1211': 'be1211.csv',
    'be1212': 'be1212.csv',
    'be1213': 'be1213.csv',
    'be1214': 'be1214.csv',
    'be1215': 'be1215.csv',
    'be1216': 'be1216.csv',
    'be1301': 'be1301.csv',
    'be1302': 'be1302.csv',
    'be1303': 'be1303.csv',
    'be1304': 'be1304.csv',
    'be1305': 'be1305.csv',
    'be1306': 'be1306.csv',
    'be1307': 'be1307.csv',
    'be1308': 'be1308.csv',
    'be1309': 'be1309.csv',
    'be130a': 'be13a.csv',
    'be1310': 'be1310.csv',
    'be1311': 'be1311.csv',
    'be1312': 'be1312.csv',
    'be1401': 'be1401.csv',
    'be1402': 'be1402.csv',
    'be1403': 'be1403.csv',
    'be1404': 'be1404.csv',
    'be1405': 'be1405.csv',
    'be1406': 'be1406.csv',
    'be1407': 'be1407.csv',
    'be1408': 'be1408.csv',
    'be1409': 'be1409.csv',
    'be1501': 'be1501.csv',
    'be1502': 'be1502.csv',
    'be1503': 'be1503.csv',
    'be1504': 'be1504.csv',
    'be1505': 'be1505.csv',
    'be1506': 'be1506.csv',
    'be1507': 'be1507.csv',
    'be1508': 'be1508.csv',
    'be1509': 'be1509.csv',
    'be150a': 'be15a.csv',
    'be150b': 'be15b.csv',
    'be150c': 'be15c.csv',
    'be1510': 'be1510.csv',
    'be1511': 'be1511.csv',
    'be1512': 'be1512.csv',
    'be1513': 'be1513.csv',
    'be1514': 'be1514.csv',
    'be1515': 'be1515.csv',
    'be1516': 'be1516.csv',
    'be1517': 'be1517.csv',
    'be1518': 'be1518.csv',
    'be1519': 'be1519.csv',
    'be1520': 'be1520.csv',
    'be1521': 'be1521.csv',
    'be1522': 'be1522.csv',
    'be1523': 'be1523.csv',
    'be1524': 'be1524.csv',
    'be1525': 'be1525.csv',
    'be1526': 'be1526.csv',
    'be1527': 'be1527.csv',
    'be1528': 'be1528.csv',
    'be1529': 'be1529.csv',
    'be1530': 'be1530.csv',
    'be1601': 'be1601.csv',
    'be1602': 'be1602.csv',
    'be1603': 'be1603.csv',
    'be1604': 'be1604.csv',
    'be1605': 'be1605.csv',
    'be1606': 'be1606.csv',
    'be1607': 'be1607.csv',
    'be1608': 'be1608.csv',
    'be1609': 'be1609.csv',
    'be1701': 'be1701.csv',
    'be1702': 'be1702.csv',
    'be1703': 'be1703.csv',
    'be1704': 'be1704.csv',
    'be1705': 'be1705.csv',
    'be1706': 'be1706.csv',
    'be1707': 'be1707.csv',
    'be1708': 'be1708.csv',
    'be1709': 'be1709.csv',
    'be1710': 'be1710.csv',
    'be1711': 'be1711.csv',
    'be1712': 'be1712.csv',
    'be1713': 'be1713.csv',
    'be1714': 'be1714.csv',
    'be1715': 'be1715.csv',
    'be1716': 'be1716.csv',
    'be1721': 'be1721.csv',
    'be1722': 'be1722.csv',
    'be1723': 'be1723.csv',
    'be1724': 'be1724.csv',
    'be1725': 'be1725.csv',
    'be1726': 'be1726.csv',
    'be1727': 'be1727.csv',
    'be1728': 'be1728.csv',
    'be1729': 'be1729.csv',
    'be172a': 'be172a.csv',
    'be1730': 'be1730.csv',
    'be1731': 'be1731.csv',
    'be1732': 'be1732.csv',
    'be173a': 'be173a.csv',
    'be1740': 'be1740.csv',
    'be1741': 'be1741.csv',
    'be1742': 'be1742.csv',
    'be1743': 'be1743.csv',
    'be1744': 'be1744a.csv',
    'be1745': 'be1745.csv',
    'be174a': 'be174a.csv',
    'be174b': 'be174b.csv',
    'be174c': 'be174c.csv',
    'be174d': 'be174d.csv',
    'be174e': 'be174e.csv',
    'be174f': 'be174f.csv',
    'be175a': 'be175a.csv',
    'be176a': 'be176a.csv',
    'be1801': 'be1801.csv',
    'be1802': 'be1802.csv',
    'be1803': 'be1803.csv',
    'be1804': 'be1804.csv',
    'be1805': 'be1805.csv',
    'be1806': 'be1806.csv',
    'be1807': 'be1807.csv',
    'be1901': 'be1901.csv',
    'be1902': 'be1902.csv',
    'be1903': 'be1903.csv',
    'be1904': 'be1904.csv',
    'be1905': 'be1905.csv',
    'be1906': 'be1906.csv',
    'be1907': 'be1907.csv',
    'be1908': 'be1908.csv',
    'be1909': 'be1909.csv',
    'be1910': 'be1910.csv',
    'be1911': 'be1911.csv',
    'be1912': 'be1912.csv',
    'be1913': 'be1913.csv',
    'be1914': 'be1914.csv',
    'be1915': 'be1915.csv',
    'be1916': 'be1916.csv',
    'be1917': 'be1917.csv',
    'be2001': 'be2001.csv',
    'be2002': 'be2002.csv',
    'be2003': 'be2003.csv',
    'be2004': 'be2004.csv',
    'be2005': 'be2005.csv',
    'be2006': 'be2006.csv',
    'be2007': 'be2007.csv',
    'be2008': 'be2008.csv',
    'be2101': 'be2101.csv',
    'be2102': 'be2102.csv',
    'be2103': 'be2103.csv',
    'be2106': 'be2106.csv',
    'be2107': 'be2107.csv',
    'be2108': 'be2108.csv',
    'be2109': 'be2109.csv',
    'be2110': 'be2110.csv',
    'be2111': 'be2111.csv',
    'be2112': 'be2112.csv',
    'be2113': 'be2113.csv',
    'be2114': 'be2114.csv',
    'be2115': 'be2115.csv',
    'be2116': 'be2116.csv',
    'be2117': 'be2117.csv',
    'be2118': 'be2118.csv',
    'be2119': 'be2119.csv',
    'be2120': 'be2120.csv',
    'be2121': 'be2121.csv',
    'be2122': 'be2122.csv',
    'be2123': 'be2123.csv',
    'be2124': 'be2124.csv',
    'be2125': 'be2125.csv',
    'be2126': 'be2126.csv',
    'be2127': 'be2127.csv',
    'be2128': 'be2128.csv',
    'be2134': 'be2134.csv',
    'be2135': 'be2135.csv',
    'be2201': 'be2201.csv',
    'be2202': 'be2202.csv',
    'be2203': 'be2203.csv',
    'be2204': 'be2204.csv',
    'be2205': 'be2205.csv',
    'be2206': 'be2206.csv',
    'be2207': 'be2207.csv',
    'be2208': 'be2208.csv',
    'be2222': 'be2222.csv',
    'be2223': 'be2223.csv',
    'be2224': 'be2224.csv',
    'be2225': 'be2225.csv',
    'be2226': 'be2226.csv',
    'be2227': 'be2227.csv',
    'be2230': 'be2230.csv',
    'be2231': 'be2231.csv',
    'be2232': 'be2232.csv',
    'be2233': 'be2233.csv',
    'be2234': 'be2234.csv',
    'be2241': 'be2241.csv',
    'be2242': 'be2242.csv',
    'be2243': 'be2243.csv',
    'be2244': 'be2244.csv',
    'be2301': 'be2301.csv',
    'be2302': 'be2302.csv',
    'be2303': 'be2303.csv',
    'be2304': 'be2304.csv',
    'be2306': 'be2306.csv',
    'be2308': 'be2308.csv',
    'be2309': 'be2309.csv',
    'be230a': 'be23a.csv',
    'be230b': 'be23b.csv',
    'be230c': 'be23c.csv',
    'be230d': 'be23d.csv',
    'be230e': 'be23e.csv',
    'be230f': 'be23f.csv',
    'be230g': 'be23g.csv',
    'be230h': 'be23h.csv',
    'be230i': 'be23i.csv',
    'be230j': 'be23j.csv',
    'be230k': 'be23k.csv',
    'be230l': 'be23l.csv',
    'be230m': 'be23m.csv',
    'be230n': 'be23n.csv',
    'be2310': 'be2310.csv',
    'be2311': 'be2311.csv',
    'be2312': 'be2312.csv',
    'be2313': 'be2313.csv',
    'be2314': 'be2314.csv',
    'be2315': 'be2315.csv',
    'be2316': 'be2316.csv',
    'be2317': 'be2317.csv',
    'be2319': 'be2319.csv',
    'be2401': 'be2401.csv',
    'be2402': 'be2402.csv',
    'be2403': 'be2403.csv',
    'be2404': 'be2404.csv',
    'be2405': 'be2405.csv',
    'be2406': 'be2406.csv',
    'be2407': 'be2407.csv',
    'be2408': 'be2408.csv',
    'be2409': 'be2409.csv',
    'be2410': 'be2410.csv',
    'be2411': 'be2411.csv',
    'be2412': 'be2412.csv',
    'be2413': 'be2413.csv',
    'be2415': 'be2415.csv',
    'be2416': 'be2416.csv',
    'be2417': 'be2417.csv',
    'be2418': 'be2418.csv',
    'be2419': 'be2419.csv',
    'be2420': 'be2420.csv',
    'be2421': 'be2421.csv',
    'be2422': 'be2422.csv',
    'be2423': 'be2423.csv',
    'be2424': 'be2424.csv',
    'be2425': 'be2425.csv',
    'be2426': 'be2426.csv',
    'be2427': 'be2427.csv',
    'be2428': 'be2428.csv',
    'be2501': 'be2501.csv',
    'be2502': 'be2502.csv',
    'be2503': 'be2503.csv',
    'be2504': 'be2504.csv',
    'be2505': 'be2505.csv',
    'be2506': 'be2506.csv',
    'be2507': 'be2507.csv',
    'be2508': 'be2508.csv',
    'be2509': 'be2509.csv',
    'be2601': 'be2601.csv',
    'be2602': 'be2602.csv',
    'be2611': 'be2611.csv',
    'be2612': 'be2612.csv',
    'be2621': 'be2621.csv',
    'be2622': 'be2622.csv',
    'be2623': 'be2623.csv',
    'be2631': 'be2631.csv',
    'be2632': 'be2632.csv',
    'be2633': 'be2633.csv',
    'be2634': 'be2634.csv',
    'be2635': 'be2635.csv',
    'be2636': 'be2636.csv',
    'si_1_1': 'si_1_1.csv',
    'si_1_2': 'si_1_2.csv',
    'si_1_3a': 'si_1_3a.csv',
    'si_1_3b': 'si_1_3b.csv',
    'si_1_4': 'si_1_4.csv',
    'si_1_5': 'si_1_5.csv',
    'si_1_6': 'si_1_6.csv',
    'si_1_6a': 'si_1_6a.csv',
    'si_1_6b': 'si_1_6b.csv',
    'si_1_6c': 'si_1_6c.csv',
    'si_2_1': 'si_2_1.csv',
    'si_2_2': 'si_2_2.csv',
    'si_3_1': 'si_3_1.csv',
    'tc_1_1': 'tc_1_1.csv',
    'tc_1_2': 'tc_1_2.csv',
    'tc_1_3': 'tc_1_3.csv',
    'ti_1_1': 'ti_1_1.csv',
    'ti_1_3': 'ti_1_3.csv',
    'ti_1_4': 'ti_1_4.csv',
    'ti_1_6': 'ti_1_6.csv',
    'ti_1_7': 'ti_1_7.csv',
}

DOWNLOAD_SPECS = [
    NodeSpec(
        id=SLUG + "-" + eid.lower().replace("_", "-"),
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_FILE
]
