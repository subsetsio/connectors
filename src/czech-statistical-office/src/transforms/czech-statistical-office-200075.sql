-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("casz_cis" AS BIGINT) AS casz_cis,
    "casz_kod",
    CAST("stavprace_cis" AS BIGINT) AS stavprace_cis,
    "stavprace_kod",
    CAST("oceneni_cis" AS BIGINT) AS oceneni_cis,
    "oceneni_kod",
    CAST("ocisteni_cis" AS BIGINT) AS ocisteni_cis,
    "ocisteni_kod",
    CAST("mesic" AS BIGINT) AS mesic,
    CAST("rok" AS BIGINT) AS rok,
    CAST("mesicz" AS BIGINT) AS mesicz,
    CAST("rokz" AS BIGINT) AS rokz,
    "stapro_txt",
    "casz_txt",
    "stavprace_txt",
    "oceneni_txt",
    "ocisteni_txt"
FROM "czech-statistical-office-200075"
