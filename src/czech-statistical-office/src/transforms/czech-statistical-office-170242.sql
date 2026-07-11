-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("ekonaktiv_cis" AS BIGINT) AS ekonaktiv_cis,
    CAST("ekonaktiv_kod" AS BIGINT) AS ekonaktiv_kod,
    CAST("uzemiz_cis" AS BIGINT) AS uzemiz_cis,
    CAST("uzemiz_kod" AS BIGINT) AS uzemiz_kod,
    CAST("uzemido_cis" AS BIGINT) AS uzemido_cis,
    CAST("uzemido_kod" AS BIGINT) AS uzemido_kod,
    strptime("datum", '%Y-%m-%d')::DATE AS datum,
    "uzemiz_txt",
    "uzemido_txt"
FROM "czech-statistical-office-170242"
