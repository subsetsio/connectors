-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nom_reservatorio",
    "cod_resplanejamento",
    "tip_reservatorio",
    "nom_bacia",
    "nom_ree",
    "id_subsistema",
    "nom_subsistema",
    "id_subsistema_jusante",
    "nom_subsistema_jusante",
    strptime("ear_data", '%Y-%m-%d')::DATE AS ear_data,
    "ear_reservatorio_subsistema_proprio_mwmes",
    "ear_reservatorio_subsistema_jusante_mwmes",
    "earmax_reservatorio_subsistema_proprio_mwmes",
    "earmax_reservatorio_subsistema_jusante_mwmes",
    "ear_reservatorio_percentual",
    CAST("ear_total_mwmes" AS DOUBLE) AS ear_total_mwmes,
    CAST("ear_maxima_total_mwmes" AS DOUBLE) AS ear_maxima_total_mwmes,
    CAST("val_contribearbacia" AS DOUBLE) AS val_contribearbacia,
    CAST("val_contribearmaxbacia" AS DOUBLE) AS val_contribearmaxbacia,
    CAST("val_contribearsubsistema" AS DOUBLE) AS val_contribearsubsistema,
    CAST("val_contribearmaxsubsistema" AS DOUBLE) AS val_contribearmaxsubsistema,
    CAST("val_contribearsubsistemajusante" AS DOUBLE) AS val_contribearsubsistemajusante,
    CAST("val_contribearmaxsubsistemajusante" AS DOUBLE) AS val_contribearmaxsubsistemajusante,
    CAST("val_contribearsin" AS DOUBLE) AS val_contribearsin,
    CAST("val_contribearmaxsin" AS DOUBLE) AS val_contribearmaxsin
FROM "ons-brazil-ear-diario-por-reservatorio"
