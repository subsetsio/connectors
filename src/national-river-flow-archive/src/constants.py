SLUG = "national-river-flow-archive"
BASE = "https://nrfaapps.ceh.ac.uk/nrfa/ws"

# Time-series data-type feeds (rank-accepted). Each is one download node that
# pulls the series across every station that offers it, plus its transform.
TIMESERIES_TYPES = [
    "gdf",
    "ndf",
    "gmf",
    "nmf",
    "cdr",
    "cmr",
    "amax-flow",
    "amax-stage",
    "pot-flow",
    "pot-stage",
]

# How each data type's value column and date column are typed/named downstream.
# kind: "daily" -> DATE token "YYYY-MM-DD"
#       "monthly" -> "YYYY-MM" (published as first-of-month DATE)
#       "event"  -> "YYYY-MM-DDThh:mm:ss" instantaneous peak (published TIMESTAMP)
FEED_SHAPE = {
    "gdf": ("daily", "flow_m3s"),
    "ndf": ("daily", "flow_m3s"),
    "cdr": ("daily", "rainfall_mm"),
    "gmf": ("monthly", "flow_m3s"),
    "nmf": ("monthly", "flow_m3s"),
    "cmr": ("monthly", "rainfall_mm"),
    "amax-flow": ("event", "flow_m3s"),
    "pot-flow": ("event", "flow_m3s"),
    "amax-stage": ("event", "stage_m"),
    "pot-stage": ("event", "stage_m"),
}
