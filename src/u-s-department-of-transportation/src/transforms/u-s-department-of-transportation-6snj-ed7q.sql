-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "docket_number",
    CAST("usdot_number" AS BIGINT) AS usdot_number,
    "co_name",
    "street_po",
    "city",
    "state_code",
    "zip_code",
    "ctry_code"
FROM "u-s-department-of-transportation-6snj-ed7q"
