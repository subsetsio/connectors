-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "change_date",
    CAST("inspection_id" AS BIGINT) AS inspection_id,
    CAST("insp_study_id" AS BIGINT) AS insp_study_id,
    "study",
    CAST("seq_no" AS BIGINT) AS seq_no
FROM "u-s-department-of-transportation-5qik-smay"
