"""Shared fetch infrastructure for the WGMS connector.

HTTP-with-retry, release-zip URL resolution from the wgms.ch listing pages, and
a small zip-member text helper. Used by every node module; contains no NodeSpec
definitions.
"""

from __future__ import annotations

import io
import re
import zipfile

from subsets_utils import get, transient_retry

AMCE_VERSIONS_URL = "https://wgms.ch/mass_change_estimates/"

# Zip filename embeds the release date; format is YYYY-MM, YYYY-MMx (letter
# suffix), or YYYY-MM-DD. max() over the matched URLs picks the newest.
_AMCE_ZIP_RE = re.compile(
    r"https://wgms\.ch/downloads/wgms-amce-\d{4}-\d{2}(?:-\d{2}|[a-z])?\.zip"
)


@transient_retry()
def get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def get_bytes(url: str) -> bytes:
    # Large zips — generous read timeout.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def latest_url(page_url: str, pattern: re.Pattern) -> str:
    text = get_text(page_url)
    urls = sorted(set(pattern.findall(text)))
    if not urls:
        raise AssertionError(
            f"no release zip matching {pattern.pattern!r} found at {page_url}"
        )
    return max(urls)


def latest_amce_url() -> str:
    return latest_url(AMCE_VERSIONS_URL, _AMCE_ZIP_RE)


def read_zip_text(zf: zipfile.ZipFile, name: str):
    return io.TextIOWrapper(zf.open(name), encoding="utf-8", newline="")
