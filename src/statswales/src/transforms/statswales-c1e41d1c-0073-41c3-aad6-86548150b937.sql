-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Food security status of household" AS food_security_status_of_household,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-c1e41d1c-0073-41c3-aad6-86548150b937"
