"""Download specs for the Park Attendance connector."""

from subsets_utils import NodeSpec

from nodes.attendance import fetch_attendance
from nodes.parks import fetch_parks


DOWNLOAD_SPECS = [
    NodeSpec(id="park-attendance-attendance", fn=fetch_attendance, kind="download"),
    NodeSpec(id="park-attendance-parks", fn=fetch_parks, kind="download"),
]
