-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "facility_id",
    "facility_name",
    "collisions",
    "collisions_with_injuries",
    "crossings",
    "collisions_per_million",
    "collisions_with_injuries_per_million_crossings"
FROM "mta-open-data-2wqd-qady"
