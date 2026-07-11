-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "REGION_CODE" AS region_code,
    "REGION_LIBELLE" AS region_libelle,
    "NATURE_PROJET" AS nature_projet,
    "TYPE_LGT" AS type_lgt,
    "MEV" AS mev,
    "RESA" AS resa,
    "ANNUL" AS annul,
    "STOCK" AS stock,
    "DELAI_ECOUL" AS delai_ecoul,
    "PRIX_M2" AS prix_m2,
    "PRIX_MOY_IND" AS prix_moy_ind
FROM "sdes-5f7f9846-0aad-47a0-91e8-4afa610f3f80"
