import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from consumer_complaints import _DOWNLOAD_SPECS as _COMPLAINT_SPECS
from credit_trends import _DOWNLOAD_SPECS as _CREDIT_TRENDS_SPECS
from hmda import _DOWNLOAD_SPECS as _HMDA_SPECS
from mortgage_performance import _DOWNLOAD_SPECS as _MORTGAGE_PERFORMANCE_SPECS


DOWNLOAD_SPECS = [
    *_CREDIT_TRENDS_SPECS,
    *_COMPLAINT_SPECS,
    *_HMDA_SPECS,
    *_MORTGAGE_PERFORMANCE_SPECS,
]
