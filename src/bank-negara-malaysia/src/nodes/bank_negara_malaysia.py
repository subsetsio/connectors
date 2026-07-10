"""Bank Negara Malaysia (BNM) Open API connector — every subset.

REST at https://api.bnm.gov.my/public; every request carries the versioned
`Accept: application/vnd.BNM.API.v1+json` header (see utils). JSON payload sits
under a top-level `data` key. No auth, no documented rate limit. The corpus is
small (daily-cadence rate/price series, MB-scale), so every subset is a
**stateless full re-pull**: re-fetch the whole series each run and overwrite —
revisions and late corrections are picked up for free.

There is no single bulk endpoint; history is reached by iterating path params,
and the iteration shape differs by resource. The fetch functions group by that
shape (one top-level fn per family, dispatched on the resource recovered from
the node id):

  - fetch_snapshot      base-rate, renminbi-fx-forward-price
                        single latest-state call (/<res>), no history endpoint.
  - fetch_exchange_rate exchange-rate
                        per-currency month-grid fan-out; the live currency set
                        is read from the latest /exchange-rate snapshot.
  - fetch_interest      interest-rate, interest-volume
                        month-grid crossed with three `?product=` slices.
  - fetch_monthly       kl-usd-reference-rate, usd-interbank-intraday-rate,
                        fx-turn-over, kijang-emas, islamic-interbank-rate,
                        interbank-swap
                        one call per (year, month); a per-resource normalizer
                        shapes each record.
  - fetch_opr           opr
                        year-iterated policy decisions (/opr/year/{y}).

Shared transport (versioned Accept header, retrying JSON fetch, bounded
thread-pool fan-out, start-year discovery, month grid, tenor normalizer) lives
in `src/utils.py`.
"""
from subsets_utils import NodeSpec, save_raw_ndjson

from utils import (
    PREFIX,
    _discover_start_year,
    _fetch,
    _has_rows,
    _month_grid,
    _norm_tenor,
    _now,
    _parallel,
)


# ============================================================ snapshot family
# base-rate: a list of per-bank rates, stamped with the snapshot effective_date.
# renminbi-fx-forward-price: one nested record flattened into selling_*/buying_*.

def _collect_snapshot(resource: str):
    payload = _fetch(resource)
    if not _has_rows(payload):
        raise RuntimeError(f"{resource}: empty snapshot")
    data = payload.get("data")
    meta = payload.get("meta") or {}
    rows = []
    if resource == "base-rate":
        eff = meta.get("effective_date")
        for rec in data:
            row = dict(rec)
            row["effective_date"] = eff
            rows.append(row)
    else:  # renminbi-fx-forward-price: single nested record
        rec = data
        row = {"date": rec.get("date")}
        for side in ("selling", "buying"):
            for k, v in (rec.get(side) or {}).items():
                row[f"{side}_{k}"] = v
        rows.append(row)
    return rows


def fetch_snapshot(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_snapshot(resource)
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


# ============================================================= consumer alert
# A current full reference list. BNM does not expose year/month history variants.

def fetch_consumer_alert(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    payload = _fetch(resource)
    if not _has_rows(payload):
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(payload.get("data") or [], node_id)


# ============================================================== exchange-rate
# Per-currency historical fan-out (/exchange-rate/{cur}/year/{y}/month/{m}). The
# current currency set is read from the latest snapshot, then each currency is
# pulled month by month back to its discovered start year. Heaviest BNM resource.

def _collect_exchange_rate():
    snap = _fetch("exchange-rate")
    currencies = sorted({r["currency_code"] for r in (snap or {}).get("data", [])
                         if r.get("currency_code")})
    if not currencies:
        raise RuntimeError("exchange-rate: no currencies in latest snapshot")
    start = _discover_start_year(lambda y: f"exchange-rate/USD/year/{y}/month/6")
    tasks = []
    for cur in currencies:
        for y, m in _month_grid(start):
            tasks.append(((cur, y, m), f"exchange-rate/{cur}/year/{y}/month/{m}"))
    rows = []
    for (cur, _y, _m), payload in _parallel(tasks):
        if not payload:
            continue
        d = payload.get("data")
        if not d:
            continue
        unit = d.get("unit")
        code = d.get("currency_code", cur)
        rate = d.get("rate")
        if isinstance(rate, dict):
            rate = [rate]
        for rr in rate or []:
            rows.append({
                "currency_code": code,
                "unit": unit,
                "date": rr.get("date"),
                "buying_rate": rr.get("buying_rate"),
                "selling_rate": rr.get("selling_rate"),
                "middle_rate": rr.get("middle_rate"),
            })
    return rows


def fetch_exchange_rate(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_exchange_rate()
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


# ================================================ product-iterated interest feeds
# interest-rate, interest-volume: month-iterated with a `?product=` query param
# crossed over the three products. Both share this body (parametric on resource);
# their schemas differ only in that interest-volume carries an extra `other` tenor.

PRODUCTS = ["overall", "interbank", "money_market_operations"]


def _collect_by_product(resource: str):
    start = _discover_start_year(
        lambda y: f"{resource}/year/{y}/month/6?product=overall"
    )
    tasks = []
    for product in PRODUCTS:
        for y, m in _month_grid(start):
            tasks.append(((product, y, m),
                          f"{resource}/year/{y}/month/{m}?product={product}"))
    rows = []
    for (product, _y, _m), payload in _parallel(tasks):
        if not payload:
            continue
        for rec in payload.get("data") or []:
            row = _norm_tenor(rec)
            row["product"] = product
            rows.append(row)
    return rows


def fetch_interest(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_by_product(resource)
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


# ============================================================= month-iterated
# One call per (year, month) over /<res>/year/{y}/month/{m}, returning a whole
# month of daily records. A single parametric body drives every resource here;
# they differ only in their per-record normalizer (selected from a config map).

def _norm_identity(rec: dict) -> dict:
    return dict(rec)


def _norm_kijang(rec: dict) -> dict:
    def pair(key):
        d = rec.get(key) or {}
        return d.get("buying"), d.get("selling")
    ob, os_ = pair("one_oz")
    hb, hs = pair("half_oz")
    qb, qs = pair("quarter_oz")
    return {
        "date": rec.get("effective_date"),
        "one_oz_buying": ob, "one_oz_selling": os_,
        "half_oz_buying": hb, "half_oz_selling": hs,
        "quarter_oz_buying": qb, "quarter_oz_selling": qs,
    }


# month-iterated resources -> their per-record normalizer
_MONTHLY_NORMALIZERS = {
    "kl-usd-reference-rate": _norm_identity,
    "usd-interbank-intraday-rate": _norm_identity,
    "fx-turn-over": _norm_identity,
    "kijang-emas": _norm_kijang,
    "islamic-interbank-rate": _norm_tenor,
    "interbank-swap": _norm_tenor,
}


def _collect_monthly(resource: str):
    start = _discover_start_year(lambda y: f"{resource}/year/{y}/month/6")
    norm = _MONTHLY_NORMALIZERS[resource]
    tasks = [((y, m), f"{resource}/year/{y}/month/{m}") for y, m in _month_grid(start)]
    rows = []
    for _key, payload in _parallel(tasks):
        if not payload:
            continue
        for rec in payload.get("data") or []:
            rows.append(norm(rec))
    return rows


def fetch_monthly(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_monthly(resource)
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


# ======================================================================== opr
# Year-iterated (/opr/year/{y}); one call per year from the discovered start year
# through the current year. Each call returns that year's policy decisions.

def _collect_opr():
    start = _discover_start_year(lambda y: f"opr/year/{y}")
    cur_year, _ = _now()
    tasks = [(y, f"opr/year/{y}") for y in range(start, cur_year + 1)]
    rows = []
    for _y, payload in _parallel(tasks):
        if not payload:
            continue
        for rec in payload.get("data") or []:
            rows.append({
                "year": rec.get("year"),
                "date": rec.get("date"),
                "change_in_opr": rec.get("change_in_opr"),
                "new_opr_level": rec.get("new_opr_level"),
            })
    return rows


def fetch_opr(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_opr()
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


# =================================================================== download
DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}base-rate", fn=fetch_snapshot, kind="download"),
    NodeSpec(id=f"{PREFIX}consumer-alert", fn=fetch_consumer_alert, kind="download"),
    NodeSpec(id=f"{PREFIX}renminbi-fx-forward-price", fn=fetch_snapshot, kind="download"),
    NodeSpec(id=f"{PREFIX}exchange-rate", fn=fetch_exchange_rate, kind="download"),
    NodeSpec(id=f"{PREFIX}interest-rate", fn=fetch_interest, kind="download"),
    NodeSpec(id=f"{PREFIX}interest-volume", fn=fetch_interest, kind="download"),
    NodeSpec(id=f"{PREFIX}kl-usd-reference-rate", fn=fetch_monthly, kind="download"),
    NodeSpec(id=f"{PREFIX}usd-interbank-intraday-rate", fn=fetch_monthly, kind="download"),
    NodeSpec(id=f"{PREFIX}fx-turn-over", fn=fetch_monthly, kind="download"),
    NodeSpec(id=f"{PREFIX}kijang-emas", fn=fetch_monthly, kind="download"),
    NodeSpec(id=f"{PREFIX}islamic-interbank-rate", fn=fetch_monthly, kind="download"),
    NodeSpec(id=f"{PREFIX}interbank-swap", fn=fetch_monthly, kind="download"),
    NodeSpec(id=f"{PREFIX}opr", fn=fetch_opr, kind="download"),
]
