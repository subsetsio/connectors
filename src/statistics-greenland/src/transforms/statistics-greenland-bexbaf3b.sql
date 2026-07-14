-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    CAST("age" AS BIGINT) AS age,
    "district from" AS district_from,
    "place of birth" AS place_of_birth,
    "gender",
    "district of migration" AS district_of_migration,
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-bexbaf3b"
