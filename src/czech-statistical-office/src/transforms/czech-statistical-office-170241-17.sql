-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_member",
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    "stapro_txt",
    strptime("datum", '%Y-%m-%d')::DATE AS datum,
    "zsjd_kod",
    "zsjd_txt",
    CAST("obec_kod" AS BIGINT) AS obec_kod,
    "obec_txt"
FROM "czech-statistical-office-170241-17"
