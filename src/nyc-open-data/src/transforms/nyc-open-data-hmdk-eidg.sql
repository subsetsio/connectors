-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "monthperiod",
    "mean_temperature",
    "mean_precipitation",
    "ensemble_average_mean_changes_in_annual_temperature_ssp245",
    "ensemble_average_mean_changes_in_annual_temperature_ssp585",
    "ensemble_average_mean_changes_in_annual_precipitation_ssp245",
    "ensemble_average_mean_changes_in_annual_precipitation_ssp585"
FROM "nyc-open-data-hmdk-eidg"
