-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "TYPE_CODE" AS type_code,
    "TYPE_LIBELLE" AS type_libelle,
    "PAYS_ORIG_CODE" AS pays_orig_code,
    "PAYS_ORIG_LIBELLE" AS pays_orig_libelle,
    "PAYS_DEST_CODE" AS pays_dest_code,
    "PAYS_DEST_LIBELLE" AS pays_dest_libelle,
    "REG_ORIG_CODE" AS reg_orig_code,
    "REG_ORIG_LIBELLE" AS reg_orig_libelle,
    "REG_DEST_CODE" AS reg_dest_code,
    "REG_DEST_LIBELLE" AS reg_dest_libelle,
    "TONNES" AS tonnes,
    "TKM" AS tkm
FROM "sdes-f00e7c3b-c732-477c-872e-4a8ca1c0d7d9"
