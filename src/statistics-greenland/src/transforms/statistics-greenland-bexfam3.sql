-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    "age",
    "adults in the family" AS adults_in_the_family,
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-bexfam3"
