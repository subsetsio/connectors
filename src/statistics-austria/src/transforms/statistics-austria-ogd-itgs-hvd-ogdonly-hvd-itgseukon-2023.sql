-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("reporting_period" AS BIGINT) AS reporting_period,
    "partnercountries_according_to_eu_concept",
    "cn8_digit",
    "import_quantity_in_kg",
    "import_value_in_euro",
    "import_supplementary_unit",
    "export_quantity_in_kg",
    "export_value_in_euro",
    "export_supplementary_unit"
FROM "statistics-austria-ogd-itgs-hvd-ogdonly-hvd-itgseukon-2023"
