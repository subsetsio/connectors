-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `year`.
-- caution: Dimension column(s) `age`, `number of children and youth`, `type of family` carry source-provided aggregate members (labels such as 'Total' / 'All Greenland') that summarise the other members of the same dimension alongside them. Filter each of those columns to a single level before summing `obs_value`, or the aggregate rows are counted twice.
SELECT
    "inventory variable" AS inventory_variable,
    "age",
    "number of children and youth" AS number_of_children_and_youth,
    "type of family" AS type_of_family,
    CAST("year" AS BIGINT) AS year,
    "obs_value"
FROM "statistics-greenland-soxou04"
