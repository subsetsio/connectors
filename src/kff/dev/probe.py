"""Probe: exercise the real parser against a few live indicators (no raw writes)."""
import sys
sys.path.insert(0, "/Users/nathansnellaert/Documents/hardened/connectors/src/kff/src")
from nodes.kff import _fetch_html, _parse_rows, _URL

for slug in ["total-population", "abortion-rate", "total-medicaid-spending",
             "births-financed-by-medicaid"]:
    html = _fetch_html(_URL.format(slug=slug))
    rows = _parse_rows(html)
    tfs = sorted({r["timeframe"] for r in rows})
    metrics = sorted({r["metric"] for r in rows})
    num = sum(1 for r in rows if r["value"] is not None)
    print(f"\n{slug}: rows={len(rows)} numeric={num} timeframes={len(tfs)}{tfs[:4]} metrics={metrics[:6]}")
    print("  sample:", rows[0], "|", rows[7] if len(rows) > 7 else "")
