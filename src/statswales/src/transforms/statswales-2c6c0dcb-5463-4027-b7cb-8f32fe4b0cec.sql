-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Number of children in the household" AS number_of_children_in_the_household,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-2c6c0dcb-5463-4027-b7cb-8f32fe4b0cec"
