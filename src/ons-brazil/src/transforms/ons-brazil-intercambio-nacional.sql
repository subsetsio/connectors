-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "din_instante",
    "id_subsistema_origem",
    "nom_subsistema_origem",
    "id_subsistema_destino",
    "nom_subsistema_destino",
    CAST("val_intercambiomwmed" AS DOUBLE) AS val_intercambiomwmed,
    CAST("val_intercambioprogmwmed" AS DOUBLE) AS val_intercambioprogmwmed
FROM "ons-brazil-intercambio-nacional"
