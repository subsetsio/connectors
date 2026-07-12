-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "main_economic_activity_ar",
    "indicator",
    "indicator_ar",
    "establishment_size",
    "establishment_size_ar",
    "establishments_and_employees",
    "establishments_and_employees_ar",
    "value",
    "activity_code",
    "rmz_lnsht",
    "sn",
    "qym"
FROM "qatar-planning-and-statistics-authority-number-of-establishments-and-employees-by-size-of-establishment-and-main-economic-activity"
