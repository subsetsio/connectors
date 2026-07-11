-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "REG_DEST_CODE" AS reg_dest_code,
    "REG_DEST_LIBELLE" AS reg_dest_libelle,
    "TYPE_CODE" AS type_code,
    "TYPE_LIBELLE" AS type_libelle,
    "COND_CODE" AS cond_code,
    "COND_LIBELLE" AS cond_libelle,
    "DIVNST_CODE" AS divnst_code,
    "DIVNST_LIBELLE" AS divnst_libelle,
    "PAV_CODE" AS pav_code,
    "PAV_LIBELLE" AS pav_libelle,
    "DEPT_DEST_CODE" AS dept_dest_code,
    "DEPT_DEST_LIBELLE" AS dept_dest_libelle,
    "TONNES" AS tonnes,
    "TKM" AS tkm
FROM "sdes-755e0f05-acb0-4a44-b573-4f28bab81458"
