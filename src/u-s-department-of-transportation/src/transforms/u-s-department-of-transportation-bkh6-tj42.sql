-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tbl",
    CAST("year" AS BIGINT) AS year,
    CAST("quarter" AS BIGINT) AS quarter,
    CAST("mkt_fare" AS DOUBLE) AS mkt_fare,
    CAST("citymarketid_1" AS BIGINT) AS citymarketid_1,
    CAST("citymarketid_2" AS BIGINT) AS citymarketid_2,
    "city1",
    "city2",
    CAST("carairlineid" AS BIGINT) AS carairlineid,
    "car",
    CAST("carpax" AS BIGINT) AS carpax,
    CAST("carpaxshare" AS DOUBLE) AS carpaxshare,
    CAST("caravgfare" AS DOUBLE) AS caravgfare,
    CAST("fareinc_min" AS BIGINT) AS fareinc_min,
    CAST("fareinc_minpaxsh" AS DOUBLE) AS fareinc_minpaxsh,
    CAST("fareinc_max" AS BIGINT) AS fareinc_max,
    CAST("fare_inc_maxpaxsh" AS DOUBLE) AS fare_inc_maxpaxsh,
    CAST("fare_inc_x3paxsh" AS DOUBLE) AS fare_inc_x3paxsh,
    "cityname_location1",
    "cityname_location1_address",
    "cityname_location1_city",
    "cityname_location1_state",
    "cityname_location1_zip",
    "cityname_location2",
    "cityname_location2_address",
    "cityname_location2_city",
    "cityname_location2_state",
    "cityname_location2_zip",
    "tbl5pk"
FROM "u-s-department-of-transportation-bkh6-tj42"
