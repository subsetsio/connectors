-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Monthly, dated to the first of the month. `mcpi_monthly_chg` is a raw one-month FRACTIONAL change (0.0041 = 0.41%) while `mcpi_ann_monthly_chg` is the same change annualized and expressed in percent — the two columns are on different scales.
-- caution: 'Revised' means the median CPI is recomputed as the BLS revises seasonal factors, so past values can change between runs.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "mcpi_monthly_chg",
    "mcpi_ann_monthly_chg"
FROM "cleveland-fed-mediancpi-mcpi-revised"
