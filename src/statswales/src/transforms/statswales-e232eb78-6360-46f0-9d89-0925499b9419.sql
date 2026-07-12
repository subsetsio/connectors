-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Place of birth" AS place_of_birth,
    "Breastfeeding status" AS breastfeeding_status,
    "Notes" AS notes
FROM "statswales-e232eb78-6360-46f0-9d89-0925499b9419"
