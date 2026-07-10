-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "province",
    CAST("year" AS BIGINT) AS year,
    "age",
    "sex",
    "main_variant"
FROM "statistics-austria-ogd-bevstprog-pr-bevjd-4"
