-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "ZONE_ENS" AS zone_ens,
    "RESA" AS resa
FROM "sdes-9cbf90ed-d50d-4f03-b19e-9c21616c9098"
