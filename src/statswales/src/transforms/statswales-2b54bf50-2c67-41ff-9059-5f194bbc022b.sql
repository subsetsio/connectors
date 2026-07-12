-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Age" AS age,
    "Reason" AS reason,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-2b54bf50-2c67-41ff-9059-5f194bbc022b"
