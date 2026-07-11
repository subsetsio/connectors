-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a prevalence snapshot rather than a time series; compare it separately from annual incidence or mortality tables.
SELECT
    "statistic",
    CAST("sex" AS BIGINT) AS sex,
    "sex_label",
    CAST("age_range" AS BIGINT) AS age_range,
    "age_range_label",
    CAST("site" AS BIGINT) AS site,
    "site_label",
    "count",
    CAST("percent" AS DOUBLE) AS percent
FROM "nci-seer-explorer-prevalence"
