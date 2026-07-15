-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "mother_occupation",
    "order",
    "birth_count"
FROM "sg-data-d-cb058a2f7ee7aa5c6b1f0d8c7ef45f21"
