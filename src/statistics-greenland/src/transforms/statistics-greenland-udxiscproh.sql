-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `aar`.
-- caution: `unit` is a dimension of this cube, not a table-wide constant: rows in the same `obs_value` column are expressed in different units. Filter to one `unit` before aggregating or comparing values.
SELECT
    "unit",
    "alder_grp",
    "Komm" AS komm,
    "ISCED11_level_grp" AS isced11_level_grp,
    CAST("Aar" AS BIGINT) AS aar,
    "Sex" AS sex,
    "obs_value"
FROM "statistics-greenland-udxiscproh"
