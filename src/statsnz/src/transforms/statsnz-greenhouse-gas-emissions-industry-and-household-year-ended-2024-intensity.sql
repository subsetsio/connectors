-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "anzsic",
    "anzsic_descriptor",
    "variable1",
    "variable2",
    "category",
    "units",
    "magnitude",
    "source",
    CAST("data_value" AS DOUBLE) AS data_value
FROM "statsnz-greenhouse-gas-emissions-industry-and-household-year-ended-2024-intensity"
