-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "borough",
    "_1950" AS 1950,
    "_1950_boro_share_of_nyc_total" AS 1950_boro_share_of_nyc_total,
    "_1960" AS 1960,
    "_1960_boro_share_of_nyc_total" AS 1960_boro_share_of_nyc_total,
    "_1970" AS 1970,
    "_1970_boro_share_of_nyc_total" AS 1970_boro_share_of_nyc_total,
    "_1980" AS 1980,
    "_1980_boro_share_of_nyc_total" AS 1980_boro_share_of_nyc_total,
    "_1990" AS 1990,
    "_1990_boro_share_of_nyc_total" AS 1990_boro_share_of_nyc_total,
    "_2000" AS 2000,
    "_2000_boro_share_of_nyc_total" AS 2000_boro_share_of_nyc_total,
    "_2010" AS 2010,
    "_2010_boro_share_of_nyc_total" AS 2010_boro_share_of_nyc_total,
    "_2020" AS 2020,
    "_2020_boro_share_of_nyc_total" AS 2020_boro_share_of_nyc_total,
    "_2030" AS 2030,
    "_2030_boro_share_of_nyc_total" AS 2030_boro_share_of_nyc_total,
    "_2040" AS 2040,
    "_2040_boro_share_of_nyc_total" AS 2040_boro_share_of_nyc_total
FROM "nyc-open-data-xywu-7bv9"
