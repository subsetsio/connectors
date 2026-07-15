-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "operators",
    "call_success_rate"
FROM "sg-data-d-3333a6e762fa0388582dffd9c84e6163"
