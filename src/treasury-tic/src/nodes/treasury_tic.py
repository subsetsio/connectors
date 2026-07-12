"""Download specs for the Treasury TIC connector."""

from subsets_utils import NodeSpec

from nodes.mfh import fetch_mfh as _fetch_mfh
from nodes.slt import fetch_slt as _fetch_slt


def fetch_mfh(node_id: str) -> None:
    _fetch_mfh(node_id)


def fetch_slt(node_id: str) -> None:
    _fetch_slt(node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="treasury-tic-mfh-treasury-holdings", fn=fetch_mfh, kind="download"),
    NodeSpec(id="treasury-tic-slt1-us-lt-securities-held-by-foreign-residents", fn=fetch_slt, kind="download"),
    NodeSpec(id="treasury-tic-slt2-foreign-lt-securities-held-by-us-residents", fn=fetch_slt, kind="download"),
    NodeSpec(id="treasury-tic-slt3-us-treasury-securities-held-by-foreign-residents", fn=fetch_slt, kind="download"),
    NodeSpec(id="treasury-tic-slt4-us-purchases-sales-lt-securities-by-type", fn=fetch_slt, kind="download"),
]
