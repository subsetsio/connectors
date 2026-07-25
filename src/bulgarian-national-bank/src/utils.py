"""Shared helpers for the Bulgarian National Bank (BNB) connector.

HTTP-with-retry and XML parsing shared by the exchange-rates and SDMX node
modules. Holds no NodeSpec definitions.
"""

import xml.etree.ElementTree as ET

import httpx

from subsets_utils import transient_retry

PREFIX = "bulgarian-national-bank-"
BASE = "https://www.bnb.bg/Statistics"

_client: httpx.Client | None = None


def _get_client() -> httpx.Client:
    """BNB serves an incomplete TLS chain in GitHub's trust store."""
    global _client
    if _client is None:
        _client = httpx.Client(
            timeout=httpx.Timeout(180.0, connect=10.0),
            headers={"User-Agent": "subsets-bulgarian-national-bank/1.0"},
            follow_redirects=True,
            verify=False,
        )
    return _client


@transient_retry()
def get_bytes(url: str) -> bytes:
    resp = _get_client().get(url)
    resp.raise_for_status()
    return resp.content


def xml_root(content: bytes):
    return ET.fromstring(content.lstrip(b"\xef\xbb\xbf"))
