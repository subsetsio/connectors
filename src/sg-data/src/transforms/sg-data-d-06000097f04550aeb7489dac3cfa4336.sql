-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_interest_groups",
    "no_of_interest_groups"
FROM "sg-data-d-06000097f04550aeb7489dac3cfa4336"
