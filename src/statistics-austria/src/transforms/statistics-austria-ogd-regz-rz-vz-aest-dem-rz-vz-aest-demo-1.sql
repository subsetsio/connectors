-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "place_of_usual_residence",
    "age_level_3",
    "sex",
    "citizenship_level_4",
    "number_of_persons"
FROM "statistics-austria-ogd-regz-rz-vz-aest-dem-rz-vz-aest-demo-1"
