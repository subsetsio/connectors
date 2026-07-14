-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    "Decile: Palma ratio" AS decile_palma_ratio,
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-inxpi403"
