"""Aggregate ADP download specs for harness tooling.

The runtime discovers ``*_SPECS`` from every module in ``src/nodes``. This
module owns the specs so ids are registered once, while leaf modules contain
only implementation details.
"""

from subsets_utils import NodeSpec

from nodes.ner_employment import fetch_ner_employment
from nodes.pay_insights import fetch_pay_insights

DOWNLOAD_SPECS = [
    NodeSpec(id="adp-ner-employment", fn=fetch_ner_employment, kind="download"),
    NodeSpec(id="adp-pay-insights", fn=fetch_pay_insights, kind="download"),
]
