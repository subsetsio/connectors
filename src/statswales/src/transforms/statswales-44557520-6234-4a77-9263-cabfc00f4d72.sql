-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Flooding Type" AS flooding_type,
    "Risk" AS risk,
    "Property Type" AS property_type,
    "Defence Type" AS defence_type,
    "Area" AS area,
    CAST("Year" AS BIGINT) AS year,
    "Notes" AS notes
FROM "statswales-44557520-6234-4a77-9263-cabfc00f4d72"
