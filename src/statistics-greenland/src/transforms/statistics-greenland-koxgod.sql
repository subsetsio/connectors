-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    "time",
    "shipping way" AS shipping_way,
    "specification method" AS specification_method,
    "obs_value"
FROM "statistics-greenland-koxgod"
