-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("DRUHZVIRE_cis" AS BIGINT) AS druhzvire_cis,
    CAST("DRUHZVIRE_kod" AS BIGINT) AS druhzvire_kod,
    CAST("refobdobi" AS BIGINT) AS refobdobi,
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "STAPRO_TXT" AS stapro_txt,
    "uzemi_txt",
    "DRUHZVIRE_txt" AS druhzvire_txt
FROM "czech-statistical-office-270230"
