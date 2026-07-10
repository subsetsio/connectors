-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year_of_discharge" AS BIGINT) AS year_of_discharge,
    "sex",
    "age_four_classes",
    "nuts_2_region_place_of_residence",
    "medical_procedures_subchapters",
    "medical_procedures"
FROM "statistics-austria-ogd-krankenbewegungen-ex-leistungen-1"
