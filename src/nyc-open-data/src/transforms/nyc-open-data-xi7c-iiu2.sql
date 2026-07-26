-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "cd_number",
    "cd_name",
    "_1970_population" AS 1970_population,
    "_1980_population" AS 1980_population,
    "_1990_population" AS 1990_population,
    "_2000_population" AS 2000_population,
    "_2010_population" AS 2010_population
FROM "nyc-open-data-xi7c-iiu2"
