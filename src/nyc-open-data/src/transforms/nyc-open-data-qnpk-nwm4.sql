-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_month" AS month,
    "ride_time_hours",
    "student_count"
FROM "nyc-open-data-qnpk-nwm4"
