-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    CAST("age" AS BIGINT) AS age,
    "quarter",
    "cohabiting",
    "length of pregnancy" AS length_of_pregnancy,
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-suxa1"
