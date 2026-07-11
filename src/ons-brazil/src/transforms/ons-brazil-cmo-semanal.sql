-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "din_instante",
    CAST("val_cmomediasemanal" AS DOUBLE) AS val_cmomediasemanal,
    CAST("val_cmoleve" AS DOUBLE) AS val_cmoleve,
    CAST("val_cmomedia" AS DOUBLE) AS val_cmomedia,
    CAST("val_cmopesada" AS DOUBLE) AS val_cmopesada
FROM "ons-brazil-cmo-semanal"
