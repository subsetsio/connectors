-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_member",
    CAST("ID_OKRSKY" AS BIGINT) AS id_okrsky,
    CAST("TYP_FORM" AS BIGINT) AS typ_form,
    CAST("OPRAVA" AS BIGINT) AS oprava,
    CAST("CHYBA" AS BIGINT) AS chyba,
    CAST("OKRES" AS BIGINT) AS okres,
    CAST("OBEC" AS BIGINT) AS obec,
    CAST("OKRSEK" AS BIGINT) AS okrsek,
    CAST("KC_1" AS BIGINT) AS kc_1,
    CAST("VOL_SEZNAM" AS BIGINT) AS vol_seznam,
    CAST("VYD_OBALKY" AS BIGINT) AS vyd_obalky,
    CAST("ODEVZ_OBAL" AS BIGINT) AS odevz_obal,
    CAST("PL_HL_CELK" AS BIGINT) AS pl_hl_celk,
    CAST("KC_2" AS BIGINT) AS kc_2,
    "ZAKRSTRANA" AS zakrstrana
FROM "czech-statistical-office-kz2024kzt6"
