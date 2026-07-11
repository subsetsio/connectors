-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the latest State Cancer Profiles mortality cross-section, not an annual time series; rows include the national total and state or territory areas.
SELECT
    "area",
    "fips",
    "rate",
    "rate_lower_ci",
    "rate_upper_ci",
    "avg_annual_count",
    "recent_trend",
    "recent_5yr_trend_pct",
    "cancer_code",
    "cancer_label",
    CAST("sex_code" AS BIGINT) AS sex_code,
    "sex_label"
FROM "nci-scp-mortality"
