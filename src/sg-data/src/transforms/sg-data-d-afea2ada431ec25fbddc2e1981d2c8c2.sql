-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_case_type",
    "main_category",
    "subcategory",
    "count"
FROM "sg-data-d-afea2ada431ec25fbddc2e1981d2c8c2"
