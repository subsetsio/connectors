from nodes.fiw_all_data import fetch_fiw_all_data
from nodes.fiw_ratings_statuses import fetch_fiw_ratings_statuses
from nodes.freedom_of_the_press import fetch_freedom_of_the_press
from nodes.freedom_on_the_net import fetch_freedom_on_the_net
from nodes.nations_in_transit import fetch_nations_in_transit
from subsets_utils import NodeSpec

DOWNLOAD_SPECS = [
    NodeSpec(id="freedom-house-fiw-all-data", fn=fetch_fiw_all_data, kind="download"),
    NodeSpec(id="freedom-house-fiw-ratings-statuses", fn=fetch_fiw_ratings_statuses, kind="download"),
    NodeSpec(id="freedom-house-freedom-of-the-press", fn=fetch_freedom_of_the_press, kind="download"),
    NodeSpec(id="freedom-house-freedom-on-the-net", fn=fetch_freedom_on_the_net, kind="download"),
    NodeSpec(id="freedom-house-nations-in-transit", fn=fetch_nations_in_transit, kind="download"),
]
