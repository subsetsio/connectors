"""Static configuration for the ENTSOG Transparency Platform connector.

`ENTITIES` maps each download spec's lowercased id-suffix (the slug-stripped
NodeSpec id) to the real, case-sensitive ENTSOG API endpoint path. The spec id
is `f"entsog-transparency-platform-{entity_id.lower().replace('_','-')}"`, so the
suffix loses the original camelCase — this table recovers it.
"""

# slug-stripped, lowercased spec suffix -> real ENTSOG endpoint path
ENTITIES = {
    "aggregateinterconnections": "aggregateInterconnections",
    "balancingzones": "balancingzones",
    "cmpunavailables": "cmpUnavailables",
    "cmpunsuccessfulrequests": "cmpUnsuccessfulRequests",
    "connectionpoints": "connectionpoints",
    "interconnections": "interconnections",
    "interruptions": "interruptions",
    "operationaldata": "operationaldata",
    "operatorpointdirections": "operatorpointdirections",
    "operators": "operators",
    "tariffssimulations": "tariffssimulations",
    "urgentmarketmessages": "urgentmarketmessages",
}

# Endpoints the API serves in full without a date filter: a single offset-paged
# sweep returns the whole (finite) corpus.
CATALOG_SUFFIXES = [s for s in ENTITIES if s != "operationaldata"]

# operationaldata is the one endpoint that must be windowed by date. Unfiltered
# and wide-window queries make the gateway time out (502/504); one calendar
# month per window keeps every request inside the server's 60s execution cap.
SOURCE_MIN_YEAR = 2021
SOURCE_MIN_MONTH = 1
