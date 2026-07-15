-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "ethnic_group",
    "household_size",
    "percentage"
FROM "sg-data-d-a5095643f088aafc71d5aeae09c1f08f"
