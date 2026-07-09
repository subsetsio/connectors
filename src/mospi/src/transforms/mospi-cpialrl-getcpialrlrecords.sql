-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Separate index columns for agricultural labourers (`index_al`) and rural labourers (`index_rl`); the inflation columns are populated only for the recent base-year series.
-- caution: `state` includes the All-India aggregate alongside the states.
SELECT
    "indicator",
    "base_year",
    "year",
    "month",
    "state",
    CAST("index_al" AS DOUBLE) AS index_al,
    CAST("index_rl" AS DOUBLE) AS index_rl,
    CAST("inflation_al" AS DOUBLE) AS inflation_al,
    CAST("inflation_rl" AS DOUBLE) AS inflation_rl,
    "group"
FROM "mospi-cpialrl-getcpialrlrecords"
