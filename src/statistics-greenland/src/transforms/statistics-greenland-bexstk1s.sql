-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time_primo`.
-- caution: Dimension column(s) `residence type`, `citizenship`, `sex` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    CAST("age" AS BIGINT) AS age,
    "residence type" AS residence_type,
    "citizenship",
    "sex",
    "time (primo)" AS time_primo,
    "obs_value"
FROM "statistics-greenland-bexstk1s"
