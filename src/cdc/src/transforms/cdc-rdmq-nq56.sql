-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("week_end", '%Y-%m-%d')::DATE AS week_end,
    "geography",
    "county",
    CAST("percent_visits_combined" AS DOUBLE) AS percent_visits_combined,
    CAST("percent_visits_covid" AS DOUBLE) AS percent_visits_covid,
    CAST("percent_visits_influenza" AS DOUBLE) AS percent_visits_influenza,
    CAST("percent_visits_rsv" AS DOUBLE) AS percent_visits_rsv,
    CAST("percent_visits_smoothed_combined" AS DOUBLE) AS percent_visits_smoothed_combined,
    CAST("percent_visits_smoothed_covid" AS DOUBLE) AS percent_visits_smoothed_covid,
    CAST("percent_visits_smoothed_influenza" AS DOUBLE) AS percent_visits_smoothed_influenza,
    CAST("percent_visits_smoothed_rsv" AS DOUBLE) AS percent_visits_smoothed_rsv,
    "ed_trends_covid",
    "ed_trends_influenza",
    "ed_trends_rsv",
    "hsa",
    "hsa_counties",
    "hsa_nci_id",
    CAST("fips" AS BIGINT) AS fips,
    "trend_source",
    strptime("BuildNumber", '%Y-%m-%d')::DATE AS buildnumber
FROM "cdc-rdmq-nq56"
