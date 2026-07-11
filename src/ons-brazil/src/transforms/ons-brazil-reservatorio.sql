-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nom_reservatorio",
    "tip_reservatorio",
    "cod_resplanejamento",
    "cod_posto",
    "nom_usina",
    "ceg",
    "id_subsistema",
    "nom_subsistema",
    "nom_bacia",
    "nom_rio",
    "nom_ree",
    strptime("dat_entrada", '%Y-%m-%d')::DATE AS dat_entrada,
    CAST("val_cotamaxima" AS DOUBLE) AS val_cotamaxima,
    CAST("val_cotaminima" AS DOUBLE) AS val_cotaminima,
    CAST("val_volmax" AS DOUBLE) AS val_volmax,
    CAST("val_volmin" AS DOUBLE) AS val_volmin,
    CAST("val_volutiltot" AS DOUBLE) AS val_volutiltot,
    "val_produtibilidadeespecifica",
    "val_produtividade65volutil",
    "val_tipoperda",
    "val_perda",
    "val_latitude",
    "val_longitude",
    "res_id"
FROM "ons-brazil-reservatorio"
