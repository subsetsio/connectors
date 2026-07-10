-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The `series` values use different index bases and source methodologies; compare `annual_average_index` values only within a single series.
SELECT
    "series",
    "year",
    "annual_average_index",
    "annual_percent_change"
FROM "federal-reserve-bank-of-minneapolis-cpi-historical"
