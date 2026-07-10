-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("month_end", '%Y-%m')::DATE AS month_end,
    "condition",
    "demographics_type",
    "demographics_values",
    CAST("rate_per_100000_visits" AS BIGINT) AS rate_per_100000_visits
FROM "cdc-eze9-ahe5"
