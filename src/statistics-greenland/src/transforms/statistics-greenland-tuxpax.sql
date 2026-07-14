-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `aar`.
SELECT
    "direction",
    "airport",
    CAST("aar" AS BIGINT) AS aar,
    "kvt",
    "obs_value"
FROM "statistics-greenland-tuxpax"
