-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    "mother's place of birth" AS mother_s_place_of_birth,
    CAST("mother's age" AS BIGINT) AS mother_s_age,
    "parity",
    "mother's birthsday" AS mother_s_birthsday,
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-bexbbpl"
