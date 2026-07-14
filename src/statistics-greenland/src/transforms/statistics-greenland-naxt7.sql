-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `cohort`.
SELECT
    "first firstname" AS first_firstname,
    CAST("cohort" AS BIGINT) AS cohort,
    "obs_value"
FROM "statistics-greenland-naxt7"
