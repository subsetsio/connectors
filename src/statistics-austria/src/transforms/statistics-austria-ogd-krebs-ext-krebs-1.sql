-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "tumore_icd_10_3_steller",
    CAST("reporting_year" AS BIGINT) AS reporting_year,
    "province_of_residence",
    "sex",
    "number_of_records_f_kre"
FROM "statistics-austria-ogd-krebs-ext-krebs-1"
