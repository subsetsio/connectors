-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "Location" AS location,
    "Short Indicator Text" AS short_indicator_text,
    "Long Indicator Text" AS long_indicator_text,
    "Stratification 1" AS stratification_1,
    "Stratification Group 1" AS stratification_group_1,
    "Stratification 2" AS stratification_2,
    "Stratification Group 2" AS stratification_group_2,
    "Stratification Group 2 Label" AS stratification_group_2_label,
    "Data Type" AS data_type,
    "Data Type Label" AS data_type_label,
    CAST("Data Value" AS DOUBLE) AS data_value,
    "95 % CI" AS 95_ci,
    CAST("Lower CI" AS DOUBLE) AS lower_ci,
    CAST("Upper CI" AS DOUBLE) AS upper_ci,
    "FIPS" AS fips,
    "Geolocation" AS geolocation
FROM "cdc-ircd-wk4g"
