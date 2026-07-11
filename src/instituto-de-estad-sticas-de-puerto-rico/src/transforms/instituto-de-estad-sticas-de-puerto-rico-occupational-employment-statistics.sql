-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    CAST("AREA" AS BIGINT) AS area,
    "ST" AS st,
    "STATE" AS state,
    "OCC_CODE" AS occ_code,
    "OCC_TITLE" AS occ_title,
    "OCC_GROUP" AS occ_group,
    "TOT_EMP" AS tot_emp,
    "EMP_PRSE" AS emp_prse,
    "JOBS_1000" AS jobs_1000,
    "LOC_Q" AS loc_q,
    "H_MEAN" AS h_mean,
    "A_MEAN" AS a_mean,
    "MEAN_PRSE" AS mean_prse,
    "H_PCT10" AS h_pct10,
    "H_PCT25" AS h_pct25,
    "H_MEDIAN" AS h_median,
    "H_PCT75" AS h_pct75,
    "H_PCT90" AS h_pct90,
    "A_PCT10" AS a_pct10,
    "A_PCT25" AS a_pct25,
    "A_MEDIAN" AS a_median,
    "A_PCT75" AS a_pct75,
    "A_PCT90" AS a_pct90,
    CAST("ANNUAL" AS BOOLEAN) AS annual,
    CAST("HOURLY" AS BOOLEAN) AS hourly
FROM "instituto-de-estad-sticas-de-puerto-rico-occupational-employment-statistics"
