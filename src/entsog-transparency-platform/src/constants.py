"""Static configuration for the ENTSOG Transparency Platform connector.

`ENTITIES` maps each download spec's lowercased id-suffix (the slug-stripped
NodeSpec id) to the real, case-sensitive ENTSOG API endpoint path. The spec id
is `f"entsog-transparency-platform-{entity_id.lower().replace('_','-')}"`, so the
suffix loses the original camelCase — this table recovers it.
"""

# slug-stripped, lowercased spec suffix -> real ENTSOG endpoint path
ENTITIES = {
    "operationaldata": "operationaldata",
    "operatorpointdirections": "operatorpointdirections",
    "interruptions": "interruptions",
    "cmpunavailables": "cmpUnavailables",
    "cmpunsuccessfulrequests": "cmpUnsuccessfulRequests",
    "tariffssimulations": "tariffssimulations",
    "urgentmarketmessages": "urgentmarketmessages",
}

# The date-filtered operationaldata endpoint only serves rows from ~2021-02
# (Jan 2021 and earlier return HTTP 404 "no result"). We start the monthly
# crawl a month early; empty/404 months are skipped, so this floor is resilient
# to the source extending its history backwards without a code change.
SOURCE_MIN_YEAR = 2021
SOURCE_MIN_MONTH = 1
