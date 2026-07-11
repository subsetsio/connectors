-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "ZONE_ABC" AS zone_abc,
    "MEV" AS mev,
    "RESA" AS resa,
    "STOCK" AS stock
FROM "sdes-0dcbc5ca-8397-46eb-8554-b3a4b07f6b57"
