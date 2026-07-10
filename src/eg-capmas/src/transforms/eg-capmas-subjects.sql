-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "main_subject_id",
    "main_subject_en",
    "main_subject_ar",
    "sub_subject_id",
    "sub_subject_en",
    "sub_subject_ar"
FROM "eg-capmas-subjects"
