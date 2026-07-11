-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "POLLUANT" AS polluant,
    "TYPOLOGIE" AS typologie,
    "MOYENNE_ANNUELLE" AS moyenne_annuelle
FROM "sdes-9db8c875-10d8-49b3-ac30-1e6f358ab6b0"
