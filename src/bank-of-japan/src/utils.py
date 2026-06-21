"""Shared HTTP/parse helpers for the Bank of Japan connector.

The BOJ stat-search REST API (https://www.stat-search.boj.or.jp/api/v1/) is a
public, no-auth CSV API. Both published subsets (``series`` and ``values``)
walk the same set of databases and share the same request/parse plumbing, which
lives here so neither subset file duplicates it. This module is ``_``-prefixed
so the node loader (orchestrator.py:1123) skips it — it holds no NodeSpecs.
"""
import csv
import io

from ratelimit import limits, sleep_and_retry

from subsets_utils import get, transient_retry

BASE = "https://www.stat-search.boj.or.jp/api/v1/"

# The BOJ DB Names table (API manual II.3.(2)) — the source's own grouping of
# its ~200,000 series. The grouping dimension carried as a column, enumerated
# here so the crawl can walk every database.
DATABASES = {
    "IR01": "The Basic Discount Rates and Basic Loan Rates",
    "IR02": "Average Interest Rates Posted at Financial Institutions by Type of Deposit",
    "IR03": "Average Interest Rates on Time Deposits by Term",
    "IR04": "Average Contract Interest Rates on Loans and Discounts",
    "FM01": "Uncollateralized Overnight Call Rate (average)",
    "FM02": "Short-term Money Market Rates",
    "FM03": "Amounts Outstanding in Short-term Money Market",
    "FM04": "Amounts Outstanding in the Call Money Market",
    "FM05": "Issuance, Redemption, and Outstanding of Public and Corporate Bonds",
    "FM06": "Trading of Interest-bearing Government Bonds by Purchaser",
    "FM07": "(Reference) Government Bonds Sales Over the Counter / Counter Sales Ratio",
    "FM08": "Foreign Exchange Rates",
    "FM09": "Effective Exchange Rate",
    "PS01": "Other Payment and Settlement Systems",
    "PS02": "Basic Figures on Fails",
    "MD01": "Monetary Base",
    "MD02": "Money Stock",
    "MD03": "Monetary Survey",
    "MD04": "(Reference) Changes in Money Stock (M2+CDs) and Credit",
    "MD05": "Currency in Circulation",
    "MD06": "Sources of Changes in Current Account Balances at the BOJ and Market Operations",
    "MD07": "Reserves",
    "MD08": "BOJ Current Account Balances by Sector",
    "MD09": "Monetary Base and the Bank of Japan's Transactions",
    "MD10": "Amounts Outstanding of Deposits by Depositor",
    "MD11": "Deposits, Vault Cash, and Loans and Bills Discounted",
    "MD12": "Deposits, Vault Cash, and Loans and Bills Discounted by Prefecture",
    "MD13": "Principal Figures of Financial Institutions",
    "MD14": "Time Deposits: Amounts Outstanding and New Deposits by Maturity",
    "LA01": "Loans and Bills Discounted by Sector",
    "LA02": "Loans and Discounts by the Bank of Japan",
    "LA03": "Outstanding of Loans (Others)",
    "LA04": "Commitment Lines Extended by Japanese Banks",
    "LA05": "Senior Loan Officer Opinion Survey on Bank Lending Practices",
    "BS01": "Bank of Japan Accounts",
    "BS02": "Financial Institutions Accounts",
    "FF": "Flow of Funds",
    "OB01": "Bank of Japan's Transactions with the Government",
    "OB02": "Collateral Accepted by the Bank of Japan",
    "CO": "TANKAN",
    "PR01": "Corporate Goods Price Index (CGPI)",
    "PR02": "Services Producer Price Index (SPPI)",
    "PR03": "Input-Output Price Index of the Manufacturing Industry by Sector (IOPI)",
    "PR04": "Final Demand-Intermediate Demand price indexes (FD-ID)",
    "PF01": "Statement of Receipts and Payments of the Treasury Accounts",
    "PF02": "National Government Debt",
    "BP01": "Balance of Payments",
    "DER": "Regular Derivatives Market Statistics in Japan",
    "BIS": "BIS International Locational/Consolidated Banking Statistics in Japan",
    "OT": "Others",
}

# Columns of the /getMetadata data block, in order.
_META_COLS = [
    "SERIES_CODE", "NAME_OF_TIME_SERIES", "UNIT", "FREQUENCY", "CATEGORY",
    "LAYER1", "LAYER2", "LAYER3", "LAYER4", "LAYER5",
    "START_OF_THE_TIME_SERIES", "END_OF_THE_TIME_SERIES", "LAST_UPDATE", "NOTES",
]


class _PermanentError(Exception):
    """A non-retryable source error (bad request, missing DB, API STATUS!=200)."""


@sleep_and_retry
@limits(calls=60, period=60)  # conservative ~1 req/s; manual: "space out requests"
@transient_retry()
def _request_csv(operation: str, params: dict) -> list[list[str]]:
    """One throttled, retried GET against the BOJ API, returning parsed CSV
    rows. Raises HTTPStatusError (handled by the retry predicate) on HTTP
    failure and _PermanentError when the body reports a non-200 API STATUS."""
    p = {"format": "csv", "lang": "en", **params}
    resp = get(BASE + operation, params=p, timeout=(10.0, 120.0))
    resp.raise_for_status()
    rows = list(csv.reader(io.StringIO(resp.content.decode("utf-8", errors="replace"))))
    status = None
    for r in rows:
        if r and r[0] == "STATUS":
            status = r[1] if len(r) > 1 else None
            break
    if status != "200":
        raise _PermanentError(f"{operation} {params}: API STATUS={status}")
    return rows


def _data_block(rows: list[list[str]]) -> tuple[list[str], list[list[str]], str | None]:
    """Split a parsed CSV response into (header, data_rows, next_position).

    The response is a header block (STATUS/MESSAGE/PARAMETER/NEXTPOSITION lines)
    followed by a data table whose first row starts with 'SERIES_CODE'.
    """
    next_pos = None
    header_idx = None
    for i, r in enumerate(rows):
        if r and r[0] == "NEXTPOSITION":
            next_pos = (r[1].strip() if len(r) > 1 else "") or None
        if r and r[0] == "SERIES_CODE":
            header_idx = i
            break
    if header_idx is None:
        return [], [], next_pos
    header = rows[header_idx]
    data = [r for r in rows[header_idx + 1:] if r]
    return header, data, next_pos


def _to_int(s: str):
    s = (s or "").strip()
    return int(s) if s.isdigit() else None


def _fetch_metadata(db: str) -> list[dict]:
    """Return one dict per real series in `db` (layer-header rows dropped)."""
    rows = _request_csv("getMetadata", {"db": db})
    header, data, _ = _data_block(rows)
    idx = {name: header.index(name) for name in _META_COLS if name in header}

    def col(row, name):
        j = idx.get(name)
        return (row[j].strip() if j is not None and j < len(row) else "")

    out = []
    for row in data:
        code = col(row, "SERIES_CODE")
        if not code:
            continue  # layer-tree header row, not a series
        out.append({
            "db": db,
            "series_code": code,
            "name": col(row, "NAME_OF_TIME_SERIES"),
            "unit": col(row, "UNIT"),
            "frequency": col(row, "FREQUENCY"),
            "category": col(row, "CATEGORY"),
            "layer1": col(row, "LAYER1"),
            "layer2": col(row, "LAYER2"),
            "layer3": col(row, "LAYER3"),
            "layer4": col(row, "LAYER4"),
            "layer5": col(row, "LAYER5"),
            "start_date": col(row, "START_OF_THE_TIME_SERIES"),
            "end_date": col(row, "END_OF_THE_TIME_SERIES"),
            "last_update": col(row, "LAST_UPDATE"),
            "notes": col(row, "NOTES"),
        })
    return out
