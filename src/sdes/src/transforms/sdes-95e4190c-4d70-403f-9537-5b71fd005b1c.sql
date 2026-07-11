-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "DEP_CODE" AS dep_code,
    "DEP_LIBELLE" AS dep_libelle,
    "TYPE_LGT" AS type_lgt,
    "MEV" AS mev,
    "RESA" AS resa,
    "ANNUL" AS annul,
    "STOCK" AS stock,
    "DELAI_ECOUL" AS delai_ecoul,
    "PRIX_M2" AS prix_m2,
    "PRIX_MOY_IND" AS prix_moy_ind
FROM "sdes-95e4190c-4d70-403f-9537-5b71fd005b1c"
