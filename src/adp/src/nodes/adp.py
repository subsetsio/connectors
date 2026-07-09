"""Aggregate ADP download specs for harness tooling."""

from nodes.ner_employment import DOWNLOAD_SPECS as NER_DOWNLOAD_SPECS
from nodes.pay_insights import DOWNLOAD_SPECS as PAY_DOWNLOAD_SPECS

DOWNLOAD_SPECS = [
    *NER_DOWNLOAD_SPECS,
    *PAY_DOWNLOAD_SPECS,
]
