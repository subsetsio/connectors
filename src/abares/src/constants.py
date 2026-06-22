# ABARES entity union — the rank-accepted, reliably-fetchable datasets.
# Copied from data/sources/abares/work/entity_union.json.
# NOTE: ABARES publishes 338 packages on data.gov.au, but ~56 of the tabular
# ones link only to the decommissioned data.daff.gov.au warehouse (broken TLS
# cert, host mostly unreachable). The datasets below are the ones whose primary
# tabular resource is served from data.gov.au's own storage / CKAN datastore.
ENTITY_IDS = [
    "agricultural-commodities-march-quarter-2018",
    "australia-s-indigenous-land-and-forest-estate-2024",
    "australian-crop-report-february-2018-no-185",
    "fires-in-australia-s-forests-2016-21-2024",
    "forests-of-australia-2023",
]
