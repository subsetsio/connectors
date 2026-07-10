-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_as_of",
    "jurisdiction_residence",
    "data_period_start",
    strptime("data_period_end", '%m/%d/%Y')::DATE AS data_period_end,
    "group",
    "subgroup1",
    "subgroup2",
    CAST("covid_deaths" AS BIGINT) AS covid_deaths,
    CAST("crude_rate" AS DOUBLE) AS crude_rate,
    CAST("conf_int_95pct_lower_crude" AS DOUBLE) AS conf_int_95pct_lower_crude,
    CAST("conf_int_95pct_upper_crude" AS DOUBLE) AS conf_int_95pct_upper_crude,
    "note"
FROM "cdc-exs3-hbne"
