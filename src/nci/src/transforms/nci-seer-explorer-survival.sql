-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are relative survival snapshot measurements by survival interval, not annual observations.
SELECT
    "statistic",
    CAST("sex" AS BIGINT) AS sex,
    "sex_label",
    CAST("race" AS BIGINT) AS race,
    "race_label",
    CAST("age_range" AS BIGINT) AS age_range,
    "age_range_label",
    CAST("stage" AS BIGINT) AS stage,
    "stage_label",
    CAST("subtype" AS BIGINT) AS subtype,
    CAST("site" AS BIGINT) AS site,
    "site_label",
    CAST("relative_survival_interval" AS BIGINT) AS relative_survival_interval,
    "relative_survival_interval_label",
    CAST("rate" AS DOUBLE) AS rate,
    CAST("rate_se" AS DOUBLE) AS rate_se,
    CAST("rate_lower_ci" AS DOUBLE) AS rate_lower_ci,
    CAST("rate_upper_ci" AS DOUBLE) AS rate_upper_ci,
    "count",
    "subtype_label"
FROM "nci-seer-explorer-survival"
