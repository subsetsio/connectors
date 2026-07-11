-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified for this upstream table; treat rows as source observations and avoid assuming uniqueness without applying source-specific dimensions.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    "vuk",
    "vuk_text",
    CAST("vuzemi_cis" AS BIGINT) AS vuzemi_cis,
    "vuzemi_kod",
    "vuzemi_txt",
    CAST("rok" AS BIGINT) AS rok,
    strptime("casref_od", '%Y-%m-%d')::DATE AS casref_od,
    strptime("casref_do", '%Y-%m-%d')::DATE AS casref_do,
    "ER_kod" AS er_kod
FROM "czech-statistical-office-340131"
