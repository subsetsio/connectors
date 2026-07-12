-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Gender" AS gender,
    "Primary type of disability or learning difficulty" AS primary_type_of_disability_or_learning_difficulty,
    "Strand" AS strand,
    "Financial year" AS financial_year,
    "Notes" AS notes
FROM "statswales-01163996-29cf-46ca-8c7c-bea9ec134faa"
