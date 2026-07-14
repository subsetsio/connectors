-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `taar`.
SELECT
    "ART" AS art,
    CAST("taar" AS BIGINT) AS taar,
    "obs_value"
FROM "statistics-greenland-fixsdyr"
