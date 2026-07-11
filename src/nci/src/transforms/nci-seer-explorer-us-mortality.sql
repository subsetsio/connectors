-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are annual United States mortality trends with race and age range pinned by the source fetch; compare separately from State Cancer Profiles geographic mortality.
SELECT
    "statistic",
    CAST("sex" AS BIGINT) AS sex,
    "sex_label",
    CAST("race" AS BIGINT) AS race,
    "race_label",
    CAST("age_range" AS BIGINT) AS age_range,
    "age_range_label",
    CAST("site" AS BIGINT) AS site,
    "site_label",
    "year",
    CAST("rate" AS DOUBLE) AS rate,
    CAST("rate_lower_ci" AS DOUBLE) AS rate_lower_ci,
    CAST("rate_upper_ci" AS DOUBLE) AS rate_upper_ci,
    CAST("modeled_rate" AS DOUBLE) AS modeled_rate,
    "count"
FROM "nci-seer-explorer-us-mortality"
