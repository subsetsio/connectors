-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local authority" AS local_authority,
    "Age group" AS age_group,
    "Residence" AS residence,
    "Type of care and support" AS type_of_care_and_support,
    "Notes" AS notes
FROM "statswales-d5903e99-40d5-40e2-b486-731f6832447c"
