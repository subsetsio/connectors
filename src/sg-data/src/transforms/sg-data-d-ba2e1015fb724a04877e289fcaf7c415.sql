-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "school_type",
    "number_of_mixed_level_sch"
FROM "sg-data-d-ba2e1015fb724a04877e289fcaf7c415"
