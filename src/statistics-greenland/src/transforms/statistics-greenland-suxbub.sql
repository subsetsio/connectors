-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: PxWeb declares no time role for this cube, so the
--     download node wrote the column 100% null.
SELECT
    "Indicator" AS indicator,
    CAST("Time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-suxbub"
