-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "REG_CODE" AS reg_code,
    "REG_LIBELLE" AS reg_libelle,
    "TYPE_FLUX_CODE" AS type_flux_code,
    "TYPE_FLUX_LIBELLE" AS type_flux_libelle,
    "TONNES" AS tonnes,
    "TKM" AS tkm
FROM "sdes-557246bf-d008-4c0b-b7b2-f29bace647e4"
