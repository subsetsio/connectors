-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes the overseas départements and the aggregate pseudo-départements used by the indicator tables, so a plain row count is not the number of real départements.
SELECT
    "reg_code",
    "reg_name",
    "dep_code",
    "dep_name",
    "dep_name_upper",
    "dep_type",
    "tri"
FROM "cnam-referentiel-departements"
