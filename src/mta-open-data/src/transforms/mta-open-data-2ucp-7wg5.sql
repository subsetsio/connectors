-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "valid_from",
    "valid_to",
    "in_effect",
    "route_id",
    "route_short_name",
    "route_long_name",
    "route_description",
    "route_color",
    "stop_id",
    "stop_name",
    "direction_id",
    "direction",
    "revenue_stop",
    "timepoint",
    "boarding",
    "alighting",
    "is_cbd",
    "latitude",
    "longitude",
    "bundle",
    "georeference"
FROM "mta-open-data-2ucp-7wg5"
