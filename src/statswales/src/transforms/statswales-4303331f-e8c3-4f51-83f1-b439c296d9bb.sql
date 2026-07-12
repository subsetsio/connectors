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
    "Gender" AS gender,
    "Reason" AS reason,
    "Notes" AS notes
FROM "statswales-4303331f-e8c3-4f51-83f1-b439c296d9bb"
