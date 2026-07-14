-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    "price unit" AS price_unit,
    CAST("time" AS BIGINT) AS time,
    "production",
    "COICOP" AS coicop,
    "obs_value"
FROM "statistics-greenland-nrx16"
