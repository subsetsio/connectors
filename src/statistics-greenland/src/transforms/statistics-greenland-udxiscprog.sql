-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `aar`.
SELECT
    "alder_grp",
    "Dist" AS dist,
    "ISCED11_level" AS isced11_level,
    "Sex" AS sex,
    CAST("Aar" AS BIGINT) AS aar,
    "obs_value"
FROM "statistics-greenland-udxiscprog"
