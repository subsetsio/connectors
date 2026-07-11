SELECT
    TRY_CAST(Mfr_ID AS BIGINT)                                              AS manufacturer_id,
    NULLIF(TRIM(Mfr_Name), '')                                              AS manufacturer_name,
    NULLIF(TRIM(Mfr_CommonName), '')                                        AS common_name,
    NULLIF(TRIM(Country), '')                                               AS country,
    NULLIF(array_to_string(list_transform(VehicleTypes, x -> x.Name), ', '), '') AS vehicle_types
FROM "nhtsa-vpic-manufacturers"
WHERE Mfr_ID IS NOT NULL
