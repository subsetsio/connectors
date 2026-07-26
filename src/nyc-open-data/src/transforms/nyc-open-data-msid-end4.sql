-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "event_type",
    "_event" AS event,
    "date",
    "borough",
    "spray_area_neighborhood",
    "zip_codes"
FROM "nyc-open-data-msid-end4"
