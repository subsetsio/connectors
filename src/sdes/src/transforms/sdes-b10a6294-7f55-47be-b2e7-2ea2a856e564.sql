-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "POLLUANT" AS polluant,
    "TYPOLOGIE" AS typologie,
    "INDICE" AS indice
FROM "sdes-b10a6294-7f55-47be-b2e7-2ea2a856e564"
