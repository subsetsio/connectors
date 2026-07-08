SELECT
    hpi_type, hpi_flavor, frequency, level, place_name, place_id,
    CAST(NULLIF(yr, '') AS INTEGER)        AS year,
    CAST(NULLIF(period, '') AS INTEGER)    AS period,
    CAST(NULLIF(index_nsa, '') AS DOUBLE)  AS index_nsa,
    CAST(NULLIF(index_sa, '') AS DOUBLE)   AS index_sa,
    CAST(NULLIF(rstderr, '') AS DOUBLE)    AS rstderr,
    NULLIF(note, '')                       AS note
FROM "fhfa-hpi"
WHERE NULLIF(index_nsa, '') IS NOT NULL OR NULLIF(index_sa, '') IS NOT NULL
