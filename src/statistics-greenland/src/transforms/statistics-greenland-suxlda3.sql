-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
-- caution: Dimension column(s) `causes`, `month of death`, `sex` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    CAST("age" AS BIGINT) AS age,
    "causes",
    "month of death" AS month_of_death,
    "sex",
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-suxlda3"
