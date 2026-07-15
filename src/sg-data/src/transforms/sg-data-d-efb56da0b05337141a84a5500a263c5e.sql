-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "mother_age",
    "child_birth_weight",
    "child_gender",
    "period_of_gestation",
    "still_births_count"
FROM "sg-data-d-efb56da0b05337141a84a5500a263c5e"
