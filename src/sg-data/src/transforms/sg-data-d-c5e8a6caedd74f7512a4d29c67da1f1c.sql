-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "occupation",
    "recruitment_rate"
FROM "sg-data-d-c5e8a6caedd74f7512a4d29c67da1f1c"
