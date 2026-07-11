-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "ZONE_ABC" AS zone_abc,
    "RESA" AS resa
FROM "sdes-039fb42a-e06a-46a0-bacc-8e47f57f3483"
