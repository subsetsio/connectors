-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
-- caution: Dimension column(s) `place of birth`, `age` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    "area",
    "place of birth" AS place_of_birth,
    "age",
    "kvot",
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-bexbbsf"
