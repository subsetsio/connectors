-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    CAST("number of given names" AS BIGINT) AS number_of_given_names,
    "surname",
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-naxt3"
