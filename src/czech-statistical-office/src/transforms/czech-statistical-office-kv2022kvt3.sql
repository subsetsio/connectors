-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_member",
    CAST("DATUMVOLEB" AS BIGINT) AS datumvoleb,
    CAST("ID_OKRSKY" AS BIGINT) AS id_okrsky,
    CAST("KRAJ" AS BIGINT) AS kraj,
    CAST("OKRES" AS BIGINT) AS okres,
    CAST("OBEC" AS BIGINT) AS obec,
    CAST("OKRSEK" AS BIGINT) AS okrsek,
    CAST("TYPZASTUP" AS BIGINT) AS typzastup,
    CAST("COBVODU" AS BIGINT) AS cobvodu,
    CAST("VOL_SEZNAM" AS BIGINT) AS vol_seznam,
    CAST("VYD_OBALKY" AS BIGINT) AS vyd_obalky,
    CAST("ODEVZ_OBAL" AS BIGINT) AS odevz_obal,
    CAST("PL_HL_CELK" AS BIGINT) AS pl_hl_celk,
    CAST("POCET_VS" AS BIGINT) AS pocet_vs,
    CAST("POC_VS_HL" AS BIGINT) AS poc_vs_hl,
    CAST("KODZASTUP" AS BIGINT) AS kodzastup
FROM "czech-statistical-office-kv2022kvt3"
