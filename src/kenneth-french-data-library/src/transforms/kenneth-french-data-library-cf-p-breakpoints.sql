-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows the source marked missing (-99.99 / -999 sentinels) are absent, not zero: a missing (date, variable) pair means the portfolio had no observation that period.
-- caution: The single `value` column mixes units, distinguished by `variable`: `n_firms` (and `n_firms_le_0` / `n_firms_gt_0`, the counts of firms with a non-positive vs positive ratio) are counts of NYSE firms; `p5`..`p100` are the 5th through 100th NYSE percentiles of the sort variable, in that variable's own units (ME in millions of USD, the ratio sorts as ratios, prior-return and OP/INV sorts in percent). Never aggregate `value` across `variable`.
SELECT
    "block",
    "statistic",
    "period",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "variable",
    "value"
FROM "kenneth-french-data-library-cf-p-breakpoints"
