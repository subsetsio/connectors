"""Catalog metadata for the MPA (data.gov.sg) connector.

This is DATA, not logic: which datasets we pull (the rank-accepted entity union)
and each dataset's column shape, observed by probing the datastore_search API.
The node module imports these to build DOWNLOAD_SPECS / TRANSFORM_SPECS.

SCHEMA shape per datasetId:
  period:     name of the time column -> "month" ('YYYY-MM' text) or "year" (text 'YYYY')
  categories: ordered list of dimension columns (kept as text)
  values:     numeric measure columns (cast to DOUBLE in the transform)
"""

SCHEMAS = {
    # Bunker Sales
    "d_0a76d48f3754aafd08f98629324a54c6": {"period": "year",  "categories": ["bunker_type"], "values": ["bunker_sales"]},
    "d_4f5abbf4486bf8e52bbed3be56dde562": {"period": "month", "categories": ["bunker_type"], "values": ["bunker_sales"]},
    "d_ccb330e6679674ffaa330dc76136e198": {"period": "year",  "categories": [],             "values": ["bunker_sales"]},
    "d_89d2874dad74a273270369334f1e7d28": {"period": "month", "categories": [],             "values": ["bunker_sales"]},
    # Cargo Throughput
    "d_a30479ad55e045bcaffacf587d05966c": {"period": "year",  "categories": ["cargo_type_primary", "cargo_type_secondary"], "values": ["cargo_throughput"]},
    "d_835d43b9238c6fc877dfcd62d73054a9": {"period": "month", "categories": ["cargo_type_primary", "cargo_type_secondary"], "values": ["cargo_throughput"]},
    "d_8ab8d71a6bf44097889dd6a3b4258928": {"period": "year",  "categories": [], "values": ["cargo_throughput"]},
    "d_042dd8b935eab998f389adaf559c80de": {"period": "month", "categories": [], "values": ["cargo_throughput"]},
    # Container Throughput
    "d_085682b824700b4e88d946529f503da0": {"period": "year",  "categories": [], "values": ["container_throughput"]},
    "d_da030f7028200d19ffcbe4a2d71af39c": {"period": "month", "categories": [], "values": ["container_throughput"]},
    # Registered Vessels and Shipping Tonnage
    "d_0c586210d33756a56ef6213078e749aa": {"period": "year",  "categories": [], "values": ["number_of_vessels", "gross_tonnage"]},
    "d_56f64b2d5a31eb0ee465cc51e83ac60a": {"period": "month", "categories": [], "values": ["number_of_vessels", "gross_tonnage"]},
    # Tanker Arrivals
    "d_1714a141d8bbf1996965eb3f71565525": {"period": "year",  "categories": ["category"], "values": ["number_of_tankers", "gross_tonnage"]},
    "d_c9dcfd8b85990669d1e74dd7ad71eb8b": {"period": "month", "categories": ["category"], "values": ["number_of_tankers", "gross_tonnage"]},
    "d_eb1c7c0c9ee013f9be42cc8abf523326": {"period": "year",  "categories": [], "values": ["number_of_tankers", "gross_tonnage"]},
    "d_9adb5ace517591edd9a8c88291ac1f1c": {"period": "month", "categories": [], "values": ["number_of_tankers", "gross_tonnage"]},
    # Vessel Arrivals (>75 GT)
    "d_b0c64c019b252698a9f1a222dcf9e0a6": {"period": "year",  "categories": ["vessel_type"], "values": ["number_of_vessels", "gross_tonnage"]},
    "d_8f264219109e61fffa87ac64dd5a9a65": {"period": "month", "categories": ["vessel_type"], "values": ["number_of_vessels", "gross_tonnage"]},
    "d_8392e9bea6ca351a38f67172ccdf6a6a": {"period": "year",  "categories": [], "values": ["number_of_vessels", "gross_tonnage"]},
    "d_d48c5a038904f6da3c603cd854b6c191": {"period": "month", "categories": [], "values": ["number_of_vessels", "gross_tonnage"]},
    # Vessel Calls (>75 GT)
    "d_60410de1bc1e63ddcf51a619081b11b3": {"period": "year",  "categories": ["purpose_type"], "values": ["number_of_vessel_calls", "gross_tonnage"]},
    "d_48cb38d12697d3463c8cadfb22e6c61d": {"period": "month", "categories": ["purpose_type"], "values": ["number_of_vessel_calls", "gross_tonnage"]},
}

ENTITY_IDS = list(SCHEMAS.keys())
