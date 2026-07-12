-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Region" AS region,
    "Anzsic_descriptor" AS anzsic_descriptor,
    "Sub_industry" AS sub_industry,
    "Household_category" AS household_category,
    "Gas" AS gas,
    CAST("Year" AS BIGINT) AS year,
    "Data_value" AS data_value,
    "Units" AS units,
    "Magnitude" AS magnitude
FROM "statsnz-greenhouse-gas-emissions-by-region-industry-and-household-year-ended-2024"
