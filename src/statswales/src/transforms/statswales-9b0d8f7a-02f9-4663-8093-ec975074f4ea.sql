-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "School" AS school,
    "Sector" AS sector,
    "Year group" AS year_group,
    "Notes" AS notes
FROM "statswales-9b0d8f7a-02f9-4663-8093-ec975074f4ea"
