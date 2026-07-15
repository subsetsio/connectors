-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "status",
    "age_group",
    "no_of_inhalant_abusers_arrested"
FROM "sg-data-d-06dec2e253224d72d528ddf39f57a548"
