-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "NB_PIECES_COLL" AS nb_pieces_coll,
    "MEV" AS mev,
    "RESA" AS resa,
    "STOCK" AS stock,
    "PRIX_M2" AS prix_m2
FROM "sdes-6cf74a3f-911b-4ab9-9d1f-5bcfcd2abe9f"
