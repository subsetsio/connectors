-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PERIODE" AS periode,
    "POLLUANT" AS polluant,
    "TYPOLOGIE" AS typologie,
    "POURC_STATION_DEP" AS pourc_station_dep
FROM "sdes-6bcf0cf8-c721-4de9-a964-f040cb2798ab"
