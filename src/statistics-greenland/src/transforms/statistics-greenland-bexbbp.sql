-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    "mothers place of birth" AS mothers_place_of_birth,
    "mothers age" AS mothers_age,
    "parity",
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-bexbbp"
