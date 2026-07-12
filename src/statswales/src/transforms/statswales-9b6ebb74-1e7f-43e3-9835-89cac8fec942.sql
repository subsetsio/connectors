-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Area" AS area,
    "Dwelling type" AS dwelling_type,
    "Notes" AS notes
FROM "statswales-9b6ebb74-1e7f-43e3-9835-89cac8fec942"
