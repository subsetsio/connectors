-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "id",
    "created_at",
    "agency",
    "location_category",
    "location_name",
    "line_route_branch",
    "case_type",
    "category",
    "subcategory",
    "source_reporting",
    "status"
FROM "mta-open-data-nh7m-at3e"
