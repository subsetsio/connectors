-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is preliminary incidence only and includes a data_model dimension; do not combine data models without filtering or grouping it.
SELECT
    "statistic",
    CAST("rate_type" AS BIGINT) AS rate_type,
    "rate_type_label",
    CAST("sex" AS BIGINT) AS sex,
    "sex_label",
    CAST("race" AS BIGINT) AS race,
    "race_label",
    CAST("age_range" AS BIGINT) AS age_range,
    "age_range_label",
    CAST("data_model" AS BIGINT) AS data_model,
    CAST("site" AS BIGINT) AS site,
    "site_label",
    "year",
    CAST("rate" AS DOUBLE) AS rate,
    CAST("rate_se" AS DOUBLE) AS rate_se,
    CAST("rate_lower_ci" AS DOUBLE) AS rate_lower_ci,
    CAST("rate_upper_ci" AS DOUBLE) AS rate_upper_ci,
    CAST("modeled_rate" AS DOUBLE) AS modeled_rate,
    "count"
FROM "nci-seer-explorer-preliminary-incidence-rates"
