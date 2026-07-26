-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "ytd_attendance_avg",
    "ytd_enrollment_avg"
FROM "nyc-open-data-rfpq-hs49"
