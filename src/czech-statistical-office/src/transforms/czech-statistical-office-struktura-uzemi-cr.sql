-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("platnost_datum", '%Y-%m-%d')::DATE AS platnost_datum,
    "obec_text",
    CAST("obec_kod" AS BIGINT) AS obec_kod,
    "obec_typ",
    "pou_text",
    CAST("pou_csu_cis61_kod" AS BIGINT) AS pou_csu_cis61_kod,
    CAST("pou_ruian_kod" AS BIGINT) AS pou_ruian_kod,
    CAST("pou_sidlo_obec_kod" AS BIGINT) AS pou_sidlo_obec_kod,
    "orp_text",
    CAST("orp_csu_cis65_kod" AS BIGINT) AS orp_csu_cis65_kod,
    CAST("orp_ruian_kod" AS BIGINT) AS orp_ruian_kod,
    CAST("orp_sidlo_obec_kod" AS BIGINT) AS orp_sidlo_obec_kod,
    "okres_text",
    CAST("okres_csu_cis101_lau_kod" AS BIGINT) AS okres_csu_cis101_lau_kod,
    "okres_csu_cis109_nuts_kod",
    CAST("okres_ruian_kod" AS BIGINT) AS okres_ruian_kod,
    "kraj_text",
    "kraj_zkratka",
    CAST("kraj_csu_cis100_kod" AS BIGINT) AS kraj_csu_cis100_kod,
    "kraj_csu_cis108_nuts_kod",
    CAST("kraj_ruian_vusc_kod" AS BIGINT) AS kraj_ruian_vusc_kod,
    "region_text",
    CAST("region_csu_cis99_kod" AS BIGINT) AS region_csu_cis99_kod,
    "region_csu_cis107_nuts_kod",
    CAST("region_ruian_kod" AS BIGINT) AS region_ruian_kod,
    "stat_text",
    CAST("stat_csu_cis97_kod" AS BIGINT) AS stat_csu_cis97_kod,
    "stat_csu_cis105_nuts_kod",
    CAST("stat_ruian_kod" AS BIGINT) AS stat_ruian_kod,
    "odkaz_SMS" AS odkaz_sms,
    "odkaz_RSO" AS odkaz_rso
FROM "czech-statistical-office-struktura-uzemi-cr"
