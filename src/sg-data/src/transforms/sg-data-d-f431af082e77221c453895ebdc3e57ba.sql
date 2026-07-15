-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Date" AS date,
    "7day_Moving_Average_Daily_Estimated_Numbers_of_COVID_19_Infecti" AS 7day_moving_average_daily_estimated_numbers_of_covid_19_infecti,
    "Weekends_or_Public_Holidays" AS weekends_or_public_holidays
FROM "sg-data-d-f431af082e77221c453895ebdc3e57ba"
