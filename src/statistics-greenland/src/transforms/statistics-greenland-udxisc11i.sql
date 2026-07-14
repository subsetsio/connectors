-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `startaar`.
SELECT
    "Isced" AS isced,
    "sex",
    "skolenr_ny",
    "uddkode_ny",
    "startalder",
    CAST("startaar" AS BIGINT) AS startaar,
    "obs_value"
FROM "statistics-greenland-udxisc11i"
