-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "PAYS_ORIG_CODE" AS pays_orig_code,
    "PAYS_ORIG_LIBELLE" AS pays_orig_libelle,
    "REG_ORIG_CODE" AS reg_orig_code,
    "REG_ORIG_LIBELLE" AS reg_orig_libelle,
    "TYPE_CODE" AS type_code,
    "TYPE_LIBELLE" AS type_libelle,
    "REGR_NST_CODE" AS regr_nst_code,
    "REGR_NST_LIBELLE" AS regr_nst_libelle,
    "NST_2_CODE" AS nst_2_code,
    "NST_2_LIBELLE" AS nst_2_libelle,
    "PAYS_DEST_CODE" AS pays_dest_code,
    "PAYS_DEST_LIBELLE" AS pays_dest_libelle,
    "REG_DEST_CODE" AS reg_dest_code,
    "REG_DEST_LIBELLE" AS reg_dest_libelle,
    "TONNES" AS tonnes,
    "TKM" AS tkm
FROM "sdes-a1681dc6-e72d-4205-8d57-412132347d28"
