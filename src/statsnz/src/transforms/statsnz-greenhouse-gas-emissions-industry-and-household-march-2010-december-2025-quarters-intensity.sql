-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("Period" AS DOUBLE) AS period,
    "Anzsic" AS anzsic,
    "Anzsic_descriptor" AS anzsic_descriptor,
    "Variable2" AS variable2,
    "Units" AS units,
    CAST("Data_value" AS DOUBLE) AS data_value,
    "Gas" AS gas,
    "Variable1" AS variable1
FROM "statsnz-greenhouse-gas-emissions-industry-and-household-march-2010-december-2025-quarters-intensity"
