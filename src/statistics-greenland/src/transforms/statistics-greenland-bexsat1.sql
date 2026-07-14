-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: PxWeb declares no time role for this cube, so the
--     download node wrote the column 100% null.
-- caution: Dimension column(s) `place of birth` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    CAST("time" AS BIGINT) AS time,
    "type",
    "place of birth" AS place_of_birth,
    "obs_value"
FROM "statistics-greenland-bexsat1"
