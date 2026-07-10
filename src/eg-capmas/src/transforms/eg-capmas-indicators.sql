-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator_id",
    "name_en",
    "name_ar",
    "main_subject_id",
    "main_subject_en",
    "sub_subject_id",
    "sub_subject_en",
    "publication_id",
    "publication_en",
    "publication_ar",
    "periodicity_en",
    "measure_unit_en",
    "measure_unit_ar",
    "start_year",
    "end_year"
FROM "eg-capmas-indicators"
