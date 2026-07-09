-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows the source marked missing (-99.99 / -999 sentinels) are absent, not zero: a missing (date, variable) pair means the portfolio had no observation that period.
SELECT
    "block",
    "statistic",
    "period",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "variable",
    "value"
FROM "kenneth-french-data-library-f-f-research-data-factors-daily"
