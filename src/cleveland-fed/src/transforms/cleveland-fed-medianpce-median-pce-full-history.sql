-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Monthly, dated to the first of the month. The two columns are different transforms of the same measure (one-month percent change and year-over-year percent change) and are not comparable to each other.
-- caution: The source writes the literal token `NaN` for months with no observation (the first month of the history, and the first eleven months for the year-over-year column).
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "median_pce_inflation_monthly_percent_change",
    "median_pce_inflation_year_over_year_percent_change"
FROM "cleveland-fed-medianpce-median-pce-full-history"
