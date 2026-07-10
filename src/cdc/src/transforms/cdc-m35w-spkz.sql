-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MeasureID" AS measureid,
    "Measure full name" AS measure_full_name,
    "Measure short name" AS measure_short_name,
    "CategoryID" AS categoryid,
    "Category name" AS category_name,
    "PLACES Release 2024" AS places_release_2024,
    "Measure full name 2016-2023" AS measure_full_name_2016_2023,
    "Measure short name 2016-2023" AS measure_short_name_2016_2023,
    "PLACES Release 2023" AS places_release_2023,
    "PLACES Release 2022" AS places_release_2022,
    "PLACES Release 2021" AS places_release_2021,
    "PLACES Release 2020" AS places_release_2020,
    "500 Cities Release 2019" AS 500_cities_release_2019,
    "500 Cities Release 2018" AS 500_cities_release_2018,
    "500 Cities Release 2017" AS 500_cities_release_2017,
    "500 Cities Release 2016" AS 500_cities_release_2016,
    "Frequency_BRFSS_year" AS frequency_brfss_year
FROM "cdc-m35w-spkz"
