-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include both risk of diagnosis and risk of dying; filter stat_type before aggregating or comparing risk values.
SELECT
    "statistic",
    CAST("stat_type" AS BIGINT) AS stat_type,
    "stat_type_label",
    CAST("sex" AS BIGINT) AS sex,
    "sex_label",
    CAST("race" AS BIGINT) AS race,
    "race_label",
    CAST("age_range" AS BIGINT) AS age_range,
    "age_range_label",
    CAST("site" AS BIGINT) AS site,
    "site_label",
    "risk_interval",
    CAST("risk" AS DOUBLE) AS risk,
    CAST("risk_lower_ci" AS DOUBLE) AS risk_lower_ci,
    CAST("risk_upper_ci" AS DOUBLE) AS risk_upper_ci
FROM "nci-seer-explorer-risk-of-diagnosis-dying"
