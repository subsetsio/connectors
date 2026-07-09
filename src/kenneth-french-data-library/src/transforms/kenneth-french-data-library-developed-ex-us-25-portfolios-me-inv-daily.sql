-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows the source marked missing (-99.99 / -999 sentinels) are absent, not zero: a missing (date, variable) pair means the portfolio had no observation that period.
-- caution: Stacks several sub-tables with DIFFERENT units in the single `value` column, identified by `statistic`/`block` (e.g. returns in percent, number of firms as a count, average firm size in $millions, BE/ME as a ratio). Never aggregate `value` across `statistic` — always filter to one.
SELECT
    "block",
    "statistic",
    "period",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "variable",
    "value"
FROM "kenneth-french-data-library-developed-ex-us-25-portfolios-me-inv-daily"
