-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A cross-sectional snapshot of the LATEST month only, sorted by one-month annualized percent change; it has no time axis and is overwritten each month.
-- caution: `cumulative_relative_importance` is a running total down the source's sort order, so it is only meaningful in that order and must never be aggregated. `relative_importance_normalized` is the weight in percent and sums to ~100 across rows.
SELECT
    "label",
    "1_month_annualized_percent_change",
    "relative_importance_normalized",
    "cumulative_relative_importance"
FROM "cleveland-fed-mediancpi-mediancpi-component-table"
