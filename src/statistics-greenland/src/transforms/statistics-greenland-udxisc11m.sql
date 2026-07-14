-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `startaar`.
SELECT
    "aar",
    "isced",
    "sex",
    "status",
    CAST("startaar" AS BIGINT) AS startaar,
    "obs_value"
FROM "statistics-greenland-udxisc11m"
