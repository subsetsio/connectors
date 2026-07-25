-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ai_use_case",
    "commercial_examples",
    CAST("agency_use_y_n" AS BOOLEAN) AS agency_use_y_n,
    "name_of_commercial_product",
    "estimated_of_licenses_users"
FROM "u-s-department-of-transportation-catv-cnxv"
