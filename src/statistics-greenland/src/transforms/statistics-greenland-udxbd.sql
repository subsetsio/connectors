-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `slutaar`.
SELECT
    "aar",
    "bosted",
    "Udd_land" AS udd_land,
    "UD_niveau" AS ud_niveau,
    CAST("slutaar" AS BIGINT) AS slutaar,
    "obs_value"
FROM "statistics-greenland-udxbd"
