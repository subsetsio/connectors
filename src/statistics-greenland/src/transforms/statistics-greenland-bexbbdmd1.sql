-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    CAST("age" AS BIGINT) AS age,
    "residence",
    "place of birth" AS place_of_birth,
    "month",
    "gender",
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-bexbbdmd1"
