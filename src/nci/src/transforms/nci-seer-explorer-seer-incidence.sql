-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are annual SEER incidence trends with race, age range, rate type, and subtype pinned by the source fetch; compare separately from preliminary incidence.
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
    CAST("subtype" AS BIGINT) AS subtype,
    CAST("site" AS BIGINT) AS site,
    "site_label",
    "year",
    CAST("rate" AS DOUBLE) AS rate,
    CAST("rate_lower_ci" AS DOUBLE) AS rate_lower_ci,
    CAST("rate_upper_ci" AS DOUBLE) AS rate_upper_ci,
    CAST("modeled_rate" AS DOUBLE) AS modeled_rate,
    "count",
    "subtype_label"
FROM "nci-seer-explorer-seer-incidence"
