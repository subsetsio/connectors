-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "ethnic_group",
    "average_age",
    "median_age"
FROM "sg-data-d-a24664d0ad7d21edfc7245e0195d7503"
