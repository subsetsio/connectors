-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "year_of_graduation",
    "level_of_education_level_3",
    "sex",
    "labour_market_status_after_18_months_level_5",
    "number_of_persons"
FROM "statistics-austria-ogd-aeapp-biber-abschl-ext-biber-abschl-1"
