from nodes.consumer_complaints import _DOWNLOAD_SPECS as _COMPLAINT_SPECS
from nodes.credit_trends import _DOWNLOAD_SPECS as _CREDIT_TRENDS_SPECS
from nodes.hmda import _DOWNLOAD_SPECS as _HMDA_SPECS
from nodes.mortgage_performance import _DOWNLOAD_SPECS as _MORTGAGE_PERFORMANCE_SPECS


DOWNLOAD_SPECS = [
    *_CREDIT_TRENDS_SPECS,
    *_COMPLAINT_SPECS,
    *_HMDA_SPECS,
    *_MORTGAGE_PERFORMANCE_SPECS,
]
