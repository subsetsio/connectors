-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The verified row identity includes storage values because the source does not expose a stable subsystem observation id.
SELECT
    "id_subsistema",
    "nom_subsistema",
    strptime("ear_data", '%Y-%m-%d')::DATE AS ear_data,
    CAST("ear_max_subsistema" AS DOUBLE) AS ear_max_subsistema,
    CAST("ear_verif_subsistema_mwmes" AS DOUBLE) AS ear_verif_subsistema_mwmes,
    CAST("ear_verif_subsistema_percentual" AS DOUBLE) AS ear_verif_subsistema_percentual
FROM "ons-brazil-ear-diario-por-subsistema"
