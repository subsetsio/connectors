-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Family type and work status" AS family_type_and_work_status,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-676925b3-1961-47ef-8341-c186f968efa4"
