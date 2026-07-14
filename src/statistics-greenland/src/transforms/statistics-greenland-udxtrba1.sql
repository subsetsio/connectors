-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `dim_aar`.
SELECT
    "aar",
    "isced",
    "sex",
    "status",
    CAST("dim_aar" AS BIGINT) AS dim_aar,
    "obs_value"
FROM "statistics-greenland-udxtrba1"
