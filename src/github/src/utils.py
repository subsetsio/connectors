"""Shared GitHub Advisory Database fetch helpers.

The entire github/advisory-database repository is downloaded as one tar.gz
archive (whole corpus in one shot, no auth, no per-entity pagination, served by
codeload — not the 60/hr REST core) and every advisories/**/*.json file (OSV
format) is parsed. Both publishable subsets (advisories, affected) derive from
this same archive, so the download + member iteration lives here once.
"""

from __future__ import annotations

import io
import json
import tarfile

from subsets_utils import get, transient_retry

# github.com archive redirects to codeload.github.com and serves the working
# tree (not git history) as tar.gz. The top-level dir is the stable
# "advisory-database-main/" (branch archive), not a per-sha name.
ARCHIVE_URL = "https://github.com/github/advisory-database/archive/refs/heads/main.tar.gz"


@transient_retry()
def download_archive() -> bytes:
    """Fetch the full advisory-database tarball (~hundreds of MB) into memory.

    One reliable request to codeload; retried with backoff on transient
    transport/5xx/429 failures. Returned as bytes so tarfile can stream members
    out without a second network pass.
    """
    resp = get(ARCHIVE_URL, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def iter_osv():
    """Stream (source_directory, osv_dict) for every advisory JSON in the
    archive. Bounded memory — one member is decoded at a time."""
    buf = io.BytesIO(download_archive())
    tar = tarfile.open(fileobj=buf, mode="r:gz")
    for member in tar:
        if not member.isfile() or not member.name.endswith(".json"):
            continue
        parts = member.name.split("/")
        # parts: [advisory-database-main, advisories, <github-reviewed|unreviewed>, YEAR, MM, GHSA-.., GHSA-...json]
        if len(parts) < 4 or parts[1] != "advisories":
            continue
        source_directory = parts[2]
        fh = tar.extractfile(member)
        if fh is None:
            continue
        try:
            data = json.loads(fh.read())
        except (ValueError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict) or not data.get("id"):
            continue
        yield source_directory, data
