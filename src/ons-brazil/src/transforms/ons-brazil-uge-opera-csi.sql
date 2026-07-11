-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("dat_verificada", '%Y-%m-%d')::DATE AS dat_verificada,
    "hora_verificada",
    "tip_usina",
    "nom_usina",
    "nom_unidadegeradora",
    CAST("cod_usinadpp" AS BIGINT) AS cod_usinadpp,
    "cod_ugedpp",
    "cod_pontomedicao",
    "flg_operasincrono",
    "dsc_comentario",
    "flg_sincrono"
FROM "ons-brazil-uge-opera-csi"
