-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `ukioq`.
SELECT
    CAST("ukioq" AS BIGINT) AS ukioq,
    "kvartal-i" AS kvartal_i,
    "suussusaa",
    "obs_value"
FROM "statistics-greenland-fix009"
