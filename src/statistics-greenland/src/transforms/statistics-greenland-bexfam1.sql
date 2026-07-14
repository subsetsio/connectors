-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    "type of address" AS type_of_address,
    "age",
    "district",
    "gender",
    "type of family" AS type_of_family,
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-bexfam1"
