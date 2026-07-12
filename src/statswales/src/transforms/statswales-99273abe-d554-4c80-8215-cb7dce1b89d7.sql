-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Sexual orientation of the head of household" AS sexual_orientation_of_the_head_of_household,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-99273abe-d554-4c80-8215-cb7dce1b89d7"
