-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "station_name",
    "station_complex",
    "lines",
    "historical",
    "borough",
    "county",
    "latitude",
    "longitude",
    "wifi_available",
    "at_t",
    "sprint",
    "t_mobile",
    "verizon",
    "location",
    "georeference"
FROM "mta-open-data-pwa9-tmie"
