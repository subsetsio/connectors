-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: PxWeb declares no time role for this cube, so the
--     download node wrote the column 100% null.
-- caution: `unit` is a dimension of this cube, not a table-wide constant: rows in the same `obs_value` column are expressed in different units. Filter to one `unit` before aggregating or comparing values.
SELECT
    CAST("time" AS BIGINT) AS time,
    "municipality",
    "species",
    "unit",
    "month",
    "obs_value"
FROM "statistics-greenland-fix004"
