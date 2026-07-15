-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "institution_type",
    "no_of_visits"
FROM "sg-data-d-1f13195bc2a16584c52bd8bec993b5e3"
