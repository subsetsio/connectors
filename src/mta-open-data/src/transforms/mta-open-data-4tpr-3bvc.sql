-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "week",
    "day_type",
    "borough",
    "route",
    "direction",
    "hour",
    "load_percentage",
    "trips_with_apc"
FROM "mta-open-data-4tpr-3bvc"
