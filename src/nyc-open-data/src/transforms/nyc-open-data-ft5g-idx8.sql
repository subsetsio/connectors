-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "opt_code",
    "eligible_stop_to_school_students",
    "eligible_door_to_door_students"
FROM "nyc-open-data-ft5g-idx8"
