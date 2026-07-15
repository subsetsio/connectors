-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "order",
    "mother_race",
    "mother_age",
    "birth_count"
FROM "sg-data-d-aa2bc6e6570aa886f263ae7397e6bd1a"
