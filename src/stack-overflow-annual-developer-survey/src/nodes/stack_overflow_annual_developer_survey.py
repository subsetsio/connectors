"""Canonical download node module for Stack Overflow Annual Developer Survey."""

from subsets_utils import NodeSpec

from constants import RESULTS_YEARS
from nodes.codebook import fetch_codebook as _fetch_codebook
from nodes.results import fetch_results as _fetch_results


SLUG = "stack-overflow-annual-developer-survey"


def fetch_results(node_id: str) -> None:
    _fetch_results(node_id)


def fetch_codebook(node_id: str) -> None:
    _fetch_codebook(node_id)


DOWNLOAD_SPECS = [
    *[
        NodeSpec(id=f"{SLUG}-results-{year}", fn=fetch_results, kind="download")
        for year in RESULTS_YEARS
    ],
    NodeSpec(id=f"{SLUG}-schema-codebook", fn=fetch_codebook, kind="download"),
]
