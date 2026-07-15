-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "town_estate",
    "age_group",
    "percentage"
FROM "sg-data-d-c6edbb9c9c3ed1642a89e7515a6baca7"
