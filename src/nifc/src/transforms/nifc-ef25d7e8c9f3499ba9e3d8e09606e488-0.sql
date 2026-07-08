SELECT
    uniquefireidentifier                     AS unique_fire_id,
    irwinid                                  AS irwin_id,
    incidentname                             AS incident_name,
    TRY_CAST(fireyear AS INTEGER)            AS fire_year,
    TRY_CAST(gisacres AS DOUBLE)             AS gis_acres,
    agency                                   AS agency,
    state                                    AS state,
    pooresponsibleunit                       AS poo_responsible_unit,
    complexname                              AS complex_name,
    firecode                                 AS fire_code,
    incomplex                                AS in_complex,
    CASE WHEN epoch_ms(TRY_CAST(datecurrent AS BIGINT)) BETWEEN TIMESTAMP '1900-01-01' AND TIMESTAMP '2027-12-31' THEN epoch_ms(TRY_CAST(datecurrent AS BIGINT)) END                     AS date_current,
    CASE WHEN epoch_ms(TRY_CAST(perimeterdatetime AS BIGINT)) BETWEEN TIMESTAMP '1900-01-01' AND TIMESTAMP '2027-12-31' THEN epoch_ms(TRY_CAST(perimeterdatetime AS BIGINT)) END               AS perimeter_at
FROM "nifc-ef25d7e8c9f3499ba9e3d8e09606e488-0"
