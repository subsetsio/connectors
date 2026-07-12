-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Ethnic group" AS ethnic_group,
    "Gender" AS gender,
    "Strand" AS strand,
    "Financial year" AS financial_year,
    "Notes" AS notes
FROM "statswales-1d404a9a-e77b-4735-9eb8-615cb5fe859d"
