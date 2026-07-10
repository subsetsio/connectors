-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("reporting_year" AS BIGINT) AS reporting_year,
    "selection_of_value_and_volumes",
    "prodcom_8_digit",
    "actual_production",
    "sold_production",
    "production_under_sub_contracted_operations"
FROM "statistics-austria-ogd-prodcom001-hvd-prodcom-j-1"
