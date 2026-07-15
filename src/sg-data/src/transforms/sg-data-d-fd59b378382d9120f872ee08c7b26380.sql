-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "type_of_space",
    "development_status",
    "amount_of_space"
FROM "sg-data-d-fd59b378382d9120f872ee08c7b26380"
