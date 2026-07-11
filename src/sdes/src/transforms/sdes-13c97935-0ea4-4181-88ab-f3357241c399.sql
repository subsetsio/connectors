-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "ZONE" AS zone,
    "NATURE_PROJET" AS nature_projet,
    "MEV" AS mev,
    "RESA" AS resa,
    "ANNUL" AS annul,
    "STOCK" AS stock
FROM "sdes-13c97935-0ea4-4181-88ab-f3357241c399"
