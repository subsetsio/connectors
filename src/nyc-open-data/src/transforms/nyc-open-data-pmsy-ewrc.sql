-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "profile_id",
    "_name" AS name,
    "rank",
    "command",
    "shield",
    "appointment_date",
    "arrests_total",
    "department_recognitions",
    "export_date"
FROM "nyc-open-data-pmsy-ewrc"
