import sys
from pathlib import Path


_NODES_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_NODES_DIR.parent))
sys.path.insert(0, str(_NODES_DIR))

from subsets_utils import NodeSpec

from consumer_complaints import fetch_complaints as _fetch_complaints
from credit_trends import fetch_credit_trend as _fetch_credit_trend
from hmda import (
    fetch_hmda_filers as _fetch_hmda_filers,
    fetch_hmda_loan_records as _fetch_hmda_loan_records,
)
from mortgage_performance import fetch_mortgage_performance as _fetch_mortgage_performance


def fetch_credit_trend(node_id: str) -> None:
    _fetch_credit_trend(node_id)


def fetch_complaints(node_id: str) -> None:
    _fetch_complaints(node_id)


def fetch_hmda_filers(node_id: str) -> None:
    _fetch_hmda_filers(node_id)


def fetch_hmda_loan_records(node_id: str) -> None:
    _fetch_hmda_loan_records(node_id)


def fetch_mortgage_performance(node_id: str) -> None:
    _fetch_mortgage_performance(node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="cfpb-cct-crt-data", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-inq-data", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-map-data", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-num-data", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-vol-data", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-volume-data-age-group", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-volume-data-income-level", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-volume-data-score-level", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-yoy-data-age-group", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-yoy-data-all", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-yoy-data-income-level", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-yoy-data-score-level", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-consumer-complaints", fn=fetch_complaints, kind="download"),
    NodeSpec(id="cfpb-hmda-filers", fn=fetch_hmda_filers, kind="download"),
    NodeSpec(id="cfpb-hmda-loan-records", fn=fetch_hmda_loan_records, kind="download"),
    NodeSpec(id="cfpb-mortgage-performance-county", fn=fetch_mortgage_performance, kind="download"),
    NodeSpec(id="cfpb-mortgage-performance-metro-area", fn=fetch_mortgage_performance, kind="download"),
    NodeSpec(id="cfpb-mortgage-performance-state", fn=fetch_mortgage_performance, kind="download"),
]
