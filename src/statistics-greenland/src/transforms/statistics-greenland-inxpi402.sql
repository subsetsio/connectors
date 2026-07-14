-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
-- caution: Dimension column(s) `district`, `age`, `place of residence`, `place of birth` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    "district",
    "gender",
    "age",
    "place of residence" AS place_of_residence,
    "place of birth" AS place_of_birth,
    CAST("decile" AS BIGINT) AS decile,
    "type of income" AS type_of_income,
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-inxpi402"
