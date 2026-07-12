-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "establishment_size",
    "record_type",
    "activity_code",
    "main_economic_activity_ar",
    "establishment_size_ar",
    "record_type_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-number-of-establishments-and-employees-by-size-of-establishment-and-main-economic-activity-transport2"
