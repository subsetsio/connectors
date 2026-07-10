-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year_under_review" AS BIGINT) AS year_under_review,
    "deceased"
FROM "statistics-austria-ogd-gestorbene-ext-ges-1"
