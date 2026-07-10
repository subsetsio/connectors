-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "bundesland",
    CAST("year" AS BIGINT) AS year,
    "alter_in_5_jahresgruppen",
    "country_of_birth",
    "sex",
    "main_variant"
FROM "statistics-austria-ogd-bevstprogjdgebland-pr-bevjdgb-5"
