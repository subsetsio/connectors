-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "TYPE_CODE" AS type_code,
    "TYPE_LIBELLE" AS type_libelle,
    "NST_2_CODE" AS nst_2_code,
    "NST_2_LIBELLE" AS nst_2_libelle,
    strptime("MOIS", '%Y-%m')::DATE AS mois,
    "RID_CODE" AS rid_code,
    "RID_LIBELLE" AS rid_libelle,
    "TONNES" AS tonnes,
    "TKM" AS tkm,
    "TRAINSKM" AS trainskm
FROM "sdes-b7894d99-9ae3-4520-837e-f4aa271793a3"
