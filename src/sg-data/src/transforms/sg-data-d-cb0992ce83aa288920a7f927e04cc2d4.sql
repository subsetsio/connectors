-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "status",
    "race",
    "no_of_inhalant_abusers_arrested"
FROM "sg-data-d-cb0992ce83aa288920a7f927e04cc2d4"
