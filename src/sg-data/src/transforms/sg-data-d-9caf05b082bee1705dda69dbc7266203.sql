-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "occupation",
    "total",
    "short_work_week",
    "temporary_layoff"
FROM "sg-data-d-9caf05b082bee1705dda69dbc7266203"
