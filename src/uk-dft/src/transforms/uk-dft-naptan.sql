SELECT
    ATCOCode                         AS atco_code,
    NaptanCode                       AS naptan_code,
    CommonName                       AS common_name,
    Street                           AS street,
    Landmark                         AS landmark,
    Town                             AS town,
    Suburb                           AS suburb,
    LocalityName                     AS locality_name,
    StopType                         AS stop_type,
    Status                           AS status,
    TRY_CAST(Easting AS INTEGER)     AS easting,
    TRY_CAST(Northing AS INTEGER)    AS northing,
    TRY_CAST(Longitude AS DOUBLE)    AS longitude,
    TRY_CAST(Latitude AS DOUBLE)     AS latitude
FROM "uk-dft-naptan"
WHERE ATCOCode IS NOT NULL
