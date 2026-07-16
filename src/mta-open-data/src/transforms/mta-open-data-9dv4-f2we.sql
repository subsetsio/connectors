-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "shape_id",
    "shape",
    "station_name",
    "agency",
    "division",
    "borough",
    "shape_length",
    "shape_area"
FROM "mta-open-data-9dv4-f2we"
