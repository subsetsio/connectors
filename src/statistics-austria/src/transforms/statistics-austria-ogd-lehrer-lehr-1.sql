-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "school_year",
    "pol_district",
    "number_of_teaching_staff",
    "full_time_equivalent"
FROM "statistics-austria-ogd-lehrer-lehr-1"
