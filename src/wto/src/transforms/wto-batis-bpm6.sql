SELECT
    Reporter                            AS reporter,
    type_Reporter                       AS reporter_type,
    Partner                             AS partner,
    type_Partner                        AS partner_type,
    Flow                                AS flow,
    Item_code                           AS item_code,
    type_Item                           AS item_type,
    TRY_CAST(Year AS INTEGER)           AS year,
    TRY_CAST(Reported_value AS DOUBLE)  AS reported_value,
    TRY_CAST(Final_value AS DOUBLE)     AS final_value,
    Final_value_methodology             AS final_value_methodology,
    TRY_CAST(Balanced_value AS DOUBLE)  AS balanced_value
FROM "wto-batis-bpm6"
WHERE TRY_CAST(Year AS INTEGER) IS NOT NULL
