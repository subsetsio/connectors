-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
-- caution: Dimension column(s) `place of birth(mother)`, `municipality(mother)` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    "place of birth(mother)" AS place_of_birth_mother,
    CAST("age(mother)" AS BIGINT) AS age_mother,
    "municipality(mother)" AS municipality_mother,
    "time",
    "obs_value"
FROM "statistics-greenland-bexbblfk"
