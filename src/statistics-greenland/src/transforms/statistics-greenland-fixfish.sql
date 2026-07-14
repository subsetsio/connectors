-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `taar`.
SELECT
    "nat_id",
    "area_id",
    "art_id",
    CAST("taar" AS BIGINT) AS taar,
    "m",
    "obs_value"
FROM "statistics-greenland-fixfish"
