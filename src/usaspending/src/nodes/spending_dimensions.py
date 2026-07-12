"""USAspending.gov — full-fiscal-year obligation totals by dimension.

``/spending/`` returns full-fiscal-year obligation totals broken out by a chosen
``type`` dimension (agency, budget_function, budget_subfunction, object_class,
federal_account, program_activity). One POST per (dimension, completed-fiscal-year);
the aggregate is returned in one shot — no pagination.

Fetch shape: **stateless full re-pull** every run. The corpus is small and
USAspending restates historical figures, so a full snapshot is always correct
and a watermark would only risk skipping revisions.

The fiscal-year set is **discovered** from the ``/references/submission_periods/``
reference endpoint (years whose period-12 submission has been revealed) — never
hardcoded.
"""
import datetime

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import _get, _post

# entity id (collect) -> /spending/ `type` value
DIMENSIONS = {
    "spending-by-agency": "agency",
    "spending-by-budget-function": "budget_function",
    "spending-by-budget-subfunction": "budget_subfunction",
    "spending-by-object-class": "object_class",
    "spending-by-federal-account": "federal_account",
    "spending-by-program-activity": "program_activity",
}


def _completed_fiscal_years() -> list[int]:
    """Fiscal years whose full-year (period 12) submission has been revealed.

    Discovered from the submission_periods reference endpoint so the connector
    picks up each new fiscal year automatically once it closes.
    """
    periods = _get("/references/submission_periods/")["available_periods"]
    now = datetime.datetime.now(datetime.timezone.utc)
    years = set()
    for p in periods:
        if p.get("submission_fiscal_month") != 12:
            continue
        reveal = p.get("submission_reveal_date")
        if not reveal:
            continue
        revealed_at = datetime.datetime.fromisoformat(reveal.replace("Z", "+00:00"))
        if revealed_at <= now:
            years.add(int(p["submission_fiscal_year"]))
    if not years:
        raise RuntimeError(
            "no completed fiscal years discovered from submission_periods — "
            "endpoint shape may have changed"
        )
    return sorted(years)


DIMENSION_SCHEMA = pa.schema([
    ("fiscal_year", pa.int64()),
    ("id", pa.string()),              # source-unique aggregate id
    ("code", pa.string()),            # dimension code (not unique for program_activity)
    ("name", pa.string()),
    ("account_number", pa.string()),  # federal_account only; null elsewhere
    ("total_obligations", pa.float64()),
])


def fetch_spending_dimension(node_id: str) -> None:
    """Fetch full-year obligation totals for one /spending/ dimension across all
    completed fiscal years."""
    asset = node_id
    entity = node_id[len("usaspending-"):]
    sp_type = DIMENSIONS[entity]

    rows = []
    for fy in _completed_fiscal_years():
        results = _post(
            "/spending/",
            {"type": sp_type, "filters": {"fy": str(fy), "period": "12"}},
        ).get("results", [])
        for r in results:
            amount = r.get("amount")
            if amount is None:
                continue
            ident = r.get("id")
            code = r.get("code")
            rows.append({
                "fiscal_year": fy,
                "id": str(ident) if ident is not None else None,
                "code": str(code) if code is not None else None,
                "name": r.get("name"),
                "account_number": r.get("account_number"),
                "total_obligations": float(amount),
            })

    table = pa.Table.from_pylist(rows, schema=DIMENSION_SCHEMA)
    save_raw_parquet(table, asset)
