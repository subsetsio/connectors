-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Monthly, dated to the first of the month. `core_index` is a price index level (1982-84 = 100 CPI convention) while `ann_monthly_chg` is the annualized one-month percent change derived from it — the two columns are on different scales and the first month has no change value.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "core_index",
    "ann_monthly_chg"
FROM "cleveland-fed-mediancpi-core"
