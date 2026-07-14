-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `eksamensaar`.
-- caution: `unit` is a dimension of this cube, not a table-wide constant: rows in the same `obs_value` column are expressed in different units. Filter to one `unit` before aggregating or comparing values.
SELECT
    CAST("eksamensaar" AS BIGINT) AS eksamensaar,
    "gymnasie",
    "vaegtet_interval",
    "unit",
    "obs_value"
FROM "statistics-greenland-udxkap"
