-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "housing_schm_type",
    "no_of_mbrs"
FROM "sg-data-d-3d6dab1e71a8176ae2155b161f9c6b70"
