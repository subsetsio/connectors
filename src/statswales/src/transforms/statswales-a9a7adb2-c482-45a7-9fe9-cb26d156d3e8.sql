-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Age of the youngest child in the household" AS age_of_the_youngest_child_in_the_household,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-a9a7adb2-c482-45a7-9fe9-cb26d156d3e8"
