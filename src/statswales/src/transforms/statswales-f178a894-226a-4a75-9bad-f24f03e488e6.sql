-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Whether there is disability within the family" AS whether_there_is_disability_within_the_family,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-f178a894-226a-4a75-9bad-f24f03e488e6"
