-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "NATURE_PROJET" AS nature_projet,
    "TYPE_LGT" AS type_lgt,
    "MEV" AS mev,
    "RESA" AS resa,
    "ANNUL" AS annul,
    "STOCK" AS stock,
    "DELAI_ECOUL" AS delai_ecoul,
    "PRIX_M2" AS prix_m2,
    "PRIX_MOY_IND" AS prix_moy_ind
FROM "sdes-6a038126-312a-4974-b5a6-c5a1394b4267"
