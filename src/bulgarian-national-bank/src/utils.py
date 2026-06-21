"""Shared helpers for the Bulgarian National Bank (BNB) connector.

HTTP-with-retry and XML parsing shared by the exchange-rates and SDMX node
modules. Holds no NodeSpec definitions.
"""

import xml.etree.ElementTree as ET

from subsets_utils import get, transient_retry

PREFIX = "bulgarian-national-bank-"
BASE = "https://www.bnb.bg/Statistics"


@transient_retry()
def get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def xml_root(content: bytes):
    return ET.fromstring(content.lstrip(b"\xef\xbb\xbf"))
