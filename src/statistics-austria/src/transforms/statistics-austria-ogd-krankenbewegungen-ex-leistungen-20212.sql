-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year_of_discharge" AS BIGINT) AS year_of_discharge,
    "sex",
    "age_in_4_classes",
    "medical_procedures_codes_from_2009_subchapters",
    "number_of_medical_procedures"
FROM "statistics-austria-ogd-krankenbewegungen-ex-leistungen-20212"
