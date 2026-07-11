-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "NB_PIECES_IND" AS nb_pieces_ind,
    "MEV" AS mev,
    "RESA" AS resa,
    "STOCK" AS stock,
    "PRIX_MOY_IND" AS prix_moy_ind
FROM "sdes-ef5c7e5f-a286-45ef-82ef-31fd879e88ff"
