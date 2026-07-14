-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    "month",
    "mothers residence" AS mothers_residence,
    "place of birth" AS place_of_birth,
    "gender",
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-bexbbl0"
