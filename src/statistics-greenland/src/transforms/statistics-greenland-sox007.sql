-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
-- caution: Dimension column(s) `age`, `amount interval`, `gender` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    "age",
    "amount interval" AS amount_interval,
    "gender",
    "type",
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-sox007"
