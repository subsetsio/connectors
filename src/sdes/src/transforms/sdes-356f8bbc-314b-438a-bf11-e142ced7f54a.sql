-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "NATURE_PROJET" AS nature_projet,
    "NB_PIECES_COLL" AS nb_pieces_coll,
    "MEV" AS mev,
    "RESA" AS resa,
    "ANNUL" AS annul,
    "STOCK" AS stock,
    "DELAI_ECOUL" AS delai_ecoul,
    "PRIX_M2" AS prix_m2
FROM "sdes-356f8bbc-314b-438a-bf11-e142ced7f54a"
