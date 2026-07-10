from nodes.fiw_all_data import _DOWNLOAD_SPECS as FIW_ALL_DATA_SPECS
from nodes.fiw_all_data import fetch_fiw_all_data
from nodes.fiw_ratings_statuses import _DOWNLOAD_SPECS as FIW_RATINGS_STATUSES_SPECS
from nodes.fiw_ratings_statuses import fetch_fiw_ratings_statuses
from nodes.freedom_of_the_press import _DOWNLOAD_SPECS as FREEDOM_OF_THE_PRESS_SPECS
from nodes.freedom_of_the_press import fetch_freedom_of_the_press
from nodes.freedom_on_the_net import _DOWNLOAD_SPECS as FREEDOM_ON_THE_NET_SPECS
from nodes.freedom_on_the_net import fetch_freedom_on_the_net
from nodes.nations_in_transit import _DOWNLOAD_SPECS as NATIONS_IN_TRANSIT_SPECS
from nodes.nations_in_transit import fetch_nations_in_transit

DOWNLOAD_SPECS = [
    *FIW_ALL_DATA_SPECS,
    *FIW_RATINGS_STATUSES_SPECS,
    *FREEDOM_OF_THE_PRESS_SPECS,
    *FREEDOM_ON_THE_NET_SPECS,
    *NATIONS_IN_TRANSIT_SPECS,
]
