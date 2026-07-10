-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime(NULLIF("earning_period", 'null'), '%Y-%m')::DATE AS earning_period,
    "earning_period_start",
    "earning_period_end",
    strptime(NULLIF("issue_year_month", 'null'), '%Y-%m')::DATE AS issue_year_month,
    CAST(NULLIF("fixed_rate", 'null') AS DOUBLE) AS fixed_rate,
    CAST(NULLIF("semi_annual_inflation_rate", 'null') AS DOUBLE) AS semi_annual_inflation_rate,
    CAST(NULLIF("combined_rate", 'null') AS DOUBLE) AS combined_rate
FROM "us-treasury-fiscal-data-v1-accounting-od-i-bonds-interest-rates"
