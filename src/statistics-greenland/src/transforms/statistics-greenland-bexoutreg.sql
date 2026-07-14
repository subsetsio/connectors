-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `period`.
-- caution: Dimension column(s) `pob`, `sex.code` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    "area",
    "pob",
    "rate.code" AS rate_code,
    CAST("age" AS BIGINT) AS age,
    "sex.code" AS sex_code,
    "src.code" AS src_code,
    CAST("period" AS BIGINT) AS period,
    "obs_value"
FROM "statistics-greenland-bexoutreg"
