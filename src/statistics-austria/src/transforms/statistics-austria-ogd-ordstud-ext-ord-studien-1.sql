-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "academic_year",
    "regular_studies",
    "regular_studies_in_the_first_semester"
FROM "statistics-austria-ogd-ordstud-ext-ord-studien-1"
