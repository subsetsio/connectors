-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The verified row identity includes the interchange value because the source does not expose a stable border-flow observation id.
SELECT
    "din_instante",
    "nom_paisdestino",
    CAST("val_intercambiomwmed" AS DOUBLE) AS val_intercambiomwmed,
    CAST("val_intercambioprogmwmed" AS DOUBLE) AS val_intercambioprogmwmed
FROM "ons-brazil-intercambio-internacional"
