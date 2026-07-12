-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Sex" AS sex,
    "Full-time or part-time" AS full_time_or_part_time,
    "Notes" AS notes
FROM "statswales-73c77570-4ac3-4b14-90ca-8bae3a577bab"
