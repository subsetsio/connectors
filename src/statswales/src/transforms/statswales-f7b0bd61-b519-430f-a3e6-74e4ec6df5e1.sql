-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Ethnic group of head of household" AS ethnic_group_of_head_of_household,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-f7b0bd61-b519-430f-a3e6-74e4ec6df5e1"
