-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is one observation for a source-defined series and period; series values represent distinct measures or units, so filter or group by series before aggregating value.
SELECT
    CAST("period" AS BIGINT) AS period,
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "series",
    "value"
FROM "central-bank-taiwan-ega9y01"
