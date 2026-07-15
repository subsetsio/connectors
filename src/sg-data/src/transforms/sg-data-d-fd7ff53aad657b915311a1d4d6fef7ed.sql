-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "school_type",
    "teachers_preu"
FROM "sg-data-d-fd7ff53aad657b915311a1d4d6fef7ed"
