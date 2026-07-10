-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "commune_of_residence_2411",
    "census_year_14",
    "population"
FROM "statistics-austria-ogd-f0743-vz-his-gem-1"
