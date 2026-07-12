-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Authority" AS authority,
    "Services" AS services,
    "Notes" AS notes
FROM "statswales-4e4cd837-e9a4-43ca-92d3-2dac1c22f0ff"
