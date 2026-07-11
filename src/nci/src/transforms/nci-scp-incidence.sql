-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the latest State Cancer Profiles incidence cross-section, not an annual time series; rows include the national total and state or territory areas.
SELECT
    "area",
    "fips",
    CAST("rate" AS DOUBLE) AS rate,
    CAST("rate_lower_ci" AS DOUBLE) AS rate_lower_ci,
    CAST("rate_upper_ci" AS DOUBLE) AS rate_upper_ci,
    CAST("avg_annual_count" AS BIGINT) AS avg_annual_count,
    "recent_trend",
    "recent_5yr_trend_pct",
    "cancer_code",
    "cancer_label",
    CAST("sex_code" AS BIGINT) AS sex_code,
    "sex_label"
FROM "nci-scp-incidence"
