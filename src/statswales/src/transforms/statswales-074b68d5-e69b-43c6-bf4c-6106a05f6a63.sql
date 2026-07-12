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
FROM "statswales-074b68d5-e69b-43c6-bf4c-6106a05f6a63"
