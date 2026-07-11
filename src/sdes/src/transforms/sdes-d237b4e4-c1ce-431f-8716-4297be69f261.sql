-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PERIODE" AS periode,
    "POLLUANT" AS polluant,
    "TYPOLOGIE" AS typologie,
    "INDICATEUR_EXPO_MOY" AS indicateur_expo_moy,
    "OBJECTIF_2020" AS objectif_2020,
    "OBJECTIF_2025" AS objectif_2025,
    "OBJECTIF_2030" AS objectif_2030
FROM "sdes-d237b4e4-c1ce-431f-8716-4297be69f261"
