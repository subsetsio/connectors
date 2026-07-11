-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "NATURE_PROJET" AS nature_projet,
    "NB_PIECES_IND" AS nb_pieces_ind,
    "MEV" AS mev,
    "RESA" AS resa,
    "ANNUL" AS annul,
    "STOCK" AS stock,
    "DELAI_ECOUL" AS delai_ecoul,
    "PRIX_MOY_IND" AS prix_moy_ind
FROM "sdes-0018cbe0-cdb0-4846-9baa-382bc87b2d9a"
