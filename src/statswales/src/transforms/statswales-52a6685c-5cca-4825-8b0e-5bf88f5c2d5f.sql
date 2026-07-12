-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Indicator" AS indicator,
    "Period" AS period,
    "Notes" AS notes
FROM "statswales-52a6685c-5cca-4825-8b0e-5bf88f5c2d5f"
