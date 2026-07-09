-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes overseas régions and the aggregate pseudo-régions used by the indicator tables.
SELECT
    "reg_code",
    "reg_name",
    "reg_name_upper",
    "reg_type",
    "tri"
FROM "cnam-referentiel-regions"
