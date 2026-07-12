-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Financial year" AS financial_year,
    "Provider" AS provider,
    "Strand" AS strand,
    "Gender" AS gender,
    "Notes" AS notes
FROM "statswales-58518b5f-db38-4512-a059-44486c4cc6eb"
