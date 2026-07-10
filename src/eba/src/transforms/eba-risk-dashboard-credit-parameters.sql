-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The period is an integer quarter code in YYYYQ form, not a calendar date.
-- caution: Rows mix country values with aggregate geographies; filter `country` before summing or comparing peer groups.
SELECT
    "period",
    "country",
    "segment",
    "metric",
    "statistic",
    "value"
FROM "eba-risk-dashboard-credit-parameters"
