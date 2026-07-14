-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    "district",
    "species",
    "fishing segment" AS fishing_segment,
    "vessel type" AS vessel_type,
    "enhed",
    "month",
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-fix012"
