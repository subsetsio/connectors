-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "_month" AS month,
    "agency_name",
    "name_of_employee",
    "last_name",
    "first_name",
    "title"
FROM "nyc-open-data-wf8t-6cqt"
