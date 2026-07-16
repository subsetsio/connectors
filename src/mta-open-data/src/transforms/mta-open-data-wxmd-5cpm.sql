-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "railroad",
    "code",
    "station_name",
    "branch",
    "latitude",
    "longitude",
    "outbound_title",
    "inbound_title",
    "zone",
    "station_url",
    "parking_map_url",
    "accessibility",
    "georeference"
FROM "mta-open-data-wxmd-5cpm"
