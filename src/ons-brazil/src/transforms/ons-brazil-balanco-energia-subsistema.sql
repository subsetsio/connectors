-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Hourly subsystem energy balance rows contain multiple generation and load components; avoid summing all value columns as a single measure.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "din_instante",
    "val_gerhidraulica",
    "val_gertermica",
    "val_gereolica",
    "val_gersolar",
    "val_carga",
    "val_intercambio"
FROM "ons-brazil-balanco-energia-subsistema"
