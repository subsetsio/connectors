-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "borough",
    "_2010" AS 2010,
    "of_total_borough_population_2010",
    "_2020" AS 2020,
    "of_total_borough_population_2020",
    "_2030" AS 2030,
    "of_total_borough_population_2030",
    "_2040" AS 2040,
    "of_total_borough_population_2040",
    "change_in_number_20102020",
    "change_in_percent_20102020",
    "change_in_number_20202030",
    "change_in_percent_20202030",
    "change_in_number_20302040",
    "change_in_percent_20302040",
    "change_in_number_20102040",
    "change_in_percent_20102040"
FROM "nyc-open-data-ph5g-sr3v"
