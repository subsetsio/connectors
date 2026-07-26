-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "confirmed_cases",
    "probable_cases",
    "total_cases",
    "_7day_average_of_confirmed_cases" AS 7day_average_of_confirmed_cases,
    "_7day_average_of_probable_cases" AS 7day_average_of_probable_cases,
    "_7day_average_of_total_cases" AS 7day_average_of_total_cases,
    "status",
    "etldate"
FROM "nyc-open-data-xwtc-hedq"
