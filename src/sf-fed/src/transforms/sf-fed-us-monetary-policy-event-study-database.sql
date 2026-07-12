-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sheet",
    "row_idx",
    strptime("period", '%Y-%m-%d')::DATE AS period,
    "period_date",
    "series",
    "value",
    strptime("value_text", '%Y-%m-%d')::DATE AS value_text
FROM "sf-fed-us-monetary-policy-event-study-database"
