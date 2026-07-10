-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year_of_discharge" AS BIGINT) AS year_of_discharge,
    "sex",
    "nuts_2_region_place_of_residence",
    "diagnosis_ishmt_shortlist_diagnoses",
    "number_of_inpatient_discharges",
    "number_of_bed_days"
FROM "statistics-austria-ogd-krankenbewegungen-ex-entlassungen-ka-2"
