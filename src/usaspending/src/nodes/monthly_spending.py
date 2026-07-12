"""USAspending.gov — monthly obligation time series by award type.

``/search/spending_over_time/`` returns a monthly time series of obligations
split by award type. The full FY2008-present history returns in a single request
(~230 months), so one POST covers it.

Fetch shape: **stateless full re-pull** every run. USAspending restates
historical figures, so a full snapshot is always correct.

The monthly series uses the documented data floor (FY2008, 2007-10-01) with a
dynamic upper bound (today).
"""
import datetime

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import _post

# FY2008 is the earliest fiscal year served by spending_over_time (DATA Act /
# award transaction history floor). Fixed source characteristic, not an
# iterated range — the upper bound is dynamic (today).
MONTHLY_START = "2007-10-01"


MONTHLY_SCHEMA = pa.schema([
    ("date", pa.string()),  # YYYY-MM-01 calendar month, normalized from fiscal (fy, month)
    ("total_obligations", pa.float64()),
    ("contract_obligations", pa.float64()),
    ("direct_payment_obligations", pa.float64()),
    ("grant_obligations", pa.float64()),
    ("idv_obligations", pa.float64()),
    ("loan_obligations", pa.float64()),
    ("other_obligations", pa.float64()),
])


def _f(val) -> float:
    return float(val) if val is not None else 0.0


def fetch_monthly_spending(node_id: str) -> None:
    """Fetch the full monthly obligation time series, split by award type.

    The API reports each month as (fiscal_year, fiscal_month) where fiscal_month
    1 = October. Normalize to a calendar first-of-month date here so the
    transform stays a thin cast.
    """
    asset = node_id
    end_date = datetime.date.today().isoformat()
    results = _post(
        "/search/spending_over_time/",
        {
            "group": "month",
            "filters": {"time_period": [{"start_date": MONTHLY_START, "end_date": end_date}]},
        },
    ).get("results", [])

    rows = []
    for r in results:
        tp = r["time_period"]
        fy = int(tp["fiscal_year"])
        fm = int(tp["month"])
        cal_year = fy - 1 if fm <= 3 else fy
        cal_month = ((fm + 8) % 12) + 1
        rows.append({
            "date": f"{cal_year}-{cal_month:02d}-01",
            "total_obligations": _f(r.get("aggregated_amount")),
            "contract_obligations": _f(r.get("Contract_Obligations")),
            "direct_payment_obligations": _f(r.get("Direct_Obligations")),
            "grant_obligations": _f(r.get("Grant_Obligations")),
            "idv_obligations": _f(r.get("Idv_Obligations")),
            "loan_obligations": _f(r.get("Loan_Obligations")),
            "other_obligations": _f(r.get("Other_Obligations")),
        })

    rows.sort(key=lambda x: x["date"])
    table = pa.Table.from_pylist(rows, schema=MONTHLY_SCHEMA)
    save_raw_parquet(table, asset)
