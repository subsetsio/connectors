-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "place_of_study",
    "semester",
    "ordinary_studies",
    "newly_enrolled_ordinary_studies"
FROM "statistics-austria-ogd-fhsstud-ext-fhs-s-2"
