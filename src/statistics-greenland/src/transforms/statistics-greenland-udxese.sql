-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `aargang`.
SELECT
    "Befo" AS befo,
    "distrikt",
    "sex",
    CAST("Aargang" AS BIGINT) AS aargang,
    "obs_value"
FROM "statistics-greenland-udxese"
