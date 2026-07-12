-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Area" AS area,
    "Provider" AS provider,
    "Sale type" AS sale_type,
    "Notes" AS notes
FROM "statswales-555e8825-1d7b-477e-b94b-b41415b785b0"
