"""GitHub Advisory Database — advisory-level subset.

github-advisories: one row per security advisory (advisory-level fields),
derived from the OSV JSON in the shared advisory-database archive.

The download spec re-fetches the full archive (the corpus is a single snapshot
with no incremental delta filter — see research download_handoff), streams the
parsed advisory rows to NDJSON, and the SQL transform types/projects them.
Stateless full re-pull: revisions and withdrawals are picked up for free every
run.
"""

from __future__ import annotations

import json

from subsets_utils import raw_writer
from utils import iter_osv


def _cve_id(aliases):
    for a in aliases or []:
        if isinstance(a, str) and a.startswith("CVE-"):
            return a
    return None


def _cvss_vector(severity_list, kind):
    for s in severity_list or []:
        if isinstance(s, dict) and s.get("type") == kind:
            return s.get("score")
    return None


def _ts(value):
    """Normalize an OSV ISO-8601 timestamp ('2017-10-24T18:33:36Z') to a form
    DuckDB casts cleanly ('2017-10-24 18:33:36'). try_cast in the transform is
    the safety net for any odd value this misses."""
    if not value or not isinstance(value, str):
        return None
    return value.replace("T", " ").replace("Z", "")


def _advisory_row(source_directory: str, osv: dict) -> dict:
    ds = osv.get("database_specific") or {}
    aliases = osv.get("aliases") or []
    sev = osv.get("severity") or []
    cwes = ds.get("cwe_ids") or []
    # Every key is always present (None when absent) so read_json_auto infers a
    # stable, consistent column set across all ~290k records.
    return {
        "ghsa_id": osv.get("id"),
        "cve_id": _cve_id(aliases),
        "aliases": ",".join(a for a in aliases if isinstance(a, str)) or None,
        "summary": osv.get("summary"),
        "severity": ds.get("severity"),
        "cvss_v3_vector": _cvss_vector(sev, "CVSS_V3"),
        "cvss_v4_vector": _cvss_vector(sev, "CVSS_V4"),
        "cwe_ids": ",".join(c for c in cwes if isinstance(c, str)) or None,
        "github_reviewed": bool(ds.get("github_reviewed")),
        "published_at": _ts(osv.get("published")),
        "modified_at": _ts(osv.get("modified")),
        "withdrawn_at": _ts(osv.get("withdrawn")),
        "github_reviewed_at": _ts(ds.get("github_reviewed_at")),
        "nvd_published_at": _ts(ds.get("nvd_published_at")),
        "source_directory": source_directory,
    }


def fetch_advisories(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    n = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for source_directory, osv in iter_osv():
            out.write(json.dumps(_advisory_row(source_directory, osv)) + "\n")
            n += 1
    if n == 0:
        raise AssertionError(f"{asset}: parsed 0 advisories from archive")

