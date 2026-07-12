-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Source of funding" AS source_of_funding,
    "Authority" AS authority,
    "Notes" AS notes
FROM "statswales-48f882eb-eb8c-49b3-a35b-b6a74248358e"
