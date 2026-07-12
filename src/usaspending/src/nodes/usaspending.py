"""Canonical USAspending node module.

The implementation is split by endpoint family; this module exposes the
combined specs at the path the factory harness expects.
"""

from subsets_utils import NodeSpec

from nodes.monthly_spending import fetch_monthly_spending
from nodes.spending_dimensions import fetch_spending_dimension

DOWNLOAD_SPECS = [
    NodeSpec(id="usaspending-monthly-spending-by-award-type", fn=fetch_monthly_spending, kind="download"),
    NodeSpec(id="usaspending-spending-by-agency", fn=fetch_spending_dimension, kind="download"),
    NodeSpec(id="usaspending-spending-by-budget-function", fn=fetch_spending_dimension, kind="download"),
    NodeSpec(id="usaspending-spending-by-budget-subfunction", fn=fetch_spending_dimension, kind="download"),
    NodeSpec(id="usaspending-spending-by-object-class", fn=fetch_spending_dimension, kind="download"),
    NodeSpec(id="usaspending-spending-by-federal-account", fn=fetch_spending_dimension, kind="download"),
    NodeSpec(id="usaspending-spending-by-program-activity", fn=fetch_spending_dimension, kind="download"),
]
