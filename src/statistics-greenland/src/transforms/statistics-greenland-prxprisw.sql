-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: PxWeb declares no time role for this cube, so the
--     download node wrote the column 100% null.
-- caution: Dimension column(s) `commodity group` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    "commodity group" AS commodity_group,
    "time",
    "obs_value"
FROM "statistics-greenland-prxprisw"
