"""GitHub Advisory Database — affected-package subset.

github-affected: long-format, one row per (advisory x affected package range),
exploded from the OSV `affected` array in the shared advisory-database archive.

The download spec re-fetches the full archive (the corpus is a single snapshot
with no incremental delta filter — see research download_handoff), streams the
exploded rows to NDJSON, and the SQL transform types/projects them. Stateless
full re-pull: revisions and withdrawals are picked up for free every run.
"""

from __future__ import annotations

import json

from subsets_utils import raw_writer
from utils import iter_osv


def _affected_rows(source_directory: str, osv: dict):
    ghsa_id = osv.get("id")
    for aff in osv.get("affected") or []:
        if not isinstance(aff, dict):
            continue
        pkg = aff.get("package") or {}
        ecosystem = pkg.get("ecosystem")
        name = pkg.get("name")
        if not ecosystem or not name:
            continue
        introduced = fixed = last_affected = None
        for rng in aff.get("ranges") or []:
            for ev in rng.get("events") or []:
                if "introduced" in ev:
                    introduced = ev["introduced"]
                if "fixed" in ev:
                    fixed = ev["fixed"]
                if "last_affected" in ev:
                    last_affected = ev["last_affected"]
        bounds = []
        if introduced is not None:
            bounds.append(f">= {introduced}")
        if fixed is not None:
            bounds.append(f"< {fixed}")
        elif last_affected is not None:
            bounds.append(f"<= {last_affected}")
        vrange = ", ".join(bounds) if bounds else None
        if vrange is None:
            versions = aff.get("versions") or []
            versions = [v for v in versions if isinstance(v, str)]
            if versions:
                vrange = "in: " + ",".join(versions[:50])
        yield {
            "ghsa_id": ghsa_id,
            "ecosystem": ecosystem,
            "package_name": name,
            "vulnerable_version_range": vrange,
            "first_patched_version": fixed,
            "source_directory": source_directory,
        }


def fetch_affected(node_id: str) -> None:
    asset = node_id
    n = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for source_directory, osv in iter_osv():
            for row in _affected_rows(source_directory, osv):
                out.write(json.dumps(row) + "\n")
                n += 1
    if n == 0:
        raise AssertionError(f"{asset}: parsed 0 affected-package rows from archive")

