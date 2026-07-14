-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    "number of children" AS number_of_children,
    "age oldest child" AS age_oldest_child,
    "number of adults" AS number_of_adults,
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-bexfam5"
