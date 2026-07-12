-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Migrant status of the head of household" AS migrant_status_of_the_head_of_household,
    "Time period" AS time_period,
    "Country" AS country,
    "Notes" AS notes
FROM "statswales-339156cd-77a6-4419-9354-84cb300a1404"
