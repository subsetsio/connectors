-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
-- caution: Dimension column(s) `place of birth`, `locality`, `gender` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    CAST("age" AS BIGINT) AS age,
    "place of birth" AS place_of_birth,
    "locality",
    "gender",
    CAST("seniority (years in locality)" AS BIGINT) AS seniority_years_in_locality,
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-bexstdt"
