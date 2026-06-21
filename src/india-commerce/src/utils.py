"""Shared transport and dimension-discovery helpers for the india-commerce
connector (DGCIS / TIA portal).

The TIA portal (https://trade-analytics.commerce.gov.in) is an undocumented
JSON REST surface over the official DGCIS export/import data bank. No auth.
Years and the country list are discovered from the source each run (year and
country <option> dropdowns), never hardcoded.
"""
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from subsets_utils import get, transient_retry

log = logging.getLogger(__name__)

BASE = "https://trade-analytics.commerce.gov.in"

# Codes that appear in the country <select> but are not bilateral partners.
_NON_PARTNER = {"USD", "INR", "ALL", "WRD"}


# --------------------------------------------------------------------------- #
# transport
# --------------------------------------------------------------------------- #
@transient_retry(attempts=5, min_wait=2, max_wait=60)
def _fetch_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_text(url: str) -> str:
    @transient_retry(attempts=5, min_wait=2, max_wait=60)
    def _go():
        resp = get(url, timeout=(10.0, 120.0))
        resp.raise_for_status()
        return resp.text

    return _go()


def _num(v):
    """Coerce a TIA value (str with trailing zeros, float, or None) to float."""
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _run_jobs(jobs, fn, label, *, workers, max_fail_ratio=0.10):
    """Run fn(*job) across a thread pool; collect row lists. A handful of
    permanent per-entity failures are tolerated (logged); a systemic failure
    rate raises so a broken endpoint/format is loud, not silent."""
    rows, fails = [], 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(fn, *j): j for j in jobs}
        for fut in as_completed(futs):
            try:
                rows.extend(fut.result())
            except Exception as exc:  # noqa: BLE001 - logged with context
                fails += 1
                log.warning("%s: job %s failed: %s: %s",
                            label, futs[fut], type(exc).__name__, exc)
    if jobs and fails / len(jobs) > max_fail_ratio:
        raise RuntimeError(
            f"{label}: {fails}/{len(jobs)} jobs failed "
            f"(> {max_fail_ratio:.0%}); endpoint likely broken"
        )
    log.info("%s: %d rows from %d jobs (%d failed)",
             label, len(rows), len(jobs), fails)
    return rows


# --------------------------------------------------------------------------- #
# dimension discovery (from the source, every run)
# --------------------------------------------------------------------------- #
def _discover_countries() -> dict:
    """ISO3 -> name from the server-rendered <option> list on /public/country."""
    html = _fetch_text(f"{BASE}/public/country")
    out = {}
    for code, name in re.findall(
        r'<option[^>]*value="([A-Z]{3})"[^>]*>([^<]+)</option>', html
    ):
        if code in _NON_PARTNER:
            continue
        out.setdefault(code, name.strip())
    if len(out) < 150:
        raise RuntimeError(
            f"country discovery returned only {len(out)} codes (expected >=150)"
        )
    return out


def _discover_years() -> list:
    """Calendar years offered by the portal's year <option> dropdown."""
    html = _fetch_text(f"{BASE}/public/country")
    years = sorted({int(y) for y in re.findall(r'<option[^>]*value="(20\d{2})"', html)})
    if not years:
        raise RuntimeError("year discovery found no 20xx options")
    return years
