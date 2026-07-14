-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
-- caution: Dimension column(s) `no of children`, `no of adults`, `amount intervals` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    "no of children" AS no_of_children,
    "no of adults" AS no_of_adults,
    "amount intervals" AS amount_intervals,
    "type",
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-sox011"
