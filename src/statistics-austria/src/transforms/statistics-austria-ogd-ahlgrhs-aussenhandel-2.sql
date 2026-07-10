-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "country_groups",
    "year",
    "sitc_1digit",
    "import_value_in_euro",
    "export_value_in_euro"
FROM "statistics-austria-ogd-ahlgrhs-aussenhandel-2"
