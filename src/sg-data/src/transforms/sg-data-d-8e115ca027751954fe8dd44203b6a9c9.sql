-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "housing_schm_type",
    "no_of_mbrs"
FROM "sg-data-d-8e115ca027751954fe8dd44203b6a9c9"
