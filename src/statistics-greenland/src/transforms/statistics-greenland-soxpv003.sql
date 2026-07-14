-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `year`.
-- caution: Dimension column(s) `first adress in greenland` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    "first adress in greenland" AS first_adress_in_greenland,
    CAST("year" AS BIGINT) AS year,
    "obs_value"
FROM "statistics-greenland-soxpv003"
