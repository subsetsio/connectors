-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("dsz_cis" AS BIGINT) AS dsz_cis,
    CAST("dsz_kod" AS BIGINT) AS dsz_kod,
    CAST("rok" AS BIGINT) AS rok,
    CAST("obec_kod" AS BIGINT) AS obec_kod,
    "obec_txt",
    CAST("okres_kod" AS BIGINT) AS okres_kod,
    "okres_txt",
    "dsz_txt"
FROM "czech-statistical-office-190037"
