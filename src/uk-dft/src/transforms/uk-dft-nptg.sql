SELECT
    NptgLocalityCode                 AS nptg_locality_code,
    LocalityName                     AS locality_name,
    QualifierName                    AS qualifier_name,
    ParentLocalityName               AS parent_locality_name,
    AdministrativeAreaCode           AS administrative_area_code,
    TRY_CAST(Easting AS INTEGER)     AS easting,
    TRY_CAST(Northing AS INTEGER)    AS northing
FROM "uk-dft-nptg"
WHERE NptgLocalityCode IS NOT NULL
