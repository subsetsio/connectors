-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Area" AS area,
    "Hazard" AS hazard,
    "Dwelling" AS dwelling,
    "Notes" AS notes
FROM "statswales-34f5ec92-1447-45be-9dab-ec73708e3e8b"
