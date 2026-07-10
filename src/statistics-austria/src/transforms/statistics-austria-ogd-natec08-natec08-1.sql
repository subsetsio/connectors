-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("reference_year" AS BIGINT) AS reference_year,
    "activity_sector_nace_level_2",
    "type_of_ownership",
    "import_number_of_enterprises",
    "import_value_in_euro",
    "export_number_of_enterprises",
    "export_value_in_euro",
    "trade_intensity_number_of_enterprises",
    "trade_intensity_value_in_euro"
FROM "statistics-austria-ogd-natec08-natec08-1"
