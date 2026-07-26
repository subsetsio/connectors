-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "training_entity",
    "training_site",
    "borough",
    "district",
    "school",
    "class_number",
    "adaptive_class",
    "_session" AS session,
    "session_date_range",
    "school_year",
    "first_day_of_class",
    "number_of_sessions_attended"
FROM "nyc-open-data-mtt6-ywt4"
