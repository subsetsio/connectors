-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified for this upstream table; treat rows as source observations and avoid assuming uniqueness without applying source-specific dimensions.
SELECT
    "lokalizace",
    "op_lau1_kod",
    "op_okres",
    CAST("op_orp_kod" AS BIGINT) AS op_orp_kod,
    "op_orp",
    CAST("op_obec_kod" AS BIGINT) AS op_obec_kod,
    "op_obec",
    "doj_lau1_kod",
    "doj_okres",
    CAST("doj_orp_kod" AS BIGINT) AS doj_orp_kod,
    "doj_orp",
    CAST("doj_obec_kod" AS BIGINT) AS doj_obec_kod,
    "doj_obec",
    CAST("dojizdka_prace" AS BIGINT) AS dojizdka_prace,
    CAST("dojizdka_skola" AS BIGINT) AS dojizdka_skola,
    CAST("dojizdka_celkova" AS BIGINT) AS dojizdka_celkova,
    CAST("dojizdka_celkova_denni" AS BIGINT) AS dojizdka_celkova_denni
FROM "czech-statistical-office-sldb2021-dojizdka-obce"
