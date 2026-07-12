-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Variant" AS variant,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-edf40524-b51a-47ce-b1fc-69647f74b5a0"
