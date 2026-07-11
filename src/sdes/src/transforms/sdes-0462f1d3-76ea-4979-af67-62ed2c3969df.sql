-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "REG_ORIG_CODE" AS reg_orig_code,
    "REG_ORIG_LIBELLE" AS reg_orig_libelle,
    "TYPE_CODE" AS type_code,
    "TYPE_LIBELLE" AS type_libelle,
    "COND_CODE" AS cond_code,
    "COND_LIBELLE" AS cond_libelle,
    "DIVNST_CODE" AS divnst_code,
    "DIVNST_LIBELLE" AS divnst_libelle,
    "PAV_CODE" AS pav_code,
    "PAV_LIBELLE" AS pav_libelle,
    "DEPT_ORIG_CODE" AS dept_orig_code,
    "DEPT_ORIG_LIBELLE" AS dept_orig_libelle,
    "TONNES" AS tonnes,
    "TKM" AS tkm
FROM "sdes-0462f1d3-76ea-4979-af67-62ed2c3969df"
