-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "ZONE_ABC_IND" AS zone_abc_ind,
    "MEV" AS mev,
    "RESA" AS resa,
    "ANNUL" AS annul,
    "STOCK" AS stock,
    "DELAI_ECOUL" AS delai_ecoul,
    "PRIX_MOY_IND" AS prix_moy_ind
FROM "sdes-45411359-bcea-4d88-a513-1d655215fed5"
