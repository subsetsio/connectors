-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "division",
    "car_class",
    "total_miles",
    "number_of_failures",
    "number_of_cars",
    "mdbf",
    "_12_month_average_mdbf" AS "12_month_average_mdbf"
FROM "mta-open-data-e2qc-xgxs"
