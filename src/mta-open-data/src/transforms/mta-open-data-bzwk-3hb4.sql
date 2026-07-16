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
    "trip_type",
    "route_type",
    "bundle",
    "route_color",
    "direction_id",
    "direction",
    "shape_id",
    "vertices",
    "shape_length",
    "min_longitude",
    "min_latitude",
    "max_longitude",
    "max_latitude",
    "geometry"
FROM "mta-open-data-bzwk-3hb4"
