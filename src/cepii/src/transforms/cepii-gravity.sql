SELECT * REPLACE (
    CAST(scaled_sci_2021 AS BIGINT) AS scaled_sci_2021,
    CAST(col_dep_end_year AS VARCHAR) AS col_dep_end_year,
    CAST(col_dep_end_conflict AS VARCHAR) AS col_dep_end_conflict,
    CAST(rta_coverage AS VARCHAR) AS rta_coverage,
    CAST(rta_type AS VARCHAR) AS rta_type
)
FROM "cepii-gravity"
