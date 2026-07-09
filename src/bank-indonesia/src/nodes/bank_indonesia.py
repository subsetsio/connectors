"""Bank Indonesia exchange-rate connector (wsKursBI web service).

Chosen mechanism: kurs_webservice — the ASMX service at
https://www.bi.go.id/biwebservice/wskursbi.asmx, queried via plain HTTP GET
(method name in the path) returning an XML DataSet diffgram.

Three published exchange-rate products, each a stateless full re-pull:
  - kurs-transaksi-bi : BI transaction buy/sell rates    (Lokal  family)
  - kurs-uka          : foreign banknote (UKA) buy/sell  (Asing  family)
  - jisdor            : official USD/IDR spot reference   (Jisdor family)

The fourth family the service exposes (NonUSD_IDR) is not built: Bank
Indonesia's service returns "Sorry you cannot access this feature" / connection
resets for the NonUSD_IDR method family, so the accept stage defers it until the
upstream endpoint becomes usable.

Method variants (pinned from the WSDL):
  - variant2(tgl)                   -> all currencies for one date; used to
                                       enumerate the live currency set.
  - variant3(mts,startdate,enddate) -> full per-currency history in ONE call
                                       (USD Lokal returns ~5200 rows, 2005..today).
The Jisdor variant3 uses camelCase startDate/endDate (lowercase 500s).

Full re-pull is cheap (~50 GETs, a few MB) so no incremental state is kept;
upstream revisions are picked up for free on every run. The service
intermittently 500s / resets the connection ("Kendala akses API Kurs") — those
are transient and handled by the retry decorator.
"""
from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET

import httpx
import pyarrow as pa
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import NodeSpec, get, save_raw_parquet

BASE = "https://www.bi.go.id/biwebservice/wskursbi.asmx"
SOURCE_MIN = "2000-01-01"   # earliest startdate; service returns from when data begins

SCHEMA = pa.schema([
    ("date",     pa.string()),    # YYYY-MM-DD; CAST to DATE in the transform
    ("currency", pa.string()),
    ("unit",     pa.float64()),
    ("buy",      pa.float64()),
    ("sell",     pa.float64()),
])

_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError, httpx.ProxyError,
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
def _get_xml(method, params):
    resp = get(f"{BASE}/{method}", params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _parse_rows(content):
    """Parse a wsKursBI diffgram into dicts keyed by the field prefix
    (id, lnk, nil, beli, jual, tgl, mts) — uniform across the lokal/asing schemas
    whose columns are suffixed _subkurslokal / _subkursasing."""
    root = ET.fromstring(content)
    out = []
    for el in root.iter():
        if el.tag.split("}")[-1] in ("Table", "Table1"):
            out.append({c.tag.split("}")[-1].split("_")[0]: c.text for c in el})
    return out


def _to_float(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _row_record(row):
    tgl = row.get("tgl")
    return {
        "date": tgl[:10] if tgl else None,
        "currency": (row.get("mts") or "").strip() or None,
        "unit": _to_float(row.get("nil")),
        "buy": _to_float(row.get("beli")),
        "sell": _to_float(row.get("jual")),
    }


def _today_plus_one():
    # Overshoot the upper bound by a day so the latest Jakarta (UTC+7) business
    # day is always inside the window regardless of UTC clock skew.
    return (datetime.now(timezone.utc) + timedelta(days=1)).date().isoformat()


def _enumerate_currencies(method2):
    """Live currency set from variant2 (all currencies for one date), walking
    back from today to skip weekends / holidays / transient errors."""
    today = datetime.now(timezone.utc).date()
    for back in range(0, 21):
        d = (today - timedelta(days=back)).isoformat()
        try:
            rows = _parse_rows(_get_xml(method2, {"tgl": d}))
        except Exception:
            continue
        curs = sorted({(r.get("mts") or "").strip() for r in rows if (r.get("mts") or "").strip()})
        if curs:
            return curs
    raise RuntimeError(f"{method2}: no currencies found in the last 21 days")


def _fetch_history(method3, currency, camel):
    if camel:
        params = {"mts": currency, "startDate": SOURCE_MIN, "endDate": _today_plus_one()}
    else:
        params = {"mts": currency, "startdate": SOURCE_MIN, "enddate": _today_plus_one()}
    return _parse_rows(_get_xml(method3, params))


def _collect(asset, method3, currencies, camel):
    records = []
    for cur in currencies:
        for row in _fetch_history(method3, cur, camel):
            rec = _row_record(row)
            if rec["date"] and rec["currency"]:
                records.append(rec)
    if not records:
        raise RuntimeError(f"{asset}: no rows collected across {len(currencies)} currencies")
    save_raw_parquet(pa.Table.from_pylist(records, schema=SCHEMA), asset)


def fetch_kurs_transaksi_bi(node_id):
    curs = _enumerate_currencies("getSubKursLokal2")
    _collect(node_id, "getSubKursLokal3", curs, camel=False)


def fetch_kurs_uka(node_id):
    curs = _enumerate_currencies("getSubKursAsing2")
    _collect(node_id, "getSubKursAsing3", curs, camel=False)


def fetch_jisdor(node_id):
    # JISDOR is the USD/IDR reference rate only; variant3 wants camelCase params.
    _collect(node_id, "getSubKursJisdor3", ["USD"], camel=True)


DOWNLOAD_SPECS = [
    NodeSpec(id="bank-indonesia-kurs-transaksi-bi", fn=fetch_kurs_transaksi_bi, kind="download"),
    NodeSpec(id="bank-indonesia-kurs-uka", fn=fetch_kurs_uka, kind="download"),
    NodeSpec(id="bank-indonesia-jisdor", fn=fetch_jisdor, kind="download"),
]
