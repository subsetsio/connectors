-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `aar`.
-- caution: Dimension column(s) `branche`, `komkod`, `bybygd`, `sex` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    "branche",
    "komkod",
    "bybygd",
    "sex",
    CAST("aar" AS BIGINT) AS aar,
    "obs_value"
FROM "statistics-greenland-arxbfb11"
