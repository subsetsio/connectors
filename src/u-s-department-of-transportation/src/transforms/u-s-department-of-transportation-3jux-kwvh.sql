-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bridge_name",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("_2009" AS BIGINT) AS 2009,
    CAST("_2010" AS BIGINT) AS 2010,
    CAST("_2011" AS BIGINT) AS 2011,
    CAST("_2012" AS BIGINT) AS 2012,
    CAST("_2013" AS BIGINT) AS 2013,
    CAST("_2014" AS BIGINT) AS 2014,
    CAST("_2015" AS BIGINT) AS 2015,
    CAST("_2016" AS BIGINT) AS 2016,
    CAST("_2017" AS BIGINT) AS 2017,
    CAST("_2018" AS BIGINT) AS 2018,
    CAST("_2019" AS BIGINT) AS 2019,
    CAST("_2020" AS BIGINT) AS 2020,
    CAST("_2021" AS BIGINT) AS 2021,
    CAST("_2022" AS BIGINT) AS 2022,
    CAST("_2023" AS BIGINT) AS 2023,
    CAST("_2024" AS BIGINT) AS 2024,
    "bridge_coordinates"
FROM "u-s-department-of-transportation-3jux-kwvh"
