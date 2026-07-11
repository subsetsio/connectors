-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "REGION_CODE" AS region_code,
    "REGION_LIBELLE" AS region_libelle,
    "RESA" AS resa
FROM "sdes-f84c3042-c01f-4784-a454-c89aff92818f"
