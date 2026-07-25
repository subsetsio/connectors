-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("perf_year" AS BIGINT) AS perf_year,
    "STATE_NAME" AS state_name,
    "COUNTY_NAME" AS county_name,
    "STATE_ID" AS state_id,
    "COUNTY_ID" AS county_id,
    CAST("expnd_pbpm_ad" AS DOUBLE) AS expnd_pbpm_ad,
    CAST("avg_prosp_risk_score_ad" AS DOUBLE) AS avg_prosp_risk_score_ad,
    CAST("elig_months_ad" AS BIGINT) AS elig_months_ad,
    "EXPND_PBPM_ESRD" AS expnd_pbpm_esrd,
    "AVG_PROSP_RISK_SCORE_ESRD" AS avg_prosp_risk_score_esrd,
    "ELIG_MONTHS_ESRD" AS elig_months_esrd
FROM "cms-54551982-39a8-4744-90f6-c38bb4dd5108"
