-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "status",
    "no_of_inhalant_abusers_arrested"
FROM "sg-data-d-41ec44c6ad0613d2bbc7717589da30bb"
