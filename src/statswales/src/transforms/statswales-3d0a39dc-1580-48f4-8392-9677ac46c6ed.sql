-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Organisation" AS organisation,
    "Sex" AS sex,
    "Legal status" AS legal_status,
    "Notes" AS notes
FROM "statswales-3d0a39dc-1580-48f4-8392-9677ac46c6ed"
