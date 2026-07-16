-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "car_number",
    "car_class",
    "object_description",
    "controller",
    "division",
    "in_service_date",
    "retirement_date",
    "object_year_built"
FROM "mta-open-data-kir5-i9xt"
