-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_member",
    CAST("idhod" AS BIGINT) AS idhod,
    "hodnota",
    "vuk",
    "vuk_text",
    CAST("obdobi" AS BIGINT) AS obdobi,
    CAST("rok" AS BIGINT) AS rok,
    "mesic",
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "uzemi_txt"
FROM "czech-statistical-office-250169r15"
