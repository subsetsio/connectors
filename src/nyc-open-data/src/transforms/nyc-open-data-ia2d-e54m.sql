-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "new_york_city_population",
    "nyc_consumptionmillion_gallons_per_day",
    "per_capitagallons_per_person_per_day"
FROM "nyc-open-data-ia2d-e54m"
