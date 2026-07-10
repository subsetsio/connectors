-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("reporting_year" AS BIGINT) AS reporting_year,
    "selection_of_value_and_volumes",
    "oe_cpa_2_digit",
    "sold_production",
    "technical_actual_production",
    "actual_production",
    "economic_actual_production"
FROM "statistics-austria-ogd-prodcom001-prodcom-j-1"
